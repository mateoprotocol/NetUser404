import requests
from datetime import datetime

def get_metrics(*args):
    status_codes= []
    response_times= []
    sizes= []
    types = []

    for i in args:
        r= requests.get(i)
        status_codes.append(r.status_code)
        response_times.append(r.elapsed.total_seconds()*1000) # tiempo de respuesta en milisegundos
        sizes.append(len(r.content))
        types.append(r.headers['content-type'].split(";")[0]) # tipo de contenido

        # modificando y usando el formato de la fecha
        date= r.headers['date'] # resultado en string
        newDate= datetime.strptime(date,"%a, %d %b %Y %H:%M:%S %Z") # cambiar de string a datetime para poder manipular la fecha
        newDate= newDate.now() # cambiar la zona horaria a la de mi región
        onlydate= newDate.date()
        minute= newDate.minute
        hour= newDate.hour

    return status_codes, response_times, str(onlydate), f"{hour}:{minute}", sizes, types




if __name__ == "__main__":

    url= "https://calculos-energeticos.netlify.app/_astro/hoisted.D_3o3WCS.js"
    metrics = get_metrics(url)
    print(metrics)