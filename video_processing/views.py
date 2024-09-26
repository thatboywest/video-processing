import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import VideoUploadForm
from .utils.subtitle_processing import load_subtitles_from_file
import ffmpeg

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fs = FileSystemStorage()

            # Save uploaded files
            video_file = request.FILES['video']
            srt_file = request.FILES['subtitles']

            video_path = fs.save(video_file.name, video_file)
            srt_path = fs.save(srt_file.name, srt_file)

            # Full paths
            video_full_path = os.path.join(settings.MEDIA_ROOT, video_path)
            srt_full_path = os.path.join(settings.MEDIA_ROOT, srt_path)

            # Load subtitles (if needed for additional processing)
            subtitles = load_subtitles_from_file(srt_full_path)

            output_file_name = 'output_video.mp4'
            output_file_path = os.path.join(settings.MEDIA_ROOT, output_file_name)

            try:
                # Use ffmpeg to burn subtitles into the video
                ffmpeg.input(video_full_path) \
                    .output(output_file_path, vf=f"subtitles={srt_full_path}", vcodec='libx264', acodec='aac') \
                    .run(overwrite_output=True)

                # Generate URL for the output file using fs.url
                output_file_url = fs.url(output_file_name)

                return render(request, 'video_processing/result.html', {
                    'video_url': output_file_url  
                })
            except ffmpeg.Error as e:
                # Handle ffmpeg error
                error_message = f"An error occurred during video processing: {str(e)}"
                return render(request, 'video_processing/error.html', {'error_message': error_message})
    else:
        form = VideoUploadForm()

    return render(request, 'video_processing/upload.html', {'form': form})
