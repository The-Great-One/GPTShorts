from Media_Download import *
from transcription import Transcribe
from split_srt import splitter
from GPTAnalyser import GPT_Analyser
from segment import segment_video

def main():
    download_video("https://rumble.com/v4vblgu-sitdown-with-andrew-tate-michael-franzese.html")
    Transcribe()
    splitter()
    GPT_Analyser()
    segment_video()