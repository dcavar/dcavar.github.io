#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
lid.py
(C) 2005 by Damir Cavar <dcavar@indiana.edu>

License:

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.


Functionality:

1. Startup:
   Lid loads all *.dat files in the current directory, assuming that
   the files contain the tri-gram model of the language which is named
   with the file name (e.g. japanese.dat, german.dat etc.).

2. Processing:
	Lid processes all the files given as parameters to the script and prints
	out the language of the text that the file contains.

Lid can be used within an application by importing the class and using its
methods as shown in the end of this code (the __main__ part):

myLid = Lid()
languagename = myLid("This is an English example.")

Basics:

	Lid is based on a tri-gram model of a training corpus for a given language.
	Use lidtrainer.py to generate such language models.

	The language models are sets of three character sequences (tri-grams) extracted
	from the training corpus, with their frequency. The probability of each
	tri-gram is calculated (given the frequency of the tri-gram and the number
	of all tri-grams in the corpus) and stored with the tri-gram in the language
	model.

	Lid generates all tri-grams for the test document and compares the probability
	of each tri-gram with the probabilities the corresponding tri-grams in the
	training corpus or the language model. For each tri-gram the deviation from
	the corresponding tri-gram in the language model is calculated. If a tri-gram is
	not found in the language model, the deviation is assumed to be maximal, i.e.
	equal to 1.

	The language model that has the minimal deviation score for the tri-grams in
	the tested text is assumed to represent the language of the tested text.

	This is a very simple but effective language ID strategy. It is developed for
	teaching purposes. A real world application would require much more evaluation
	of the significance of the deviations, optimization of the language models and
	many many other things.

Please send your comments and suggestions!
"""


__version__ = 0.2
__author__ = "Damir Cavar"


import sys, re, os.path, glob
from string import *
from os import listdir, getcwd


class Lid:
	"""The basic Language Identification class
	"""

	num        = 0  # number of trigrams
	characters = 0  # number of characters
	languages  = [] # list of loaded language models
	models     = [] # list with the trigram models
	trigrams   = {} # trigrams of the analyzed document

	def __init__(self):
		"""Lid constructor
			The constructor loads automatically all language models in the
			current directory.
			The language models are stored in files that are made up as follows:
			LANGUAGE_NAME followd by .dat.
		"""
		for x in listdir(getcwd()):
			if x[-4:] == ".dat":
				modelfile = file(x)
				self.languages.append(upper(x[0]) + x[1:-4])
				newdict = {}
				for line in modelfile:
					tokens = split(line)
					if len(tokens) == 2:
						newdict[tokens[0]] = float(tokens[1])
				self.models.append(newdict)
				modelnum = len(self.models)
				modelfile.close()


	def checkText(self, text):
		"""Check which language a text is."""
		self.createTrigrams(text) # create trigrams of submitted text
		self.calcProb()           # calculate probabilities

		result = []               # storage for the matches with the models
		for x in range(len(self.languages)):
			result.append(0)
		# for all keys in trigrams
		for x in self.trigrams.keys():
			# for 0 to number language models
			for i in range(len(self.models)):
				# get the current model
				mymodel = self.models[i]
				if mymodel.has_key(x):
					# if the model contains the key, get the deviation
					value = mymodel[x] - self.trigrams[x]
					if value < 0:
						value = value * -1
					result[i] += value
				else:
					# otherwise set the resulting value to 1 = max. deviation
					result[i] += 1
		value = float(1.0)
		element = 0
		for x in range(len(result)):
			result[x] = float(result[x])/float(self.num)
			if value > result[x]:
				value = float(result[x])
				element = x
		return self.languages[element]


	def createTrigrams(self, text):
		"""Creates tri-grams from characters."""
		self.num = 0                    # storage for the number of trigrams
		self.trigrams = {}              # dictionary storage for trigrams
		text = re.sub(r"\n", " ", text) # replace newlines in text
		text = self.cleanTextSC(text)   # clean trigrams with punctuation marks
		text = re.sub(r"\s+", " ", text) # replace multiple spaces/tabs 
		self.characters = len(text)     # get number of characters

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
	if len(sys.argv) > 1:
		myLid = Lid()
		for i in sys.argv[1:]:
			for y in glob.glob(os.path.normcase(i)):
				try:
					print "File:\t" + str(y) + "\tLanguage:\t" + myLid.checkText(open(y).read())
				except IOError:
					print "Cannot open file:" + str(y)
					pass
	else:
		print "Usage:"
		print "python Lid.py [filename]"
