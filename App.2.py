import pandas as pd
import unicodedata
import streamlit as st

@st.cache
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

# Mapeo de las opciones del usuario a los nombres de las columnas en el dataframe
mapeo_opciones = {
    "Goles": "Goals",
    "Jugador con mas faltas recibidas": "Was fouled",
    "Asistencias": "Assists",
    "Oportunidades de gol creadas": "Big chances created",
    "Entradas": "Tackles",
    "Rechazos": "Clearances",
    "Intercepciones": "Interceptions",
    "Salvadas": "Saves",
    "Porteria invicta": "Clean sheets",
    "Penaltis salvados": "Penalties saved"
}

# Define las 5 características para cada posición
caracteristicas_por_posicion = {
    "Delanteros": ["Big chances missed","Goals","Headed goals"],
    "Mediocampista": ["Set piece conversion", "Dribbled past","Assists"],
    "Defensas": ["Tackles", "Interceptions", "Was fouled"],
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

# Muestra el máximo en cada característica
for caracteristica in caracteristicas:
    max_jugador = Data.loc[Data[mapeo_opciones[caracteristica]].idxmax()]
    st.write(f"El jugador con el máximo {caracteristica} es:")
    st.write(max_jugador[['Name', mapeo_opciones[caracteristica], 'League']])
