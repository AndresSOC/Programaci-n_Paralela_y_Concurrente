import time
import threading

acumulado = 10


def api(nombre:str, incremento: int) -> None:

    global acumulado
    print(f"hilo { nombre } empezando a descargar ... ")
    time.sleep(5)
    acumulado += incremento
    print(f"Hilo {nombre} terminó con incremto: {acumulado}")

if __name__ == "__main__":
    start = time.time()
    threads = []
    for number in range(3):
        threads.append(
            threading.Thread(target=api,args=(number,number))
        )

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end = time.time()

    print(f"Tiempo total {end - start}")