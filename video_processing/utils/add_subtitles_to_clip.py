import ffmpeg

def add_subtitles_to_clip(video_path, subtitles, output_path, font_size, color, font_path):
    # Convert color from hex to ASS format (hex without the '#')
    color_ass = color[1:]  # Remove '#' to fit ASS format, e.g., 'FFFFFF'

    try:
        # Apply subtitles with a background color and re-encode the video
        (
            ffmpeg
            .input(video_path)
            .output(
                output_path,
                vf=f"subtitles={subtitles}:force_style='Fontsize={font_size},Font={font_path},BackColour=&H{color_ass}&,BorderStyle=4'",
                **{'c:v': 'libx264', 'c:a': 'aac'}  # Re-encode video and audio
            )
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        error_message = e.stderr.decode() if e.stderr else "Unknown error occurred"
        print(f"An error occurred: {error_message}")
        raise
