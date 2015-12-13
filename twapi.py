# -*- coding: utf-8 -*-
import sys
import tweepy
from tweepy.auth import OAuthHandler
from tweepy.api import API
import keys

class myExeption(Exception): pass

class StreamListener(tweepy.streaming.StreamListener):
	def __init__(self, bot):
		super(StreamListener,self).__init__()
		self.bot = bot

	def __del__(self):
		return

	def on_status(self,status):
		self.bot.receiveMention(status.text, status.id, status.author.name)
		return True

	def on_error(self,status):
		print "Twitter Streaming error"

	def on_timeout(self):
		raise myExeption

def get_oauth():
	consumer_key = keys.twKeys['consumer_key'].encode('utf-8')
	consumer_secret = keys.twKeys['consumer_secret'].encode('utf-8')
	access_key = keys.twKeys['access_token'].encode('utf-8')
	access_secret = keys.twKeys['access_secret'].encode('utf-8')
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	return auth

twApi = tweepy.API(get_oauth());

