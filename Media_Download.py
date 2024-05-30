import yt_dlp

# Video Processing
def download_video(URL):
    ydl_opts = {'format': 'best', 'outtmpl': f'Input/Input.mp4'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])