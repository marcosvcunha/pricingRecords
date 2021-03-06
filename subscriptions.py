from datetime import datetime
import database as db
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
import numpy as np
from os import system
import ezgmail
import glob


"""
    Report Subscription
    Username | Email    | ProdName        | ProdType    | Period (days) | LastReport |
    Text     | Text     | [n1, n2, ...]   | [t1, t2...] | int           | timestamp  |

    O Report é composto por:
        Dois gráficos para cada produto:
            Do ultimo mês:
                - Menor preço por dia.
                - Media dos 3 menores preços por dia.
            ?? Grafico de Barras com quantidade de produtos por dia ??
"""
def createSub():
    username = "Marcos"
    email = "marcoscunha2903@gmail.com"
    prodNames = ["rx 580", "rx 570", "gtx 1050", "gtx 1060"]
    prodTypes = ["vga", "vga", "vga", "vga"]
    period = 15
    db.insertSub(username, email, prodNames, prodTypes, period)

## Recebe uma lista com os produtos e as datas. Faz uma média para cada dia.
"""
    Data está no seguinte formato:
    data = {
        'price':[p1, p2, p3, ...],
        'time':[t1, t2, t3, ...]
    }
"""
def _getAvarageForEachDay(data):
    newData = {}
    newData['prices'] = []
    newData['times'] = []
    dayCount = []
    
    for i in range(len(data['prices'])):
        if(not data['times'][i] in newData['times']):
            newData['prices'].append(data['prices'][i])
            newData['times'].append(data['times'][i])
            dayCount.append(1)
        else:
            position = newData['times'].index(data['times'][i])
            newData['prices'][position] = (newData['prices'][position]*dayCount[position] + data['prices'][i])/(dayCount[position] + 1)
            dayCount[position] += 1
    return newData

"""
    Confere todas as subs, vê quais precisam de report, e faz o report.
"""
def checkSubs():
    now = datetime.now().timestamp()
    subs = db.getAllReportSubs()
    secondsInADay = 86400
    for sub in subs:
        try:
            if(sub['lastReport'] + sub['period'] * secondsInADay < now):
                ## Fazer Report
                for i in range(len(sub['prodNames'])):
                    ## tem apenas o produto mais barato de cada dia.
                    singleProd = db.getCheapestsProductEachDay(sub['prodNames'][i], prodType=sub['prodTypes'][i], 
                        startTime=(now - secondsInADay*30), endTime=now, countPerDay=1)
                    ## Tem os 3 produtos mais baratos de cada dia
                    threeProds = db.getCheapestsProductEachDay(sub['prodNames'][i], prodType=sub['prodTypes'][i], 
                        startTime=(now - secondsInADay*30), endTime=now, countPerDay=3)
                    threeProdsAvg = _getAvarageForEachDay(threeProds)
                    _plotProducts(singleProd, threeProdsAvg, sub['prodNames'][i].upper())
                _sendPlotsByEmail(sub)
                _deletePlots(sub['prodNames'])
                db.updateReportSub(sub['username'], datetime.now().timestamp())
        except Exception as e:
            db.registerError('checkSubs', 'subscriptions.py', str(e), otherInfo='sub: ' + str(sub))
            pass

def _deletePlots(names):
    pngFiles = glob.glob('*.png')
    for name in names:
        fileName = name.replace(" ", "").upper() + ".png"
        if(fileName in pngFiles):
            system("rm " + fileName)

def _plotProducts(singleProd, threeProdsAvg, title):
    dateTimes = []
    for value in singleProd['times']:
        dateTimes.append(datetime.fromtimestamp(value))
    dates1 = matplotlib.dates.date2num(dateTimes)
    
    dateTimes = []
    for value in threeProdsAvg['times']:
        dateTimes.append(datetime.fromtimestamp(value))
    dates2 = matplotlib.dates.date2num(dateTimes)

    if(len(dates1) > 0 and len(dates2) > 0):
        plt.plot(dates1, singleProd['prices'], marker='o', color='b', label='Produto mais Barato do dia')
        plt.plot(dates2, threeProdsAvg['prices'], marker='X', color='r', label='Média dos três produtos mais baratos')
        plt.legend(fontsize='x-small')
        plt.title(title)
        plt.xlabel('Datas')
        plt.ylabel('Preços')
        plt.gcf().autofmt_xdate()
        myFmt = mdates.DateFormatter('%d/%m')
        plt.gca().xaxis.set_major_formatter(myFmt)
        plt.savefig('{}.png'.format(title.replace(" ", "")))
        plt.clf()


def _sendPlotsByEmail(subReport):
    fileNames = []
    pngFiles = glob.glob('*.png')
    for prodName in subReport['prodNames']:
        fileName = prodName.replace(" ", "") + '.png'
        if(fileName in pngFiles):
            fileNames.append(fileName)
    ezgmail.init()
    ezgmail.send(subReport['email'], 'PriceMonitor Relatorio', 'Olá {}, segue por anexo seu relatório do PriceMonitor.'
        .format(subReport['username']), fileNames)
    print("Email enviado!")


def main():
    createSub()
    checkSubs()
    return

if __name__ == "__main__":
    main()