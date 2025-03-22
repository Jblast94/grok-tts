# Live Streaming Speech Agent

## Project Overview

This project aims to create a Docker container that encapsulates a text-to-speech (TTS) system with a web interface, deployable on RunPod with minimal effort. The system uses the fastspeech2-en-ljspeech model from the realtime-tts library for real-time audio streaming, and Flask as the web framework.

## Files

### Dockerfile
Defines the Docker image, including dependencies and the application setup.

### requirements.txt
Lists the Python packages needed:
- flask
- realtime-tts

### app.py
The Flask application that serves the web interface, streams audio, and provides performance testing functionality.

#### Performance Testing
The app.py file includes a `/performance` endpoint that allows users to measure the time taken for text-to-speech conversion. To use this feature, send a POST request to `/performance` with a JSON payload containing the text to be converted. The response will include the duration of the conversion process in seconds.

Example usage:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"text": "Hello, world!"}' http://localhost:5000/performance
```

### index.html
A simple web interface for users to input text and play audio.

## Usage

1. **Build the Docker Image:**
   ```
   docker build -t yourusername/live-streaming-speech-agent:latest .
   ```
   Replace `yourusername` with your Docker Hub username.

2. **Push the Image to Docker Hub:**
   ```
   docker push yourusername/live-streaming-speech-agent:latest
   ```
   You'll need a Docker Hub account and to log in (`docker login`) first.

3. **Deploy on RunPod:**
   - Go to RunPod and log in or sign up.
   - Click "Deploy" or "New Pod" to create a new pod.
   - Configure the pod:
     - Container Image: Enter `yourusername/live-streaming-speech-agent:latest`.
     - Instance Type: Select a GPU instance (e.g., NVIDIA A40 or similar).
     - Exposed Ports: Set to 5000 (HTTP).
     - (Optional) Environment Variables: Add `MODEL_NAME` if you want a different TTS model (e.g., `xtts` for higher quality, though it's larger).
   - Click "Deploy" or "Start" to launch the pod.

4. **Use the Speech Agent:**
   - Open the public URL provided by RunPod in a browser.
   - Type text into the textarea.
   - Click "Play" to hear the text spoken in real-time.

## Deployment on DigitalOcean

### Prerequisites
1. DigitalOcean account
2. Docker Hub account
3. Domain name (optional)

### Deployment Steps

1. **Create a DigitalOcean Droplet:**
   - Choose Ubuntu 20.04 LTS
   - Select a CPU-Optimized droplet (minimum 4GB RAM)
   - Enable monitoring
   - Add your SSH key

2. **Configure Domain (Optional):**
   - Add an A record pointing to your droplet's IP
   - Update `nginx.conf` with your domain

3. **Deploy the Application:**
   ```bash
   # Configure deployment variables
   vim deployment/deploy.sh
   
   # Make scripts executable
   chmod +x deployment/*.sh
   
   # Run deployment
   ./deployment/deploy.sh
   ```

4. **Monitor the Application:**
   - Access logs: `docker logs speech-agent`
   - Nginx logs: `/var/log/nginx/`
   - Gunicorn logs: `/var/log/gunicorn/`

### Security Considerations
- Enable UFW firewall
- Configure SSL with Let's Encrypt
- Keep system and packages updated
- Monitor system resources

### Scaling
To handle more traffic:
1. Increase Gunicorn workers
2. Use larger droplet
3. Enable DigitalOcean monitoring
4. Consider load balancing for high availability

## Quick Deployment on DigitalOcean

### Prerequisites
1. DigitalOcean droplet with Docker installed
2. Git installed on the droplet
3. Domain name (optional)

### One-Command Deployment
1. SSH into your droplet:
   ```bash
   ssh root@your_droplet_ip
   ```

2. Clone and run:
   ```bash
   git clone https://github.com/yourusername/grok-tts.git
   cd grok-tts
   chmod +x deployment/deploy.sh
   ./deployment/deploy.sh
   ```

The application will be available at `http://your_droplet_ip`.

### Updating the Application
To update to the latest version:
```bash
cd /opt/speech-agent
./deployment/deploy.sh
```

### Monitoring
View logs with:
```bash
docker compose logs -f speech-agent
```

## Customization (Optional)

- **Change TTS Model:** Set the `MODEL_NAME` environment variable in RunPod to use a different model (e.g., `xtts` for higher quality, ~1.5GB).
- **Port:** If you need a different port, update `EXPOSE` in the Dockerfile and the `app.run()` port in `app.py`.

## Why This Approach?

- **No Subscriptions:** Uses open-source `realtime-tts`, avoiding APIs like OpenAI.
- **Simplicity:** Docker and Flask minimize setup complexity.
- **RunPod Compatibility:** Leverages RunPod's GPU support and public URL feature.
- **Practicality:** The fastspeech2 model balances quality, speed, and size.

This template provides a functional, 1-click deployable live streaming speech agent that meets the project requirements.
