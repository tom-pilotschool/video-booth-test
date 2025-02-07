#!/usr/bin/env python3
from flask import Flask, jsonify, request
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import threading
import time

app = Flask(__name__)

# Global variables to manage the camera and recording state.
picam2 = None
recording = False
record_thread = None
MAX_DURATION = 60  # Maximum recording time in seconds (1 minute)


def record_video():
    global picam2, recording
    try:
        # Initialize Picamera2 and configure it for 1080p recording.
        picam2 = Picamera2()
        video_config = picam2.create_video_configuration(
            {"size": (1920, 1080)})
        picam2.configure(video_config)

        # Start the camera.
        picam2.start()

        # Create an H264 encoder with a specified bitrate.
        encoder = H264Encoder(bitrate=10000000)
        output = "test.h264"  # Output filename

        # Start recording with the encoder and output filename.
        picam2.start_recording(encoder, output)
        print(f"Recording to {output}...")

        start_time = time.time()
        # Keep recording until 'recording' is set to False or max duration is reached.
        while recording:
            elapsed = time.time() - start_time
            if elapsed >= MAX_DURATION:
                print(
                    "Maximum recording duration reached. Stopping recording automatically.")
                recording = False
                break
            time.sleep(0.1)

        # Stop recording and shut down the camera.
        picam2.stop_recording()
        picam2.stop()
        print("Recording finished.")

    except Exception as e:
        print("Error in record_video:", e)


@app.route('/start_recording', methods=['POST'])
def start_recording_endpoint():
    global recording, record_thread
    if recording:
        return jsonify({'status': 'already recording'}), 400

    recording = True
    # Start the recording in a background thread.
    record_thread = threading.Thread(target=record_video)
    record_thread.start()
    return jsonify({'status': 'recording started'}), 200


@app.route('/stop_recording', methods=['POST'])
def stop_recording_endpoint():
    global recording, record_thread
    if not recording:
        return jsonify({'status': 'not recording'}), 400

    # Signal the recording thread to stop.
    recording = False

    # Optionally, wait for the recording thread to finish.
    if record_thread is not None:
        record_thread.join()
    return jsonify({'status': 'recording stopped'}), 200


if __name__ == '__main__':
    # Run the Flask app on all network interfaces.
    app.run(host='0.0.0.0', port=5000)
