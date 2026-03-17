import time
import multiprocessing

def es_primo(x):
    for i in range(2,x//2+1):
        if x%i == 0:
            return False
    return True
        
if __name__ =="__main__":
    numeros = range(10_000_000,10_010_000)
    start = time.time()
    lista_primos = []
    for i in numeros:
        if es_primo(i):
            lista_primos.append(i)
    print(f"Tiempo total: ", time.time()-start)

    start = time.time()
    with multiprocessing.Pool() as pool:
        pool.map(es_primo,numeros)
    print(f"Tiempo total: ", time.time()-start)

