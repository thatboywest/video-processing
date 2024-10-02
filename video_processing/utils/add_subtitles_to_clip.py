import ffmpeg

def add_subtitles_to_clip(video_path, audio_path, subtitles, output_path, font_size, color, font_path):
    # Convert color from hex to ASS format (hex without the '#')
    color_ass = color[1:]  # Remove '#' to fit ASS format, e.g., 'FFFFFF'

    try:
        # Define input for video and audio
        input_video = ffmpeg.input(video_path)
        input_audio = ffmpeg.input(audio_path)

        # Apply subtitles with styling using the correct subtitle filter syntax
        ffmpeg_output = (
            ffmpeg
            .filter(input_video, 'subtitles', f"{subtitles}", force_style=f"Fontsize={font_size},Font={font_path},BackColour=&H{color_ass}&,BorderStyle=4")
            .output(input_audio, output_path, vcodec='libx264', acodec='aac')  # Combine audio and video
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        error_message = e.stderr.decode() if e.stderr else "Unknown error occurred"
        print(f"An error occurred: {error_message}")
        raise
