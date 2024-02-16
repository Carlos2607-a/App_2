import pandas as pd
import unicodedata
import streamlit as st

@st.cache
def importar_datos(posicion):
    filename = f"df_{posicion}_medias.csv"
    df = pd.read_csv(filename)
    return df

st.set_page_config(layout="wide")

st.write("¡Bienvenido a la aplicación The Best")

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

if opcion == "Delanteros":
    opciones = ["Goles", "Jugador con mas faltas recibidas", "Asistencias"]
elif opcion == "Mediocampista":
    opciones = ["Asistencias", "Oportunidades de gol creadas", "Entradas"]
elif opcion == "Defensas":
    opciones = ["Entradas", "Intercepciones", "Rechazos"]
elif opcion == "Porteros":
    opciones = ["Salvadas", "Penaltis salvados", "Porteria invicta"]
else:
    opciones = []

opcion = st.selectbox("¿Qué característica deseas ver?", opciones)

if opcion:
    columna_df = mapeo_opciones[opcion]
    max_jugador = Data.loc[Data[columna_df].idxmax()]
    st.write(max_jugador[['Name', columna_df, 'League']], width=1500)



