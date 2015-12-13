# -*- coding: utf-8 -*-

from chatapi import *
import threading
import shelve

class Chatbot:
	tickInterval = 1.0;
	def __init__(self):
		self.capi = ChatbotAPI()
		self.grade = 0
		self.localDB = shelve.open('./louDB', writeback=True)
		if not ("lastMentionID" in self.localDB) :
			self.localDB["lastMentionID"] = 0;
		print "lastMentionID:" + str(self.localDB["lastMentionID"])
		self.timer = threading.Timer(self.tickInterval, self.tick);
		self.timer.start()
	
	def dbSave(self):
		self.localDB.close()
		self.localDB = shelve.open('./louDB', writeback=True)

	def tick(self):
		res = self.capi.getReply()
		if res :
			self.grade = res["grade"];
			p = 0
			if "replies" in res :
				r = res["replies"]
				for i in range(len(r)) :
					if r[i]["mention_id"] == self.localDB["lastMentionID"] :
						p = i + 1
						break
				for i in range(p, len(r)) :
					self.receiveMention(r[i]["text"], r[i]["mention_id"], r[i]["user_name"])
					self.localDB["lastMentionID"] = r[i]["mention_id"];
				self.dbSave()
		#print pp(res);
		#
		self.timer = threading.Timer(self.tickInterval, self.tick);
		self.timer.start()

	def receiveMention(self, text, mentionID, userName):
		print "**** Receive new"
		print text
		print mentionID
		print userName
		self.capi.postTweet(self.capi.convMorphsToStr(self.capi.generateMarkov()))
		

loubot = Chatbot()

