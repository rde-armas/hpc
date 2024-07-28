import folium
from folium.plugins import HeatMap
import pandas as pd
import json
import sys
from pyproj import Proj, transform

def crear_mapa_de_calor(json_file_path, key_integer, parada_acenso):
    # Cargar el JSON desde el archivo
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo {json_file_path} no se encuentra.")
        return

    otro_texto = '00-10'  # Asegúrate de que este texto coincida con el del JSON
    # Construir la clave correctamente
    key = f'({key_integer}, \'{otro_texto}\')'
    print(f"Buscando clave: {key}")

    matrix = None
    for item in data:
        if key in item:
            matrix = item[key]
            break

    if matrix is None:
        raise ValueError(f"No se encontró la matriz para la clave {key_integer}")

    # Extraer las columnas necesarias en un solo bucle
    paradas = []
    for row in matrix:
        paradas.append(row[0])
    
    paradas = [int(numero) for numero in paradas]
    cant_paradas = len(paradas)
    print('cant paradas', len(paradas), paradas)

    # Cargar el archivo CSV paradas en un DataFrame
    df_paradas_lineas = pd.read_csv('csv\\paradas_lineas_direc.csv')

    # Filtrar el DataFrame para mantener solo las columnas 'COD_UBIC_P', 'X' y 'Y'
    df_paradas_lineas = df_paradas_lineas[['COD_UBIC_P', 'COD_VARIAN', 'X', 'Y']]

    # Filtrar el DataFrame para mantener solo las filas donde 'COD_UBIC_P' coincide con las paradas
    df_paradas_lineas = df_paradas_lineas[df_paradas_lineas['COD_VARIAN'] == key_integer]

    # Eliminar duplicados
    df_paradas_lineas = df_paradas_lineas.drop_duplicates()

    df_paradas_lineas = df_paradas_lineas.reset_index(drop=True)

    print(df_paradas_lineas)
    
    df_paradas_lineas_filtradas = df_paradas_lineas[df_paradas_lineas.index >= df_paradas_lineas[df_paradas_lineas['COD_UBIC_P'] == parada_acenso].index[0]]
    
    print(df_paradas_lineas_filtradas)

    index = df_paradas_lineas_filtradas[df_paradas_lineas_filtradas['COD_UBIC_P'] == parada_acenso].index[0]


    probabilidades = []
    for row in matrix:
            probabilidades.append(row[index + 1])


    #Filtro probabilidades
    num_filas = df_paradas_lineas_filtradas.shape[0]
    print('numero de paradas siguientes', num_filas)
    n = cant_paradas - num_filas
    probabilidades = probabilidades[n:]

    print('cant prob', len(probabilidades), probabilidades)

    # Agregar las probabilidades de descenso a las paradas filtradas
    df_paradas_lineas_filtradas = df_paradas_lineas_filtradas.assign(probabilidad_descenso=probabilidades)

    print(df_paradas_lineas_filtradas)

    # Definir sistemas de coordenadas
    utm_proj = Proj('epsg:32721')  # Asegúrate de usar el código EPSG correcto para tus coordenadas UTM
    wgs84_proj = Proj('epsg:4326')

    # Convertir coordenadas UTM a latitud y longitud
    def convert_coordinates(row):
        lon, lat = transform(utm_proj, wgs84_proj, row['X'], row['Y'])
        return pd.Series([lat, lon])

    df_paradas_lineas_filtradas[['lat', 'lon']] = df_paradas_lineas.apply(convert_coordinates, axis=1)

    # Crear un mapa centrado en Montevideo
    mapa = folium.Map(location=[-34.9011, -56.1645], zoom_start=13)

    # Preparar datos para el HeatMap
    heat_data = df_paradas_lineas_filtradas[['lon', 'lat', 'probabilidad_descenso']].values.tolist()

    # Agregar el HeatMap al mapa
    HeatMap(heat_data).add_to(mapa)

    df_paradas_lineas_filtradas = df_paradas_lineas_filtradas.reset_index(drop=True)

    # Agregar iconos para cada parada de ómnibus
    for index, row in df_paradas_lineas_filtradas.iterrows():
        if index == 0:
            icon_color = 'green' if index == 0 else 'blue'  # El primer icono es verde, el resto azul
            folium.Marker(
            location=[row['lon'], row['lat']],
            popup=f"Parada: {row['COD_UBIC_P']}<br>Probabilidad de descenso: {row['probabilidad_descenso']}",
            icon=folium.Icon(icon="bus", prefix='fa', color=icon_color)
            ).add_to(mapa)

    # Guardar el mapa como archivo HTML
    mapa.save('mapa_de_calor_con_iconos.html')

if __name__ == "__main__":
    crear_mapa_de_calor('resultados.json', 218, 4912)