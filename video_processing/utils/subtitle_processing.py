from pathlib import Path

def load_subtitles_from_file(srt_file):
    subtitles = []
    with open(srt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            if '-->' in lines[i]:
                time = lines[i].strip()
                text = lines[i+1].strip()
                subtitles.append({'time': time, 'text': text})
                i += 3
            else:
                i += 1
    return subtitles

def replace_srt_text(input_file_path, txt_file, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as srt, \
         open(txt_file, 'r', encoding='utf-8') as txt, \
         open(output_file_path, 'w', encoding='utf-8') as output:
        
        translations = txt.readlines()
        translation_index = 0
        
        for line in srt:
            if '-->' not in line and line.strip() and not line.strip().isdigit():
                line = translations[translation_index].strip() + '\n'
                translation_index += 1
            output.write(line)

    print(f"Translated SRT saved as {output_file_path}")