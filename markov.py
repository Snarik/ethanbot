#!/usr/bin/env python
import sys 

import markovify

from scraper import Scraper

NUM_TRIAL_RUNS = 100
MAX_PROBABLE_KMER = 10
STATE_SIZE_THRESHOLD = 0.05

TWEET_LENGTH = 140

class TweetModel(object):
	"""A tweet model can be a model generated based on one or multiple
	   twitter corpus sources
	   Twitter Model can be initialized by passing in one or more users to build on
	"""
	def __init__(self, users):
		self.users = users

		if len(self.users)>1:
			self.mashup = True
		else:
			self.mashup = False
		self.corpora = self._get_all_corpora(self.users)

	def build_model(self, text):
		for i in range(1, MAX_PROBABLE_KMER):
			model = markovify.NewlineText(text, state_size=i)
			if self.test_model(model):
				break
		return model

	def test_model(self, model):
		"""Test if most of the model's outputs are None.
		   This maximizes the model's human soundingness
		"""
		# this is a poor metric for human readability
		# decent attempt but not great. Put more thought into this feature. 
		trials = []
		for i in range(NUM_TRIAL_RUNS):
			trials.append(model.make_short_sentence(TWEET_LENGTH))

		none_count = 0.0
		for trial in trials:
			if not trial:
				none_count += 1
		if STATE_SIZE_THRESHOLD < none_count / len(trials) < 1.0:
			return True

	def _get_all_corpora(self, users):
		"""Takes users list, returns dict of user : corpus"""
		scraper = Scraper(in_memory=True)
		corpora = {}
		for user in users:
			text = "\n".join(scraper.get_user_corpus(user))
			corpora[user] = text

		return corpora

	def run(self):

		if not self.mashup:
			model = self.build_model(self.corpora[self.users[0]])
		else:
			models = []
			for user in self.users:
				models.append(self.build_model(self.corpora[user]))
			combo = makovify.combine(models)
		print "Examples:"
		print "===================="
		for i in range(5):
			print "%s) %s" % (i,  model.make_short_sentence(140))


if __name__ == "__main__":

	q = TweetModel(sys.argv[1:])

	q.run()



