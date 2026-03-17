import requests
from bs4 import BeautifulSoup 

try:
    with open("data/sp_500.html","r") as f:
        response = f.read()
        print("Documento encontrado")
    soup = BeautifulSoup(response,"html.parser")
    table = soup.find(id="constituents")
    symbols = []
    for row in table.find_all("tr")[1:]:
        symbols.append(row.find("td").text.strip())
    with open("data/lista_sp500.txt","w") as f:
        f.write(str(symbols))
        
except:
    url = "https://es.wikipedia.org/wiki/Anexo:Compa%C3%B1%C3%ADas_del_S%26P_500"
    header={
        "User-Agent":"Mi proyecto/SP500/1.0"
    }
    response = requests.get(url,headers=header)
    if response.status_code == 200:
        with open("data/sp_500.html","w") as f:
            f.write(response.text)
    else:
        print("Error")
        print(response.text)
        

