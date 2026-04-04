#Analisis de Latencia en Sistemas Concurrentes: APIs REST

import time
import requests
import threading

ciudades = [
    {"city": "CDMX","lat": 19.43 , "lon": -99.13} , # CDMX
    {"city": "NY","lat": 40.71 , "lon": -74.00} , # NY
    {"city": "Londres","lat": 51.50 , "lon": -0.12} , # Londres
    {"city": "Tokio","lat": 35.68 , "lon": 139.69} # Tokio
]

def obtener_clima(ciudad):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={ciudad['lat']}&longitude={ciudad['lon']}&current=temperature_2m"
    )
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        temp = data["current"]["temperature_2m"]
        unidad_temp = data["current_units"]["temperature_2m"]
        print(ciudad["city"], "Temperatura: ", temp, unidad_temp)


if __name__ == "__main__":
    #PROCESAMINETO SECUENCIAL
    start = time.time()
    for ciudad in ciudades:
        obtener_clima(ciudad)

    print(f"Tiempo total secuencial: {time.time()-start}")

    #PROCESAMIENTO PARALELO
    start1 = time.time()
    threads = []
    for ciudad in ciudades:
        threads.append(
            threading.Thread(target=obtener_clima, args=(ciudad,))
        )

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print(f"Tiempo total paralelo: {time.time()-start1}")

    








