# -*- coding: utf-8 -*-

import chatapi
import random

capi = chatapi.ChatbotAPI()

quizfilename = "Quiz/quiz{}.txt"

# read quiz file
# "question - answerword"
def readQuizFile(state):
    quizlist = []
    with open(quizfilename.format(state),"r") as quizfile:
        for quiz in quizfile:
            quiz = quiz.decode("utf-8").rstrip()
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
    tweet = skeleton.format(answerword)
    if is_collect:
        tweet += u"コングラッチュレーショーン！！"
    else:
        tweet += u"まだまだだねボーイ！！"
    return tweet

def generateMistakeMessage():
    tweet = u"オーマイガー！考えなおすんだ！" # 辞書を作る？
    return tweet

# 正解単語が入っていればOK
def is_collect(answer,mension):
    if answer in mension:
        return True
    return False

def is_quiz(text,userName):
    keywords = [u"クイズ", u"なぞなぞ", u"問題"]
    for keyword in keywords:
        if keyword in text:
            return True
    if userName in quizUsers:
        return True
    return False

# quiz main function
# state - state number 0~2
# number - the question number
# mension - user mension text
def genQuizMessage(number=-1,mension=""):
    tweet = u""
    state += 1 # need???
    if number == -1:
        number, tweet = readQuestion(state)
    else:
        answer = readAnswer(capi.grade,number)
        if is_surrender(mension): # 降参された場合
            tweet = generateAnswerMessage(answer,False)
        if is_collect(answer,mension): # 正解がmension中にあればOK
            tweet = generateAnswerMessage(answer)
        else:
            tweet = generateMistakeMessage()
#    print tweet
    return tweet

def quiz():

    return genQuizMessage()

#genQuizMessage(1,)
#genQuizMessage(2,2,u"答えは三角")
#genQuizMessage(2,3,u"答えはパンジー")
