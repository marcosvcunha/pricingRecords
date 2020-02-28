import getPrices
from getPrices import getProductsFromWeb as getProds
from utils import *
from datetime import datetime
import json
from database import saveInJson

urls = {
    "kabum":{
        "vga":['https://www.kabum.com.br/hardware/placa-de-video-vga?string=&pagina=1&ordem=5&limite=100'],
        "ram":['https://www.kabum.com.br/hardware/memoria-ram?ordem=5&limite=100&pagina=1&string=']
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

    ## Carregando os classificadores
    #with open('classifier.json', 'r') as fp:
    #    classifiers = json.load(fp)

    ## Carregando DB
    #with open('products.json', 'r') as fp:
    #    products = json.load(fp)

    #print(items[min(items.keys(), key=(lambda k: items[k]['price']))])
    products = getProds(urls)
    saveInJson(products)

    #with open('products.json', 'w') as fp:
    #    json.dump(products, fp)


if __name__ == '__main__':
    main()