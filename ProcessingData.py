import json


with open("/home/ommirandap/PRISMA/DynamicNewsAnalysis/data/emol.txt", 'r') as datafile:
    for line in datafile:
        tweet = json.loads(line)
        print tweet["text"]
        break
