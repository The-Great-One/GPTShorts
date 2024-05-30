from transcribe_anything.api import transcribe

def Transcribe():
    transcribe(
        url_or_file="Input/Input.mp4",
        output_dir="Generated_Files"    
    )