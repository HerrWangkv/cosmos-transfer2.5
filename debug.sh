#!/bin/bash

DOCKER_BUILDKIT=1 docker build -t cosmos-transfer25 .

docker run -it --rm --gpus all --ipc=host \
    -v $PWD:/workspace \
    -v /workspace/.venv \
    -v /root/.cache:/root/.cache \
    -e HF_TOKEN="$HUGGING_FACE_TOKEN" cosmos-transfer25