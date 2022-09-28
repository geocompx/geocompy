# Aim: test building book in Docker container for reproducibility
docker pull ubuntu:22.04
docker run -it  -v $(pwd):/home/geo ubuntu:22.04 /bin/bash
apt update
apt install software-properties-common -y
apt install python
python3
python -m ensurepip --upgrade
sudo apt install pip

