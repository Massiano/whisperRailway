import os
import tempfile
import traceback
from flask import Flask, request, jsonify
import whisper

app = Flask(__name__)

# Load model ONCE at startup — force CPU
print("Loading Whisper 'small' model on CPU...")
model = whisper.load_model("small", device="cpu")
print("✅ Whisper 'small' model loaded and ready!")

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio = request.files['audio']
    temp_path = None
    try:
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            temp_path = tmp.name
            audio.save(temp_path)

        # Transcribe
        result = model.transcribe(temp_path, fp16=False)  # fp16=False for CPU stability
        return jsonify({'text': result['text'].strip()})

    except Exception as e:
        print("Transcription error:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

    finally:
        # Ensure cleanup
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
