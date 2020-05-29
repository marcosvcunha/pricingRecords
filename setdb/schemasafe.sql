CREATE TABLE IF NOT EXISTS products(
    name TEXT, 
    price INT, 
    price12x INT, 
    link TEXT, 
    img_url TEXT, 
    time TIMESTAMP, 
    store TEXT, 
    prodType TEXT, 
    model TEXT);

CREATE TABLE IF NOT EXISTS reads(
    id INTEGER PRIMARY KEY, 
    time TIMESTAMP);

CREATE TABLE IF NOT EXISTS reportSubs(
    id INTEGER PRIMARY KEY, 
    username TEXT, 
    email TEXT, 
    prodNames TEXT, 
    prodTypes TEXT, 
    period INT, 
    lastReport TIMESTAMP);

CREATE TABLE IF NOT EXISTS urls(
    store TEXT, 
    prodType TEXT, 
    urls TEXT);

CREATE TABLE IF NOT EXISTS errors(
    func TEXT,
    file TEXT,
    error TEXT,
    otherInfo TEXT,
    date TIMESTAMP);