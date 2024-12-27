from metrics import get_transferred_and_time, is_connected, get_status_code, ping
from network_identify import get_bssid, get_MAC, get_local_ip, detect_OS
from datetime import datetime
import time
import json
import os
import requests

# Constantes
URL_API = 'http://192.168.1.14:8000/metrics'
URLS_FILE = 'urls.txt'
DATA_FILE = 'datos.json'
PING_TARGET = '8.8.8.8'

# Funciones auxiliares
def get_urls(file_path):
    """Carga y limpia las URLs desde un archivo."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")
    with open(file_path, 'r') as file:
        return [url.strip() for url in file.readlines()]

def get_deadline():
    """Solicita al usuario la hora y minuto límite."""
    while True:
        try:
            hora = int(input("Hora límite (0-23): "))
            minuto = int(input("Minuto límite (0-59): "))
            return datetime.now().replace(hour=hora, minute=minuto, second=0, microsecond=0)
        except ValueError:
            print("Por favor, ingresa valores válidos para la hora y el minuto.")

def get_metrics_and_id(url, id):
    """Obtiene las métricas de red y sistema."""
    interfaz, bssid = get_bssid()
    mac_address = get_MAC(interfaz)
    ip = get_local_ip()
    sistema = detect_OS()
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")

    if is_connected():
        transferred, load = get_transferred_and_time(url)
        status = get_status_code(url)
        delay = ping(PING_TARGET, unit='ms')
    else:
        print("No hay conexión a internet.")
        transferred, load, status, delay = 0.0, 0.0, 0, 0.0

    return {
        'id': str(id),
        'date': fecha,
        'hour': hora,
        'system': sistema,
        'MAC': mac_address,
        'bssid': bssid,
        'ip': ip,
        'url': url,
        'status': status,
        'load': load,
        'transferred': transferred,
        'delay': delay
    }

def save_data(datos, file_path):
    """Guarda los datos localmente en un archivo JSON."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as archivo:
            datos_existentes = json.load(archivo)
    else:
        datos_existentes = []
    datos_existentes.append(datos)
    with open(file_path, 'w') as archivo:
        json.dump(datos_existentes, archivo, indent=4)

def send_to_api(datos, url_api):
    """Envía los datos a una API REST."""
    try:
        response = requests.post(url_api, json=datos)
        print(f"Envío a API: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error al enviar los datos a la API: {e}")

# Programa principal
if __name__ == "__main__":
    try:
        urls = get_urls(URLS_FILE)
        deadline = get_deadline()
        id = 0
        i = 0

        while datetime.now() < deadline:
            if i >= len(urls):  # Reinicio de la lista de URLs
                i = 0

            url = urls[i]
            i += 1

            print("*" * 20)
            datos = get_metrics_and_id(url, id)
            print(datos)

            save_data(datos, DATA_FILE)
            send_to_api(datos, URL_API)

            time.sleep(5)  # Esperar antes de la siguiente iteración
            id += 1

        print("*" * 20)
        print("Fin de la medición.")
    except Exception as e:
        print(f"Error en la ejecución del programa: {e}")
