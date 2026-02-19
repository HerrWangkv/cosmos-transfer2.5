#!/bin/bash

docker build -t cosmos-transfer25 .

docker run -it --rm --gpus all --ipc=host \
    -v .:/workspace \
    -v /workspace/.venv \
    -v /root/.cache:/root/.cache \
    -e HF_TOKEN="$HUGGING_FACE_TOKEN" cosmos-transfer25