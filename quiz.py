# -*- coding: utf-8 -*-

import chatapi
import random

capi = chatapi.ChatbotAPI()

quizfilename = "Quiz/quiz{}.txt"
quizUsers = {} # quiz active user - problem number

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

def is_surrender(mention):
    keywords = [u"まいった",u"降参",u"もういい",u"疲れた",u"終わり",u"分から",u"ダメ"]
    for keyword in keywords:
        if keyword in mention:
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
def is_collect(answer,mention):
    if answer in mention:
        return True
    return False

def is_quiz(text,userName):
    keywords = [u"クイズ", u"なぞなぞ", u"問題", u"ゲーム"]
    for keyword in keywords:
        if keyword in text:
            return True
    if userName in quizUsers.keys():
        return True
    return False

# quiz main function
# state - state number 0~2
# number - the question number
# mention - user mention text
def genQuizMessage(userName,number=-1,mention=""):
    tweet = u""
    if number == -1:
        number, tweet = readQuestion(capi.grade)
        global quizUsers
        quizUsers[userName] = number
    else:
        answer = readAnswer(capi.grade,number)
        if is_surrender(mention): # 降参された場合
            tweet = generateAnswerMessage(answer,False)
            del quizUsers[userName]
        elif is_collect(answer,mention): # 正解がmention中にあればOK
            tweet = generateAnswerMessage(answer)
            del quizUsers[userName]
        else:
            tweet = generateMistakeMessage()
    print tweet
    return tweet

def quiz(text,userName):
    print text,userName,quizUsers
    if userName in quizUsers: # プレイ中
        return genQuizMessage(userName,quizUsers[userName],text)
    else: # これからプレイ
        return genQuizMessage(userName)

# quiz(u"クイズしようよ","test1")
# quiz(u"問題出してよ","test2")
# quiz(u"それはどうなの","test1")
# quiz(u"降参","test1")
# quiz(u"問題出してよ","test2")
