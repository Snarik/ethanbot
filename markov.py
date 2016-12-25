#!/usr/bin/env python
import markovify

USER = "eperlste"
with open("%s.corpus" % USER) as f:
	text = f.read()
model = markovify.NewlineText(text)

if __name__ == "__main__":
