from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from ping3 import ping
import requests
import socket

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

    if is_connected():
        url = 'https://es.wikipedia.org/wiki/Antigua_Atenas#Primeros_tiempos'
        url2 = 'es.wikipedia.org'

        status = get_status_code(url)
        transferred, load_time = get_transferred_and_time(url)
        delay = average_ping(url2)

        print(f"Status code: {status}\nTransferred: {transferred:.2f} kB\nLoad time: {load_time:.2f} ms\ndelay: {delay}")
    else:
        print("No hay conexión a internet")