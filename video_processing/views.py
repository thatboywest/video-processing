import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import VideoUploadForm
from .utils.subtitle_processing import load_subtitles_from_file
from .utils.add_subtitles_to_clip import add_subtitles_to_clip
import ffmpeg

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fs = FileSystemStorage()

            # Save uploaded files
            video_file = request.FILES['video']
            srt_file = request.FILES['subtitles']
            font_file = request.FILES.get('font', None) 

            video_path = fs.save(video_file.name, video_file)
            srt_path = fs.save(srt_file.name, srt_file)

            # Save font if provided
            font_path = None
            if font_file:
                font_path = fs.save(font_file.name, font_file)

            # Get overlay color and font size from the form data
            overlay_color = form.cleaned_data.get('overlay_color', '#FFFFFF') 
            font_size = form.cleaned_data.get('font_size', 24)  # Default font size

            # Full paths for saved video and subtitle files
            video_full_path = os.path.join(settings.MEDIA_ROOT, video_path)
            srt_full_path = os.path.join(settings.MEDIA_ROOT, srt_path)

            output_file_name = 'output_video.mp4'
            output_file_path = os.path.join(settings.MEDIA_ROOT, output_file_name)

            try:
                # Add subtitles to the video with the specified options
                add_subtitles_to_clip(
                    video_path=video_full_path,
                    subtitles=srt_full_path,
                    output_path=output_file_path,
                    font_size=font_size,
                    color=overlay_color,  # Use overlay_color instead of color
                    font_path=font_path
                )

                # Generate the URL for the output file
                output_file_url = fs.url(output_file_name)

                return render(request, 'video_processing/result.html', {
                    'video_url': output_file_url  
                })
            except ffmpeg.Error as e:
                # Handle ffmpeg errors
                error_message = f"An error occurred during video processing: {str(e)}"
                return render(request, 'video_processing/error.html', {'error_message': error_message})
    else:
        form = VideoUploadForm()

    return render(request, 'video_processing/upload.html', {'form': form})
