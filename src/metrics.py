from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from ping3 import ping
import requests
import socket

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False  

def start_browser(url):
    # Inicializar el navegador con opciones
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Modo headless (sin interfaz gráfica)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--incognito')
    options.add_argument('--disable-cache')
    options.add_argument('--disk-cache-size=0')

    # Iniciar el navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Ir a la página deseada y esperar hasta que se complete la carga
    driver.get(url)
    driver.implicitly_wait(20)  # Espera hasta 10 segundos por la carga de recursos si es necesario
    time.sleep(2)

    return driver


def get_transferred_and_time(url):
    driver = start_browser(url)

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

    driver.quit()
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
        delay = ping(url2,unit='ms')

        print(f"Status code: {status}\nTransferred: {transferred:.2f} kB\nLoad time: {load_time:.2f} ms\ndelay: {delay}")
    else:
        print("No hay conexión a internet")