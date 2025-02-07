from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

# This variable will hold the subprocess that is recording video
recording_process = None


@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recording_process
    if recording_process is not None:
        return jsonify({'error': 'Recording already in progress'}), 400

    # Example: Launch a Python script that handles video recording natively.
    # Adjust the command to suit your script/requirements.
    recording_process = subprocess.Popen(['python3', 'record_video.py'])
    return jsonify({'status': 'Recording started'}), 200


@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global recording_process
    if recording_process is None:
        return jsonify({'error': 'No recording in progress'}), 400

    # Terminate the recording process. You might need to implement a more graceful shutdown.
    recording_process.terminate()
    recording_process = None
    return jsonify({'status': 'Recording stopped and saved'}), 200


if __name__ == '__main__':
    # Listen on all interfaces or restrict to localhost if needed
    app.run(host='0.0.0.0', port=5000)
