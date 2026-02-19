#! /bin/bash

DOCKER_BUILDKIT=1 docker build -t cosmos-transfer25 .

docker run -it --runtime=nvidia --ipc=host --rm \
    -v $PWD:/workspace \
    -v /workspace/.venv \
    -v /root/.cache:/root/.cache \
    -e HF_TOKEN="$HUGGING_FACE_TOKEN" cosmos-transfer25 \
    bash -c "CUDA_VISIBLE_DEVICES=5 python examples/inference.py -i synthia_configs/depth_edge.json -o outputs/synthia_depth_edge"