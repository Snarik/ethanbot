#!/usr/bin/env python
""" File to get all tweets of a given user
relies on : 
 https://api.twitter.com/1.1/statuses/user_timeline.json
end point

"""
import os

import twitterapi

USER = "eperlste"

class Scraper(object):

	def __init__(self):
	try:
		self.api_key = os.environ['TWITTER_API_KEY']
		self.api_secret = os.environ['TWITTER_API_SECRET']
	except KeyError: 
		Exception("You need to have the TWITTER_API_KEY and TWITTER_API_SECRET set in your environment")

	def get_user_corpus(user):




if __name__ == "__main__":
	scraper = Scraper()
