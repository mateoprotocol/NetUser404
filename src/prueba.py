import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import concurrent.futures
import time
import os
import gzip
import brotli
from io import BytesIO

def descargar_recursos_paralelo(url, max_workers=20, timeout=10):
    # Iniciar sesión para mantener cookies
    sesion = requests.Session()
    
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
        
        # Parsear el HTML
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
        
        # Información general
        print("\nResumen de Recursos Descargados:")
        print(f"URL: {url}")
        print(f"Tiempo total: {fin - inicio:.2f} segundos")
        print(f"Tamaño HTML: {recursos['html']} bytes")
        print(f"CSS: {len(recursos['css'])} archivos")
        print(f"JavaScript: {len(recursos['js'])} archivos")
        print(f"Imágenes: {len(recursos['imagenes'])} archivos")
        
        return recursos

    except Exception as e:
        print(f"Error general: {e}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    url_prueba = "https://www.unillanos.edu.co/"
    descargar_recursos_paralelo(url_prueba)