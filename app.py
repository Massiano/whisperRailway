import os
from flask import Flask, request, jsonify
import whisper
import tempfile

app = Flask(__name__)

print("Loading Whisper small model...")
model = whisper.load_model("small")
print("Model ready!")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file"}), 400

    audio_file = request.files["audio"]
    ext = os.path.splitext(audio_file.filename)[1].lower()
    if ext not in [".wav", ".mp3", ".m4a", ".ogg", ".webm"]:
        return jsonify({"error": "Unsupported format"}), 400

    try:
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            audio_file.save(tmp.name)
            result = model.transcribe(tmp.name)
            os.unlink(tmp.name)

        return jsonify({"text": result["text"].strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))