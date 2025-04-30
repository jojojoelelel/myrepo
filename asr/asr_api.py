# Import Libraries
from flask import Flask, request, jsonify

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch

import librosa
from pydub import AudioSegment

import os

# Initialise Flask App
app = Flask(__name__)

# load model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

# Enable GPU if available and not using torch+cpu
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Ping Endpoint for testing
@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200
     
# ASR Endpoint
@app.route('/asr', methods=['POST'])
def asr():
    # Check if file is given
    if 'file' not in request.files:
        return jsonify({'error': 'No file given'}), 400

    # Get file
    file = request.files['file']

    # Check if file is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Create temporary mp3 file path
        temp_file_path = 'temp_audio.mp3'
        # Save input file as temporary mp3 file
        file.save(temp_file_path)

        # Convert temporary mp3 file to wav for processing
        audio = AudioSegment.from_mp3(temp_file_path)
        wav_file_path = 'temp_audio.wav'
        audio.export(wav_file_path, format='wav')

        # Load wav file and resample at 16000 Hz
        audio_input, _ = librosa.load(wav_file_path, sr=16000)

        # Run transcription
        input_values = processor(audio_input, return_tensors='pt').input_values.to(device)
        with torch.no_grad():
            logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.decode(predicted_ids[0])

        # Obtain duration of audio file
        duration = librosa.get_duration(y=audio_input, sr=16000)

        # Remove temporary files
        os.remove(temp_file_path)
        os.remove(wav_file_path)

        # Return transcription and duration
        return jsonify({
            'transcription': transcription,
            'duration': str(duration)
        }), 200
    
    # Error handling
    except Exception as e:
        print(f"Error processing the file: {e}")
        return jsonify({'error': str(e)}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)