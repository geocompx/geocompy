# Aim: run all Python scripts in code folder for testing outputs
# for f in code/chapters/*.py; do python "$f"; done
for f in ipynb/*.ipynb; do ipython "$f"; done
