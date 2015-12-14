# -*- coding: utf-8 -*-

from chatapi import *
import threading
import shelve
from twapi import *
import gen_reply
import quiz
import re
import random

class Chatbot:
	tickInterval = 60;
	def __init__(self):
		self.aborted = False
		self.capi = ChatbotAPI()
		print "current grade: " + str(self.capi.grade)
		#
		self.localDB = shelve.open('./louDB', writeback=True)
		if not ("lastMentionID" in self.localDB) :
			self.localDB["lastMentionID"] = 0;
		print "lastMentionID:" + str(self.localDB["lastMentionID"])
		#
		self.louDict = {}
		with open("./lou_dict/dic_dif.csv", 'r') as louDictFile:
			for line in louDictFile:
				sp = line.decode('utf-8').rstrip('\n').split(',')
				self.louDict[sp[0]] = sp[4]
		#
                self.readDict()
                self.firstPerson = [ x.decode("utf-8") for x in open("./first_person.txt").readlines() ]
		self.timer = threading.Timer(self.tickInterval, self.tick);
		self.timer.start()

	def dbSave(self):
		self.localDB.close()
		self.localDB = shelve.open('./louDB', writeback=True)

	def tick(self):
		if self.aborted:
			print "Aborted."
			sys.exit(1)

		self.capi.getReply()
		#
		self.timer = threading.Timer(self.tickInterval, self.tick);
		self.timer.start()

	def convToLouLang(self, str):
                print "352"
		morphs = self.capi.getMorphs(str);
		text = u""
                print "264"
		for i in range(1, len(morphs) - 1):
			if morphs[i]["surface"] in self.louDict:
                                # 段階にあわせてルー語割合を変える
                                if random.randrange(1,4) <= self.capi.grade:
                                        text += self.louDict[morphs[i]["surface"]]
			else:
                                if morphs[i]["surface"] != "BOS":
				        text += morphs[i]["surface"]
                print "158"
                # change first person
                for line in self.firstPerson:
                    text = text.replace(line, u"ｍｅ")

		return text

	def convToTsuboLang(self, str):
		print "fhatejj"
		text = str
		text = text.replace(u"!", u"つぼ！")
		print "aaaaaa"
		text = text.replace(u"！", u"つぼ！")
		text = text.replace(u"?", u"つぼ？")
		text = text.replace(u"？", u"つぼ？")
		text = text.replace(u"．", u"つぼ")
		text = text.replace(u"。", u"つぼ")
		text = text.replace(u".", u"つぼ")
		text += u"つぼ"

		print self.firstPerson
		print "456"		

		# change first person
		for line in self.firstPerson:
			text = text.replace(line, u"つぼ")
			
		return text

	def readDict(self):
		self.greetings = {}
		with open("greetings.txt","r") as greetingfile: # self.capi.gradeで読む辞書を分岐 # for つぼ
			for greeting in greetingfile:
				g = greeting.rstrip().split()
				self.greetings[g[0]] = g[1]

	def receiveMention(self, text, mentionID, userName):
		print "**** Receive new"
		print pp(text)
		print mentionID
		print userName

		print "00"
		if text in self.greetings: # テンプレート返答
			print "01"
			self.capi.postReply(self.greetings[text], mentionID, userName)
		elif quiz.is_quiz(text,userName): # quiz中/開始中
			print "02"
			self.capi.postReply(quiz.quiz(text,userName), mentionID, userName)
		else: # 返答生成
			if self.capi.grade == 0:
				print "03"
				ca = gen_reply.generateReply(text)
				print "13"
				cv = self.convToTsuboLang(ca);
				print "09"
				self.capi.postReply(cv, mentionID, userName)
			else:
				print "04"
                                ca = gen_reply.generateReply(text)
                                print "876"
                                cv = self.convToLouLang(ca)
                                print "123"
				self.capi.postReply(cv, mentionID, userName)
		print "05";

if __name__ == '__main__':
	loubot = Chatbot()
	auth = get_oauth()
	stream = tweepy.Stream(auth,StreamListener(loubot))
	while True :
		# ストリーミング再接続用ループ
		try:
			stream.userstream()
		except myExeption() :
			time.sleep(30)
			stream = tweepy.Stream(auth,StreamListener())
