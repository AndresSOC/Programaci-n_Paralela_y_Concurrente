import time

# Condiciones de Carrera y Sincronización: Exclusión Mutua

boletos_disponibles = 1000

def vender_boletos(cantidad):
    global boletos_disponibles
    
    #Simulacion latencia I/O en consulta a la bd

    temp = boletos_disponibles
    time.sleep(.0001)
    