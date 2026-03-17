""" streams
    semaforos-> num de hilos a ejecutar
    open -> wr archivos
    socket.socket -> paquetes de red
    con.connect()   -> bd
    lock   -> bloquea vataibles en memoria """ 

import threading
import time
start = time.time()

lock_teatro = threading.Lock

asientos = [None] *10000
ventas_totales = 0

def vender_tickets(id_vendedor):
    global ventas_totales  

for _ in range(20):
    for i in range(len(asientos)):
        with lock_teatro:
            if asientos[i] is None:
                time.sleep(.0001)

                asientos[i] = f"Vendedor-{id_vendedor}"
                ventas_totales+=1
                break

    for i in range(10_000):
        id_vendedor=threading.Thread(target=vender_tickets, arg=(i,))
        vendedores.append(t)

    for threads in threading:
        threads.start()

    for threads in threading:
        threads.join()  