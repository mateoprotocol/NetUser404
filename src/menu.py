from questionary import select
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
import time
from metrics import is_connected_to_network
from validation import API_available
from dotenv import dotenv_values, set_key

console = Console()

def mostrar_titulo():
    # Diseño con rich
    titulo = Text("  MENÚ PRINCIPAL  ", style="bold white on blue")
    panel = Panel(titulo, expand=False, border_style="yellow")
    console.print(panel)

def nombre():

    nombre = input("¿Como quieres que recordemos este dispositivo?\n>>>")
    
    set_key(".env","NAME",nombre) 

    console.print(f"Dispositivo guardado como: [cyan]{nombre}[/]")

def add_network_name():
    nombre_red = input("Ingrese un nombre para identificar su red en caso de no detectar SSID o estar conectado por cable\n>>> ")
    console.print(f"Se ha guardado la red como: {nombre_red}")
    set_key(".env", "NETWORK_NAME", nombre_red)


def check_api_menu():
    while True:
        ip = input("Ingrese la dirección ip de la API\n>>>")
        console.print(f"Dirección Ip guardada como: {ip}")

        puerto = input("Ingrese el puerto relacionado con la API\n>>>")
        console.print(f"Puerto guardado como: {puerto}")

        if API_available(f"http://{ip}:{puerto}/check-mongodb"):
            set_key(".env","SERVER_URL",ip)
            set_key(".env","SERVER_PORT", puerto)
            break
        else:
            console.print("Ingrese la dirección ip y el puerto adecuado para la api")


def delete_all_urls():
    pass
def add_url(pagina):
    pass
def print_urls():
    pass

def add_url_menu():
    while True:
        print_urls()
        opcion = select(
            "¿Desea ingresar otra página a monitorear?",
            choices=[
                {"name": "Sí, ingresar otra página",  "value": "si"},
                {"name": "No, dejar las que ya están", "value": "no"},
                {"name": "Eliminar las que ya están e ingresar nuevamente", "value": "eliminar"}],
                use_arrow_keys=True,
                qmark="?"
        ).ask()
        if opcion == "si":
            pagina = input("Ingresar página:\n>>>")
            add_url(pagina)
        if opcion == "no":
            console.print("Estas son las páginas a monitorear")
            break
        if opcion == "eliminar":
            delete_all_urls()
            pagina = input("Ingresar página:\n>>>")
            add_url(pagina)

def interface_available():
    return is_connected_to_network()

def check_interfaz_menu():
    while True:

        opcion = select(
        """No hemos detectado ninguna interfaz de red. Por favor, active el wifi o conecte el cable de internet\n
        Cuando realice eso, dar a la opción recargar""",
        choices=[
            {"name": "Recargar",  "value": "re"}],
            use_arrow_keys=True,
            qmark="?"
        ).ask()
        
        if opcion == "re":
            if interface_available():
                break


def add_ping():
    ip = input("Ingrese la dirección ip de referencia a la cual quiere medir la latencia\n>>>")
    console.print(f"Se ha seleccionado la ip: {ip}")

    set_key(".env","PING_TARGET", ip)

if __name__ == "__main__":
    nombre()

    if not interface_available():
        check_interfaz_menu()
    
    check_api_menu()

    add_url_menu()

    add_ping()

    add_network_name()
    

