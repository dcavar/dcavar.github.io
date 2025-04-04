#! /usr/bin/env python
# -*- coding: utf8 -*-

"""
freq5.py
(C) 2005 by Damir Cavar <dcavar@indiana.edu>
GNU General Public License

Functionality: Counting words
"""

import sys, os.path, glob, string, codecs, re
from operator import itemgetter

countername = u"__count__"

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


def countWords(words, filename):
	"""Counts words in file and returns dictionary."""
	count = words.get(countername, 0)
	try:
		file = codecs.open(filename, "r", "utf8")
		tokens = [string.lower(i) for i in re.findall(ur"[A-Za-zčČćĆšŠžŽđĐ]+'?[A-Za-zčČćĆšŠžŽđĐ]?",file.read())]
		for i in tokens:
			if i not in functionWordsEN:
				words[i] = words.get(i, 0) + 1
				count += 1
		file.close()
	except IOError:
		print "Cannot read from file:", filename
	words[countername] = count
	return words


if __name__ == "__main__":
	words = {}
	for x in sys.argv[1:]:
		for y in glob.glob(os.path.normcase(x)):
			words = countWords(words, y)

	# get word count
	count = words.get(countername, 1)

	# Items sorted by value
	wordsort = sorted(words.items(), key=itemgetter(1), reverse=True)

	try:
		file = codecs.open("log.txt", "w", "utf8")
		file.write("word\tfrequency\n")
		for x in wordsort:
			if x[0] != countername:
				file.write(x[0] + "\t" + str(float(x[1])/float(count)) + "\n")
		file.close()
	except IOError:
		print "Output error."
