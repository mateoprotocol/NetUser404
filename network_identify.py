import socket
import requests

# local IP
def get_local_ip():
    hostname = socket.gethostname() 
    local_ip = socket.gethostbyname(hostname)   #Ojo, solo ipv4, aun se debe consultar para IPv4/IPv6
    return local_ip

# public IP
def get_public_ip():
    try:
        public_ip = requests.get('https://api.ipify.org').text
        return public_ip
    except requests.RequestException:
        return "No se pudo obtener la IP pública"



if __name__ == "__main__":
    print(get_local_ip())
    print(get_public_ip())

 