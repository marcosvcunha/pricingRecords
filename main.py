import getPrices
from getPrices import getProductsFromWeb as getProds
from utils import *
from datetime import datetime
from database import *

urls = {
    "kabum":{
        "vga":['https://www.kabum.com.br/hardware/placa-de-video-vga?string=&pagina=1&ordem=5&limite=100'],
        "ram":['https://www.kabum.com.br/hardware/memoria-ram?ordem=5&limite=100&pagina=1&string='],
        "mother_board":['https://www.kabum.com.br/hardware/placas-mae?ordem=5&limite=100&pagina=1&string='],
        "ssd":['https://www.kabum.com.br/hardware/ssd-2-5?ordem=5&limite=100&pagina=1&string='],
        "hd":['https://www.kabum.com.br/hardware/disco-rigido-hd?ordem=5&limite=100&pagina=1&string='],
        "cpu":['https://www.kabum.com.br/hardware/processadores?ordem=5&limite=100&pagina=1&string='],
        "pc":['https://www.kabum.com.br/computadores/computadores?ordem=5&limite=100&pagina=1&string='],
        "monitor":['https://www.kabum.com.br/computadores/monitores?ordem=5&limite=100&pagina=1&string='],
        "notebook":['https://www.kabum.com.br/computadores/notebooks-ultrabooks?ordem=5&limite=100&pagina=1&string='],
        "chair":['https://www.kabum.com.br/cgi-local/site/listagem/listagem.cgi?ordem=5&limite=100&pagina=1&string=cadeira']

    },
    "pichau":{
        "vga":["https://www.pichau.com.br/hardware/placa-de-video?p=1&product_list_limit=48"],
        "ram":["https://www.pichau.com.br/hardware/memorias?p=1&product_list_limit=48"]
    }
}

test_urls = {
    "kabum":{
        "vga":['https://www.kabum.com.br/hardware/placa-de-video-vga?string=&pagina=1&ordem=5&limite=100']
    }
}



"""
    models vem no seguinte formato:
    models = {
        "modelo1",["palavrachave1", "palavrachave2"],
        "modelo2",["palavrachave1", "palavrachave2"],
        ...
    }
    check model vai conferir se name contem todas as palavras chaves
    retorna uma lista com todos os modelos os quais todas palavras chaves apareçam no nome
    se nao encontrar nenhum modelo, retorna uma lisa com "desconhecido"
"""

"""
    Cria um dicionario com base em "classifier"
"""

def main():

    startTime = datetime.now().timestamp()
    products = getProds(urls)
    endTime = datetime.now().timestamp()
    getProdsTime = endTime - startTime

    startTime = datetime.now().timestamp()
    saveSqlite(products)
    endTime = datetime.now().timestamp()
    saveSqliteTime = endTime - startTime

    print("Captura dos preços completa!")
    print("Tempo decorrido: " + str(getProdsTime + saveSqliteTime))
    print("Tempo para obter os dados: " + str(getProdsTime))
    print("Tempo para salvar em Sqlite: " + str(saveSqliteTime))


if __name__ == '__main__':
    main()