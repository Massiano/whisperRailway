FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Install CPU-only PyTorch 2.1.2 — this wheel exists and works
RUN pip install --no-cache-dir \
    torch==2.1.2+cpu \
    torchaudio==2.1.2+cpu \
    -f https://download.pytorch.org/whl/cpu/torch_stable.html

RUN pip install --no-cache-dir \
    openai-whisper==20231117 \
    Flask==2.3.3

COPY app.py .

CMD ["python", "app.py"]
