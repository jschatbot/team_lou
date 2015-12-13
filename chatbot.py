# -*- coding: utf-8 -*-

from chatapi import *
import threading
import shelve
from twapi import *

class Chatbot:
	tickInterval = 1.0;
	def __init__(self):
		if len(sys.argv) > 1:
			self.debugMode = sys.argv[1];
		else:
			self.debugMode = False
		#
		self.capi = ChatbotAPI(self.debugMode)
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
		self.timer = threading.Timer(self.tickInterval, self.tick);
		self.timer.start()
	
	def dbSave(self):
		self.localDB.close()
		self.localDB = shelve.open('./louDB', writeback=True)

	def tick(self):

		self.timer = threading.Timer(self.tickInterval, self.tick);
		self.timer.start()
	
	def convToLouLang(self, chunked):
		for i in range(0, len(chunked)):
			if chunked[i] in lou_dict:
				chunked[i] = lou_dict[chunked[i]],
	
	def receiveMention(self, text, mentionID, userName):
		print "**** Receive new"
		print pp(text)
		print mentionID
		print userName
		self.capi.postReply(self.capi.convMorphsToStr(self.capi.generateMarkov()), mentionID, userName)
		
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
