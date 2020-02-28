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
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    ## Pega todas os cards
    return page_soup

def getPricesKabum(my_url):
    products = {}
    page_soup = getPage(my_url)
    cards = page_soup.findAll("div", {"style":"position:relative;"})
    avaibleProd = True
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
                        productId = getRandomString()
                        while(productId in products):
                            productId = getRandomString()
                        products[productId] = {}
                        link = cards[i].findAll("div",{"class":"listagem-titulo_descr"})[0].h2.a["href"]
                        name = cards[i].section.div.div.a.img["title"]
                        price12xStr = cards[i].findAll("div", {"class":"listagem-precoavista"})[0].text[3:].replace(".", "")
                        price12x = int(price12xStr[:(len(price12xStr) - 3)])
                        priceStr = cards[i].findAll("div", {"class":"listagem-preco"})[0].text[3:].replace(".", "")
                        price = int(priceStr[:(len(priceStr) - 3)])
                        products[productId]["name"] = name
                        products[productId]["price"] = price
                        products[productId]["price12x"] = price12x
                        products[productId]["link"] = link
            except:
                print("Erro no item: " + str(i))
        ## Se nenhum produto disponivel for encontrado nesta página, as proximas nao precisam ser verificadas.
        if(avaibleProd):
            my_url = increasePageKabum(my_url)
            page_soup = getPage(my_url)
            cards = page_soup.findAll("div", {"style":"position:relative;"})
    return products

def getPricesPichau(my_url):
    products = {}
    page_soup = getPage(my_url)
    cards = page_soup.findAll("li", {"class":"item product product-item"})

    avaibleProd = True
    while((len(cards) > 0) and avaibleProd):
        ## essa flag fica em falso até que um produto disponivel seja encontrado na pagina
        ## Se nenhum produto disponivel for encontrado em uma página, as proximas paginas não precisam ser verificadas.
        avaibleProd = False
        for i in range(len(cards)):
            try:
                ## Ver se o produto está disponivel
                submitButton = cards[30].findAll("button",{"type":"submit"})
                if(len(submitButton) > 0):
                    avaibleProd = True ## um produto disponivel foi encontrado
                    productId = getRandomString()
                    while(productId in products):
                        productId = getRandomString()
                    products[productId] = {}
                    link = cards[i].findAll("a",{"class":"product-item-link"})[0]['href']
                    name = cards[i].findAll("a",{"class":"product-item-link"})[0].text.strip()
                    price12xStr = cards[i].findAll("span",{"class":"price"})[0].text[2:].replace(".", "")
                    price12x = int(price12xStr[:(len(price12xStr) - 3)])
                    priceStr = cards[i].findAll("span",{"class":"price-boleto"})[0].text.strip()
                    priceStr = priceStr[10:(priceStr.find("no boleto") - 4)].replace(".", "")
                    price = int(priceStr)
                    products[productId]["name"] = name
                    products[productId]["price"] = price
                    products[productId]["price12x"] = price12x
                    products[productId]["link"] = link
            except:
                print("Erro no item: " + str(i))
        ## Se nenhum produto disponivel for encontrado nesta página, as proximas nao precisam ser verificadas.
        if(avaibleProd and (len(cards) == 48)):
            my_url = increasePagePichau(my_url)
            page_soup = getPage(my_url)
            cards = page_soup.findAll("li", {"class":"item product product-item"})
        else:
            cards = []
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

    products = createProductDict(classifiers)
    for store in urls:
        for prodType in urls[store]:
            for link in urls[store][prodType]:
                items = getProductsFromPage(link, store)
                for key in items:
                    try:
                        models = getModels(classifiers[prodType], items[key]['name'])
                        for model in models:
                            productId = getRandomString()
                            if(model in products[prodType]):
                                while(productId in products[prodType][model]):
                                    productId = getRandomString()
                            products[prodType][model][productId] = items[key]
                            products[prodType][model][productId]["time"] = now
                            products[prodType][model][productId]["store"] = store
                    except:
                        #print("Pequeno erro insignificante.")
                        pass

    return products