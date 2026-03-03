import json
out = {}
with open('moves.json', 'r', encoding='utf-8') as f:

    file = json.load(f)
    index = 1
    for move in file["results"]:
        out[index] = move["name"]
        index += 1

print(out)