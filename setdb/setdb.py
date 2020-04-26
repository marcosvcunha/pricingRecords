import sqlite3 as lite
import os

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


def setdb(safe=True):
    if(safe):
        con = lite.connect('priceMonitor.db')
        with con:
            cur = con.cursor()
            with open('./setdb/schemasafe.sql', 'r', encoding='utf8') as f:
                cur.executescript(f.read())

            urlsList = []
            for store in urls:
                for prodType in urls[store]:
                    urlsList.append((store, prodType, repr(urls[store][prodType])))
            cur.executemany("INSERT INTO urls VALUES(?,?,?)", urlsList)
    else:
        con = lite.connect('priceMonitor.db')
        with con:
            cur = con.cursor()
            with open('./setdb/schemanotsafe.sql', 'r', encoding='utf8') as f:
                cur.executescript(f.read())

            urlsList = []
            for store in urls:
                for prodType in urls[store]:
                    urlsList.append((store, prodType, repr(urls[store][prodType])))
            cur.executemany("INSERT INTO urls VALUES(?,?,?)", urlsList)

if __name__ == '__main__':
    os.chdir('../')
    setdb()