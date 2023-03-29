# Aim: unzip geocompy folder

from pathlib import Path 
data_path = Path("ipynb") 
if data_path.is_dir(): 
 print("path exists") # directory exists 
else: 
 print("Attempting to get and unzip the data") 
 import requests, zipfile, io 
 r = requests.get("https://github.com/geocompx/geocompy/archive/refs/heads/main.zip") 
 z = zipfile.ZipFile(io.BytesIO(r.content)) 
 z.extractall(".") 
# files are now in py-main/
