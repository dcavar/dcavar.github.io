#! /usr/bin/env python
# -*- coding: utf8 -*-

"""
freq4.py
(C) 2005 by Damir Cavar <dcavar@indiana.edu>
GNU General Public License

Functionality: Counting words
"""

import sys, os.path, glob, string, codecs
from operator import itemgetter

def countWords(words, filename):
	"""Counts words in file and returns dictionary."""
	count = words.get("__count__", 0)
	try:
		file = codecs.open(filename, "r", "utf8")
		tokens = [ string.strip(string.lower(i)) for i in file.read().split() ]
		for i in tokens:
			words[i] = words.get(i, 0) + 1
			count += 1
		file.close()
	except IOError:
		print "Cannot read from file:", filename
	words["__count__"] = count
	return words


if __name__ == "__main__":
	words = {}
	for x in sys.argv[1:]:
		for y in glob.glob(os.path.normcase(x)):
			words = countWords(words, y)

	# Items sorted by value
	#    The keyword argument `key` allows easy selection of sorting criteria
	wordsort = sorted(words.items(), key=itemgetter(1), reverse=True)

	# In-place sort still works, and also has the same new features as sorted
	#wordsort = words.items()
	#wordsort.sort(key=itemgetter(1), reverse=True)

	try:
		file = codecs.open("log.txt", "w", "utf8")
		file.write("word\tfrequency\n")
		count = words.get("__count__", 1)
		for x in wordsort:
			if x[0] != "__count__":
				file.write(x[0] + "\t" + str(float(x[1])/float(count)) + "\n")
		file.close()
	except IOError:
		print "Output error."
