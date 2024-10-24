from metrics import get_transferred_and_time, is_connected, get_status_code, ping
from network_identify import obtener_bssid, obtener_mac, obtener_ip_activa, detectar_sistema_operativo
from datetime import datetime
import time
import csv

id = 0

if __name__ == "__main__":


    #Obtención de urls
    file_path = 'src/urls.txt'

    with open(file_path, 'r') as file:
        urls = file.readlines()

   
    urls = [url.strip() for url in urls]  # Eliminar los caracteres de nueva línea
    i = 0 # variable de iteración para cada url

    # Programación de registros
    hora_ = int(input("hora: "))
    minuto_ = int(input("minutos: "))
    hora_limite = datetime.now().replace(hour=hora_, minute=minuto_, second=0, microsecond=0)

    while datetime.now() < hora_limite:

        if i >= len(urls): # reinicio de la lista de urls
            i = 0

        print("*"*20)
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
            url= urls[i]
            i+=1
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
            
        time.sleep(5)
        id +=1
    print("*"*20)
    print("Fin de la medición")