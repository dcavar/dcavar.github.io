#!/usr/bin/env python

"""
VectorSpace.py
(C) 2005 by Damir Cavar

This code is free; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This is an implementation of a simple vector space generator for documents and
words in documents.

The columns are words and their relative frequency. The rows are documents.
The program only keeps track of which word appears in which document
how many times. The vectors contain relative frequencies for each word
occurance. The sum over all numbers in a vector is 1.
"""

import sys, re, glob, os.path, string

documents  = {}
words      = {}
wordlist   = []
docnames   = []
eliminated = []


functionWordsEN = ["a", "abroad", "about", "above", "across", "after", "again",
	"against", "ago", "ahead", "all", "almost", "alongside", "already",
	"also", "although", "always", "am", "amid", "amidst", "among", "amongst",
	"an", "and", "another", "any", "anybody", "anyone", "anything", "anywhere",
	"apart", "are", "aren't", "around", "as", "aside", "at", "away", "back",
	"backward", "backwards", "be", "because", "been", "before", "beforehand",
	"behind", "being", "below", "between", "beyond", "both", "but", "by",
	"can", "can't", "cannot", "could", "couldn't", "dare", "daren't", "despite",
	"did", "didn't", "directly", "do", "does", "doesn't", "doing", "don't",
	"done", "down", "during", "each", "either", "else", "elsewhere", "enough",
	"even", "ever", "evermore", "every", "everybody", "everyone", "everything",
	"everywhere", "except", "fairly", "farther", "few", "fewer", "for",
	"forever", "forward", "from", "further", "furthermore", "had", "hadn't",
	"half", "hardly", "has", "hasn't", "i", "have", "haven't", "having", "he",
	"hence", "her", "here", "hers", "herself", "him", "himself", "his", "how",
	"however", "if", "in", "indeed", "inner", "inside", "instead", "into",
	"is", "isn't", "it", "its", "itself", "just", "keep", "kept", "later",
	"least", "less", "lest", "like", "likewise", "little", "low", "lower",
	"many", "may", "mayn't", "me", "might", "mightn't", "mine", "minus",
	"moreover", "most", "much", "must", "mustn't", "my", "myself", "near",
	"need", "needn't", "neither", "never", "nevertheless", "next", "no",
	"no-one", "nobody", "none", "nor", "not", "nothing", "notwithstanding",
	"now", "nowhere", "of", "off", "often", "on", "once", "one", "ones",
	"only", "onto", "opposite", "or", "other", "others", "otherwise", "ought",
	"oughtn't", "our", "ours", "ourselves", "out", "outside", "over", "own",
	"past", "per", "perhaps", "please", "plus", "provided", "quite", "rather",
	"really", "round", "same", "self", "selves", "several", "shall", "shan't",
	"she", "should", "shouldn't", "since", "so", "some", "somebody", "someday",
	"someone", "something", "sometimes", "somewhat", "still", "such", "that",
	"than", "the", "their", "theirs", "them", "themselves", "then", "there",
	"therefore", "these", "they", "thing", "things", "this", "those", "though",
	"through", "throughout", "thus", "till", "to", "together", "too", "towards",
	"under", "underneath", "undoing", "unless", "unlike", "until", "up", "upon",
	"upwards", "us", "versus", "very", "via", "was", "wasn't", "way", "we",
	"well", "were", "weren't", "what", "whatever", "when", "whence", "whenever",
	"where", "whereby", "wherein", "wherever", "whether", "which", "whichever",
	"while", "whilst", "whither", "who", "whoever", "whom", "whose", "why",
	"will", "with", "within", "without", "won't", "would", "wouldn't", "yet",
	"you", "your", "yours", "yourself", "yourselves", "thou", "thee", "thy" ]



def makeVectorSpace():
	"""Generate the vector space from dictionary data."""
	global words, wordlist, documents, docnames, eliminated

	wordlist = words.keys()
	docnames = documents.keys()

	# eliminate words that appear in all documents
	for x in wordlist:
		if len(words.get(x, [])) == len(docnames):
			eliminated.append(x)
			del words[x]
	wordlist = words.keys()

	# create vectors
	vectorspace = []
	for x in docnames:
		vector = len(wordlist) * [ 0 ]
		for i in range(len(wordlist)):
			vector[i] = documents[x].get(wordlist[i], 0)

		# append vector with relative frequencies
		#i = float(vsum(vector))
		#vectorspace.append(tuple([ float(a)/i for a in vector ]))
		vectorspace.append(tuple(vector))

	# convert vectorspace to tuple
	return tuple(vectorspace)


def vsum(seq):
	"""Sum over all elements in a list."""
	def add(x,y): return x+y
	return reduce(add, seq, 0)


def collectWords(document):
	"""Collect all words from document into dictionary data structures."""
	global documents, words
	file   = open(document)
	tokens = [string.lower(i) for i in re.findall(r"[A-Za-z]+'?[A-Za-z]?", file.read())]
	file.close()

	# get wordlist
	wordlist = {}
	for i in tokens:
		if i not in functionWordsEN:
			wordlist[i] = wordlist.get(i, 0) + 1
			value       = words.get(i, [])
			if document not in value:
				value.append(document)
				words[i] = value

	# store document specific dictionary
	documents[document] = wordlist



if __name__ == "__main__":
	if len(sys.argv) > 1:
		for x in sys.argv[1:]:
			for y in glob.glob(os.path.normcase(x)):
				print "Loading file:", y
				collectWords(y)
		vectorspace = makeVectorSpace()
		documents = {}  # clean up memory
		for x in range(len(vectorspace)):
			print docnames[x], vectorspace[x]
	else:
		print "Usage:"
		print "python VectorSpace.py filename[s]"
