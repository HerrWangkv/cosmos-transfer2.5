import argparse
import json
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Prepare sim2real batch input json")
    parser.add_argument("--input_dir", type=str, required=True, help="Directory containing images")
    parser.add_argument("--output_dir", type=str, required=True, help="Path to save the output JSON spec")
    parser.add_argument("--prompt", type=str, default="a photorealistic urban street scene under clear weather with soft late-afternoon daylight, natural lighting, realistic materials and textures, real-world camera photo.", help="Prompt for generation")
    parser.add_argument("--gpu_num", type=int, required=True, help="Number of GPUs to split the configs across")
    return parser.parse_args()

def split_list(data_list, num_chunks):
    # Safely divide the list into exact number of chunks
    k, m = divmod(len(data_list), num_chunks)
    return [data_list[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(num_chunks)]

def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    depth_lst = []
    depth_edge_lst = []
    depth_edge_seg_lst = []

    for img_idx in range(9400):
        img_path = os.path.join(args.input_dir, f"{img_idx:07d}.png")
        data = {
            "name": os.path.basename(img_path).split('.')[0],
            "prompt": args.prompt,
            "video_path": "/workspace/" + str(img_path),
            "num_video_frames_per_chunk": 1,
            "max_frames": 1,
            "seed": 1,
            "depth": {},
        }
        depth_lst.append(data.copy())
        
        data["edge"] = {}
        depth_edge_lst.append(data.copy())
        
        data["seg"] = {}
        depth_edge_seg_lst.append(data.copy())

    depth_chunks = split_list(depth_lst, args.gpu_num)
    depth_edge_chunks = split_list(depth_edge_lst, args.gpu_num)
    depth_edge_seg_chunks = split_list(depth_edge_seg_lst, args.gpu_num)

    for i in range(args.gpu_num):
        depth_json = os.path.join(args.output_dir, f"depth_part_{i}.json")
        depth_edge_json = os.path.join(args.output_dir, f"depth_edge_part_{i}.json")
        depth_edge_seg_json = os.path.join(args.output_dir, f"depth_edge_seg_part_{i}.json")

        with open(depth_json, 'w') as f:
            json.dump(depth_chunks[i], f, indent=4)
        with open(depth_edge_json, 'w') as f:
            json.dump(depth_edge_chunks[i], f, indent=4)
        with open(depth_edge_seg_json, 'w') as f:
            json.dump(depth_edge_seg_chunks[i], f, indent=4)

        print(f"Saved part {i} JSON specs to {args.output_dir}")

if __name__ == "__main__":
    main()