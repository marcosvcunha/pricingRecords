import json

"""
    SAVE:
    with open('data.json', 'w') as fp:
        json.dump(data, fp)
    LOAD:
    with open('data.json', 'r') as fp:
        data = json.load(fp)
"""

with open('products.json', 'r') as fp:
    data = json.load(fp)

print("Qual produto deseja visualizar?")
prod = input()

for item in data['vga'][prod].values():
    print("Nome: " + item['name'])
    print("Preço a vista: " + str(item['price']) + "  em 12x: " + str(item['price12x']))
    print(item['link'])
    print("\n")

