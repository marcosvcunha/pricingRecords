#from utils import *
import sqlite3 as lite
from datetime import datetime


## Salva os produtos no db
def storeProducts(data):
    con = lite.connect("priceMonitor.db")
    products = data
    now = datetime.now().timestamp()
    with con:
        cur = con.cursor()
        ## Salva o momento da leitura na tabela reads:
        cur.execute("INSERT INTO reads(time) VALUES({})".format(now))
        timeIndex = cur.lastrowid
        print('Time Index: ' + str(timeIndex))
        productsList = []
        for item in products:
            productsList.append((item['name'], item['price'], item['price12x'], item['link'], now,
                timeIndex, item['store'], item["prodType"], item['img_url']))
        cur.executemany("""INSERT INTO products(name, price, price12x, link, time, timeKey, store, prodType, img_url) 
            VALUES(?,?,?,?,?,?,?,?,?)""", productsList)


## Retorna o timestamp da ultima leitura de produtos feita
def getLastRead():
    con = lite.connect("priceMonitor.db")
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        # cur.executescript(""" 
        #     CREATE TABLE IF NOT EXISTS reads(id INTEGER PRIMARY KEY, time TIMESTAMP);
        # """)
        cur.execute("SELECT time FROM reads ORDER BY id DESC LIMIT 1;")
        rows = cur.fetchall()
    if(len(rows) > 0):
        return rows[0]['time']
    else:
        return 0


## Retorna todos os timestamps das leituras entre startTime e endTime
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
        cur.execute("""INSERT INTO reportSubs(username, email, prodNames, prodTypes, period, lastReport) 
            VALUES(?,?,?,?,?,?)""", (username, email, repr(prodNames), repr(prodTypes), period, float(0)))

def getAllReportSubs():
    con = lite.connect("priceMonitor.db")
    subs = []
    
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

def registerError(func, file, error, otherInfo=''):
    con = lite.connect('priceMonitor.db')

    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO errors VALUES(?, ?, ?, ?, ?);", (func, file, error, otherInfo, datetime.now().timestamp()))