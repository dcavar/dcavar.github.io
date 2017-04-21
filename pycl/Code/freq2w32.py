#! /usr/bin/env python
# -*- coding: utf8 -*-

"""
freq2.py
(C) 2005 by Damir Cavar <dcavar@indiana.edu>
GNU General Public License

Functionality: Counting words
"""

import sys, os.path, glob, string, codecs

from win32com.client import constants
import win32com.client


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
	speaker = win32com.client.Dispatch('SAPI.SpVoice')
	speaker.Speak('Computational linguistics is very cool')
	speaker.Speak('Loading file')
	for x in sys.argv[1:]:
		for y in glob.glob(os.path.normcase(x)):
			speaker.Speak(y)
			words = countWords(words, y)

	# sort the dictionary on frequency
	items = words.items()
	wordsort = [ [ v[1], v[0] ] for v in items ]
	wordsort.sort()
	wordsort.reverse()

	try:
		file = codecs.open("log.txt", "w", "utf8")
		file.write("word\tfrequency\n")
		speaker.Speak('Counting words finished')
		speaker.Speak('Saving frequency profile')
		for x in wordsort:
			file.write(x[1] + "\t" + str(x[0]) + "\n")
		file.close()
	except IOError:
		print "Output error."

