import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import mplcursors  # Importar mplcursors para interactividad
from matplotlib.gridspec import GridSpec

# Función para leer datos del archivo JSON
def leer_datos_json(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        datos = json.load(archivo)
    return datos

# Configurar la gráfica
def graficar_tiempos(nombre_archivo):
    datos = leer_datos_json(nombre_archivo)

    # Listas para almacenar los datos
    tiempos = []
    carga_vals = []
    delay_vals = []
    status_codes = []  # Lista para los códigos de estado

    # Extraer los datos de tiempo de carga, delay, tiempo y status code
    for entrada in datos:
        hora = datetime.strptime(entrada['hora'], "%H:%M:%S")
        carga = round(entrada['load'], 3)  # Redondear a 3 decimales
        delay = round(entrada['delay'], 3)  # Redondear el delay a 3 decimales
        status_codes.append(entrada['status'])  # Agregar código de estado

        tiempos.append(hora)
        carga_vals.append(carga)
        delay_vals.append(delay)

    # Contar los códigos de estado
    status_count = {
        '200': status_codes.count(200),
        '300': status_codes.count(300),
        '400': status_codes.count(400)
    }

    # Crear la figura y el GridSpec para la disposición de subgráficas
    fig = plt.figure(figsize=(20, 8))  # Aumentar el ancho de la figura
    gs = GridSpec(2, 2, figure=fig, width_ratios=[2, 1], height_ratios=[1, 1])  # Ajustar las proporciones

    # Panel de control en la parte superior derecha
    ax_dashboard = fig.add_subplot(gs[0, 1])
    ax_dashboard.axis("off")

    # Crear una tabla para mostrar los códigos de estado
    tabla_data = [['Código de Estado', 'Cantidad'],
                  ['200', status_count['200']],
                  ['300', status_count['300']],
                  ['400', status_count['400']]]

    # Establecer colores para cada fila de la tabla
    colores_tabla = ['green', 'orange', 'red']

    # Crear la tabla y aplicar colores
    tabla = ax_dashboard.table(cellText=tabla_data, loc='center', cellLoc='center', colLabels=None)
    for i, color in enumerate(colores_tabla):
        tabla[(i+1, 0)].set_facecolor(color)  # Aplicar color a las celdas de códigos de estado
        tabla[(i+1, 1)].set_facecolor(color)  # Aplicar color a las celdas de cantidades
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(12)
    tabla.scale(0.7, 1.5)  # Ajustar el tamaño de la tabla

    # Título de la tabla más cerca
    ax_dashboard.text(0.5, 1.1, "Códigos de Estado", ha="center", fontsize=14, fontweight='bold')

    ax_dashboard.set_title("Dashboard de Estado", fontsize=14)

    # Graficar el tiempo de carga en la primera subgráfica (izquierda superior)
    ax1 = fig.add_subplot(gs[0, 0])  # Primera fila, primera columna
    ax1.plot(tiempos, carga_vals, color='slateblue', linewidth=1, label='Tiempo de Carga (ms)')
    ax1.fill_between(tiempos, carga_vals, color='cyan', alpha=0.3)
    scatter_plot_load = ax1.scatter(tiempos, carga_vals, color='mediumpurple', s=50, zorder=5)

    ax1.set_ylabel("Tiempo de Carga (ms)")
    ax1.set_title("Tiempo de Carga a lo largo del Tiempo")
    ax1.set_ylim(0, max(carga_vals) + 10)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True)

    # Graficar el delay en la segunda subgráfica (izquierda inferior)
    ax2 = fig.add_subplot(gs[1, 0])  # Segunda fila, primera columna
    for i in range(len(tiempos)):
        ax2.plot([tiempos[i], tiempos[i]], [0, delay_vals[i]], color='orange', linewidth=1, linestyle='--')
    scatter_plot_delay = ax2.scatter(tiempos, delay_vals, color='tomato', s=50, zorder=5)

    ax2.set_ylabel("Ping (ms)")
    ax2.set_title("Delay (Ping) a lo largo del Tiempo")
    ax2.set_ylim(0, max(delay_vals) + 10)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True)

    # Asegurarse de que cada punto en Y tenga su respectivo tiempo en X
    ax1.set_xticks(tiempos)
    ax2.set_xticks(tiempos)

    # Crear gráfico de pastel para los códigos de estado en la esquina inferior derecha
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.pie(
        status_count.values(),
        labels=status_count.keys(),
        colors=['green', 'orange', 'red'],
        autopct='%1.1f%%',
        startangle=90,
        explode=(0.1, 0.1, 0.1),
        wedgeprops=dict(width=0.3, edgecolor='w')  # Ajuste del ancho de los sectores
    )
    ax3.set_title('Distribución de Códigos de Estado')
    ax3.axis('equal')

    # Ajustar el diseño
    plt.tight_layout()

    # Añadir etiquetas interactivas a los puntos de carga
    mplcursors.cursor(scatter_plot_load, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"Load: {round(carga_vals[sel.index], 3)} ms"))
    
    # Añadir etiquetas interactivas a los puntos de delay
    mplcursors.cursor(scatter_plot_delay, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"Ping: {round(delay_vals[sel.index], 3)} ms"))

    # Establecer el primer valor del eje X como el primer tiempo leído
    ax1.set_xlim(tiempos[0], tiempos[-1])
    ax2.set_xlim(tiempos[0], tiempos[-1])

    plt.show()  # Mostrar la gráfica

# Nombre del archivo JSON
nombre_archivo = 'datos.json'
graficar_tiempos(nombre_archivo)
