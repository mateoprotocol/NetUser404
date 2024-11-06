import json
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017")  # Cambia la URL según tu configuración
db = client["Network_sensor"]
collection = db["Metrics"]


with open("/home/mateo/Desktop/Network Sensor/Network Monitoring Code/Network-Sensor/datos.json", "r") as file:
    datos_json = json.load(file)


if isinstance(datos_json, list):  # Si los datos JSON son una lista de documentos
    collection.insert_many(datos_json)
else:  # Si es un único documento JSON
    collection.insert_one(datos_json)


