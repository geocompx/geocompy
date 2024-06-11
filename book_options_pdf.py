import os
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.max_rows', 6)
pd.set_option('display.max_columns', 5)
plt.rcParams['figure.figsize'] = (5, 5)

if os.environ['QUARTO_PANDOC_TO'] == 'html':
  pd.options.display.max_colwidth = 35
if os.environ['QUARTO_PANDOC_TO'] == 'latex':
  pd.options.display.max_colwidth = 13
