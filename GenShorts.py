from Media_Download import *
from transcription import Transcribe
from split_srt import splitter
from GPTAnalyser import GPT_Analyser
from segment import segment_video

def main():
    print("Downloading Video")
    download_video("https://youtu.be/eIho2S0ZahI")
    print("Transcribing")
    Transcribe()
    print("Splitting SRT")
    splitter()
    print("Analysing Script")
    GPT_Analyser()
    print("Segmenting Video")
    segment_video()
    
main()