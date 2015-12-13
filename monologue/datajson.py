#coding:UTF-8
import json
import time
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../')
from chatapi import *

nowtime = str(time.localtime().tm_hour)

API = ChatbotAPI()

file = os.path.dirname(os.path.abspath(__file__))+"/grade"+str(API.grade)+".json"
f = open(file)
data = json.load(f)
f.close()

if nowtime not in data["time"]:
    sys.exit()

tweet = random.choice(data["time"][nowtime])

memo = ""
while memo != tweet:
    memo = tweet 
    for i in data["mark"]:
        mk = i
        word = [m for m in data["mark"][i]]
        tweet = tweet.replace(mk, random.choice(word))

#print tweet
API.postTweet(tweet)

