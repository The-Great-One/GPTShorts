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
    f = open('Generated_Files/data.json')
    response = json.load(f)

    for i, segment in enumerate(response):
        start_time = math.floor(float(time_str_to_seconds(segment.get("start_time", 0))))
        end_time = math.ceil(float(time_str_to_seconds(segment.get("end_time", 0)))) + 2
        output_file = f"out/output{str(i).zfill(3)}.mp4"
        command = f"ffmpeg -i Tate.mp4 -ss {start_time} -to {end_time} -c copy {output_file}"
        print(f"Processing segment {i}: {command}")
        subprocess.call(command, shell=True)
    print("Segmentation complete.")