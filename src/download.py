import os
import requests
import time

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
            print(f"Status code: 200 for: {filename}")
            print(f"Tiempo de descarga: {download_time:.2f} segundos")
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

# Ejemplo de uso
if __name__ == "__main__":
    # URL del archivo binario
    url = "https://drive.google.com/file/d/1Qumkqt-oCvSSH7b1OuT3IUT_7nYVwbWR/view?usp=drive_link"  # Cambia esto al enlace que desees probar

    # Descarga el archivo
    downloaded_file, download_time = download_binary_file(url)

    # Si se descargó correctamente, eliminar el archivo
    if downloaded_file:
        delete_file(downloaded_file)
