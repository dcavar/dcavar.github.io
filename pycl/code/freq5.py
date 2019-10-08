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


def countWords(words, filename):
	"""Counts words in file and returns dictionary."""
	count = words.get(countername, 0)
	try:
		file = codecs.open(filename, "r", "utf8")
		tokens = [string.lower(i) for i in re.findall(ur"[A-Za-zčČćĆšŠžŽđĐ]+",file.read())]
		for i in tokens:
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
