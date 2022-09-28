# Aim: test building book in Docker container for reproducibility
docker pull ubuntu:22.04
docker run -it  -v $(pwd):/home/geo ubuntu:22.04 /bin/bash
apt update
apt -y upgrade
apt install -y python3-pip
apt install -y git
apt-get install libgdal-dev libgeos-dev libproj-dev -y

cd /home/geo
ls
pip install git+https://github.com/blaze/datashape
pip install -r requirements.txt


