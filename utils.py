import random
import string
import json

def getRandomString():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

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

def writeJson(fileName, data):
    with open(fileName, 'w') as fp:
        json.dump(data, fp)

def readJson(fileName):
    with open(fileName, 'r') as fp:
        data = json.load(fp)
    return data