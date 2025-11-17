# Use slim Python 3.11 image (x86_64 Linux)
FROM python:3.11-slim

WORKDIR /app

# Install system deps (if needed for audio)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install CPU-only PyTorch from official index
RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

# Copy app
COPY . .

# Run
CMD ["python", "app.py"]
