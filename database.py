from utils import *
import sqlite3 as lite

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

def getLastRead():
    con = lite.connect("priceMonitor.db")
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute("SELECT time FROM reads ORDER BY id DESC LIMIT 1;")
        rows = cur.fetchall()
    return rows[0]['time']

