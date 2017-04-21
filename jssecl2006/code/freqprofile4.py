
"""
(C) 2006 by Damir Cavar

This code is published under the GNU Public License 2.
"""

import sys, re
from operator import itemgetter
from functionwords import english



def filterText(text):
	return re.sub(r"([0-9]|[\^'`\";:.,{}\[\]()\-_=+!$%#@&\*])+", " ", text)


def prettyPrint(items, count, relativize=False):
	if relativize:
		count = float(count)
		for i in items:
			if i[0] not in english:
				print "%s\t%s\t%s" % ( i[0], i[1], i[1]/count )
	else:
		for i in items:
			if i[0] not in english:
				print "%s\t%s" % i


def sortByValue(dict, decreasing=True):
	"""Return an item list of key-value pairs from a dictionary sorted by value."""
	return sorted(dict.items(), key = itemgetter(1), reverse=decreasing)


def countTokens(words, count, filename):
	"""Create a token list and count tokens."""
	tokenlist = filterText(open(filename).read()).lower().split()

	# creating token frequencies
	for i in tokenlist:
		words[i] = words.get(i, 0) + 1

	return count + len(tokenlist), words


if __name__ == "__main__":
	words = {}
	count = 0
	for i in sys.argv[1:]:
		count, words = countTokens(words, count, i)
	prettyPrint(sortByValue(words), count, True)


