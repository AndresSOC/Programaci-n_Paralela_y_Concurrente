def cuadrado(n):
    return n**2

lista_cuadrados = list(map(cuadrado,range(10)))
print(lista_cuadrados) 

lista_cuadrados_2 = list(map(lambda x: x**2,range(10)))
print(lista_cuadrados_2)
