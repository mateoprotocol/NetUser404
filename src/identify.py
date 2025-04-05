import subprocess
import platform
import re
from validation import registro

def get_os():
    try:
        return platform.system()
    except:
        print("Error obteniendo sistema operativo")
        return "N/A"

def get_net_interface(os="Linux"):
    if os=="Linux":
        try:
            result = subprocess.run(["ip", "r"], capture_output=True, text=True)
            interface = re.findall(r"dev (\S+)", result.stdout)

            valid_interface = {'eth0', 'eth1', 'wlan0', 'wlan1', 'enp3s0','wlp1s0','wlp2s0'}

            if interface[0] in valid_interface:
                return interface[0]
            else:
                registro["comment"] += "[Interfaz de red invalida]"
                return "No hay interfaz valida"
        except:
            print("Error obteniendo interfaces")
            return "N/A"

def get_mac(interface, os="Linux"):
    if os=="Linux":
        try:
            result = subprocess.run(["ip","link","show",interface], capture_output=True, text=True)
            mac = re.findall(r"link/ether (\S+)", result.stdout)
            return mac[0]
        except:
            print("Error obteniendo mac")
            return "N/A"
    
def get_local_ip(os="Linux"):
    if os=="Linux":
        try:
            result = subprocess.run(["ip","r"], capture_output=True, text=True)
            ip = re.findall(r"src (\S+)", result.stdout)
            return ip[0]
        except:
            print("Error al obtener la ip")
            return "N/A"
    
def get_bssid(interface, os="Linux"):
    if os=="Linux":
        try:
            result = subprocess.run(["iw", "dev", interface, "link"], capture_output=True, text=True)
            bssid = re.findall(r"Connected to (\S+)", result.stdout)
            ssid = re.findall(r"SSID:\s(.+)", result.stdout)
            
            if ssid and bssid:  # Verifica que ambos valores existen
                ssid = ssid[0].encode().decode('unicode_escape').strip()  # Decodifica caracteres escapados
                return f"{ssid} ({bssid[0]})"
            
            return "N/A"

        
        except:
            print("Error al obtener bssid y ssid")
            return "N/A"


def identify():
    os= "N/A"
    interface= "N/A"
    mac = "N/A"
    ip= "N/A"
    bssid= "N/A"


    os= get_os()
    interface= get_net_interface()
    mac= get_mac(interface)
    ip= get_local_ip()
    bssid= get_bssid(interface)

    return os, mac, ip, bssid

if __name__ == "__main__":

    print(identify())