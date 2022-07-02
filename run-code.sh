# Aim: run all Python scripts in code folder for testing outputs

# These are failing: 
# for f in code/chapters/*.py; do python "$f"; done
# for f in ipynb/*.ipynb; do ipython "$f"; done

for f in ipynb/*.ipynb; do jupyter nbconvert --execute --to html "$f"; done
