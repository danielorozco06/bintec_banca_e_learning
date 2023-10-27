#!/usr/bin/env bash
set -e

sudo apt-get update && sudo apt-get install ffmpeg python3-pip espeak -y

pip3 install --upgrade pip

pip3 install -r requirements.txt

python3 src/main.py
