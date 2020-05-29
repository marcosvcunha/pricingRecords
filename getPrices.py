import bs4
from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import re
import json
from datetime import datetime

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
    hdr = {'User-Agent':'Mozilla/5.0'}
    req = Request(url,headers=hdr)
    uClient = uReq(req, timeout=10)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")

    ## Pega todas os cards
    return page_soup

def getPricesKabum(my_url):
    products = []
    try:
        page_soup = getPage(my_url)
    except Exception as e:
        print("Erro ao baixar a página: " + str(e))
        return products

    data = re.findall('const listagemDados =(.+?);\n', str(page_soup), re.S)
    items = json.loads(data[0])
    avaibleProd = True
    while((len(items) > 0) and avaibleProd):
        ## essa flag fica em falso até que um produto disponivel seja encontrado na pagina
        ## Se nenhum produto disponivel for encontrado em uma página, as proximas paginas não precisam ser verificadas.
        avaibleProd = False
        for item in items:
            try:
                if(not item['is_marketplace'] and item['disponibilidade']):
                    avaibleProd = True
                    prodDict = {'name': item['nome'], 'price': item['preco_desconto'], 'price12x': item['preco'], 
                    'link': 'kabum.com.br' + item['link_descricao'], 'img_url':item['img']}
                    products.append(prodDict)
            except Exception as e:
                print("Erro: " + str(e))
        ## Se nenhum produto disponivel for encontrado nesta página, as proximas nao precisam ser verificadas.
        if(avaibleProd):
            my_url = increasePageKabum(my_url)
            try:
                page_soup = getPage(my_url)
            except Exception as e:
                print("Erro ao baixar a página: " + str(e))
                return products
            data = re.findall('const listagemDados =(.+?);\n', str(page_soup), re.S)
            items = json.loads(data[0])
    return products

def getPricesPichau(my_url):
    products = []
    try:
        page_soup = getPage(my_url)
    except Exception as e:
        print("Erro ao baixar a página: " + str(e))
        return products
    
    cards = page_soup.findAll("li", {"class":"item product product-item"})

    avaibleProd = True
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
                    img_url = cards[i].findAll('img', {'class':'product-image-photo'})[0]['src']
                    prodDict = {"name":name, "price":price, "price12x":price12x, "link":link, 'img_url':img_url}
                    products.append(prodDict)
            except:
                print("Erro no item: " + str(i))
        ## Se nenhum produto disponivel for encontrado nesta página, as proximas nao precisam ser verificadas.
        if(avaibleProd and (len(cards) == 48)):
            my_url = increasePagePichau(my_url)
            try:
                page_soup = getPage(my_url)
            except Exception as e:
                print("Erro ao baixar a página: " + str(e))
                return products
            cards = page_soup.findAll("li", {"class":"item product product-item"})
        else:
            cards = []
    return products

def getPricesTerabyte(my_url):
    products = []
    try:
        page_soup = getPage(my_url)
    except Exception as e:
        print("Erro ao baixar a página: " + str(e))
        return products

    cards = page_soup.findAll("div",{"class":"pbox col-xs-12 col-sm-6 col-md-3"})
    for i in range(len(cards)):
        try:
            ## Ver se o produto está disponivel
            submitButton = cards[i].findAll("button",{"type":"button"})
            if(len(submitButton) > 0):
                link = "https://www.terabyteshop.com.br" + cards[i].findAll("a",{"class":"prod-name"})[0]['href']
                name = cards[i].findAll("a",{"class":"prod-name"})[0].text
                price12xStr = cards[i].findAll("div",{"class":"prod-juros"})[0].text
                price12xStr = price12xStr[price12xStr.find("R$"):]
                price12xStr = re.sub('[^0-9]','', price12xStr)
                price12xStr = price12xStr[:(len(price12xStr) - 2)]
                price12x = int(price12xStr) * 12
                priceStr = cards[i].findAll("div",{"class":"prod-new-price"})[0].text
                priceStr = re.sub('[^0-9]','', priceStr)
                price = int(priceStr[:(len(priceStr) - 2)])
                img_url = cards[i].findAll('a',{'class':'commerce_columns_item_image'})[0].img['src']
                prodDict = {"name":name, "price":price, "price12x":price12x, "link":link, 'img_url': img_url}
                products.append(prodDict)
        except Exception as e:
            print("Erro no item {}:".format(i) +  str(e))
    return products


def getProductsFromPage(url, store):
    if(store == "kabum"):
        prods = getPricesKabum(url)
    elif(store == "pichau"):
        prods = getPricesPichau(url)
    elif(store == "terabyte"):
        prods = getPricesTerabyte(url)
    else:
        prods = {}
    return prods

"""
    Retorna todos o produtos como uma lista de dicionarios.
"""
def getProductsFromWeb(urls):
    now = datetime.now().timestamp()
    ## Carregando os classificadores
    print("Começando a pegar os produtos.")
    products = []
    for store in urls:
        print("Pegando os produtos de: " + store)
        for prodType in urls[store]:
            for link in urls[store][prodType]:
                print('Pegando {} de {}.'.format(str(prodType), str(store)))
                items = getProductsFromPage(link, store)
                for item in items:
                    try:
                        item["store"] = store
                        item["prodType"] = prodType
                        item["time"] = now
                    except:
                        print("Pequeno erro insignificante.")
                        pass
                products += items
    return {"products": products, "readTime":now}

def main():
    prods = getPricesKabum('https://www.kabum.com.br/hardware/placas-mae?ordem=5&limite=100&pagina=1&string=')
    print(len(prods))

if __name__ == "__main__":
    main()