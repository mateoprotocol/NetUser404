from metrics import  is_connected, is_connected_to_network, get_metrics 
from identify import identify
from datetime import datetime
import time
import os
from dotenv import load_dotenv
from validation import *

load_dotenv(override=True) 

# Constantes
server_url = os.getenv("SERVER_URL")
server_port = os.getenv("SERVER_PORT")
URLS_FILE = 'urls.txt'
PING_TARGET = os.getenv("PING_TARGET")
DEVICE_NAME = os.getenv("NAME", "SinNombre")
NETWORK_NAME = os.getenv("NETWORK_NAME", "RedDesconocida")

URL_API = f'http://{server_url}:{server_port}/metric'
LOCAL_FILE= "datos.json"


if __name__ == "__main__":

    urls = get_urls(URLS_FILE)
    i=0

    while True:
        registro["date"] = datetime.now().strftime("%Y-%m-%d")
        registro["hour"] = datetime.now().strftime("%H:%M:%S")
        
        if i >= len(urls):
            i=0

        registro["url"] = urls[i]
        if is_connected_to_network():
            registro["system"], mac, registro["ip"], registro["bssid"] = identify()
            if mac == "N/A":
                registro["MAC"] = DEVICE_NAME
            else:
                registro["MAC"] = f"{DEVICE_NAME}({mac})"
            if registro["bssid"] == "N/A":
                registro["bssid"] = NETWORK_NAMEm
        else:
            registro["MAC"] = DEVICE_NAME
            registro["bssid"] = NETWORK_NAME
            save_local_data(registro,LOCAL_FILE)
            reset_registro()
            time.sleep(20)
            continue 

        if is_connected():
            registro["load"], registro["transferred"], registro["status"], registro["download"], registro["delay"]= get_metrics(urls[i])

        if API_available(f"http://{server_url}:{server_port}/check-mongodb"):
            print(send_local_data(f"{URL_API}s", LOCAL_FILE))
            print(send_to_api(registro, URL_API))
        else:
            save_local_data(registro, LOCAL_FILE)
        
        i+=1
        reset_registro()
        time.sleep(20)