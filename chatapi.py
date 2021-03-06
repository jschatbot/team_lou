# -*- coding: utf-8 -*-

import codecs, sys
import requests as req
from requests.auth import HTTPBasicAuth
import re, pprint
import keys
from twapi import *

# https://github.com/bear/python-twitter

# オブジェクトダンプ日本語対応版
def pp(obj):
	pp = pprint.PrettyPrinter(indent=4, width=160)
	str = pp.pformat(obj)
	return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str)

req.packages.urllib3.disable_warnings()
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

class ChatbotAPI:
	grade = 0
	def __init__(self):
		if len(sys.argv) > 1:
			# local
			self.apiBase = "https://52.68.75.108"
			self.authData= HTTPBasicAuth(keys.apiUser, keys.apiPass)
                        self.isLocal = True
		else:
			# teamserver
			self.apiBase = "http://10.243.251.70"
			self.authData = None
                        self.isLocal = False
		self.botName = "js_tsubot01"
		#self.botName = "js_devbot01"
		
		self.getReply()

	def __postRequest(self, endp, data, key = None, isPost = False):
		url = self.apiBase + endp
		headers = {'Content-type': 'application/json'}
		if isPost:	
			rawRes = req.post(url, params=data, verify=False, auth=self.authData, headers=headers)
		else:
			rawRes = req.get(url, params=data, verify=False, auth=self.authData, headers=headers)
		if rawRes.status_code / 10 != 20:
			print url
			print "Error: status code " + str(rawRes.status_code)
			return False
		try:
			res = rawRes.json()
		except:
			print(rawRes.text)
			print "Send data:"
			print pp(data)
			return False
		if key is None:
			return res
		elif key in res:
			return res[key]
		else:	
			print "Send data:"
			print pp(data)
			return False

	def getSentence(self, str):
		return self.__postRequest("/jmat/sentence", {'query':str}, "sentences")

	def getMorphs(self, str):
		return self.__postRequest("/jmat/morph", {'query':str}, "morphs")

	def getChunks(self, str):
		return self.__postRequest("/jmat/chunk", {'query':str}, "chunks")

	def getSynonym(self, str):
		return self.__postRequest("/jmat/synonym", {'query':str}, "groups")

	def getReply(self):
		retv = self.__postRequest("/tweet/get_reply", {'bot_name':self.botName})
                print pp(retv)
		if "grade" in retv:
		    self.grade = retv["grade"]
		return retv

	def searchTweet(self, str, limit=10):
		return self.__postRequest("/search/tweet", {'query':str, 'limit':limit})

	def searchReply(self, str, limit=10):
		return self.__postRequest("/search/reply", {'query':str, 'limit':limit})

	def generateMarkov(self, surface="BOS", pos="BOS"):
		return self.__postRequest("/tk/markov", {'surface':surface, 'pos':pos}, 'morphs')

	def rewrite(self, rulename="lou_rw_01", morphs=[]):
		return self.__postRequest("/tk/rewrite", {'rule':rulename, 'morphs':morphs})

	def generateScenario(self, rulename="lou_sc_01", morphs=[]):
		return self.__postRequest("/tk/trigger", {'rule':rulename, 'morphs':morphs})

	def postTweet(self, text):
		twApi.update_status(text)
		print "Tweeted: " + text

	def postReply(self, text, mentionID, userName):
		text = '@' + userName + " " + text
		twApi.update_status(status = text, in_reply_to_status_id = mentionID)
		print "Replied: " + text

	def convMorphsToStr(self, morphs):
		s = '';
		for i in range(1, len(morphs) - 1):
			t = morphs[i].split(':')
			t.pop()
			s += ':'.join(t)
		return s

	def getMyInfo(self):
		return twApi.me()
