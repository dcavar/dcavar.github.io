#! /usr/bin/env python
# -*- coding: utf8 -*-

"""
MIRE.py

(C) 2005 by Damir Cavar <dcavar@indiana.edu>

License:

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""


import sys, string, glob, os.path, math, codecs
from stattools import sortNgrams, puncTrim, getWordList, getTokens, getBigrams, rF


def RE(bigramprob, token2p, token1p):
	"""Returns the Relative Entropy.
		Relative entropy is P1*log2(P1/P2) where here P1 is P(rightword)
		and P2 is P(right word | left word)."""
	return token1p * math.log(token1p/(bigramprob/token2p), 2)


def MI(bigram, bigramprob, tokens, tokencount):
	"""Returns the mutual information for bigrams.
		MI = P(XY|X) log2 ( P(XY) / P(X) P(Y) )
		P(XY|X) = num of bigrams XY over num bigrams with X left
	"""
	if tokens.has_key(bigram[0]):
		px = float(tokens[bigram[0]])/float(tokencount)
	else:
		px = 0.0
	if tokens.has_key(bigram[1]):
		py = float(tokens[bigram[1]])/float(tokencount)
	else:
		py = 0.0
	if py == 0.0 or px == 0.0:
		return 0.0
	return bigramprob * math.log(bigramprob/(px * py) , 2)


if __name__ == "__main__":
	bigrams     = {}	# bigram as key, frequency as value
	tokens      = {}	# token as key, frequency as value
	tokencount  = 0   # number of tokens
	bigramcount = 0   # number of bigrams

	for i in sys.argv[1:]:
		for x in glob.glob(os.path.normcase(i)):
			try:
				file = open(x, "r")
				for i in file.readlines():
					i = string.lower(string.strip(i))
					if i == "":
						continue
					wordlist = getWordList(i)
					bigrams, bigramcount = getBigrams(wordlist, bigrams, bigramcount)
					tokens, tokencount = getTokens(wordlist, tokens, tokencount)
				file.close()
			except IOError:
				file.close()

	print "Got total:\nBigrams: " + str(bigramcount) + "\nTokens: " + str(tokencount)
	print "Bigram\tFrequency\tRelative Frequency\tMutual Information\tRelative Entropy"
	for i in sortNgrams(bigrams):
		rf   = float(i[1])/float(bigramcount)
		print "%s\t%d\t%f\t%f\t%f" % (" ".join(i[0]), i[1], rf, \
		MI(i[0], rf, tokens, tokencount), \
		RE(rf, rF(tokens[i[0][0]], tokencount), rF(tokens[i[0][1]], tokencount)))
