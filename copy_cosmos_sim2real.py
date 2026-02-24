import os
import shutil
import sys

def copy_images(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for i in range(0, 9400):
        filename = f"{i:07d}.jpg"
        src = os.path.join(input_dir, filename)
        dst = os.path.join(output_dir, filename)
        if os.path.isfile(src):
            shutil.copy2(src, dst)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python copy_cosmos_sim2real.py <input_dir> <output_dir>")
        sys.exit(1)
    copy_images(sys.argv[1], sys.argv[2])