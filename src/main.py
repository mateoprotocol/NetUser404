from metrics import close_browser, get_transferred_and_time, is_connected, get_status_code, average_ping, is_connected_to_network, download_time
from identify import get_os, get_net_interface, get_mac, get_local_ip, get_bssid
from datetime import datetime
import time
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env

# Constantes
server_url = os.getenv("SERVER_URL")
server_port = os.getenv("SERVER_PORT")
URLS_FILE = os.getenv("FILE_URLS")
PING_TARGET = os.getenv("PING_TARGET")
SECRET_KEY = os.getenv("SECRET_KEY")

URL_API = f'http://{server_url}:{server_port}/metrics'
DATA_FILE = 'datos.json'

if not SECRET_KEY:
    raise ValueError("SECRET_KEY no está configurada")

headers = {
    "Authorization": SECRET_KEY
}


# Funciones auxiliares
def get_urls(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = [url.strip() for url in file if url.strip()]
    
    if not urls:
        raise ValueError(f"El archivo {file_path} está vacío o no contiene URLs válidas.")
    
    return urls

def get_deadline():
    """Solicita al usuario la hora y minuto límite."""
    while True:
        try:
            hora = int(input("Hora límite (0-23): "))
            minuto = int(input("Minuto límite (0-59): "))
            return datetime.now().replace(hour=hora, minute=minuto, second=0, microsecond=0)
        except ValueError:
            print("Por favor, ingresa valores válidos para la hora y el minuto.")

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

def send_to_api(datos, url_api, timeout=10):
    try:
        response = requests.post(url_api, json=datos, timeout=timeout, headers=headers)
        response.raise_for_status()  # Lanza una excepción si el código HTTP indica un error (4xx o 5xx)
        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json() if response.content else None  # Intenta parsear la respuesta si hay contenido
        }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Timeout", "message": "El tiempo de espera se agotó."}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": "HTTPError", "message": str(e), "status_code": response.status_code}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "RequestException", "message": str(e)}

def send_local_data(api_url,file_path):
    if os.path.exists(file_path):
        try:
            # Cargar los datos desde el archivo JSON
            with open(file_path, "r") as file:
                data = json.load(file)

            # Enviar los datos a la API
            response = requests.post(api_url, json=data)

            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                os.remove(file_path)  # Eliminar el archivo después de enviarlo
                return "Datos enviados y archivo eliminado con éxito."
            else:
                return f"Error al enviar datos: {response.status_code} - {response.text}"

        except Exception as e:
            return f"Ocurrió un error: {e}"
    else:
        return "No hay archivo 'datos.json' para enviar."

def send_data(datos, url_api, timeout=10):
    try:
        response = requests.post(url_api, json=datos, timeout=timeout, headers=headers)
        response.raise_for_status()  # Lanza una excepción si el código HTTP indica un error (4xx o 5xx)
        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json() if response.content else None  # Intenta parsear la respuesta si hay contenido
        }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Timeout", "message": "El tiempo de espera se agotó."}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": "HTTPError", "message": str(e), "status_code": response.status_code}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "RequestException", "message": str(e)}

def save_local_data(datos,file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as archivo:
            datos_existentes = json.load(archivo)
    else:
        datos_existentes = []
    datos_existentes.append(datos)
    with open(file_path, 'w') as archivo:
        json.dump(datos_existentes, archivo, indent=4)

# Programa principal
if __name__ == "__main__":
    try:
        #deadline = get_deadline()
        urls = get_urls(URLS_FILE)
        i=0
        id=0

        #while datetime.now() < deadline:
        while True:
            fecha = datetime.now().strftime("%Y-%m-%d")
            hora = datetime.now().strftime("%H:%M:%S")

            if i >= len(urls):
                i = 0

            url = urls[i]
            i += 1
            id +=1
            OS = get_os()
            interfaz = get_net_interface()
            mac = get_mac(interfaz)
            comentario = ""
            
            if is_connected_to_network():
                bssid = get_bssid(interfaz)
                ip = get_local_ip()
            else:
                comentario = "[No hay acceso a la red]"

            if os.path.exists(DATA_FILE):
                send_local_data(f"{URL_API}/datos",DATA_FILE)
            
            if is_connected():
                datos_transferidos, tiempo_carga = get_transferred_and_time(url)
                codigo_estado = get_status_code(url)
                latencia = average_ping(PING_TARGET)
                tiempo_descarga = download_time()
            else:
                comentario += "[No conexión a internet]"
                datos_transferidos = 0
                tiempo_carga = 9999.99
                codigo_estado = -1
                latencia = 9999.99
                url = "N/A"
                tiempo_descarga = 9999.99

            

            datos = {
                'id': str(id),
                'date': fecha,
                'hour': hora,
                'system': OS,
                'MAC': mac,
                'bssid': bssid,
                'ip': ip,
                'url': url,
                'status': codigo_estado,
                'load': tiempo_carga,
                'transferred': datos_transferidos,
                'delay': latencia,
                'download': tiempo_descarga,
                'comment': comentario
            }
            
            datos_info = send_data(datos, URL_API)
            print(datos_info)
            if datos_info["success"]:
                print("Envío exitoso de datos")
            else:
                print("No fue posible enviar los datos")
                datos["comment"] += "[No fue posible enviar el registro]"
                save_local_data(datos,DATA_FILE)
            print("*" * 20)

        print("Fin de la medición.")

    except Exception as e:
        print(f"Error en la ejecución del programa: {e}")
    finally:
        close_browser()
