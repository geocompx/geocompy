# Aim: update requirements.txt
# Source: https://stackoverflow.com/questions/50777849
conda activate geocompy
conda install pip
pip freeze > requirements.txt