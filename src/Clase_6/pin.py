import multiprocessing
import time
SUPER_SECRET_PASSWORD=31_152_156

def buscar_password(intento):
    if intento == SUPER_SECRET_PASSWORD:
        print("contraseña encontrada")



if __name__=="__main__":
    start = time.time()
    PASSWORD_LENGTH = 100_000_000
    # Fregmentar el espacio de busqueda 
    num_procesos = multiprocessing.cpu_count()

    rango = PASSWORD_LENGTH // num_procesos

    Procesos = []
    for i in range(num_procesos):
        p = multiprocessing.Process(target=buscar_password, args=(i*rango,(i+1)*rango))
        Procesos.append(p)

    for proceso in Procesos:
        proceso.start()

    for proceso in Procesos:
        proceso.join()

    end = time.time()-start
    print("Tiempo total :",end)