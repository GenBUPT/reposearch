import json
f = open("Javarepo.json","r")
t = json.load(f)
print(len(t))