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

#"0"をデプロイ前にstr(time.localtime().tm_hour)に変えること
tweetbegin = [m for m in data["begin"]["0"]]
tweet = random.choice(tweetbegin)

#if str(time.localtime().tm_hour) in data["end"]:
#    str += data["end"][str(time.localtime().tm_hour)]

#"0"をデプロイ前にstr(time.localtime().tm_hour)に変えること
if "0" in data["end"]:
    tweetebd = [m for m in data["end"]["0"]]
    tweet += random.choice(data["end"]["0"])
    #tweet += data["end"]["0"]

memo = ""
while memo != tweet:
    memo = tweet 
    for i in data["mark"]:
        mk = i
        word = [m for m in data["mark"][i]]
        tweet = tweet.replace(mk, random.choice(word))

print tweet 

