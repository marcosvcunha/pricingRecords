import sqlite3 as lite

def setDatabase():
    con = lite.connect('priceMonitor.db')
    with con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS products(name TEXT, price INT, price12x INT, link TEXT, time TIMESTAMP, store TEXT, 
            prodType TEXT, model TEXT, img_url TEXT);""")
        cur.execute("CREATE TABLE IF NOT EXISTS reads(id INTEGER PRIMARY KEY, time TIMESTAMP);")
        cur.execute(""" CREATE TABLE IF NOT EXISTS reportSubs(id INTEGER PRIMARY KEY, username TEXT, email TEXT,
            prodNames TEXT, prodTypes TEXT, period INT, lastReport TIMESTAMP);""")
        cur.execute("""CREATE TABLE IF NOT EXISTS urls(store TEXT, prodType TEXT, urls TEXT);""")
        cur.execute("""CREATE TABLE IF NOT EXISTS errors(func TEXT, file TEXT, error TEXT, otherInfo TEXT, date TIMESTAMP);""")

def main():
    setDatabase()

if __name__ == '__main__':
    main()