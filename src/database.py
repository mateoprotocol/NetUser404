import json
from pymongo import MongoClient


client = MongoClient("mongodb://192.168.1.16:27017")  # Cambia la URL según tu configuración

client.admin.command("ping")
print("Connected successfully")

db = client["Network_sensor"]
collection = db["Metrics"]


with open("datos.json", "r") as file:
    datos_json = json.load(file)


if isinstance(datos_json, list):  # Si los datos JSON son una lista de documentos
    collection.insert_many(datos_json)
else:  # Si es un único documento JSON
    collection.insert_one(datos_json)


