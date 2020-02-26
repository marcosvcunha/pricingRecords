import json
import random
import string
from datetime import datetime
"""
    SAVE:
    with open('data.json', 'w') as fp:
        json.dump(data, fp)
    LOAD:
    with open('data.json', 'r') as fp:
        data = json.load(fp)
"""

with open('products.json', 'r') as fp:
    prods = json.load(fp)

for card in prods['vga']['RX 580 8GB']:
    print(prods['vga']['RX 580 8GB'][card]['price'])
    time = datetime.fromtimestamp(prods['vga']['RX 580 8GB'][card]['time'])
    print(time)



