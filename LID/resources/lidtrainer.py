#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
$Revision: 0.3 $
$Date: 2004/12/01 11:00:00 $
$Id: lidtrainer.py,v 0.3 2008/11/23 10:50:00 dcavar Exp $

(C) 2003-2011 by Damir Cavar <damir@cavar.me>

License:

	This program is free software; you can redistribute it and/or modify
	it under the terms of the Lesser GNU General Public License as published by
	the Free Software Foundation; either version 3 of the License, or
	(at your option) any later version.

	Respect copyrights and mention the author of this tool in any
	subsequent or modified version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the Lesser GNU General Public License
	along with this program; if not, write to the Free Software
	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
	or download it from http://www.gnu.org/licenses/lgpl.txt


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


__version__ = 0.3
__author__ = "Damir Cavar <damir@cavar.me>"



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
			trigram = text[i:i+3]
			self.num += 1
			if self.trigrams.has_key(trigram):
				# increment the number of this trigram
				self.trigrams[trigram] += 1
			else:
				# append the trigram
				self.trigrams[trigram] = 1


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


