#coding:UTF-8
import json
import time
import random
import sys

file = "data.json"
f = open(file)
data = json.load(f)
f.close()

#if str(time.localtime().tm_sec) not in data["begin"]:
#    sys.exit()

# デプロイ前にsecをhourに変えること
#str = data["begin"][str(time.localtime().tm_sec)]

#とりあえず"0"でテスト
tweet = data["begin"]["0"]

#if str(time.localtime().tm_hour) in data["end"]:
#    str += data["end"][str(time.localtime().tm_hour)]

if "0" in data["end"]:
    tweet += data["end"]["0"]

memo = ""
while memo != tweet:
    memo = tweet 
    for i in data["mark"]:
        mk = i
        word = [m for m in data["mark"][i]]
        tweet = tweet.replace(mk, random.choice(word))

print tweet 

