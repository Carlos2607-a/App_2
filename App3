import pandas as pd
import streamlit as st

def importar_datos():
    posiciones = ["Delanteros", "Mediocampista", "Defensas", "Porteros"]
    dfs = []
    for posicion in posiciones:
        filename = f"df_{posicion}_medias.csv"
        df = pd.read_csv(filename)
        df['Posicion'] = posicion
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
caracteristicas_por_posicion = {
    # Tus características aquí
}

# Calcula el score total para cada jugador teniendo en cuenta el peso de cada característica
for posicion, caracteristicas in caracteristicas_por_posicion.items():
    Data_posicion = Data_copy[Data_copy['Posicion'] == posicion]
    for caracteristica in caracteristicas:
        Data_posicion[caracteristica] = pd.to_numeric(Data_posicion[caracteristica], errors='coerce')
    Data_posicion['Score total'] = sum(Data_posicion[caracteristica] * peso for caracteristica, peso in caracteristicas.items() if peso > 0) - sum(Data_posicion[caracteristica] * abs(peso) for caracteristica, peso in caracteristicas.items() if peso < 0)
    Data_copy[Data_copy['Posicion'] == posicion] = Data_posicion

# Ordena el dataframe por el score total y selecciona los mejores jugadores por posición
mejores_jugadores = pd.concat([
    Data_copy[Data_copy['Posicion'] == 'Delanteros'].sort_values(by='Score total', ascending=False).head(4),
    Data_copy[Data_copy['Posicion'] == 'Mediocampista'].sort_values(by='Score total', ascending=False).head(4),
    Data_copy[Data_copy['Posicion'] == 'Defensas'].sort_values(by='Score total', ascending=False).head(3),
    Data_copy[Data_copy['Posicion'] == 'Porteros'].sort_values(by='Score total', ascending=False).head(2)
])

# Muestra los resultados
st.write("Los 13 mejores jugadores según el score total son:")
st.write(mejores_jugadores[['Name', 'Score total', 'League', 'Posicion']])
