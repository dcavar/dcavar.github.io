#! /usr/bin/env python
# -*- coding: utf8 -*-

"""
freq3.py
(C) 2005 by Damir Cavar <dcavar@indiana.edu>
GNU General Public License

Functionality: Counting words
"""

import sys, os.path, glob, string, codecs
from operator import itemgetter

def countWords(words, filename):
	"""Counts words in file and returns dictionary."""
	try:
		file = codecs.open(filename, "r", "utf8")
		tokens = [ string.strip(string.lower(i)) for i in file.read().split() ]
		for i in tokens:
			words[i] = words.get(i, 0) + 1
		file.close()
	except IOError:
		print "Cannot read from file:", filename
	return words


if __name__ == "__main__":
	words = {}
	for x in sys.argv[1:]:
		for y in glob.glob(os.path.normcase(x)):
			words = countWords(words, y)

	# sort the dictionary on frequency
	#items = words.items()
	#wordsort = [ [ v[1], v[0] ] for v in items ]
	#wordsort.sort()
	#wordsort.reverse()

	# Items sorted by key
	#   The new builtin `sorted()` will return a sorted copy of the input iterable.
	#wordsort = sorted(words.items())

	# Items sorted by key, in reverse order
	#   The keyword argument `reverse` operates as one might expect
	#wordsort = sorted(words.items(), reverse=True)

	# Items sorted by value
	#    The keyword argument `key` allows easy selection of sorting criteria
	wordsort = sorted(words.items(), key=itemgetter(1))

	# In-place sort still works, and also has the same new features as sorted
	#wordsort = words.items()
	#wordsort.sort(key=itemgetter(1), reverse=True)
	# print items

	try:
		file = codecs.open("log.txt", "w", "utf8")
		file.write("word\tfrequency\n")
		for x in wordsort:
			file.write(x[1] + "\t" + str(x[0]) + "\n")
		file.close()
	except IOError:
		print "Output error."
