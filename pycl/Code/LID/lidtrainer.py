#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
lidtrainer.py

(C) 2005 by Damir Cavar <dcavar@indiana.edu>

License:

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.


Functionality:

Lidtrainer processes all the files given as parameters to the script in the
following way:
It extracts all tri-grams from all files.
It keeps track of the frequencies of single tri-grams over all documents.
It prints the sorted list (based on frequency/probability) of the tri-grams
to the screen. The output can be piped to a file. This file represents the
language model for Lid.

Read about Lid to understand how this algorithm works.

Please send your comments and suggestions!
"""

__version__ = 0.2
__author__ = "Damir Cavar"

import sys, re, os.path, glob
from string import *

class Trigrams:

	trigrams   = {} # tri-grams are stored in a dictionary
	num        = 0  # number of tri-grams
	characters = 0  # number of characters

	def createTrigrams(self, text):
		"""Creates trigrams from characters."""

		text = re.sub(r"\n", r" ", text)
		text = re.sub(r"\s+", r" ", text)
		self.characters = self.characters + len(text)

		# go thru list up to one but last word and take
		# the actual word and the following word together
		for i in range(len(text) - 2):
			self.num += 1
			self.trigrams[text[i:i+3]] = self.trigrams.get(text[i:i+3], 0) + 1


	def calcProb(self):
		"""Calculate the probabilities for each trigram."""
		for x in self.trigrams.keys():
			self.trigrams[x] = float(self.trigrams[x]) / float(self.num)


	def eliminateFrequences(self, num):
		"""Eliminates all bigrams with a frequency <= num"""
		for x in self.trigrams.keys():
			if self.trigrams[x] <= num:
				value = self.trigrams[x]
				del self.trigrams[x]
				self.num -= value


	def createTrigramNSC(self, text):
		"""Creates bigrams without punctuation symbols."""
		self.createTrigrams(self.cleanTextSC(text))


	def cleanTextSC(self, text):
		"""Eliminates punctuation symbols from the submitted text."""
		for i in punctuation:
			if i in text:
				text = replace(text, i, " ")
		return text


	def cleanPBIG(self):
		"""Eliminate tri-grams that contain punctuation marks."""
		for i in self.trigrams.keys():
			for a in punctuation:
				if a in i:
					value = self.trigrams[i]
					del self.trigrams[i]
					self.num -= value
					break


if __name__ == "__main__":
	myTrigrams = Trigrams()
	if len(sys.argv) > 1:
		for x in sys.argv[1:]:
			for y in glob.glob(os.path.normcase(x)):
				try:
					myTrigrams.createTrigrams(myTrigrams.cleanTextSC(open(y).read()))
				except IOError:
					pass
		myTrigrams.eliminateFrequences(2)
		myTrigrams.calcProb()
		pairs = zip(myTrigrams.trigrams.values(), myTrigrams.trigrams.keys())
		pairs.sort()
		pairs.reverse()
		for i in pairs:
			print i[1], i[0]
	else:
		print "Usage:"
		print "python lidtrainer.py [document1] ..."
