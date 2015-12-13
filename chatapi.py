# -*- coding: utf-8 -*-

import codecs, sys
import requests as req
from requests.auth import HTTPBasicAuth
import re, pprint
import keys 

# オブジェクトダンプ日本語対応版
def pp(obj):
	pp = pprint.PrettyPrinter(indent=4, width=160)
	str = pp.pformat(obj)
	return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str)

req.packages.urllib3.disable_warnings()
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

class ChatbotAPI:
	def __init__(self):
		#self.botName = "js_tsubot01"
		self.botName = "js_devbot01"
		self.apiBase = "https://52.68.75.108"
		self.authData= HTTPBasicAuth(keys.apiUser, keys.apiPass)

	def __postRequest(self, endp, data, key = None, isPost = False):
		url = self.apiBase + endp
		if isPost:	
			rawRes = req.post(url, params=data, verify=False, auth=self.authData)
		else:
			rawRes = req.get(url, params=data, verify=False, auth=self.authData)
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
		return self.__postRequest("/tweet/get_reply", {'bot_name':self.botName})

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
		return self.__postRequest("/tweet/simple", {'bot_name':self.botName, 'message':text}, None, True)

	def postReply(self, text, mentionID, userName):
		return self.__postRequest('/tweet/send_reply', {
			'bot_name':self.botName,
			'replies':[{
				'mention_id': mentionID,
				'user_name': userName,
				'message': text,
			}]
		}, None, True)

	def convMorphsToStr(self, morphs):
		s = '';
		for i in range(1, len(morphs) - 1):
			t = morphs[i].split(':')
			t.pop()
			s += ':'.join(t)
		return s
