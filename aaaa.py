import pandas as pd
import os

Data = pd.read_csv(r"df_Delanteros_medias.csv")

columnas_a_dividir =  ['Successful dribbles %', 'Accurate passes %', 'Aerial duels won %','Total duels won %']
# Divide todos los datos de las columnas por 10
Data[columnas_a_dividir] = Data[columnas_a_dividir] / 100


carpeta_destino = r"asas"
nombre_archivo = "df_delanteros_medias_corregido.csv"
# Combina la carpeta y el nombre del archivo para obtener la ruta completa
ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
# Guarda el DataFrame en el archivo CSV con la ruta completa
Data.to_csv(ruta_completa, index=False)