import os
import srt
from typing import List
import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def read_srt(file_path: str) -> List[srt.Subtitle]:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return list(srt.parse(content)), content

def write_srt(subtitles: List[srt.Subtitle], file_path: str):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(srt.compose(subtitles))

def splitter(file_path = "Generated_Files/out.srt", parts: int = 4):
    # Read the SRT file
    subtitles, content = read_srt(file_path)
    token_size = num_tokens_from_string(content, "gpt-4o")
    if token_size > 30000:
        total_subtitles = len(subtitles)
        part_size = total_subtitles // parts
        
        # Split the subtitles into parts
        for i in range(parts):
            start_index = i * part_size
            end_index = (i + 1) * part_size if i < parts - 1 else total_subtitles
            part_subtitles = subtitles[start_index:end_index]
            output_file = f"{os.path.splitext(file_path)[0]}_part{i + 1}.srt"
            write_srt(part_subtitles, output_file)
            print(f"Part {i + 1} written to {output_file}")
    else:
        print("Token Size is Less than GPT Limit, Skipping split")
        output_file = f"{os.path.splitext(file_path)[0]}_Full.srt"
        write_srt(subtitles, output_file)