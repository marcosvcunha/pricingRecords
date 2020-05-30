DROP TABLE products;

CREATE TABLE IF NOT EXISTS products(
    name TEXT, 
    price INT, 
    price12x INT, 
    link TEXT, 
    img_link TEXT, 
    time TIMESTAMP,
    timeKey INT,
    store TEXT, 
    prodType TEXT, 
    model TEXT);

DROP TABLE reads;

CREATE TABLE IF NOT EXISTS reads(
    id INTEGER PRIMARY KEY, 
    time TIMESTAMP);

DROP TABLE reportSubs;

CREATE TABLE IF NOT EXISTS reportSubs(
    id INTEGER PRIMARY KEY, 
    username TEXT, 
    email TEXT, 
    prodNames TEXT, 
    prodTypes TEXT, 
    period INT, 
    lastReport TIMESTAMP);

DROP TABLE urls;

CREATE TABLE IF NOT EXISTS urls(
    store TEXT, 
    prodType TEXT, 
    urls TEXT);

DROP TABLE errors;

CREATE TABLE IF NOT EXISTS errors(
    func TEXT,
    file TEXT,
    error TEXT,
    otherInfo TEXT,
    date TIMESTAMP);