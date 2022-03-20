# Aim: convert .qmd files to .ipynb and .py files

# Convert to ipynb files (requires bash, not PowerShell):
for i in *.qmd; do
  quarto convert $i
done

# Convert ipynb files to .py files
jupytext --to py *.ipynb

# Move files to correct folders
mv *.py -v code/chapters
mv *.ipynb -v ipynb

