dicc= {}

with open("../Clase_3/data/lista_sp500.txt","r") as f:
    symbols = eval(f.read())
    for symbol in symbols:
        dicc[symbol] = 1
        
print(dicc)
