import psutil

# MISION
# Interfaz  [ x ] 
# mac       [ x ]
# ip        [ x ]
# bssid

interfaces = psutil.net_if_addrs()
valid_interface = {'eth0', 'eth1', 'wlan0', 'wlan1', 'enp3s0', 'wlp1s0', 'wlp2s0'}
mac = ""
interface=""
for interfaz, direcciones in interfaces.items():
    if interfaz in valid_interface:
        for direccion in direcciones:
            if direccion.family == 2 and not direccion.address.startswith("127."):
                # Family 2 = IPv4, descartamos localhost (127.x.x.x)
                interface=interfaz
                print(f"Conectado a la red ({interfaz}: {direccion.address} - {direccion.netmask})")
            if direccion.family == 17:
                print(f"MAC:  {direccion.address}")


import platform, os

def is_mobile():
    system = platform.system()
    # En Android, platform.system() devuelve "Linux"
    if system == "Linux":
        # Verificar si hay directorios de Android
        if any(os.path.exists(p) for p in ["/system", "/data/data"]):
            return True
    return False



print(is_mobile())