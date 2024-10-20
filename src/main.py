from metrics import get_transferred_and_time, is_connected, get_status_code, ping
from network_identify import obtener_bssid, obtener_mac, obtener_ip_activa, detectar_sistema_operativo
from datetime import datetime
import time
import csv

id = 0

if __name__ == "__main__":

    hora_limite = datetime.now().replace(hour=18, minute=20, second=0, microsecond=0)

    while datetime.now() < hora_limite:
        ## Identificación 
        interfaz, bssid = obtener_bssid()
        mac_address = obtener_mac(interfaz)
        ip = obtener_ip_activa()
        sistema = detectar_sistema_operativo()
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = hora_actual = datetime.now().strftime("%H:%M:%S")

        print(f"id:    {id}\
                \nfecha: {fecha}\
                \nhora:  {hora}\
                \nSO:    {sistema}\
                \nMAC:   {mac_address}\
                \nBSSID: {bssid}\
                \nIP:    {ip}\
                ")

        if is_connected():
            url= "https://es.wikipedia.org/wiki/Urano_(planeta)"
            transferred, load = get_transferred_and_time(url)
            status = get_status_code(url)
            delay = ping('8.8.8.8',unit='ms')
        else:
            print("No hay conexión a internet")


        print(f"url:    {url}\
            \ntransf: {transferred}\
            \nload:   {load}\
            \nstatus: {status}\
            \nping:   {delay}\
            ")
        
        with open('datos.csv', mode='a', newline='') as archivo:
            escritor = csv.writer(archivo)
            datos = [id, fecha, hora, sistema, mac_address, bssid, ip, url, status, load, transferred, delay]
            escritor.writerow(datos)
            time.sleep(20)

        id +=1
    print("*"*20)
    print("Fin de la medición")