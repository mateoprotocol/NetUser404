import subprocess
import platform
import re

def get_os():
    try:
        return platform.system()
    except:
        print("Error obteniendo sistema operativo")
        return "Error obteniendo sistema operativo"

def get_net_interface(os="Linux"):
    if os=="Linux":
        try:
            result = subprocess.run(["ip", "r"], capture_output=True, text=True)
            interface = re.findall(r"dev (\S+)", result.stdout)
            return interface[0]
        except:
            print("Error obteniendo interfaces")
            return "Error obteniendo interfaces"

def get_mac(interface, os="Linux"):
    if os=="Linux":
        try:
            result = subprocess.run(["ip","link","show",interface], capture_output=True, text=True)
            mac = re.findall(r"link/ether (\S+)", result.stdout)
            return mac[0]
        except:
            return "Error obteniendo mac"
    
def get_local_ip(os="Linux"):
    if os=="Linux":
        try:
            result = subprocess.run(["ip","r"], capture_output=True, text=True)
            ip = re.findall(r"src (\S+)", result.stdout)
            return ip[0]
        except:
            print("Error al obtener la ip")
            return "Error al obtener la ip"
    
def get_bssid(interface, os="Linux"):
    if os=="Linux":
        try:
            result = subprocess.run(["iw","dev",interface,"link"], capture_output=True, text=True)
            bssid = re.findall(r"Connected to (\S+)", result.stdout)
            ssid =  re.findall(r"SSID:\s(.+)", result.stdout)

            return f"{ssid[0]} ({bssid[0]})"
        except:
            print("Error al obtener bssid y ssid")
            return "Error al obtener bssid y ssid"


if __name__ == "__main__":
   print(get_os())
   interface= get_net_interface()
   print(interface)
   print(get_mac(interface))
   print(get_local_ip())
   print(get_bssid(interface))
