# Runtime stage
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel

# Install build dependencies required for pyaudio (as root)
RUN apt-get update && apt-get install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m appuser
USER appuser

# Set working directory
WORKDIR /app

# Copy Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Install CUDA-compatible dependencies
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117

# Download and install the canopylabs/orpheus-3b-0.1-pretrained model
RUN pip install git+https://github.com/canopylabs/orpheus.git@3b-0.1-pretrained

# Pre-download the TTS model to avoid runtime delays (GPU enabled)
RUN python -c "from realtime_tts import RealTimeTTS; tts = RealTimeTTS(model='canopylabs/orpheus-3b-0.1-pretrained', device='cuda')"

# Copy application files
COPY app.py /app/app.py
COPY index.html /app/index.html

# Expose Flask port
EXPOSE 5000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:5000/ || exit 1

# Start the Flask app
CMD ["python", "app.py"]