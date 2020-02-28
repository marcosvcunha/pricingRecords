from utils import *
"""
    Salva todos os dados em um unico arquivo json
"""
def saveInJson(data):
    oldData = readJson("products.json")
    for prodType in data:
        if(not(prodType in oldData)):
            oldData[prodType] = {}
        for model in data[prodType]:
            if(not(model in oldData[prodType])):
                oldData[prodType][model] = {}
            for prod in data[prodType][model]:
                productId = getRandomString()
                while(productId in oldData[prodType][model]):
                    productId = getRandomString()
                oldData[prodType][model][productId] = data[prodType][model][prod]
    writeJson("products.json", oldData)