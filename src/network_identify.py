import subprocess
import socket
import platform

def detect_OS():
    
    sistema = platform.system()
    if sistema == "Linux":
        return "Linux"
    elif sistema == "Windows":
        return "Windows"
    else:
        return 'None'


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # Conecta con DNS de Google
        ip = s.getsockname()[0]     # Obtiene la IP local de la interfaz que responde
    except Exception:
        ip = "No active interfaces"
    finally:
        s.close()
    
    return ip


def get_bssid():
    sistema = detect_OS()
    if sistema == "Linux":
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
        
    elif sistema == "Windows":
        try:
            # Ejecuta el comando netsh para obtener información de las interfaces Wi-Fi en Windows
            resultado = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"],
                stderr=subprocess.DEVNULL,
                encoding='latin-1'
            )

            interfaz_activa = None
            bssid = None

            # Analiza la salida línea por línea
            for linea in resultado.split("\n"):
                # Busca la línea que contiene el nombre de la interfaz
                if "Nombre" in linea or "Name" in linea:
                    interfaz_activa = linea.split(":")[1].strip()

                # Busca la línea que contiene el BSSID
                if "BSSID" in linea:
                    bssid = ":".join(linea.split(":")[1:]).strip()

            if interfaz_activa and bssid:
                return interfaz_activa, bssid  # Devuelve la interfaz y el BSSID
            else:
                return None, None

        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el comando: {e}")
            return None, None




def get_MAC(interfaz=None):
    sistema = detect_OS()
    
    if sistema == "Linux":
        # Ubicación de la dirección MAC en el sistema de archivos de Linux
        ruta_mac = f"/sys/class/net/{interfaz}/address"
        try:
            with open(ruta_mac) as f:
                mac = f.read().strip()
            return mac
        except FileNotFoundError:
            return 'None'
    elif sistema == "Windows":
        try:
            # Ejecuta el comando para obtener información de las interfaces de red
            resultado = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"],
                stderr=subprocess.DEVNULL,
                encoding='latin-1'
            )
            mac = None
            # Busca la línea que contiene la dirección MAC
            for linea in resultado.split("\n"):
                if any(keyword in linea for keyword in ["Direcci¢n", "Physical address"]):
                    mac = ":".join(linea.split(":")[1:]).strip()
                    break
            if mac:
                return mac
            else:
                return 'None'
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el comando: {e}")
            return 'None'

if __name__ == "__main__":
    # Obtener el BSSID y la interfaz
    interfaz, bssid = get_bssid()
    mac_address = get_MAC(interfaz)
    ip = get_local_ip()
    sistema = detect_OS()
    print(f"Sistema: {sistema}")
    print(f"Interfaz: {interfaz}")
    print(f"BSSID: {bssid}")
    print(f"MAC Address: {mac_address}")
    print(f"IP Address: {ip}")
    

