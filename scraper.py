#!/usr/bin/env python
""" 
Get last 3200 tweets for a given user or users.

"""
import os
import logging
import time

from TwitterAPI import TwitterAPI

# parameters
USER = "NinaDiPrimio"
TWEET_WINDOW_LENGTH = "200"

# endpoints 
STATUS_ENDPOINT = "statuses/user_timeline"
USER_ENDPOINT = "users/lookup"

class Scraper(object):

	def __init__(self):
		try:
			client_key = os.environ['TWITTER_API_KEY']
			client_secret = os.environ['TWITTER_API_SECRET']
			auth_token = os.environ['TWITTER_ACCESS_TOKEN']
			auth_secret = os.environ['TWITTER_TOKEN_SECRET']
		except KeyError: 
			raise Exception("You need to have the TWITTER_API_KEY and TWITTER_API_SECRET set in your environment")
		self.api = TwitterAPI(client_key, client_secret, auth_token, auth_secret)
	
	def get_user_status_count(self, user):
		response = self.api.request(USER_ENDPOINT, {'screen_name': user})

		if response.status_code != 200:
			raise Exception()

	def get_user_corpus(self, user):
		last_tweet_id = None
		tweet_texts = []
		total_count = self.get_user_status_count(user)

		while True:
			context = {'screen_name': user,
					   'max_id' : last_tweet_id,
					   'count': TWEET_WINDOW_LENGTH}

			response = self.api.request(STATUS_ENDPOINT, context)

			if response.status_code != 200:
				raise Exception("Problem curling. {status_code} code returned".format(status_code=response.status_code))

			if last_tweet_id == response.json()[-1]['id']:
				break

			tweets = response.json()
			last_tweet_id = tweets[-1]['id']

			for tweet in tweets:
				tweet_texts.append(tweet['text'])
		
		self.write_corpus_to_file(tweet_texts)


	def write_corpus_to_file(self, corpus):
		with open("%s.corpus" % USER, 'w') as f:
			for tweet in corpus:
				f.write(tweet.encode('utf-8') + "\n")

	def _run(self, user):
		self.get_user_corpus(user)


if __name__ == "__main__":
	scraper = Scraper()
	scraper._run(USER)

