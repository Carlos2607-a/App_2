import pandas as pd
import streamlit as st

def importar_datos(posicion, liga_seleccionada):
    filename = f"df_{posicion}_medias.csv"
    df = pd.read_csv(filename)
    df['Position'] = posicion
    return df

st.set_page_config(layout="wide")

st.write("¡Bienvenido a la aplicación de Dream Team!")

# Define las posiciones y cuántos jugadores quieres para cada posición
opciones = ["Delanteros", "Mediocampista", "Defensas", "Porteros"]
num_jugadores = {"Delanteros": 3, "Mediocampista": 4, "Defensas": 3, "Porteros": 1}

# Importa los datos y obtén todas las ligas únicas en el dataframe
Data = pd.concat([importar_datos(opcion, "Todas las ligas") for opcion in opciones])
Data_copy = Data.copy()

# Elimina los valores NaN y convierte todos los valores a strings
Data_copy['League'] = Data_copy['League'].dropna().astype(str).reset_index(drop=True)

# Ahora deberías poder obtener y ordenar las ligas únicas sin problemas
ligas = ["Todas las ligas"] + sorted(Data_copy['League'].unique().tolist())
liga_seleccionada = st.selectbox("¿Qué liga deseas ver?", ligas)

# Filtra los datos por la liga seleccionada
if liga_seleccionada != "Todas las ligas":
    Data = Data[Data['League'] == liga_seleccionada]
    Data_copy = Data.copy()

# Define las características para cada posición con su respectivo peso
caracteristicas_por_posicion =  {
    "Delanteros": {'Goals':2.55, 'Headed goals':1.2, 'Total shots':1, 'Assists':1, 'Big chances created':2.6, 'Was fouled':1,'Set piece conversion %':0.55, 'Accurate passes %':0.6, 'Successful dribbles %':0.5, 'Total duels won %':0.3,'Big chances missed':-0.25},
    "Mediocampista": {'Set piece conversion %':0.45,'Dribbled past':0.8,'Assists':1.5,'Big chances created':1.8,'Accurate final third passes':1,'Was fouled':0.5,'Tackles':1.5,'Fouls':0.35,'Total shots':1,'Accurate long balls %':1,'Accurate passes %':0.75,'Successful dribbles %':0.75,'Total passes':1.5,'Interceptions':1.55,'Goals':1.5,'Total duels won %':1.8},
    "Defensas": {'Penalty committed': -0.5,'Interceptions': 0.55,'Errors lead to goal': -0.65,'Total passes': 0.65,'Tackles': 1,'Goals conceded inside the box': -0.4,'Aerial duels won %': 0.9,'Total duels won %': 1,'Accurate passes %': 0.5,'Fouls': -0.4,'Dribbled past': -0.6},
    "Porteros": {'Penalties saved': 0.5,'Saves': 2,'Errors lead to goal': -1,'Clean sheets': 3,'Aerial duels won %': 0.75,'Total duels won %': 1.5,'Penalty committed': -0.5,'Goals conceded inside the box': 1,'Goals conceded outside the box': -0.75,'Total passes': 0.5,'Accurate long balls %': 0.5,'Accurate passes %': 0.5}
}

# Calcula el score total para cada jugador teniendo en cuenta el peso de cada característica
for posicion, caracteristicas in caracteristicas_por_posicion.items():
    Data_posicion = importar_datos(posicion, liga_seleccionada)
    for caracteristica in caracteristicas:
        Data_posicion[caracteristica] = pd.to_numeric(Data_posicion[caracteristica], errors='coerce')
    Data_posicion['Score total'] = sum(Data_posicion[caracteristica].fillna(0) * peso for caracteristica, peso in caracteristicas.items() if peso > 0) - sum(Data_posicion[caracteristica].fillna(0) * abs(peso) for caracteristica, peso in caracteristicas.items() if peso < 0)
    Data_copy.loc[Data_copy['Position'] == posicion, 'Score total'] = Data_posicion['Score total']

# Ordena el dataframe por el score total y selecciona los mejores jugadores por posición
mejores_jugadores = pd.concat([Data_copy[Data_copy['Position'] == posicion].sort_values(by='Score total', ascending=False).head(num_jugadores[posicion]) for posicion in opciones])

# Muestra los resultados
st.write("El mejor equipo de estrellas es:")
st.write(mejores_jugadores[['Name', 'League', 'Position']], truncate=False)

