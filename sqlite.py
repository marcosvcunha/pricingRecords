import sqlite3 as lite
from datetime import datetime
import time

con = lite.connect("teste.db")
now = datetime.now().timestamp()

listofTuples = [("marcos", 20), ("joao", 15), ("andre", 35), ("paulo", 22)]
with con:
    cur = con.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS people;
        CREATE TABLE people(name TEXT, age INT);
    """)
    cur.executemany("INSERT INTO people VALUES(?,?)", listofTuples) 

    ##data = cur.fetchall()