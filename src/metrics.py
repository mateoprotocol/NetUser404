import time
from ping3 import ping
import requests
import socket
import psutil
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import concurrent.futures
from validation import registro
import shutil
 
def descargar_recursos_paralelo(url, max_workers=20, timeout=10):
    # Iniciar sesión para mantener cookies
    sesion = requests.Session()
    nombre_dominio =  None
    
    # Headers para simular navegador con mejor precisión
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        # Tiempo de inicio
        inicio = time.time()
        
        # Solicitud inicial para obtener el HTML con timeout
        respuesta = sesion.get(url, headers=headers, timeout=timeout)
        
        # Parsear el HTML. Extraer los enlaces a recursos
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        
        # Directorio para guardar recursos
        nombre_dominio = urlparse(url).netloc
        os.makedirs(nombre_dominio, exist_ok=True)

        # Diccionario para almacenar recursos
        recursos = {
            'html': len(respuesta.text),
            'css': [],
            'js': [],
            'imagenes': [],
            'otros': []
        }

        # Función para descargar un recurso individual
        def descargar_recurso(enlace, tipo):
            try:
                # URL absoluta
                url_absoluta = urljoin(url, enlace)
                
                # Solo descargar recursos del mismo dominio para optimizar
                if urlparse(url).netloc != urlparse(url_absoluta).netloc and tipo not in ['css', 'js']:
                    return {
                        'url': url_absoluta,
                        'tamano': 0,
                        'archivo': None,
                        'tipo': tipo,
                        'externo': True
                    }
                
                # Solicitud del recurso con timeout
                recurso = sesion.get(url_absoluta, headers=headers, timeout=timeout)
                
                # Nombre de archivo
                nombre_archivo = os.path.join(nombre_dominio, 
                    f"{urlparse(url_absoluta).netloc}_{urlparse(url_absoluta).path.replace('/', '_')}")
                
                # Guardar recurso
                with open(nombre_archivo, 'wb') as archivo:
                    archivo.write(recurso.content)
                
                # Registrar información del recurso
                return {
                    'url': url_absoluta,
                    'tamano': len(recurso.content),
                    'archivo': nombre_archivo,
                    'tipo': tipo,
                    'externo': False
                }
            except Exception as e:
                print(f"Error descargando {enlace}: {e}")
                return None

        # Recopilar todos los recursos a descargar
        recursos_a_descargar = []
        
        # Buscar hojas de estilo (CSS) - Prioridad Alta
        recursos_a_descargar.extend([
            (link['href'], 'css') 
            for link in soup.find_all('link', rel='stylesheet') 
            if link.get('href')
        ])

        # Buscar scripts (JavaScript) - Prioridad Alta
        recursos_a_descargar.extend([
            (script['src'], 'js') 
            for script in soup.find_all('script', src=True)
        ])

        # Buscar imágenes - Prioridad Media
        recursos_a_descargar.extend([
            (img['src'], 'imagenes') 
            for img in soup.find_all('img', src=True)
        ])

        # Priorizar recursos críticos (CSS y JS primero)
        recursos_a_descargar.sort(key=lambda x: 0 if x[1] in ['css', 'js'] else 1)

        # Descargar recursos en paralelo con más workers
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Usar submit en lugar de map para mejor control
            futuros = []
            for enlace, tipo in recursos_a_descargar:
                futuro = executor.submit(descargar_recurso, enlace, tipo)
                futuros.append(futuro)
            
            # Procesar resultados a medida que se completan
            resultados = []
            for futuro in concurrent.futures.as_completed(futuros):
                resultado = futuro.result()
                if resultado:
                    resultados.append(resultado)

        # Organizar recursos por tipo
        for resultado in resultados:
            if resultado and 'tipo' in resultado:
                recursos[resultado['tipo']].append(resultado)

        # Tiempo de finalización
        fin = time.time()
        tiempo_final = fin-inicio
        # Información general
        #print("\nResumen de Recursos Descargados:")
        #print(f"URL: {url}")
        #print(f"Tiempo total: {fin - inicio:.2f} segundos")
        #print(f"Tamaño HTML: {recursos['html']} bytes")
        #print(f"CSS: {len(recursos['css'])} archivos")
        #print(f"JavaScript: {len(recursos['js'])} archivos")
        #print(f"Imágenes: {len(recursos['imagenes'])} archivos")
        
        tamano_total = recursos['html'] 

        for tipo in ['css', 'js', 'imagenes', 'otros']:
            for recurso in recursos[tipo]:
                tamano_total += recurso['tamano'] 

        return tiempo_final, tamano_total, respuesta.status_code

    except Exception as e:
        print(f"Error general: {e}")
        return None
    finally:
        if nombre_dominio and os.path.exists(nombre_dominio):
            shutil.rmtree(nombre_dominio)

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

def download_time( url="https://drive.google.com/file/d/1Qumkqt-oCvSSH7b1OuT3IUT_7nYVwbWR/view?usp=drive_link", filename="filename"):
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
        registro["comment"] += "[No hay conexion a internet]"
        return False  

def is_connected_to_network():
    """Verifica si el dispositivo está conectado a una red local (WiFi o cable)."""
    interfaces = psutil.net_if_addrs()

    for interfaz, direcciones in interfaces.items():
        if "wl" in interfaz or "en" in interfaz or "eth" in interfaz:
            for direccion in direcciones:
                if direccion.family == 2 and not direccion.address.startswith("127."):
                    # Family 2 = IPv4, descartamos localhost (127.x.x.x)
                    print(f"Conectado a la red ({interfaz}: {direccion.address})")
                    return True
    registro["comment"] += "[No hay conexion a la red]"
    print("No hay conexion a la red")
    return False    


def get_metrics(url):
    load_time = -1
    transferred = 0
    status = -1
    delay = -1

    resultado = descargar_recursos_paralelo(url)
    if resultado:
        load_time, transferred, status = resultado
    else:
        load_time = -1
        transferred = 0
        status = -1

    download = download_time()
    if download is None:
        download = -1

    delay = average_ping("8.8.8.8")
    if delay is None:
        delay = -1

    return load_time, transferred, status, download, delay


if __name__ == "__main__":
    url_prueba = "https://es.wikipedia.org/wiki/Antigua_Atenas#Primeros_tiempos"

    print(get_metrics(url_prueba))
