from metrics import  is_connected, is_connected_to_network, get_metrics 
from identify import identify
from datetime import datetime
import time
import os
from dotenv import load_dotenv
from validation import *

load_dotenv()  # Carga las variables del archivo .env

# Constantes
server_url = os.getenv("SERVER_URL")
server_port = os.getenv("SERVER_PORT")
URLS_FILE = os.getenv("FILE_URLS")
PING_TARGET = os.getenv("PING_TARGET")

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
            registro["system"], registro["MAC"], registro["ip"], registro["bssid"] = identify()
        else:
            save_local_data(registro,LOCAL_FILE)
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
