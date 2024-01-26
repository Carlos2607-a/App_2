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

# Obtén todas las ligas únicas en el dataframe
ligas = ["Todas las ligas"] + Data['League'].unique().tolist()
liga_seleccionada = st.selectbox("¿Qué liga deseas ver?", ligas)

# Filtra el dataframe por la liga seleccionada, a menos que el usuario haya seleccionado "Todas las ligas"
if liga_seleccionada != "Todas las ligas":
    Data = Data[Data['League'] == liga_seleccionada]

# Define las características para cada posición
caracteristicas_por_posicion = {
    "Delanteros": ["Big chances missed","Goals","Headed goals"],
    "Mediocampista": ["Interceptions", "Goals","Assists"],
    "Defensas": ["Tackles", "Interceptions"],
    "Porteros": ["Aerial duels won %", "Penalties faced", "Saves"]
}

# Obtén las características para la posición seleccionada
caracteristicas = caracteristicas_por_posicion[opcion]

# Convierte las columnas a tipo numérico para evitar el error
Data[caracteristicas] = Data[caracteristicas].apply(pd.to_numeric, errors='coerce')

# Calcula el score total para cada jugador
Data['Score total'] = Data[caracteristicas].sum(axis=1)

# Ordena el dataframe por el score total y toma los primeros 10
Data = Data.sort_values(by='Score total', ascending=False)
top_jugadores = Data.head(10)

# Muestra los resultados
st.write("Los 10 mejores jugadores según el score total son:")
st.write(top_jugadores[['Name', 'Score total', 'League']])

