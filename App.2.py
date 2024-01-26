import pandas as pd
import unicodedata
import streamlit as st

def importar_datos(posicion):
    filename = f"df_{posicion}_medias.csv"
    df = pd.read_csv(filename)
    return df

st.set_page_config(layout="wide")

st.write("¡Bienvenido a la aplicación de FutMatch!")

opciones = ["Delanteros", "Mediocampista", "Defensas", "Porteros"]
opcion = st.selectbox("¿Qué posición deseas consultar?", opciones)

Data = importar_datos(opcion)
Data_copy = Data.copy()
# Obtén todas las ligas únicas en el Data_copyframe
ligas = ["Todas las ligas"] + Data_copy['League'].unique().tolist()
liga_seleccionada = st.selectbox("¿Qué liga deseas ver?", ligas)

# Filtra el Data_copyframe por la liga seleccionada, a menos que el usuario haya seleccionado "Todas las ligas"
if liga_seleccionada != "Todas las ligas":
    Data_copy = Data_copy[Data_copy['League'] == liga_seleccionada]

# Define las características para cada posición con su respectivo peso
caracteristicas_por_posicion = {
    "Delanteros": {"Big chances missed": -1, "Goals": 1, "Headed goals": 1},
    "Mediocampista": {"Interceptions": 1, "Goals": 1, "Assists": 1},
    "Defensas": {"Tackles": 1, "Interceptions": 1},
    "Porteros": {"Aerial duels won %": 1, "Penalties faced": -1, "Saves": 1}
}

# Obtén las características para la posición seleccionada
caracteristicas = caracteristicas_por_posicion[opcion]

# Convierte las columnas a tipo numérico para evitar el error
for caracteristica in caracteristicas:
    Data_copy[caracteristica] = pd.to_numeric(Data_copy[caracteristica], errors='coerce')

# Calcula el score total para cada jugador teniendo en cuenta el peso de cada característica
Data_copy['Score total'] = sum(Data_copy[caracteristica] * peso for caracteristica, peso in caracteristicas.items())

# Ordena el Data_copyframe por el score total y toma los primeros 10
Data_copy = Data_copy.sort_values(by='Score total', ascending=False)
top_jugadores = Data_copy.head(10)

# Muestra los resultados
st.write("Los 10 mejores jugadores según el score total son:")
st.write(top_jugadores[['Name', 'Score total', 'League']])


