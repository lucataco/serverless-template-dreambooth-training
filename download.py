# In this file, we define download_model
# It runs during container build time to get model weights built into the container

import os
import torch
from diffusers import StableDiffusionPipeline
from diffusers.models import AutoencoderKL
from huggingface_hub import HfFolder
from transformers import pipeline

# Download the weights
def download_model():
    # do a dry run of running models, which will download weights
    TOKEN = os.getenv('HF_AUTH_TOKEN')
    HfFolder.save_token(TOKEN)
    
    print("downloading model: stabilityai/sd-vae-ft-mse & runwayml/stable-diffusion-v1-5...")

    model = "runwayml/stable-diffusion-v1-5"
    vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse")
    pipe = StableDiffusionPipeline.from_pretrained(model, vae=vae)

    print("done")


if __name__ == "__main__":
    download_model()