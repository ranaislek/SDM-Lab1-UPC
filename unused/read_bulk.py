import json
path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data"

#read json
data = None
with open(path + '/bulk1') as f:
    data = json.load(f)

print(data)
