import json
from utils import readJson
"""
    SAVE:
    with open('data.json', 'w') as fp:
        json.dump(data, fp)
    LOAD:
    with open('data.json', 'r') as fp:
        data = json.load(fp)
"""
def searchEngine(words):
    classifiers = readJson("classifier.json")
    return words


def main():
    endProgram = False
    while not endProgram:
        print("O que deseja fazer?")
        print("search KEY_WORD1 KEY_WORD2 ..., get ITEM_NAME price, finish")
        cmd = input().split(" ")
        if(cmd[0].lower() == "finish"):
            endProgram = True 
        elif(cmd[0].lower() == "search"):
            matches = searchEngine(cmd[1:])
            print(matches)


if __name__ == '__main__':
    main()