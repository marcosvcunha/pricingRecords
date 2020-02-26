import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import random
import string

def getRandomString():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

def increasePage(link):
    pos = link.find("pagina=")
    nextPage = int(link[pos + 7]) + 1
    newLink = link[:(pos + 7)] + str(nextPage) + link[(pos + 8):]
    return newLink

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
    while(len(cards) > 0):
        for i in range(len(cards)):
            try:
                ## Vê se o item está a venda pelo marketplace
                if(len(cards[i].findAll("span", {"class":"mktplace_chamada"})) == 0):
                    ## Ver se o produto está disponivel
                    comprarImg = cards[i].findAll("div", {"style":"padding:0 0 5px 0;"})[0].a.img['src']
                    if(not ("comprar_off" in comprarImg)):
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
        my_url = increasePage(my_url)
        page_soup = getPage(my_url)
        cards = page_soup.findAll("div", {"style":"position:relative;"})
    return products
