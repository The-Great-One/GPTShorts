import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
import librosa
import os
import glob
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_faces(frame, face_cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def analyze_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    intervals = librosa.effects.split(y, top_db=20)
    return intervals, sr

def crop_video(input_file, output_file):
    try:
        # Load video
        video = VideoFileClip(input_file)
        audio = video.audio
        
        # Extract audio for analysis
        audio_file = input_file.replace('.mp4', '.wav')
        audio.write_audiofile(audio_file)

        # Analyze speaking intervals
        speaking_intervals, sr = analyze_audio(audio_file)

        # Load Haar cascade for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        def process_frame(get_frame, t):
            frame = get_frame(t)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            if len(faces) > 0:
                x, y, w, h = faces[0]
                center_x, center_y = x + w // 2, y + h // 2
                crop_x = max(0, center_x - target_width // 2)
                crop_y = max(0, center_y - target_height // 2)
                crop_x = min(crop_x, frame_width - target_width)
                crop_y = min(crop_y, frame_height - target_height)
                cropped_frame = frame[crop_y:crop_y + target_height, crop_x:crop_x + target_width]
                return cv2.resize(cropped_frame, (target_width, target_height))
            else:
                return cv2.resize(frame, (target_width, target_height))

        frame_width, frame_height = video.size
        fps = video.fps
        target_height = int(frame_height * 0.9)
        target_width = int(target_height * (9 / 16))

        cropped_video = video.fl(process_frame, apply_to=['mask'])

        # Merge video with original audio
        final_clip = cropped_video.set_audio(audio)
        final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')

        # Cleanup
        if os.path.exists(audio_file):
            os.remove(audio_file)

        logging.info(f"Video cropped and stabilized successfully. Output saved to {output_file}")
        return output_file

    except Exception as e:
        logging.error(f"Error during video cropping: {str(e)}")
        return None

def process_video(input_file):
    output_file = input_file.replace('.mp4', '_Cropped.mp4')
    return crop_video(input_file, output_file)

def main_crop():
    input_files = glob.glob('Output/*.mp4')

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_video, input_file): input_file for input_file in input_files}
        for future in as_completed(futures):
            input_file = futures[future]
            try:
                result = future.result()
                logging.info(f"Processing completed for {input_file}")
            except Exception as e:
                logging.error(f"Error processing {input_file}: {e}")