import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import mplcursors  # Importar mplcursors para interactividad

# Función para leer datos del archivo JSON
def leer_datos_json(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        datos = json.load(archivo)
    return datos

# Configurar la gráfica
def graficar_tiempo_de_carga(nombre_archivo):
    datos = leer_datos_json(nombre_archivo)

    # Listas para almacenar los datos
    tiempos = []
    carga_vals = []

    # Extraer los datos de tiempo de carga y tiempo
    for entrada in datos:
        hora = datetime.strptime(entrada['hora'], "%H:%M:%S")
        carga = round(entrada['load'], 3)  # Redondear a 3 decimales

        tiempos.append(hora)
        carga_vals.append(carga)

    # Crear una figura
    plt.figure(figsize=(12, 6))

    # Convertir tiempos a números para graficar
    tiempos_numericos = mdates.date2num(tiempos)

    # Graficar la línea de tiempo de carga
    plt.plot(tiempos_numericos, carga_vals, color='slateblue', linewidth=1, label='Load time (ms)')

    # Rellenar el área bajo la curva
    plt.fill_between(tiempos_numericos, carga_vals, color='cyan', alpha=0.3)

    # Graficar puntos en cada dato
    scatter_plot = plt.scatter(tiempos_numericos, carga_vals, color='mediumpurple', s=50, zorder=5)  # Puntos visibles

    plt.ylabel("Load Time (ms)")
    plt.title("Hora")
    plt.ylim(0, max(carga_vals) + 10)  # Ajustar el límite superior

    # Configurar formato de hora en el eje x
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))  # Formato de hora

    # Establecer límites del eje x
    plt.xlim(tiempos_numericos[0], tiempos_numericos[-1])  # Desde el primer tiempo al último

    # Asegurarse de que cada punto en Y tenga su respectivo tiempo en X
    plt.xticks(tiempos_numericos, rotation=45)  # Usar tiempos para las marcas del eje X

    # Ajustar el diseño
    plt.tight_layout()
    plt.grid()
    plt.legend()  # Mostrar leyenda

    # Añadir etiquetas interactivas a los puntos usando mplcursors
    mplcursors.cursor(scatter_plot, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{round(carga_vals[sel.index], 3)}"))

    plt.show()  # Mostrar la gráfica

# Nombre del archivo JSON
nombre_archivo = 'datos.json'
graficar_tiempo_de_carga(nombre_archivo)
