import subprocess
import platform
import re

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
            return interface[0]
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
            result = subprocess.run(["iw","dev",interface,"link"], capture_output=True, text=True)
            bssid = re.findall(r"Connected to (\S+)", result.stdout)
            ssid =  re.findall(r"SSID:\s(.+)", result.stdout)

            return f"{ssid[0]} ({bssid[0]})"
        except:
            print("Error al obtener bssid y ssid")
            return "N/A"


if __name__ == "__main__":
   print(get_os())
   interface= get_net_interface()
   print(interface)
   print(get_mac(interface))
   print(get_local_ip())
   print(get_bssid(interface))
