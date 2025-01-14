from Media_Download import *
from transcription import transcribe_video
from split_srt import splitter
from GPTAnalyser import GPT_Analyser
from segment import segment_video
from cropper import main_crop

def main():
    print("Downloading Video")
    source, url = download_video("https://youtu.be/eIho2S0ZahI")
    print("Transcribing")
    transcribe_video(source, url)
    print("Splitting SRT")
    splitter()
    print("Analysing Script")
    GPT_Analyser()
    print("Segmenting Video")
    segment_video()
    print("Cropping Faces")
    main_crop()
    
main()