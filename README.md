# Introducción

El módulo de recolección de datos de NetUser404 permite monitorear la calidad de la conectividad a internet desde la perspectiva del usuario final. Esta herramienta automatizada se ejecuta en segundo plano en el equipo del usuario o un equipo dedicado como una rasberry pi, recolectando métricas clave como tiempo de carga de páginas, latencia, velocidad de descarga, tamaño transferido, entre otras.

# Requisitos

* Sistema operativo Linux
* Que ya esté configurado la API y base de datos [Netuser-api](https://github.com/franyober/netUser404-api/)


# Instalación

En una terminal ejecutar:

```
wget https://raw.githubusercontent.com/mateoprotocol/NetUser404/refs/heads/main/instal|l
```

Se descargará el instalador `install`.

Ahora es necesario dar permisos de ejecución al instalador:

```
sudo chmod +x install
```

Finalmente ejecutar el instalador:

```
sudo ./install
```

# Uso del programa

Para acceder a todas las funcionalidades, se debe ejecutar:

```
netuser <comando>
```

Las opciones de `<comando>` puede ser:

* `start` : Inicia la recolección de métricas (en segundo plano).
* `stop` : Detiene la recolección.
* `status` : Verifica si la aplicación está activa.
* `logs` : Muestra los últimos registros recolectados.
* `configure` : Permite modificar parámetros como dirección de la API, nombre del dispositivo, nombre de la red, etc.
 
