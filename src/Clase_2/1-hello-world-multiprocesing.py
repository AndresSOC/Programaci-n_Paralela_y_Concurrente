import time 
import multiprocessing

tiempo_proceso = 50_000_000
def calcular(nombre: str) -> None:
    print(f"Proceso {nombre} empezando a calcular ...")
    resultado = sum(i* i for i in range (tiempo_proceso))
    print(f"Proceso {nombre} finalizo ...")

if __name__ == "__main__":
    proceso = []

    start = time.time()

    for i in range(4):
        proceso.append(
            calcular(i)
        )


    end = time.time()
    print(f"Tiempo total : {end -start}")