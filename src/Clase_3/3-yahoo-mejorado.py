import time
import random
import requests
import threading
from bs4 import BeautifulSoup
import queue

cola_procesos = queue.Queue()

def obtener_precio_stock():
    while not cola_procesos.empty():
        try:
            symbol = cola_procesos.get_nowait()
        except queue.Empty:
            break
        
        url = f"https://finance.yahoo.com/quote/{symbol}"

        header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Referer": "https://finance.yahoo.com"
            }
        
        while True:
            time.sleep(30*random.random())
            response = requests.get(url, headers=header,)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text,"html.parser")
                valor = soup.find("span",{"data-testid":"qsp-price"})
                if valor:
                    precio = valor.text.strip()
                else:
                    precio = "Privado"
                break
            else:
                continue
        
        print(f"La accion {symbol} cuesta: {precio}")
        cola_procesos.task_done()

if __name__ == "__main__":
    with open("data/lista_sp500.txt","r") as f:
        lista_symbolos = eval(f.read())
    threads = []
    for symbol in lista_symbolos:
        cola_procesos.put(symbol)
    for _ in range (8):
        t = threading.Thread(target = obtener_precio_stock)
        t.start()