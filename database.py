#from utils import *
import sqlite3 as lite
from datetime import datetime

urls = {
    "kabum":{
        "vga":['https://www.kabum.com.br/hardware/placa-de-video-vga?string=&pagina=1&ordem=5&limite=100'],
        "ram":['https://www.kabum.com.br/hardware/memoria-ram?ordem=5&limite=100&pagina=1&string='],
        "mother_board":['https://www.kabum.com.br/hardware/placas-mae?ordem=5&limite=100&pagina=1&string='],
        "ssd":['https://www.kabum.com.br/hardware/ssd-2-5?ordem=5&limite=100&pagina=1&string='],
        "hd":['https://www.kabum.com.br/hardware/disco-rigido-hd?ordem=5&limite=100&pagina=1&string='],
        "cpu":['https://www.kabum.com.br/hardware/processadores?ordem=5&limite=100&pagina=1&string='],
        "pc":['https://www.kabum.com.br/computadores/computadores?ordem=5&limite=100&pagina=1&string='],
        "monitor":['https://www.kabum.com.br/computadores/monitores?ordem=5&limite=100&pagina=1&string='],
        "notebook":['https://www.kabum.com.br/computadores/notebooks-ultrabooks?ordem=5&limite=100&pagina=1&string='],
        "chair":['https://www.kabum.com.br/cgi-local/site/listagem/listagem.cgi?ordem=5&limite=100&pagina=1&string=cadeira']

    },
    "pichau":{
        "vga":["https://www.pichau.com.br/hardware/placa-de-video?p=1&product_list_limit=48"],
        "ram":["https://www.pichau.com.br/hardware/memorias?p=1&product_list_limit=48"],
        "mother_board":['https://www.pichau.com.br/hardware/placa-m-e?p=1&product_list_limit=48'],
        "ssd":['https://www.pichau.com.br/hardware/ssd?p=1&product_list_limit=48'],
        "hd":['https://www.pichau.com.br/hardware/hard-disk-e-ssd?p=1&product_list_limit=48'],
        "cpu":['https://www.pichau.com.br/hardware/processadores?p=1&product_list_limit=48'],
        "pc":['https://www.pichau.com.br/computadores?p=1&product_list_limit=48'],
        "monitor":['https://www.pichau.com.br/monitores?p=1&product_list_limit=48'],
        "notebook":['https://www.pichau.com.br/notebooks/notebooks?p=1&product_list_limit=48'],
        "chair":['https://www.pichau.com.br/cadeiras/gamer?p=1&product_list_limit=48']
    },
    "terabyte":{
        "vga":["https://www.terabyteshop.com.br/hardware/placas-de-video/nvidia-geforce" , "https://www.terabyteshop.com.br/hardware/placas-de-video/amd-radeon"],
        "ram":["https://www.terabyteshop.com.br/hardware/memorias/ddr4", "https://www.terabyteshop.com.br/hardware/memorias/ddr3"],
        "mother_board":['https://www.terabyteshop.com.br/hardware/placas-mae'],
        "ssd":['https://www.terabyteshop.com.br/hardware/hard-disk/ssd'],
        "hd":['https://www.terabyteshop.com.br/hardware/hard-disk/hd-sata-iii'],
        "ext-hd":['https://www.terabyteshop.com.br/hardware/hard-disk/hd-externo'],
        "cpu":['https://www.terabyteshop.com.br/hardware/processadores'],
        "pc":['https://www.terabyteshop.com.br/pc-gamer/t-home', 
            "https://www.terabyteshop.com.br/pc-gamer/t-moba",
            "https://www.terabyteshop.com.br/pc-gamer/t-gamer",
            "https://www.terabyteshop.com.br/pc-gamer/t-power"],
        "monitor":['https://www.terabyteshop.com.br/monitores'],
        "chair":['https://www.terabyteshop.com.br/cadeira-gamer']
    }
}

def saveLinks():
    con = lite.connect("priceMonitor.db")
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS urls;")
        cur.executescript(""" 
            CREATE TABLE IF NOT EXISTS urls(store TEXT, prodType TEXT, urls TEXT);
        """)
        urlsList = []
        for store in urls:
            for prodType in urls[store]:
                urlsList.append((store, prodType, repr(urls[store][prodType])))

        cur.executemany("INSERT INTO urls VALUES(?,?,?)", urlsList)

def tableExists(tableName):
    con = lite.connect("priceMonitor.db")
    with con:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(tableName))
        resul = cur.fetchone()
    if(resul != None):
        return True
    else:
        return False

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
                item['store'], item["prodType"]))
        cur.executemany("INSERT INTO products(name, price, price12x, link, time, store, prodType) VALUES(?,?,?,?,?,?,?)", productsList)
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
        cur.executescript(""" 
            CREATE TABLE IF NOT EXISTS reads(id INTEGER PRIMARY KEY, time TIMESTAMP);
        """)
        cur.execute("SELECT time FROM reads ORDER BY id DESC LIMIT 1;")
        rows = cur.fetchall()
    if(len(rows) > 0):
        return rows[0]['time']
    else:
        return 0


## Retorna todas as leituras entre startTime e endTime
def getReadsBetween(startTime=None, endTime=None):
    con = lite.connect("priceMonitor.db")
    query = "SELECT time FROM reads "
    if(startTime!=None and endTime!=None):
        query += "WHERE time > {} and time < {} ".format(startTime,endTime)
    elif(startTime!=None):
        query += "WHERE time > {} ".format(startTime)
    elif(endTime!=None):
        query += "WHERE time < {} ".format(endTime)
    query += "ORDER BY time ASC;"
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        times = []
        if(tableExists("reads")):
            cur.execute(query)
            rows = cur.fetchall()
    for row in rows:
        times.append(row['time'])    
    return times

"""
    Retorna os links na seguinte forma:
    {
        "loja": {
            "Tipo1":["url1","url2", ...],
            "Tipo2":["url1","url2", ...]
        },
        ...
    }
"""
def getUrlsAsDict():
    con = lite.connect("priceMonitor.db")
    if(not tableExists('urls')):
        saveLinks()
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM urls;")
        rows = cur.fetchall()
        urlsDict = {}
        
        for row in rows:
            if(not row['store'] in urlsDict):
                urlsDict[row['store']] = {}
            urlsDict[row['store']][row['prodType']] = eval(row['urls'])
    
    return urlsDict

def getCheapestsProducts(nameLike, nameNotLike=None, startTime=None, endTime=None):
    nameLike = "%" + nameLike.replace(" ", "%") + "%"
    query = "SELECT price FROM products WHERE name LIKE '{}' ".format(nameLike)
    if(nameNotLike!=None):
        query += "AND name NOT LIKE '{}' ".format(nameNotLike)
    readTimes = getReadsBetween(startTime, endTime)
    con = lite.connect("priceMonitor.db")
    data = {}
    data['prices'] = []
    data['times'] = []
    with con:
        ##con.row_factory = lite.Row
        cur = con.cursor()    
        for readTime in readTimes:
            thisQuery = query + "AND time > {} AND time < {} ORDER BY price ASC LIMIT 1;".format(int(readTime), int(readTime) + 1)
            cur.execute(thisQuery)
            rows = cur.fetchall()
            if(len(rows) > 0):
                data['prices'].append(rows[0][0])
                data['times'].append(readTime)
    return data 
    
def getCheapestsProductEachDay(nameLike, nameNotLike=None, prodType=None, startTime=None, endTime=None, countPerDay=1):
    nameLike = "%" + nameLike.replace(" ", "%") + "%"
    query = "SELECT price FROM products WHERE name LIKE '{}' ".format(nameLike)
    if(nameNotLike!=None):
        query += "AND name NOT LIKE '{}' ".format(nameNotLike)
    if(prodType!=None):
        query += "AND prodType = '{}' ".format(prodType)
    readTimes = getReadsBetween(startTime, endTime)
    
    days = []
    for read in readTimes:
        readDatetime = datetime.fromtimestamp(read)
        ## O dia as 00h00m
        timestamp = datetime(readDatetime.year, readDatetime.month, readDatetime.day).timestamp()
        if(not timestamp in days):
            days.append(timestamp)

    con = lite.connect("priceMonitor.db")
    data = {}
    data['prices'] = []
    data['times'] = []
    with con:
        ##con.row_factory = lite.Row
        cur = con.cursor()    
        for day in days:
            thisQuery = query + "AND time > {} AND time < {} ORDER BY price ASC LIMIT {};".format(int(day), int(day) + 60*60*24, countPerDay)
            cur.execute(thisQuery)
            rows = cur.fetchall()
            for i in range(len(rows)):
                data['prices'].append(rows[i][0])
                data['times'].append(day)
    return data

"""
    Report Subscription
    id  | username | email    | prodNames       | prodTypes   | period (days) | sastReport |
    int | Text     | Text     | [n1, n2, ...]   | [t1, t2...] | int           | timestamp  |
"""
def insertSub(username, email, prodNames, prodTypes, period):
    con = lite.connect("priceMonitor.db")
    with con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS reportSubs(id INTEGER PRIMARY KEY, username TEXT, email TEXT, 
            prodNames TEXT, prodTypes TEXT, period INT, lastReport timestamp);""")
        cur.execute("""INSERT INTO reportSubs(username, email, prodNames, prodTypes, period, lastReport) 
            VALUES(?,?,?,?,?,?)""", (username, email, repr(prodNames), repr(prodTypes), period, float(0)))

def getAllReportSubs():
    con = lite.connect("priceMonitor.db")
    subs = []
    
    if(tableExists('reportSubs')):
        with con:
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM reportSubs;")
            rows = cur.fetchall()
            for row in rows:
                subs.append({'username':row['username'], 'email':row['email'], 'prodNames':eval(row['prodNames']),
                    'prodTypes':eval(row['prodTypes']), 'period':row['period'], 'lastReport':row['lastReport']})    
    return subs

def updateReportSub(username, lastReport):
    con = lite.connect("priceMonitor.db")
    with con:
        cur = con.cursor()
        cur.execute("UPDATE reportSubs SET lastReport = {} WHERE username = '{}';".format(lastReport, username))
    return