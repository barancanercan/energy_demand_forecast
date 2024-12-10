import warnings
import pandas as pd
import missingno as msno
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Tüm uyarıları kapat
warnings.filterwarnings("ignore")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 500)

