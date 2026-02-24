#! /bin/bash

# Configuration
DATA_DIR="/mrtstorage/users/kwang/nucarla_videos/rgb"
CONTAINER_DATA_DIR="/data_input"
SPEC_DIR="video_configs"

# Check if data directory exists
if [ ! -d "$DATA_DIR" ]; then
    echo "Error: Data directory $DATA_DIR does not exist."
    exit 1
fi

echo "Building Docker image..."
DOCKER_BUILDKIT=1 docker build -t cosmos-transfer25 .

echo "Running batch inference for data in $DATA_DIR..."
docker run -it --runtime=nvidia --ipc=host --rm \
    -v $PWD:/workspace \
    -v /workspace/.venv \
    -v /root/.cache:/root/.cache \
    -v "$DATA_DIR":"$CONTAINER_DATA_DIR" \
    -e HF_TOKEN="$HUGGING_FACE_TOKEN" \
    -e NCCL_P2P_DISABLE=1 \
    cosmos-transfer25 \
    bash -c "python scripts/prepare_sim2real_dataset.py --input_dir $CONTAINER_DATA_DIR --output_dir /workspace/$SPEC_DIR && \
             CUDA_VISIBLE_DEVICES=4,5,6,7 torchrun --nproc_per_node=4 examples/inference.py -i /workspace/$SPEC_DIR/depth_edge_seg.json -o /workspace/outputs/video_depth_edge_seg"
