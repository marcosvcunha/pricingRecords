import getPrices
from getPrices import getProductsFromWeb as getProds
from datetime import datetime
from database import *
from subscriptions import checkSubs
import time
from threading import Thread

test_urls = {
    "kabum":{
        "vga":['https://www.kabum.com.br/hardware/placa-de-video-vga?string=&pagina=1&ordem=5&limite=100'],
        "ram":['https://www.kabum.com.br/hardware/memoria-ram?ordem=5&limite=100&pagina=1&string=']
    }
}

def readProducts():
    while 1:
        lastRead = getLastRead()
        now = datetime.now().timestamp()
        deltaInHours = int((now - lastRead)/(3600))

        ## Só faz a leitura se se passaram pelo menos 8 horas desde a ultima leitura.
        if(deltaInHours >= 24):
            urls = getUrlsAsDict()
            startTime = datetime.now().timestamp()
            data = getProds(urls)
            endTime = datetime.now().timestamp()
            getProdsTime = endTime - startTime

            startTime = datetime.now().timestamp()
            saveSqlite(data)
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

def main():
    getProductsThread = Thread(target=readProducts)
    getProductsThread.start()
    makeReportsThread = Thread(target=makeReports)
    makeReportsThread.start()
    getProductsThread.join()
    makeReportsThread.join()

if __name__ == '__main__':
    main()