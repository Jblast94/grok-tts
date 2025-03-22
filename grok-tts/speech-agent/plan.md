# Plan to Make Speech-Agent Work on RunPod GPU Instance with Minimal Latency

## Overview
This plan outlines the steps required to adapt the speech-agent project to work on a RunPod GPU instance or VM with minimal latency, including the installation of the `canopylabs/orpheus-3b-0.1-pretrained` model as a test.

## Steps

### Step 1: Update Dockerfile for GPU Support and New Model
- **Action**: Modify the Dockerfile to use a GPU-enabled PyTorch image and install the `canopylabs/orpheus-3b-0.1-pretrained` model.
- **Details**: Change the base image to `pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel` and add commands to download and install the new model.
- **Reason**: This will allow us to leverage GPU acceleration and test the new model.

### Step 2: Install CUDA-Compatible Dependencies
- **Action**: Update the Dockerfile to install CUDA-compatible versions of dependencies.
- **Details**: Ensure that packages like `realtime-tts` are installed with CUDA support.
- **Reason**: To ensure all dependencies can utilize the GPU for faster processing.

### Step 3: Load TTS Model on GPU
- **Action**: Modify `app.py` to load the `canopylabs/orpheus-3b-0.1-pretrained` model on the GPU.
- **Details**: Change the `device` variable to always use "cuda" if available, and update the `RealTimeTTS` initialization to use the new model.
- **Reason**: To ensure the new TTS model runs on the GPU for faster processing.

### Step 4: Performance Testing
- **Action**: Implement performance tests to measure latency and compare the performance of the new model against the existing one.
- **Details**: Add a script or modify existing code to measure the time taken for text-to-speech conversion with both models.
- **Reason**: To verify that the changes result in real-time processing with minimal latency and to assess the new model's performance.

### Step 5: Configure RunPod Instance
- **Action**: Set up the RunPod instance with GPU support.
- **Details**: Choose an instance with a suitable GPU (e.g., NVIDIA A40), expose port 5000, and set the `MODEL_NAME` environment variable to use the `canopylabs/orpheus-3b-0.1-pretrained` model.
- **Reason**: To ensure the project runs on a GPU-enabled environment with the correct configuration for the new model.

### Step 6: Deployment and Verification
- **Action**: Deploy the updated Docker image to RunPod and verify functionality.
- **Details**: Build and push the new Docker image, deploy it on RunPod, and test the speech-agent through the public URL with the new model.
- **Reason**: To confirm that the project works as expected on a RunPod GPU instance with the new model.

## Mermaid Diagram

```mermaid
graph TD
A[Update Dockerfile for GPU Support and New Model] --> B[Install CUDA-Compatible Dependencies]
B --> C[Load TTS Model on GPU]
C --> D[Performance Testing]
D --> E[Configure RunPod Instance]
E --> F[Deployment and Verification]