import sqlite3 as sql
import os.path

pathProject = os.getcwd()   # directorio actual
pathDB = f"{pathProject}/Database.db"


def createDB():
    conn = sql.connect(pathDB)
    conn.commit()
    conn.close()

def createTable():
    conn = sql.connect(pathDB)
    cursor = conn.cursor() # objeto de la conexión
    cursor.execute(
        """CREATE TABLE Logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Network text,
            Date date,
            Time text,
            Status integer,
            Size real,
            Method text,
            Type text,
            Response real
        )"""
    )
    conn.commit() # realizar los cambios
    conn.close()


def insertRow(network, date, time, status, size, method, type, response):
    conn = sql.connect(pathDB)
    cursor = conn.cursor() # objeto de la conexión
    instruction = f"INSERT INTO Logs VALUES (NULL,'{network}','{date}','{time}','{status}','{size}','{method}','{type}','{response}')"
    cursor.execute(instruction)
    conn.commit() # realizar los cambios
    conn.close()

def readAllRows(): 
    conn = sql.connect(pathDB)
    cursor = conn.cursor() # objeto de la conexión
    instruction = f"SELECT * FROM Logs"
    cursor.execute(instruction)
    datos = cursor.fetchall() # se crea una lista de tuplas, cada tupla es un registro
    conn.commit() # realizar los cambios
    conn.close()
    print(datos)  


if __name__ == "__main__":
    #insertRow("192.168.1.0", "2024-09-16", "16:40", 200, 783.2, "GET", "html", 22.3)
    readAllRows()
    pass
    
    