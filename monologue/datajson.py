#coding:UTF-8
import json
import time
import random
import sys

file = "data.json"
f = open(file)
data = json.load(f)
f.close()

nowtime = str(time.localtime().tm_sec)

#この一文をデプロイ前に消すこと
nowtime = "15"

if nowtime not in data["begin"]:
    sys.exit()

tweet = random.choice(data["begin"][nowtime])

if nowtime in data["end"]:
    tweet += random.choice(data["end"][nowtime])

memo = ""
while memo != tweet:
    memo = tweet 
    for i in data["mark"]:
        mk = i
        word = [m for m in data["mark"][i]]
        tweet = tweet.replace(mk, random.choice(word))

print tweet 

