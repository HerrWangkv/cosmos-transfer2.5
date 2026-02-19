import argparse
import json
from pathlib import Path
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Prepare sim2real batch input json")
    parser.add_argument("--input_dir", type=str, required=True, help="Directory containing images")
    parser.add_argument("--output_dir", type=str, required=True, help="Path to save the output JSON spec")
    parser.add_argument("--prompt", type=str, default="a photorealistic urban street scene under clear weather with soft late-afternoon daylight, natural lighting, realistic materials and textures, real-world camera photo.", help="Prompt for generation")
    return parser.parse_args()

def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    depth_json = os.path.join(args.output_dir, "depth.json")
    depth_edge_json = os.path.join(args.output_dir, "depth_edge.json")
    depth_lst = []
    depth_edge_lst = []
    for img_idx in range(9400):
        img_path = os.path.join(args.input_dir, f"{img_idx:07d}.png")
        data = {
            "name": os.path.basename(img_path).split('.')[0],
            "prompt": args.prompt,
            "video_path": "/workspace/"+str(img_path),
            "num_video_frames_per_chunk": 1,
            "max_frames": 1,
            "seed": 1,
            "depth": {},
        }
        depth_lst.append(data.copy())
        data["edge"] = {}
        depth_edge_lst.append(data)
    with open(depth_json, 'w') as f:
        json.dump(depth_lst, f, indent=4)
    with open(depth_edge_json, 'w') as f:
        json.dump(depth_edge_lst, f, indent=4)
    print(f"Saved JSON spec to: {depth_json} and {depth_edge_json}")

if __name__ == "__main__":
    main()
