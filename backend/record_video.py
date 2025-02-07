#!/usr/bin/env python3
from picamera2 import Picamera2
import time
import subprocess
import os


def record_video(duration=10,
                 raw_filename="video_output.h264",
                 mp4_filename="video_output.mp4",
                 framerate=30):
    """
    Records a 1080p video using Picamera2 for a given duration,
    saves the raw H.264 stream to a file, and converts it to an MP4 container.

    Parameters:
      duration (int): Duration to record in seconds.
      raw_filename (str): Filename for the raw H.264 output.
      mp4_filename (str): Filename for the final MP4 output.
      framerate (int): Frame rate for recording.
    """
    # Initialize Picamera2 and create a 1080p video configuration.
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration({"size": (1920, 1080)})
    picam2.configure(video_config)

    # Start the camera.
    picam2.start()
    print("Camera started. Beginning recording...")

    # Start recording to the raw H.264 file.
    picam2.start_recording(raw_filename)
    print(f"Recording for {duration} seconds...")
    time.sleep(duration)
    picam2.stop_recording()
    print("Recording stopped.")
    picam2.stop()

    # Convert the raw H.264 file into an MP4 container using ffmpeg.
    print("Converting raw H.264 file to MP4 container...")
    try:
        subprocess.run([
            "ffmpeg",
            "-framerate", str(framerate),
            "-i", raw_filename,
            "-c", "copy",
            mp4_filename
        ], check=True)
        print(f"Conversion successful. Video saved as '{mp4_filename}'.")
    except subprocess.CalledProcessError as e:
        print("Error during conversion:", e)
        return

    # Optionally, remove the temporary raw H.264 file.
    if os.path.exists(raw_filename):
        os.remove(raw_filename)
        print(f"Removed temporary file '{raw_filename}'.")


if __name__ == '__main__':
    # Record a video for 10 seconds (adjust duration as needed).
    record_video(duration=10)
