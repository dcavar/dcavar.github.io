
"""
(C) 2006 by Damir Cavar

This code is published under the GNU Public License 2.
"""

import sys
from operator import itemgetter

def countTokens(filename):
	words = {}

	wordlist = open(filename).read().lower().split()

	# keep track of total number of tokens
	count = len(wordlist)

	# creating token frequencies
	for i in wordlist:
		words[i] = words.get(i, 0) + 1

	# sorting by value
	items = words.items()
	items.sort(key = itemgetter(1), reverse=True)

	# pretty print result
	for i in items:
		print "%s\t%s" % i


if __name__ == "__main__":
	for i in sys.argv[1:]:
		countTokens(i)

