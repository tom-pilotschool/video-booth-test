#!/usr/bin/env python3
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
import time


def record_video(duration=10, output_filename="video_output.h264"):
    # Initialize Picamera2
    picam2 = Picamera2()
    # Create a 1080p video configuration
    video_config = picam2.create_video_configuration({"size": (1920, 1080)})
    picam2.configure(video_config)

    # Start the camera
    picam2.start()

    encoder = H264Encoder(bitrate=10000000)
    output = "test.h264"

    # Start recording and provide the output filename
    picam2.start_recording(encoder, output)
    print(f"Recording to {output_filename} for {duration} seconds...")

    time.sleep(duration)

    # Stop recording and shut down the camera
    picam2.stop_recording()
    picam2.stop()
    print("Recording finished.")


if __name__ == '__main__':
    record_video()
