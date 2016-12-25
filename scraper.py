#!/usr/bin/env python
""" 
Get last 3200 tweets for a given user or users.

"""
from HTMLParser import HTMLParser
import os
import re
import time

from TwitterAPI import TwitterAPI

# parameters
USER = "NinaDiPrimio"
# USER="eperlste"
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
		self.html_parser = HTMLParser()

	def print_user_status(self, user):
		"""Return total user tweet count""" 
		response = self.api.request(USER_ENDPOINT, {"screen_name": user})
		if response.status_code != 200:
			raise Exception("something went wrong getting user stats")
		user_tweet_count = int(response.json()[0]['statuses_count'])

		print "Found {count} tweets for user {user}.".format(count=user_tweet_count,user=user)
		if user_tweet_count > 3200:
			print "Downloading 3200 most recent tweets."
		else:
			print "Downloading now. Please wait."



		return 

	def tweet_cleaner(self, tweet):
		"""Clean up tweets a little, remove urls, html, etc""" 
		removed_html_tweet = self.html_parser.unescape(tweet)
		cleaned_text = re.sub(r"http\S+", "", removed_html_tweet) 

		return cleaned_text.encode('utf-8')

	def get_user_corpus(self, user):
		last_tweet_id = None
		tweet_texts = []
		user_tweet_count = self.print_user_status(user)
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
				cleaned_tweet = self.tweet_cleaner(tweet['text'])
				tweet_texts.append(cleaned_tweet)
		
		self.write_corpus_to_file(tweet_texts, user)


	def write_corpus_to_file(self, corpus, user):
		with open("%s.corpus" % user, 'w') as f:
			for tweet in corpus:
				f.write(tweet + "\n")

	def _run(self, user):
		self.get_user_corpus(user)

if __name__ == "__main__":
	import sys

	scraper = Scraper()
	scraper._run(sys.argv[1])

