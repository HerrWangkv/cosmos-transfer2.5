import argparse
import json
from pathlib import Path
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Prepare sim2real batch input json")
    parser.add_argument("--input_dir", type=str, required=True, help="Directory containing video sequences")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save output JSON specs")
    parser.add_argument("--prompt", type=str, default="A photorealistic driving scene in a city, view from a car dashboard. Natural lighting, urban buildings, trees, cars on the street. High resolution, realistic textures.", help="Prompt for generation")
    return parser.parse_args()

def main():
    args = parse_args()
    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    depth_json_path = output_dir / "depth.json"
    depth_edge_json_path = output_dir / "depth_edge.json"
    depth_edge_seg_json_path = output_dir / "depth_edge_seg.json"
    # Find all mp4 files
    all_videos = sorted(list(input_dir.glob("**/*.mp4")))
    
    # Filter out likely control videos to find "RGB" candidates
    rgb_candidates = []
    video_map = {} # path -> Path

    for vid in all_videos:
        video_map[str(vid)] = vid
        rgb_candidates.append(vid)

    depth_specs = []
    depth_edge_specs = []
    depth_edge_seg_specs = []
    for rgb_video in rgb_candidates:
        
        # 1. Same folder, name pattern substitution
        proposals = []
        stem = rgb_video.stem
    
        spec = {
            "name": rgb_video.stem.replace("_rgb", ""),
            "prompt": args.prompt,
            "video_path": str(rgb_video),
            "depth": {}
        }
        depth_specs.append(spec.copy())
        spec["edge"] = {}
        depth_edge_specs.append(spec.copy())
        spec["seg"] = {}
        depth_edge_seg_specs.append(spec.copy())
    
    print(f"Found {len(depth_specs)} videos.")
    if depth_specs:
        with open(depth_json_path, 'w') as f:
            json.dump(depth_specs, f, indent=2)
        print(f"Saved spec to {depth_json_path}")
        with open(depth_edge_json_path, 'w') as f:
            json.dump(depth_edge_specs, f, indent=2)
        print(f"Saved spec to {depth_edge_json_path}")
        with open(depth_edge_seg_json_path, 'w') as f:
            json.dump(depth_edge_seg_specs, f, indent=2)
        print(f"Saved spec to {depth_edge_seg_json_path}")
    else:
        print("No pairs found. Check your directory structure and naming conventions.")

if __name__ == "__main__":
    main()
