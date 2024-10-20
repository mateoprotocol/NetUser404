from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Inicializar el navegador usando el WebDriver manager
options = webdriver.ChromeOptions()
# Elimina la línea de headless para ver el navegador
options.add_argument('--headless')  # Ejecutar en modo headless (sin interfaz gráfica)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-cache')
options.add_argument('--disk-cache-size=0')
options.add_argument('--incognito')

# Iniciar el navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Ir a la página deseada
url = 'https://es.wikipedia.org/wiki/Urano_(planeta)'
start_time = time.time()
driver.get(url)
time.sleep(10) 

load_time = driver.execute_script("""
    const [entry] = performance.getEntriesByType('navigation');
    return entry.loadEventEnd - entry.startTime;  // Tiempo de carga en ms
""")

# Obtener el total de datos transferidos
total_transferred = driver.execute_script("""
    let totalTransferred = 0;
    const resources = performance.getEntriesByType('resource');

    resources.forEach(resource => {
        if (resource.transferSize) {
            totalTransferred += resource.transferSize;
        } else if (resource.encodedBodySize) {
            totalTransferred += resource.encodedBodySize;
        }
    });

    return totalTransferred / 1024;  // Convertir a kB
""")
transferred_kb = total_transferred 

# Mostrar los resultados
print(f'Transferred: {transferred_kb:.2f} kB')
print(f'Load: {load_time} ms')

# Cerrar el navegador
driver.quit()
