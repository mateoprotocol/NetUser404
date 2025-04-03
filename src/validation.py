import os
import json
import requests

def get_urls(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = [url.strip() for url in file if url.strip()]
    
    if not urls:
        raise ValueError(f"El archivo {file_path} está vacío o no contiene URLs válidas.")
    
    return urls

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
        response = requests.post(url_api, json=datos, timeout=timeout)
        response.raise_for_status()  # Lanza una excepción si el código HTTP indica un error (4xx o 5xx)
        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json() if response.content else None  # Intenta parsear la respuesta si hay contenido
        }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Timeout", "message": "El tiempo de espera se agotó."}
    except requests.exceptions.HTTPError as e:
        return {
            "success": False, 
            "error": "HTTPError", 
            "message": str(e),
            "status_code": response.status_code if 'response' in locals() else None  # Verificación de existencia
        }
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
        response = requests.post(url_api, json=datos, timeout=timeout)
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

def API_available(API_URL):
    resultado= None
    try:
        response = requests.get(API_URL, timeout=5)
        
        if response.status_code == 200:
            resultado = response.text.strip()  # Eliminamos posibles espacios en blanco
            if resultado == "1":
                print("La API está disponible (conectada a MongoDB).")
            elif resultado == "0":
                print("La API no está disponible (error al conectar a MongoDB).")
            else:
                print(f"Respuesta inesperada: {resultado}")
        else:
            print(f"Error al conectar a la API. Código de estado: {response.status_code}")
    
    except requests.RequestException as e:
        print(f"Error al intentar conectar con la API: {e}")
    
    finally:
        return resultado


registro = {
    'date': "N/A",
    'hour': "N/A",
    'system': "N/A",
    'MAC': "N/A",
    'bssid': "N/A",
    'ip': "N/A",
    'url': "N/A",
    'status': -1,
    'load': 9999.99,
    'transferred': 0,
    'delay': 9999.99,
    'download': 9999.99,
    'comment': ""
}