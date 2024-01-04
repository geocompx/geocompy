# Aim: convert .qmd files to .ipynb and .py files

# Convert to ipynb files (requires bash, not PowerShell):
for i in *.qmd; do
  quarto convert $i
done

# Convert ipynb files to .py files
# jupytext --to py *.ipynb
for i in *.ipynb; do
  jupyter nbconvert --to python $i
done

# Remove irrelevant files
rm code/chapters/index.py 
rm code/chapters/preface.py 
rm code/chapters/README.py
rm ipynb/README.ipynb

# Move files to correct folders
mv *.py -v code/chapters
mv *.ipynb -v ipynb

