import pandas as pd
import os

Data = pd.read_csv(r"df_Delanteros_medias.csv")
pd.set_option('display.max_columns', None)
print(Data)