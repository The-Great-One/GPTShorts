import yt_dlp
from urllib.parse import urlparse

# Video Processing
def download_video(URL):
    ydl_opts = {'format': 'best', 'outtmpl': 'Input/Input.mp4'}
    
    # Determine the source based on the URL
    parsed_url = urlparse(URL)
    domain = parsed_url.netloc
    
    if 'youtube.com' in domain or 'youtu.be' in domain:
        source = 'YouTube'
    elif 'rumble.com' in domain:
        source = 'Rumble'
    else:
        source = domain  # Use the domain as the source for other sites
    
    # Download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])
    
    return source, URL