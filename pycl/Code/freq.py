#! /usr/bin/env python
# -*- coding: utf8 -*-

"""
freq.py
(C) 2005 by Damir Cavar <dcavar@indiana.edu>
GNU General Public License

Functionality: Counting words
"""

import sys, os.path, glob, string

def countWords(words, filename):
	"""Counts words in file and returns dictionary."""
	try:
		file = open(filename, "r")
		tokens = [ string.strip(i.lower()) for i in file.read().split() ]
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
	for x in words.keys():
		print x + "\t" + str(words[x])
