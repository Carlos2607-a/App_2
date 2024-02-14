import pandas as pd
import streamlit as st

def importar_datos():
    posiciones = ["Delanteros", "Mediocampista", "Defensas", "Porteros"]
    dfs = []
    for posicion in posiciones:
        filename = f"df_{posicion}_medias.csv"
        df = pd.read_csv(filename)
        df['Position'] = posicion
        dfs.append(df)
    return pd.concat(dfs)

st.set_page_config(layout="wide")

st.write("¡Bienvenido a la aplicación de FutMatch!")

# Obtén todas las ligas únicas en el dataframe
Data = importar_datos()
Data_copy = Data.copy()
ligas = ["Todas las ligas"] + sorted(Data_copy['League'].unique().tolist())
liga_seleccionada = st.selectbox("¿Qué liga deseas ver?", ligas)

# Filtra el dataframe por la liga seleccionada, a menos que el usuario haya seleccionado "Todas las ligas"
if liga_seleccionada != "Todas las ligas":
    Data_copy = Data_copy[Data_copy['League'] == liga_seleccionada]

# Define las características para cada posición con su respectivo peso
caracteristicas_por_posicion =  {
    "Delanteros": {'Goals':2.55, 'Headed goals':1.2, 'Total shots':1, 'Assists':1, 'Big chances created':2.6, 'Was fouled':1,'Set piece conversion %':0.55, 'Accurate passes %':0.6, 'Successful dribbles %':0.5, 'Total duels won %':0.3,'Big chances missed':-0.25},
    "Mediocampista": {'Set piece conversion %':0.45,'Dribbled past':0.8,'Assists':1.5,'Big chances created':1.8,'Accurate final third passes':1,'Was fouled':0.5,'Tackles':1.5,'Fouls':0.35,'Total shots':1,'Accurate long balls %':1,'Accurate passes %':0.75,'Successful dribbles %':0.75,'Total passes':1.5,'Interceptions':1.55,'Goals':1.5,'Total duels won %':1.8},
    "Defensas": {'Penalty committed': -0.5,'Interceptions': 0.55,'Errors lead to goal': -0.65,'Total passes': 0.65,'Tackles': 1,'Goals conceded inside the box': -0.4,'Aerial duels won %': 0.9,'Total duels won %': 1,'Accurate passes %': 0.5,'Fouls': -0.4,'Dribbled past': -0.6},
    "Porteros": {'Penalties saved': 0.5,'Saves': 2,'Errors lead to goal': -1,'Clean sheets': 3,'Aerial duels won %': 0.75,'Total duels won %': 1.5,'Penalty committed': -0.5,'Goals conceded inside the box': 1,'Goals conceded outside the box': -0.75,'Total passes': 0.5,'Accurate long balls %': 0.5,'Accurate passes %': 0.5}
}

# Calcula el score total para cada jugador teniendo en cuenta el peso de cada característica
resultados = []
for posicion, caracteristicas in caracteristicas_por_posicion.items():
    Data_posicion = Data_copy[Data_copy['Position'] == posicion].copy()
    for caracteristica in caracteristicas:
        Data_posicion[caracteristica] = pd.to_numeric(Data_posicion[caracteristica], errors='coerce')
    Data_posicion['Score total'] = sum(Data_posicion[caracteristica] * peso for caracteristica, peso in caracteristicas.items() if peso > 0) - sum(Data_posicion[caracteristica] * abs(peso) for caracteristica, peso in caracteristicas.items() if peso < 0)
    resultados.append(Data_posicion)

Data_copy = pd.concat(resultados)

# Ordena el dataframe por el score total y selecciona los mejores jugadores por posición
mejores_jugadores = pd.concat([
    Data_copy[Data_copy['Position'] == 'Delanteros'].sort_values(by='Score total', ascending=False).head(4),
    Data_copy[Data_copy['Position'] == 'Mediocampista'].sort_values(by='Score total', ascending=False).head(4),
    Data_copy[Data_copy['Position'] == 'Defensas'].sort_values(by='Score total', ascending=False).head(3),
    Data_copy[Data_copy['Position'] == 'Porteros'].sort_values(by='Score total', ascending=False).head(2)
])

# Muestra los resultados
st.write("Los 13 mejores jugadores según el score total son:")
st.write(mejores_jugadores[['Name', 'Score total', 'League', 'Posicion']])

