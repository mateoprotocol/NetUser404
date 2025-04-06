import subprocess
import platform
import re
from validation import registro
import psutil
import os

def get_os():
    try:
        if platform.system() == "Linux":
            if any(os.path.exists(p) for p in ["/system", "/data/data"]):
                return "Android" 
        return platform.system()
    except:
        print("Error obteniendo sistema operativo")
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

def get_interface_ip_mac():
    mac="N/A"
    interfaces = psutil.net_if_addrs()
    valid_interface = {'eth0', 'eth1', 'wlan0', 'wlan1', 'enp3s0', 'wlp1s0', 'wlp2s0'}
    for interfaz, direcciones in interfaces.items():
        if interfaz in valid_interface:
            for direccion in direcciones:
                if direccion.family == 2 and not direccion.address.startswith("127."):
                    # Family 2 = IPv4, descartamos localhost (127.x.x.x)
                    interface = interfaz
                    ip = direccion.address
                    print(f"Conectado a la red ({interfaz}: {direccion.address} - {direccion.netmask})")
                if direccion.family == 17:
                    mac=direccion.address
                    print(f"MAC:  {direccion.address}")
    
    return interface, ip, mac 

def identify():
    os= "N/A"
    interface= "N/A"
    mac = "N/A"
    ip= "N/A"
    bssid= "N/A"


    os= get_os()
    interface, ip, mac = get_interface_ip_mac()
    bssid= get_bssid(interface)

    return os, mac, ip, bssid

if __name__ == "__main__":

    print(identify())