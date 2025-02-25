
import requests
import json
import os

def enviar_datos(api_url="http://192.168.192.192:8000/metrics", file_path="datos.json"):
    """
    Envía los datos almacenados en un archivo JSON a la API y elimina el archivo tras el envío exitoso.

    Parámetros:
    - api_url: URL de la API que recibe los datos.
    - file_path: Ruta del archivo JSON con los datos.

    Retorna:
    - Un mensaje indicando el resultado del proceso.
    """
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
                return "✅ Datos enviados y archivo eliminado con éxito."
            else:
                return f"❌ Error al enviar datos: {response.status_code} - {response.text}"

        except Exception as e:
            return f"⚠️ Ocurrió un error: {e}"
    else:
        return "📂 No hay archivo 'datos.json' para enviar."

# Ejemplo de uso
resultado = enviar_datos()
print(resultado)
