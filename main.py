import getPrices
from getPrices import getProductsFromWeb as getProds
from utils import *
from datetime import datetime
from database import *
import time

test_urls = {
    "kabum":{
        "vga":['https://www.kabum.com.br/hardware/placa-de-video-vga?string=&pagina=1&ordem=5&limite=100'],
        "ram":['https://www.kabum.com.br/hardware/memoria-ram?ordem=5&limite=100&pagina=1&string=']
    }
}


"""
    models vem no seguinte formato:
    models = {
        "modelo1",["palavrachave1", "palavrachave2"],
        "modelo2",["palavrachave1", "palavrachave2"],
        ...
    }
    check model vai conferir se name contem todas as palavras chaves
    retorna uma lista com todos os modelos os quais todas palavras chaves apareçam no nome
    se nao encontrar nenhum modelo, retorna uma lisa com "desconhecido"
"""

"""
    Cria um dicionario com base em "classifier"
"""

def main():
    while 1:
        lastRead = getLastRead()
        now = datetime.now().timestamp()
        deltaInHours = int((now - lastRead)/(3600))

        ## Só faz a leitura se se passaram pelo menos 8 horas desde a ultima leitura.
        if(deltaInHours >= 8):
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

if __name__ == '__main__':
    main()