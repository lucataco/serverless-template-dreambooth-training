#!/bin/bash
export NUM_STEPS=1200
export MODEL_NAME="runwayml/stable-diffusion-v1-5"
export OUTPUT_DIR="stable_diffusion_weights/"
export LD_LIBRARY_PATH=/usr/lib/wsl/lib:$LD_LIBRARY_PATH

accelerate launch train_dreambooth.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --pretrained_vae_name_or_path="stabilityai/sd-vae-ft-mse" \
  --output_dir=$OUTPUT_DIR \
  --with_prior_preservation --prior_loss_weight=1.0 \
  --seed=3434554 \
  --resolution=512 \
  --train_batch_size=1 \
  --train_text_encoder \
  --mixed_precision="fp16" \
  --use_8bit_adam \
  --gradient_accumulation_steps=1 \
  --learning_rate=1e-6 \
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --num_class_images=50 \
  --sample_batch_size=1 \
  --max_train_steps=$NUM_STEPS \
  --save_interval=$NUM_STEPS \
  --save_sample_prompt="photo of sks person" \
  --concepts_list="concepts_list.json" \
  --pad_tokens
