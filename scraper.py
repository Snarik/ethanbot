#!/usr/bin/env python
""" File to get all tweets of a given user
relies on : 
 https://api.twitter.com/1.1/statuses/user_timeline.json
end point

"""
import os
import logging
import time

from TwitterAPI import TwitterAPI

# USER = "eperlste"
USER = "NinaDiPrimio"
API_ENDPOINT = "statuses/user_timeline"

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

	def get_user_corpus(self, user):
		last_tweet_id = None
		tweet_texts = []
		window_length = "200"

		while True:
			context = {'screen_name': user,
					   'max_id' : last_tweet_id,
					   'count': window_length}

			response = self.api.request(API_ENDPOINT, context)

			if response.status_code != 200:
				raise Exception("Problem curling. {status_code} code returned".format(status_code=response.status_code))

			if last_tweet_id == response.json()[-1]['id']:
				break

			tweets = response.json()
			last_tweet_id = tweets[-1]['id']

			for tweet in tweets:
				tweet_texts.append(tweet['text'])

			time.sleep(0.1)

		return tweet_texts

	def write_corpus_to_file(self, corpus):
		with open("%s.corpus" % USER, 'w') as f:
			for tweet in corpus:
				f.write(tweet.encode('utf-8') + "\n")

	def _run(self):
		tweets = self.get_user_corpus(USER)
		write_corpus_to_file(tweets)


if __name__ == "__main__":
	scraper = Scraper()

	nina = scraper.get_user_corpus()