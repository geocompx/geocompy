zip -r data.zip data
Rscript -e "piggyback::pb_upload('data.zip', 'geocompr/py')"
