import json
import random
import string
"""
    SAVE:
    with open('data.json', 'w') as fp:
        json.dump(data, fp)
    LOAD:
    with open('data.json', 'r') as fp:
        data = json.load(fp)
"""
def getRandomString():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])


name = "Oi tudo bem como vai voce"
words = ["Oi", "Bem", "Voce"]

if(all(word.lower() in name.lower() for word in words)):
    print("Sim")
else:
    print("Não")
