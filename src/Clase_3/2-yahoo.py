import time
import random
import requests
import threading
from bs4 import BeautifulSoup 


semaforo = threading.Semaphore(8)

def obtener_precio(symbol):
    with semaforo:
        url=f"https://es.finance.yahoo.com/quote/{symbol}"
       
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://finance.yahoo.com"
        }

        while True:
            time.sleep(8 *random.random())
            response = requests.get(url,headers=header)
            print(response.status_code)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text,"html.parser")
                valor=soup.find("span",{"data-testid":"qsp-price"})
                if valor:
                    precio = valor.text.strip()
                    print(f"La accion {symbol} cuesta {precio}")
                else:
                    precio = "Privado"
                    print(f"la accion {symbol} cuesta {precio}")
                break
            else:
                continue
        

if __name__ == "__main__":
    with open("data/lista_sp500.txt","r") as f:
        lista_symbolos = eval(f.read())
    threads = []
    for symbol in lista_symbolos:
        threads.append(
            threading.Thread(target=obtener_precio,args=(symbol,))
        )
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()