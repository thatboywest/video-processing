import ffmpeg
import tempfile

def replace_audio_segment(video_path, audio_path, output_path):
    try:
        # Get video duration
        probe = ffmpeg.probe(video_path)
        video_duration = float(probe['streams'][0]['duration'])
        
        # Adjust audio to match video duration
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
        ffmpeg.input(audio_path).filter('atrim', duration=video_duration).output(temp_audio).run(overwrite_output=True)
        
        # Replace audio in video
        input_video = ffmpeg.input(video_path)
        input_audio = ffmpeg.input(temp_audio)
        ffmpeg.output(input_video, input_audio, output_path, vcodec='libx264', acodec='aac').run(overwrite_output=True)
        
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}")
        raise