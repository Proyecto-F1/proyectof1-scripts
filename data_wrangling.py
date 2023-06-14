import pandas as pd
import numpy as np
import os

for file in os.listdir('data'):
    if file.endswith('.csv'):
        df = pd.read_csv(f'data/{file}')
        df.replace(regex=r'\\[A-Za-z]', value=np.nan, inplace=True)
        df.to_csv(f'clean_data/{file}')
