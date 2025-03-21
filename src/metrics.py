from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from ping3 import ping
import requests
import socket
import psutil
import os

def download_binary_file(url, filename="10MB.bin"):
    try:
        # Registra el tiempo de inicio
        start_time = time.time()

        # Descarga el archivo
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Lanza una excepción si hay un error HTTP

        # Escribe el archivo en modo binario
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # Solo escribe si hay contenido
                    file.write(chunk)

        # Registra el tiempo de finalización
        end_time = time.time()

        # Verifica si el archivo se descargó correctamente
        if os.path.exists(filename):
            download_time = end_time - start_time
            return filename, download_time
        else:
            print("La descarga falló: el archivo no se creó.")
            return None, None
    except requests.RequestException as e:
        print(f"Error durante la descarga: {e}")
        return None, None

def delete_file(filename):
    try:
        if os.path.exists(filename):
            os.remove(filename)
            #print(f"Archivo eliminado: {filename}")
        else:
            print(f"El archivo {filename} no existe.")
    except Exception as e:
        print(f"Error al eliminar el archivo: {e}")

def download_time(url = "https://drive.google.com/file/d/1Qumkqt-oCvSSH7b1OuT3IUT_7nYVwbWR/view?usp=drive_link", filename="filename"):
    downloaded_file, download_time =  download_binary_file(url)
    if downloaded_file:
        delete_file(downloaded_file)
    
    return ((10e6*8)/download_time)/1e6



def average_ping(host, count=5, timeout=1):
    """
    docstring
    """
    times = []
    for _ in range(count):
        try:
            response_time = ping(host, timeout=timeout, unit="ms")  # Tiempo en milisegundos
            if response_time is not None:
                times.append(response_time)
        except Exception as e:
            print(f"Error en el ping: {e}")

    if times:
        return sum(times) / len(times)  # Promedio de los tiempos exitosos
    else:
        return None  # Si todos los pings fallaron


def is_connected(timeout=5):
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        return True
    except OSError:
        return False  

def is_connected_to_network():
    """Verifica si el dispositivo está conectado a una red local (WiFi o cable)."""
    interfaces = psutil.net_if_addrs()
    
    for interfaz, direcciones in interfaces.items():
        for direccion in direcciones:
            if direccion.family == 2 and not direccion.address.startswith("127."):  
                # Family 2 = IPv4, descartamos localhost (127.x.x.x)
                print(f"Conectado a la red ({interfaz}: {direccion.address})")
                return True
    
    print("No hay conexión a la red")
    return False    

_browser_instance = None

def start_browser():
    """Inicializa o reutiliza una instancia del navegador."""
    global _browser_instance
    if _browser_instance is None:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Modo headless (sin interfaz gráfica)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--incognito')
        options.add_argument('--disable-cache')
        options.add_argument('--disk-cache-size=0')
        _browser_instance = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return _browser_instance

def close_browser():
    """Cierra la instancia del navegador si está abierta."""
    global _browser_instance
    if _browser_instance is not None:
        _browser_instance.quit()
        _browser_instance = None

def get_transferred_and_time(url):
    """Obtiene los datos transferidos y el tiempo de carga de una URL."""
    driver = start_browser()  # Reutiliza la instancia del navegador
    driver.get(url)
    time.sleep(2)  # Da tiempo para que se carguen los recursos

    # Obtener datos transferidos
    transferred_kb = driver.execute_script("""
        let totalTransferred = 0;
        performance.getEntriesByType('resource').forEach(resource => {
            if (resource.transferSize) {
                totalTransferred += resource.transferSize;
            } else if (resource.encodedBodySize) {
                totalTransferred += resource.encodedBodySize;
            }
        });
        return totalTransferred / 1024;  // Convertir a kB
    """)

    # Obtener tiempo de carga
    load_time = driver.execute_script("""
        const [entry] = performance.getEntriesByType('navigation');
        return entry.loadEventEnd - entry.startTime;  // Tiempo de carga en ms
    """)

    return transferred_kb, load_time


def get_status_code(url):

    r = requests.get(url)

    return r.status_code

if __name__ == "__main__":
    print(download_time()) 
    is_connected_to_network()

    if is_connected():
        url = 'https://es.wikipedia.org/wiki/Antigua_Atenas#Primeros_tiempos'
        url2 = 'es.wikipedia.org'

        status = get_status_code(url)
        transferred, load_time = get_transferred_and_time(url)
        delay = average_ping(url2)

        print(f"Status code: {status}\nTransferred: {transferred:.2f} kB\nLoad time: {load_time:.2f} ms\ndelay: {delay}")
    else:
        print("No hay conexión a internet")
