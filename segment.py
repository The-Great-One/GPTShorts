import math
import subprocess
import json
import re

def time_str_to_seconds(time_str):
    # Patterns for different time formats
    pattern_with_ms = r'(\d+):(\d+):(\d+),(\d+)'     # HH:MM:SS,MS
    pattern_without_ms = r'(\d+):(\d+):(\d+)'         # HH:MM:SS
    pattern_minutes_seconds = r'(\d+):(\d+)'          # MM:SS

    if re.match(pattern_with_ms, time_str):
        hours, minutes, seconds, milliseconds = map(int, re.match(pattern_with_ms, time_str).groups())
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
    elif re.match(pattern_without_ms, time_str):
        hours, minutes, seconds = map(int, re.match(pattern_without_ms, time_str).groups())
        total_seconds = hours * 3600 + minutes * 60 + seconds
    elif re.match(pattern_minutes_seconds, time_str):
        minutes, seconds = map(int, re.match(pattern_minutes_seconds, time_str).groups())
        total_seconds = minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid time format: {time_str}")

    return total_seconds


def segment_video():
    try:
        with open('Generated_Files/data.json', 'r') as f:
            response = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    for i, segment in enumerate(response):
        start_time = math.floor(float(time_str_to_seconds(segment.get("start_time", "0:00:00"))))
        end_time = math.ceil(float(time_str_to_seconds(segment.get("end_time", "0:00:00")))) + 2
        output_file = f"Output/{segment.get('title', f'Out_{i}')}.mp4"
        
        command = [
            'ffmpeg',
            '-i', 'Input/Input.mp4',
            '-ss', str(start_time),
            '-to', str(end_time),
            '-c', 'copy',
            output_file
        ]
        
        print(f"Processing segment {i}: {' '.join(command)}")
        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError as e:
            print(f"Error processing segment {i}: {e}")
    print("Segmentation complete.")