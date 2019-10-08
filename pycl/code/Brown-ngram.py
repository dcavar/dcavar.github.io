#!/usr/bin/env python

"""
Brown-ngram.py
(C) 2005 by Damir Cavar

This code is free; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This is an implementation of a simple ngram generator for the Brown corpus format.

Each token is structured as follows:
word + "/" + part of speech
"""


import sys, glob, os.path, string
from ngram import Ngrams


def makeNgrams(ngrams, filename):
	try:
		file = open(filename)
		tokens = file.read().split()
		file.close()
	except IOError:
		print "Cannot read from file", filename
	for i in tokens:
		i = i.split("/")
		if i[0][0] not in string.punctuation:
			i[0] = i[0].lower()
			ngrams.addNgram( tuple(i) )
	return ngrams


if __name__ == "__main__":
	myNgrams = Ngrams(2)
	if len(sys.argv) > 1:
		for x in sys.argv[1:]:
			for y in glob.glob(os.path.normcase(x)):
				print "Loading file:", y
				myNgrams = makeNgrams(myNgrams, y)
		for x in myNgrams.frequencyProfile(False):
			print x
	else:
		print "Usage:"
		print "python Brown-ngram.py filename[s]"
