# Introducción

El módulo de recolección de datos de NetUser404 permite monitorear la calidad de la conectividad a internet desde la perspectiva del usuario final. Esta herramienta automatizada se ejecuta en segundo plano en el equipo del usuario o un equipo dedicado como una rasberry pi, recolectando métricas clave como tiempo de carga de páginas, latencia, velocidad de descarga, tamaño transferido, entre otras. El repositorio general de este proyecto se encuentra en [NetUser404-docs](https://github.com/franyober/netUser404-docs/).

# Requisitos

* Sistema operativo Linux
* Que ya esté configurado la API y base de datos. Ir a [NetUser404-api](https://github.com/franyober/netUser404-api/) en caso de que no lo este.


# Instalación

En una terminal ejecutar:

```
wget https://raw.githubusercontent.com/mateoprotocol/NetUser404/refs/heads/main/install
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
El instalador hará lo siguiente:
* Descargará todas las dependencias necesarias: Python3, git, iw.
* Descargará este repositorio en la ruta /opt/Netuser404 (código fuente del proyecto).
* Creará un entorno virtual y descargará todas las dependencias del proyecto mediante pip (requests, psutil, entre otras).
* Establecerá un comando global en /usr/local/bin/netuser para permitir el acceso al programa desde la terminal.

## Desinstalación

Para la desinstalación se puede hacer manualmente eliminando el directorio /usr/local/bin/netuser y el directorio /opt/Netuser404. O si desea descargar el siguiente script que hace este proceso automaticamente:

```
wget https://raw.githubusercontent.com/mateoprotocol/NetUser404/refs/heads/main/uninstall
```

Los pasos para ejecutar el script de desinstalación son los mismos que se usó para el de instalación. 


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


