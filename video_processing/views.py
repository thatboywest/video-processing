from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import VideoUploadForm
from .utils.subtitle_processing import load_subtitles_from_file
from .utils.add_subtitles_to_clip import add_subtitles_to_clip
from elevenlabs import ElevenLabs
import os

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fs = FileSystemStorage()

            # Save uploaded files
            video_file = request.FILES['video']
            original_srt_file = request.FILES['original_subtitles']
            translated_srt_file = request.FILES['translated_subtitles']
            font_file = request.FILES.get('font', None)

            video_path = fs.save(video_file.name, video_file)
            original_srt_path = fs.save(original_srt_file.name, original_srt_file)
            translated_srt_path = fs.save(translated_srt_file.name, translated_srt_file)

            # Save font if provided
            font_path = None
            if font_file:
                font_path = fs.save(font_file.name, font_file)

            # Get overlay color and font size from the form data
            overlay_color = form.cleaned_data.get('overlay_color', '#FFFFFF')
            font_size = form.cleaned_data.get('font_size', 24)  # Default font size
            
            # Get API key and voice ID from the form data
            api_key = form.cleaned_data.get('api_key')
            voice_id = form.cleaned_data.get('voice_id')

            # Full paths for saved video and subtitle files
            video_full_path = os.path.join(settings.MEDIA_ROOT, video_path)
            translated_srt_full_path = os.path.join(settings.MEDIA_ROOT, translated_srt_path)

            output_audio_path = os.path.join(settings.MEDIA_ROOT, 'generated_audio.mp3')

            try:
                # Initialize Eleven Labs client with user's API key
                client = ElevenLabs(api_key=api_key)

                # Load the translated subtitles text from the translated SRT file
                subtitles_data = load_subtitles_from_file(translated_srt_full_path)

                if isinstance(subtitles_data, list):
                    # Assuming each dictionary in the list has a key 'text' for the subtitle text
                    subtitles_text = ' '.join(item['text'] for item in subtitles_data if 'text' in item)
                else:
                    raise ValueError("Subtitles data must be a list.")

                if not subtitles_text.strip():
                    raise ValueError("Subtitles text cannot be empty.")

                # Generate audio from the subtitles text
                audio_generator = client.text_to_speech.convert(
                    voice_id=voice_id,
                    text=subtitles_text,
                    optimize_streaming_latency="0"
                )

                # Save audio data to a file
                with open(output_audio_path, 'wb') as audio_file:
                    for chunk in audio_generator:
                        audio_file.write(chunk)

                output_file_name = 'output_video.mp4'
                output_file_path = os.path.join(settings.MEDIA_ROOT, output_file_name)

                # Add generated audio and subtitles to the video
                add_subtitles_to_clip(
                    video_path=video_full_path,
                    audio_path=output_audio_path,  # Add audio path here
                    subtitles=translated_srt_full_path,
                    output_path=output_file_path,
                    font_size=font_size,
                    color=overlay_color,
                    font_path=font_path if font_path else 'Arial'
                )

                # Generate a URL for the output video to be accessible in the browser
                                # Generate the URL for the output file
                output_file_url = fs.url(output_file_name)

                return render(request, 'video_processing/result.html', {
                    'video_url': output_file_url  
                })

            except Exception as e:
                return render(request, 'video_processing/error.html', {'error_message': str(e)})

    else:
        form = VideoUploadForm()

    return render(request, 'video_processing/upload.html', {'form': form})
