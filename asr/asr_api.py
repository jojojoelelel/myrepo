from flask import Flask, request, jsonify

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch

import librosa
from pydub import AudioSegment

import os

app = Flask(__name__)

# load model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200
     
@app.route('/asr', methods=['POST'])
def asr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file given'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        temp_file_path = 'temp_audio.mp3'
        file.save(temp_file_path)

        audio = AudioSegment.from_mp3(temp_file_path)
        wav_file_path = 'temp_audio.wav'
        audio.export(wav_file_path, format='wav')

        audio_input, _ = librosa.load(wav_file_path, sr=16000)

        input_values = processor(audio_input, return_tensors='pt').input_values
        with torch.no_grad():
            logits = model(input_values).logits
        
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.decode(predicted_ids[0])

        duration = librosa.get_duration(y=audio_input, sr=16000)

        os.remove(temp_file_path)
        os.remove(wav_file_path)

        return jsonify({
            'transcription': transcription,
            'duration': str(duration)
        }), 200
    
    except Exception as e:
        print(f"Error processing the file: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)