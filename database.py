from utils import *
import sqlite3 as lite

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

def saveSqlite(data):
    con = lite.connect("priceMonitor.db")
    products = data["products"]
    with con:
        cur = con.cursor()
        cur.executescript(""" 
            CREATE TABLE IF NOT EXISTS products(name TEXT, price INT, price12x INT, link TEXT, time TIMESTAMP, 
            store TEXT, prodType TEXT, model TEXT);
        """)
        productsList = []
        for item in products:
            productsList.append((item['name'], item['price'], item['price12x'], item['link'], item['time'],
                item['store'], item["prodType"], item["model"]))
        cur.executemany("INSERT INTO products VALUES(?,?,?,?,?,?,?,?)", productsList)
        ## Salva o momento da leitura na tabela reads:
        cur.executescript(""" 
            CREATE TABLE IF NOT EXISTS reads(id INTEGER PRIMARY KEY, time TIMESTAMP);
        """)
        cur.execute("INSERT INTO reads(time) VALUES({})".format(data["readTime"]))
