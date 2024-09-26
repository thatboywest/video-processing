import ffmpeg

def load_video(file_path):
    return str(file_path)

def crop_to_aspect_ratio(video_path, desired_aspect_ratio, output_path):
    probe = ffmpeg.probe(video_path)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    width = int(video_info['width'])
    height = int(video_info['height'])
    
    current_aspect_ratio = width / height
    if current_aspect_ratio > desired_aspect_ratio:
        new_width = int(height * desired_aspect_ratio)
        x = (width - new_width) // 2
        y = 0
    else:
        new_height = int(width / desired_aspect_ratio)
        x = 0
        y = (height - new_height) // 2
    
    ffmpeg.input(video_path).filter('crop', f'iw-{x*2}:ih-{y*2}:{x}:{y}').output(output_path).run(overwrite_output=True)

def add_subtitles_to_clip(video_path, subtitles, output_path, box_coords, font_size, color, font_path):
    x, y, w, h = box_coords
    subtitle_filter = f"subtitles={video_path}:force_style='FontName={font_path},FontSize={font_size},PrimaryColour={color},MarginV={y},MarginL={x},MarginR={x}'"
    ffmpeg.input(video_path).filter(subtitle_filter).output(output_path).run(overwrite_output=True)