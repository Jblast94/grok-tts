from flask import Flask, request, Response, send_from_directory, jsonify
from realtime_tts import RealTimeTTS
import logging
import os
import torch

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Allow model selection via environment variable, default to canopylabs/orpheus-3b-0.1-pretrained
model_name = os.getenv('MODEL_NAME', 'canopylabs/orpheus-3b-0.1-pretrained')

# Use GPU if available, otherwise raise an error
if torch.cuda.is_available():
    device = "cuda"
    logging.info("GPU is available, using CUDA.")
else:
    raise RuntimeError("GPU is not available. This application requires a GPU.")

tts = RealTimeTTS(model=model_name, device=device)

def generate_tts(text):
    """
    Generate TTS audio from the given text.

    Args:
        text (str): The text to convert to speech.

    Returns:
        generator: A generator yielding audio chunks.
    """
    try:
        for chunk in tts.stream(text):
            yield chunk
    except Exception as e:
        logging.error(f"Error in TTS generation: {e}")
        raise

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/tts', methods=['POST'])
def text_to_speech():
    try:
        text = request.json.get('text', '')
        if not text:
            return "No text provided", 400
        if len(text) > 1000:  # Input validation
            return "Text too long. Maximum 1000 characters allowed.", 400
        logging.info(f"Generating TTS for text: {text[:50]}{'...' if len(text) > 50 else ''}")
        return Response(generate_tts(text), mimetype='audio/wav')
    except Exception as e:
        logging.error(f"Error in TTS endpoint: {e}")
        return "Internal server error", 500

if __name__ == '__main__':
    import time

    def measure_tts_performance(text):
        start_time = time.time()
        for chunk in tts.stream(text):
            pass
        end_time = time.time()
        return end_time - start_time

    @app.route('/performance', methods=['POST'])
    def performance_test():
        try:
            text = request.json.get('text', '')
            if not text:
                return "No text provided", 400
            if len(text) > 1000:  # Input validation
                return "Text too long. Maximum 1000 characters allowed.", 400
            duration = measure_tts_performance(text)
            return jsonify({"duration": duration}), 200
        except Exception as e:
            logging.error(f"Error in performance test: {e}")
            return "Internal server error", 500
