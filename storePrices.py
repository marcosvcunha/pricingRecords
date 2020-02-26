import getPrices
from getPrices import getPricesKabum
from getPrices import getRandomString
from datetime import datetime
import json

urls = {
    "kabum":{
        "vga":['https://www.kabum.com.br/hardware/placa-de-video-vga?string=&pagina=1&ordem=5&limite=100'],
        "ram":['https://www.kabum.com.br/hardware/memoria-ram?ordem=5&limite=100&pagina=1&string=']
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
def getModels(models, name):
    listModels = []
    for key in models:
        ## Vai incluir na lista apenas se TODAS palavras de "include" aparecer no nome e 
        ## NENHUMA palavra de "exclude aparecer"
        if(all(word.lower() in name.lower() for word in models[key]["include"]) and 
            not any(word.lower() in name.lower() for word in models[key]["exclude"])):
            listModels.append(key)
    if(len(listModels) == 0):
        listModels.append("desconhecido")
    return listModels

"""
    Cria um dicionario com base em "classifier"
"""
def createProductDict(classifiers, oldDict):
    newDict = oldDict
    for prodType in classifiers:
        if(not (prodType in newDict)):
            newDict[prodType] = {}
        for model in classifiers[prodType]:
            if(not (model in newDict[prodType])):
                newDict[prodType][model] = {}
        if(not("desconhecido" in newDict[prodType])):
            newDict[prodType]["desconhecido"] = {}
    return newDict

def main():
    ## Carregando os classificadores
    with open('classifier.json', 'r') as fp:
        classifiers = json.load(fp)

    ## Carregando DB
    with open('products.json', 'r') as fp:
        products = json.load(fp)

    #print(items[min(items.keys(), key=(lambda k: items[k]['price']))])
    products = createProductDict(classifiers, products)
    for store in urls:
        for prodType in urls[store]:
            for link in urls[store][prodType]:
                print(link)
                items = getPricesKabum(link)
                for key in items:
                    try:
                        productId = getRandomString()
                        while(productId in products):
                            productId = getRandomString()
                        models = getModels(classifiers[prodType], items[key]['name'])
                        for model in models:
                            products[prodType][model][productId] = items[key]
                            products[prodType][model][productId]["time"] = datetime.now().timestamp()
                            products[prodType][model][productId]["store"] = store
                    except:
                        print("Pequeno erro insignificante.")

    with open('products.json', 'w') as fp:
        json.dump(products, fp)


if __name__ == '__main__':
    main()