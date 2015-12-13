# -*- coding: utf-8 -*-

import chatapi
import random

capi = chatapi.ChatbotAPI()

quizfilename = "Quiz/quiz{}.txt"

# read quiz file
# "question - answerword"
def readQuizFile(state):
    quizlist = []
    with open(quizfilename.format(state)) as quizfile:
        for quiz in quizfile:
            quizlist.append(quiz.split(" "))
    return quizlist

def readQuestion(state):
    quizlist = readQuizFile(state)
    number = random.randrange(len(quizlist))
    return number, quizlist[number][0]

def readAnswer(state,number):
    quizlist = readQuizFile(state)
    return quizlist[number][1]

def is_surrender(mension):
    keywords = [u"まいった",u"降参",u"もういい",u"疲れた",u"終わり",u"分から",u"ダメ"]
    for keyword in keywords:
        if keyword in mension:
            return True
    return False

def generateAnswerMessage(answerword,is_collect=True):
    skeleton = u"アンサーは {} でした！" # 辞書を作る？
    tweet = skeleton.format(answord)
    if is_collect:
        tweet += u"コングラッチュレーショーン！！"
    else:
        tweet += u"まだまだだねボーイ！！"
    return tweet

# quiz main function
# state - state number 0~2
# number - the question number
# mension - user mension text
def quiz(state,number=-1,mension=""):
    tweet = u""
    print tweet
    state += 1 # need???
    if number == -1:
        number, tweet = readQuestion(state)
    else:
        answer = readAnswer(state,number)
        if is_surrender(mension): # 降参された場合
            tweet = generateAnswerMessage(answer,False)
        if answer in mension: # 正解がmension中にあればOK
            tweet = generateAnswerMessage(answer)
    print tweet
    return tweet

quiz(1,)
quiz(2,2,"答えは三角")
quiz(2,2,"答えは三角")
