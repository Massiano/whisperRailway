import os
from flask import Flask, request, jsonify
import whisper
import tempfile

app = Flask(__name__)

# Load model ONCE at startup
print("Loading Whisper 'small' model...")
model = whisper.load_model("small")
print("✅ Ready to transcribe!")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'}), 400

    audio = request.files['audio']
    try:
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            audio.save(tmp.name)
            result = model.transcribe(tmp.name)
            os.unlink(tmp.name)  # cleanup

        return jsonify({'text': result['text'].strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
