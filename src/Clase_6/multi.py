import multiprocessing

def saludar():
    print("Hola desde nodo",__name__)

if __name__ == "__main__":
    p = multiprocessing.Process(target=saludar)
    p.start()
    p.join()
