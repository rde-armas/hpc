import pandas as pd
import socket
import json

# ubicacion de archivos
VIAJES = './csv/cant_viajes_franja.csv'
COD_VARIAN = './csv/cod_varian.csv'
PARADA_LINEAS_DIREC = './csv/paradas_lineas_direc.csv'


def get_datasets():
    # Leer los archivos CSV
    df_viajes = pd.read_csv(VIAJES)
    df_origen_destino_linea = pd.read_csv(PARADA_LINEAS_DIREC)
    df_orden_paradas = pd.read_csv(COD_VARIAN)

    # Eliminar duplicados
    df_orden_paradas = df_orden_paradas.drop_duplicates(subset=['DESC_LINEA', 'COD_VARIAN'])

    # Convertir DataFrames a diccionarios
    data = { 
        'paradas_lineas_direc': df_origen_destino_linea.to_dict(orient='records'),  
        'cod_varian': df_orden_paradas.to_dict(orient='records'), 
        'df_cant_viajes_franja': df_viajes.to_dict(orient='records')
    }
    
    return data

def send_data(data, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))

    json_data = json.dumps(data)
    client_socket.sendall(json_data.encode())

    client_socket.close()

if __name__ == "__main__":
    port = 65432
    data = get_datasets()
    send_data(data, port)
