import os
import sys
from PIL import Image
import numpy as np

def process_image(filename, save_dir):
    img = Image.open(filename)
    img = img.resize((1280, 704), Image.BILINEAR)
    output_path = os.path.join(save_dir, os.path.basename(filename))
    img.save(output_path)
    print(f"Resized and saved: {output_path}")

if __name__ == "__main__":
    input_dir = "/storage_local/kwang/repos/PPD-examples/data/synthia/RGB"
    output_dir = "synthia"
    os.makedirs(output_dir, exist_ok=True)
    for img_name in os.listdir(input_dir):
        if img_name.endswith('.png'):
            img_path = os.path.join(input_dir, img_name)
            process_image(img_path, output_dir)
