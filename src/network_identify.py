import subprocess
import socket
import platform

def detectar_sistema_operativo():
    
    sistema = platform.system()
    if sistema == "Linux":
        return "Linux"
    elif sistema == "Windows":
        return "Windows"
    else:
        return None


def obtener_ip_activa():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # Conecta con DNS de Google
        ip = s.getsockname()[0]     # Obtiene la IP local de la interfaz que responde
    except Exception:
        ip = "No active interfaces"
    finally:
        s.close()
    
    return ip


def obtener_bssid():
    sistema = detectar_sistema_operativo()
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




def obtener_mac(interfaz=None):
    sistema = detectar_sistema_operativo()
    
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
            resultado = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"],
                stderr=subprocess.DEVNULL,
                encoding='latin-1'
            )
            mac = None
            for linea in resultado.split("\n"):
                if "Direcci¢n" in linea:
                    mac = ":".join(linea.split(":")[1:]).strip()
            if mac:
                return mac
            else:
                return 'None'
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el comando: {e}")
            return 'None'
  
 

# Obtener el BSSID y la interfaz
interfaz, bssid = obtener_bssid()
mac_address = obtener_mac(interfaz)
ip = obtener_ip_activa()
sistema = detectar_sistema_operativo()

if __name__ == "__main__":
    print(ip)
    print(bssid)
    print(mac_address)
    print(sistema)


