# -*- coding: utf-8 -*-

from chatapi import *
import threading
import shelve
from twapi import *
import gen_reply
import quiz

class Chatbot:
	tickInterval = 1.0;
	def __init__(self):
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
				sp = line.rstrip('\n').split(',')
				self.louDict[sp[0]] = sp[4]
		#
                self.readDict()
		self.timer = threading.Timer(self.tickInterval, self.tick);
		self.timer.start()

	def dbSave(self):
		self.localDB.close()
		self.localDB = shelve.open('./louDB', writeback=True)

	def tick(self):
		self.timer = threading.Timer(self.tickInterval, self.tick);
		self.timer.start()

	def convToLouLang(self, str):
		morphs = self.capi.getMorphs(str);
		text = ""
		for i in range(1, len(morphs) - 1):
			if morphs[i]["surface"] in self.louDict:
                                # 段階にあわせてルー語割合を変える
                                if random.randrange(1,3) >= self.capi.grade:
				        text += self.louDict[morphs[i]["surface"]]
			else:
				text += morphs[i]["surface"]
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

		if text in self.greetings: # テンプレート返答
			self.capi.postReply(self.greetings[text], mentionID, userName)
		elif quiz.is_quiz(text,userName): # quiz中/開始中
			self.capi.postReply(quiz.quiz(text,userName), mensionID, userName)
		else: # 返答生成
			self.capi.postReply(self.convToLouLang(gen_reply.generateReply(text)), mentionID, userName)

if __name__ == '__main__':
	loubot = Chatbot()
	auth = get_oauth()
	stream = tweepy.Stream(auth,StreamListener(loubot))
	while True :
		# ストリーミング再接続用ループ
		try:
			stream.userstream()
		except myExeption() :
			time.sleep(60)
			stream = tweepy.Stream(auth,StreamListener())
