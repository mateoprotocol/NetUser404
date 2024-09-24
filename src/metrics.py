import requests
from datetime import datetime
from selenium import webdriver
import time
import socket



def get_date_time():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S") 
    return current_date, current_time
    

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False   

def get_metrics(*args):

    status_codes= []
    response_times= []
    sizes= []
    types = []

    for i in args:
        r= requests.get(i)
        status_codes.append(r.status_code)
        response_times.append(r.elapsed.total_seconds()*1000) # tiempo de respuesta en milisegundos
        sizes.append(len(r.content))
        types.append(r.headers['content-type'].split(";")[0]) # tipo de contenido

        # modificando y usando el formato de la fecha
        date= r.headers['date'] # resultado en string
        newDate= datetime.strptime(date,"%a, %d %b %Y %H:%M:%S %Z") # cambiar de string a datetime para poder manipular la fecha
        newDate= newDate.now() # cambiar la zona horaria a la de mi región
        onlydate= newDate.date()
        minute= newDate.minute
        hour= newDate.hour

    return status_codes, response_times, str(onlydate), f"{hour}:{minute}", sizes, types

def get_time_page(url):

    if not is_connected():
        return "No hay conexión a internet"

    # Configurar el driver (Chrome en este caso)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Para ejecutar en modo sin interfaz gráfica
    driver = webdriver.Chrome(options=options)

    # Medir tiempos
    start_time = time.time()
    driver.get(url)
    navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
    response_start = driver.execute_script("return window.performance.timing.responseStart")
    dom_complete = driver.execute_script("return window.performance.timing.domComplete")

    # Calcular métricas
    ttfb = (response_start - navigation_start) / 1000  # Time to First Byte
    total_load_time = (dom_complete - navigation_start) / 1000  # Tiempo total de carga

    driver.quit()

    return {
        'TTFB': ttfb,
        'Total Load Time': total_load_time
    }


if __name__ == "__main__":

    url= "https://calculos-energeticos.netlify.app/fotovoltaico/"
    metrics = get_time_page(url)
    print(metrics)
    print(get_date_time())