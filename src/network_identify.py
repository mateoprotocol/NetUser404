import subprocess
import socket


def obtener_bssid():
    try:
        # Elimina OUTPUT de las demás interfaces
        resultado = subprocess.check_output(["iwconfig"], stderr=subprocess.DEVNULL, encoding='utf-8')

        interfaz_activa = None
        bssid = None

        # Analiza la salida de iwconfig línea por línea
        for linea in resultado.split("\n"):
            # Detecta la interfaz inalámbrica
            if "IEEE 802.11" in linea:
                # Extrae el nombre de la interfaz (antes del primer espacio)
                interfaz_activa = linea.split()[0]
            # Busca la línea que contiene el BSSID (Access Point)
            if "Access Point" in linea and interfaz_activa:
                bssid = linea.split("Access Point: ")[1].strip()
                break 

        if interfaz_activa and bssid:
            return interfaz_activa, bssid
        else:
            return None, None

    except subprocess.CalledProcessError:
        return None, None


def obtener_ip_activa():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # Conecta con DNS de Google
        ip = s.getsockname()[0]     # Obtiene la IP local de la interfaz que responde
    except Exception as e:
        ip = "No active interfaces"
    finally:
        s.close()
    
    return ip


def obtener_mac(interfaz):
    # Ubicación de la dirección MAC en el sistema de archivos de Linux
    ruta_mac = f"/sys/class/net/{interfaz}/address"
    try:
        with open(ruta_mac) as f:
            mac = f.read().strip()
        return mac
    except FileNotFoundError:
        return None

 
# Obtener el BSSID y la interfaz
interfaz, bssid = obtener_bssid()
mac_address = obtener_mac(interfaz)

if __name__ == "__main__":
    print(obtener_ip_activa())
    print(bssid)
    print(mac_address)
    print("new branch")

