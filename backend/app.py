#!/usr/bin/env python3
import threading
import time
from datetime import datetime

from flask import Flask
from flask_socketio import SocketIO, emit
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

app = Flask(__name__)
socketio = SocketIO(app)

# Global state variables.
picam2 = None
recording = False
record_thread = None
MAX_DURATION = 60  # Maximum recording duration in seconds (1 minute)


def record_video(output_filename):
    global picam2, recording
    try:
        # Initialize and configure the camera for 1080p video.
        picam2 = Picamera2()
        video_config = picam2.create_video_configuration(
            {"size": (1920, 1080)})
        picam2.configure(video_config)
        picam2.start()

        # Set up an H264 encoder with a defined bitrate.
        encoder = H264Encoder(bitrate=10000000)
        picam2.start_recording(encoder, output_filename)
        socketio.emit('recording_status', {
                      'status': f'Recording started: {output_filename}'})
        print(f"Recording started: {output_filename}")

        start_time = time.time()
        # Continue recording until MAX_DURATION is reached or a stop is signaled.
        while recording:
            elapsed = time.time() - start_time
            if elapsed >= MAX_DURATION:
                print(
                    "Maximum recording duration reached. Stopping recording automatically.")
                recording = False
                break
            time.sleep(0.1)

        # Stop the recording and shut down the camera.
        picam2.stop_recording()
        picam2.stop()
        try:
            # Explicitly release the camera resource if supported.
            picam2.close()
        except Exception as cleanup_error:
            print("Error during camera cleanup:", cleanup_error)
        picam2 = None
        socketio.emit('recording_status', {'status': 'Recording finished'})
        print("Recording finished.")

    except Exception as e:
        print("Error in record_video:", e)
        socketio.emit('error', {'message': str(e)})
        # Attempt cleanup in case of an error.
        try:
            if picam2 is not None:
                picam2.stop_recording()
                picam2.stop()
                picam2.close()
        except Exception as cleanup_error:
            print("Error during cleanup in exception block:", cleanup_error)
        picam2 = None
        recording = False


@socketio.on('start_recording')
def handle_start_recording(data):
    global recording, record_thread
    if recording:
        emit('error', {'message': 'Already recording'})
        return

    recording = True
    # Generate a unique filename using the current datetime.
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"video_{now}.h264"
    # Start the recording in a background thread.
    record_thread = threading.Thread(
        target=record_video, args=(output_filename,))
    record_thread.start()
    emit('recording_status', {
         'status': 'Recording started', 'filename': output_filename})
    print("Start recording command received.")


@socketio.on('stop_recording')
def handle_stop_recording(data):
    global recording, record_thread
    if not recording:
        emit('error', {'message': 'Not recording'})
        return

    recording = False
    # Optionally wait for the recording thread to finish.
    if record_thread is not None:
        record_thread.join()
    emit('recording_status', {'status': 'Recording stopped'})
    print("Stop recording command received.")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
