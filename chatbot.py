# -*- coding: utf-8 -*-

import codecs, sys
import requests as req
from requests.auth import HTTPBasicAuth
import re, pprint
import keys 

def pp(obj):
	pp = pprint.PrettyPrinter(indent=4, width=160)
	str = pp.pformat(obj)
	return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str)

req.packages.urllib3.disable_warnings()
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

class ChatbotAPI:
	def __init__(self):
		#self.botName = "js_tsubot01";
		self.botName = "js_devbot01";
		self.apiBase = "https://52.68.75.108";
		self.authData= HTTPBasicAuth(keys.apiUser, keys.apiPass)

	def getSentence(self, str):
		url = self.apiBase + "/jmat/sentence";
		data = {'query':str}
		return (req.get(url, params=data, verify=False, auth=self.authData).json())["sentences"]

	def getMorphs(self, str):
		url = self.apiBase + "/jmat/morph";	
		data = {'query':str}
		return (req.get(url, params=data, verify=False, auth=self.authData).json())["morphs"]

	def getChunks(self, str):	
		url = self.apiBase + "/jmat/chunk";	
		data = {'query':str}
		return (req.get(url, params=data, verify=False, auth=self.authData).json())["chunks"]

	def getSynonym(self, str):
		url = self.apiBase + "/jmat/synonym";	
		data = {'query':str}
		return (req.get(url, params=data, verify=False, auth=self.authData).json())["groups"]

	def getReply(self):
		url = self.apiBase + "/tweet/get_reply";	
		data = {'bot_name':self.botName}
		rawRes = req.get(url, params=data, verify=False, auth=self.authData);
		try:
			res = rawRes.json();
		except:
			print(rawRes.text);
			return False;
		if "replies" in res:
			return res;
		else:
			pp(res);
			return False;

capi = ChatbotAPI()

res = capi.getReply();
print pp(res);
print keys.a


