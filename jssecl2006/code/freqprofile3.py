
"""
(C) 2006 by Damir Cavar

This code is published under the GNU Public License 2.
"""

import sys
from operator import itemgetter


def filterText(text):
	return text


def prettyPrint(items, count, relativize=False):
	if relativize:
		count = float(count)
		for i in items:
			print "%s\t%s" % ( i[0], i[1]/count )
	else:
		for i in items:
			print "%s\t%s" % i


def sortByValue(dict, decreasing=True):
	"""Return an item list of key-value pairs from a dictionary sorted by value."""
	items = dict.items()
	items.sort(key = itemgetter(1), reverse=decreasing)
	return items


def countTokens(words, count, filename):
	"""Create a token list and count tokens."""
	wordlist = open(filename).read().lower().split()

	# keep track of total number of tokens
	count += len(wordlist)

	# creating token frequencies
	for i in wordlist:
		words[i] = words.get(i, 0) + 1

	return count, words


if __name__ == "__main__":
	words = {}
	count = 0
	for i in sys.argv[1:]:
		count, words = countTokens(words, count, i)
	prettyPrint(sortByValue(words), count)


