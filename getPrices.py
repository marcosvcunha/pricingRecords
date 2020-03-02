import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json
from datetime import datetime
from utils import *

def increasePageKabum(link):
    pos = link.find("pagina=")
    nextPage = int(link[pos + 7]) + 1
    newLink = link[:(pos + 7)] + str(nextPage) + link[(pos + 8):]
    return newLink

def increasePagePichau(link):
    pos = link.find("p=")
    nextPage = int(link[pos + 2]) + 1
    newLink = link[:(pos + 2)] + str(nextPage) + link[(pos + 3):]
    return newLink

def createProductDict(classifiers):
    newDict = {}
    for prodType in classifiers:
        if(not (prodType in newDict)):
            newDict[prodType] = {}
        for model in classifiers[prodType]:
            if(not (model in newDict[prodType])):
                newDict[prodType][model] = {}
        if(not("desconhecido" in newDict[prodType])):
            newDict[prodType]["desconhecido"] = {}
    return newDict

def getPage(url):

    uClient = uReq(url, timeout=10)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")

    ## Pega todas os cards
    return page_soup

def getPricesKabum(my_url):
    products = []

    startTime = datetime.now().timestamp()
    try:
        page_soup = getPage(my_url)
    except:
        print("Erro ao baixar a página.")
        return products
    endTime = datetime.now().timestamp()
    totalTime = endTime - startTime
    print("Tempo decorrido recebendo a página: " + str(totalTime))

    cards = page_soup.findAll("div", {"style":"position:relative;"})
    avaibleProd = True
    startTime = datetime.now().timestamp()
    while((len(cards) > 0) and avaibleProd):
        ## essa flag fica em falso até que um produto disponivel seja encontrado na pagina
        ## Se nenhum produto disponivel for encontrado em uma página, as proximas paginas não precisam ser verificadas.
        avaibleProd = False
        for i in range(len(cards)):
            try:
                ## Vê se o item está a venda pelo marketplace
                if(len(cards[i].findAll("span", {"class":"mktplace_chamada"})) == 0):
                    ## Ver se o produto está disponivel
                    comprarImg = cards[i].findAll("div", {"style":"padding:0 0 5px 0;"})[0].a.img['src']
                    if(not ("comprar_off" in comprarImg)):
                        avaibleProd = True ## um produto disponivel foi encontrado
                        link = cards[i].findAll("div",{"class":"listagem-titulo_descr"})[0].h2.a["href"]
                        name = cards[i].section.div.div.a.img["title"]
                        price12xStr = cards[i].findAll("div", {"class":"listagem-precoavista"})[0].text[3:].replace(".", "")
                        price12x = int(price12xStr[:(len(price12xStr) - 3)])
                        priceStr = cards[i].findAll("div", {"class":"listagem-preco"})

                        ## Caso nao haja desconto na compra a vista: price = price12x
                        if(len(priceStr) > 0):
                            priceStr = priceStr[0].text[3:].replace(".", "")
                            price = int(priceStr[:(len(priceStr) - 3)])
                        else:
                            price = price12x

                        prodDict = {"name":name, "price":price, "price12x":price12x, "link":link}
                        products.append(prodDict)
            except:
                print("Erro no item: " + str(i))
        ## Se nenhum produto disponivel for encontrado nesta página, as proximas nao precisam ser verificadas.
        if(avaibleProd):
            my_url = increasePageKabum(my_url)
            try:
                page_soup = getPage(my_url)
            except:
                print("Erro ao baixar a página.")
                return products
            cards = page_soup.findAll("div", {"style":"position:relative;"})
    endTime = datetime.now().timestamp()
    totalTime = endTime - startTime
    print("Tempo decorrido fazendo scrap: " + str(totalTime))
    return products

def getPricesPichau(my_url):
    products = []
    startTime = datetime.now().timestamp()
    try:
        page_soup = getPage(my_url)
    except:
        print("Erro ao baixar a página.")
        return products
    endTime = datetime.now().timestamp()
    totalTime = endTime - startTime
    print("Tempo decorrido recebendo a página: " + str(totalTime))
    cards = page_soup.findAll("li", {"class":"item product product-item"})

    avaibleProd = True
    startTime = datetime.now().timestamp()
    while((len(cards) > 0) and avaibleProd):
        ## essa flag fica em falso até que um produto disponivel seja encontrado na pagina
        ## Se nenhum produto disponivel for encontrado em uma página, as proximas paginas não precisam ser verificadas.
        avaibleProd = False
        for i in range(len(cards)):
            try:
                ## Ver se o produto está disponivel
                submitButton = cards[i].findAll("button",{"type":"submit"})
                if(len(submitButton) > 0):
                    avaibleProd = True ## um produto disponivel foi encontrado
                    link = cards[i].findAll("a",{"class":"product-item-link"})[0]['href']
                    name = cards[i].findAll("a",{"class":"product-item-link"})[0].text.strip()
                    price12xStr = cards[i].findAll("span",{"class":"price"})[0].text[2:].replace(".", "")
                    price12x = int(price12xStr[:(len(price12xStr) - 3)])
                    priceStr = cards[i].findAll("span",{"class":"price-boleto"})[0].text.strip()
                    priceStr = priceStr[10:(priceStr.find("no boleto") - 4)].replace(".", "")
                    price = int(priceStr)
                    prodDict = {"name":name, "price":price, "price12x":price12x, "link":link}
                    products.append(prodDict)
            except:
                print("Erro no item: " + str(i))
        ## Se nenhum produto disponivel for encontrado nesta página, as proximas nao precisam ser verificadas.
        if(avaibleProd and (len(cards) == 48)):
            my_url = increasePagePichau(my_url)
            try:
                page_soup = getPage(my_url)
            except:
                print("Erro ao baixar a página.")
                return products
            cards = page_soup.findAll("li", {"class":"item product product-item"})
        else:
            cards = []
    endTime = datetime.now().timestamp()
    totalTime = endTime - startTime
    print("Tempo decorrido fazendo scrap: " + str(totalTime))
    return products

def getProductsFromPage(url, store):
    if(store == "kabum"):
        prods = getPricesKabum(url)
    elif(store == "pichau"):
        prods = getPricesPichau(url)
    else:
        prods = {}
    return prods

def getProductsFromWeb(urls):
    now = datetime.now().timestamp()
    ## Carregando os classificadores
    classifiers = readJson("classifier.json")
    print("Começando a pegar os produtos.")
    products = []
    for store in urls:
        print("Pegando os produtos de: " + store)
        for prodType in urls[store]:
            for link in urls[store][prodType]:
                print(link)
                items = getProductsFromPage(link, store)
                for item in items:
                    try:
                        if(prodType in classifiers):
                            models = getModels(classifiers[prodType], item['name'])
                        else:
                            models = ["desconhecido"]
                        item["time"] = now
                        item["store"] = store
                        item["model"] = models[0] ## Por hora fica apenas com o primeiro modelo encontrado
                        item["prodType"] = prodType
                    except:
                        print("Pequeno erro insignificante.")
                        pass
                products += items
    return products