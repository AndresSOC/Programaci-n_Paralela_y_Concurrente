import time
import multiprocessing
nucleos = 4
tiempo = 50_000_000
def calcular(nombre: str ) -> None:
    print(f"proceso{nombre} empezando a calcular ...")
    resultado = sum(i*i for i in range(tiempo))
    print(f"Proceso {nombre} finalizó ... ")

if __name__ == "__main__":
    start = time.time()
    procesos = []
    for i in range(nucleos):
        procesos.append(
            multiprocessing.Process(target=calcular,args=(i,))
        )
    for procces in procesos:
        procces.start()

    for procces in procesos:
        procces.join()

    end = time.time()
    print(f"Tiempo total: {end - start}")