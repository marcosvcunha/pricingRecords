import getPrices
from getPrices import getProductsFromWeb as getProds
from datetime import datetime
import database as db
from subscriptions import checkSubs
import time
from threading import Thread
import sys

test_urls = {
    "kabum":{
        "vga":['https://www.kabum.com.br/hardware/placa-de-video-vga?string=&pagina=1&ordem=5&limite=100'],
        "ram":['https://www.kabum.com.br/hardware/memoria-ram?ordem=5&limite=100&pagina=1&string=']
    },
    "pichau":{
        "vga":['https://www.pichau.com.br/hardware/placa-de-video?p=1&product_list_limit=48'],
        "ram":['https://www.pichau.com.br/hardware/memorias?p=1&product_list_limit=48']
    },
    "terabyte":{
        "vga":['https://www.terabyteshop.com.br/hardware/placas-de-video/nvidia-geforce'],
        "ram":['https://www.terabyteshop.com.br/hardware/memorias/ddr4']
    }
}

def readProducts(test=False):
    while 1:
        lastRead = db.getLastRead()
        now = datetime.now().timestamp()
        deltaInHours = int((now - lastRead)/(3600))

        ## Só faz a leitura se se passaram pelo menos 20 horas desde a ultima leitura.
        if(deltaInHours >= 20 or test):
            if(not test):
                urls = db.getUrlsAsDict()
            else:
                urls = test_urls
            startTime = datetime.now().timestamp()
            data = getProds(urls)
            endTime = datetime.now().timestamp()
            getProdsTime = endTime - startTime

            startTime = datetime.now().timestamp()
            db.storeProducts(data)
            endTime = datetime.now().timestamp()
            saveSqliteTime = endTime - startTime

            print("Captura dos preços completa!")
            print("Tempo decorrido: " + str(getProdsTime + saveSqliteTime))
            print("Tempo para obter os dados: " + str(getProdsTime))
            print("Tempo para salvar em Sqlite: " + str(saveSqliteTime))
        else:
            print("Going to sleep")
            nextRead = lastRead + 3600*8
            sleepTime = nextRead - datetime.now().timestamp()
            ## Dorme até o momento da proxima leitura.
            time.sleep(sleepTime)

def makeReports():
    while 1:
        checkSubs()
        print('Make Reports Indo Dormir')
        time.sleep(60*60)

def readTest():
    readProducts(test=True)

def main():
    print('Número de argumentos: ' + str(len(sys.argv)))
    if(len(sys.argv) == 1):
        getProductsThread = Thread(target=readProducts)
        getProductsThread.start()
        makeReportsThread = Thread(target=makeReports)
        makeReportsThread.start()
        getProductsThread.join()
        makeReportsThread.join()
    elif(len(sys.argv) == 2):
        if(sys.argv[1] == 'readTest'):
            readTest()
        else:
            print('Argumento incorreto!')
    else:
        print('Número incorreto de argumentos')

if __name__ == '__main__':
    main()