from transcribe_anything.api import transcribe
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import json


def extract_youtube_id(url):
    """
    Extracts the YouTube video ID from a given URL.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        str: The YouTube video ID or None if not found.
    """
    parsed_url = urlparse(url)
    
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query).get('v', [None])[0]
        if parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
        if parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]
    
    return None


def seconds_to_timestamp(seconds):
    """
    Converts seconds to a timestamp in SRT format.

    Args:
        seconds (float): The number of seconds.

    Returns:
        str: The timestamp in SRT format (HH:MM:SS,MS).
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def save_as_srt(transcript, file_path):
    """
    Saves a transcript as an SRT file.

    Args:
        transcript (list): The transcript to save.
        file_path (str): The path to the output SRT file.
    """
    with open(file_path, 'w') as f:
        for i, entry in enumerate(transcript, 1):
            start_time = seconds_to_timestamp(entry['start'])
            duration = entry['duration']
            end_time = seconds_to_timestamp(entry['start'] + duration)
            text = entry['text'].replace('\n', ' ')

            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")


def transcribe_video(source, url):
    """
    Transcribes a video from a YouTube URL or a local file.

    Args:
        source (str): The source of the video ("YouTube" or other).
        url (str): The URL of the video or the local file path.
    """
    if source == "YouTube":
        video_id = extract_youtube_id(url)
        if video_id:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            # Remove newlines from the transcript text
            for text in transcript:
                text["text"] = text["text"].replace("\n", "")
                
            # Save the transcript as an SRT file
            save_as_srt(transcript, 'Generated_Files/out.srt')
    else:
        # Transcribe a local video file
        transcribe(
            url_or_file="Input/Input.mp4",
            output_dir="Generated_Files"
        )