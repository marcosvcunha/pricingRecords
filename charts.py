from datetime import datetime

startTime = datetime.now().timestamp()
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
import numpy as np
#import pandas as pd
import os
from database import getCheapestsProductEachDay
endTime = datetime.now().timestamp()
totalTime = endTime - startTime
print("Tempo para realizar os imports: " + str(totalTime))


## Copia o DB real para a este diretorio
def updateDb():
    os.system("cp 'C:\Program Files (x86)\PriceMonitor\priceMonitor.db' priceMonitor.db")

def plotCheapestProducts(prodName):
    values = getCheapestsProductEachDay(prodName, prodType='ram')
    dateTimes = []
    for value in values['times']:
        dateTimes.append(datetime.fromtimestamp(value))
    dates = matplotlib.dates.date2num(dateTimes)

    #plt.scatter(dates, values['prices'])
    plt.plot(dates, values['prices'], marker='o', color='b')
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%d/%m')
    plt.gca().xaxis.set_major_formatter(myFmt)

    plt.show()

def main():
    pass
if __name__ == "__main__":
    main()
