#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
$Revision: 0.3 $
$Date: 2004/11/02 11:00:00 $
$Id: lid-speech.py,v 0.3 2008/11/23 11:05:00 dcavar Exp $

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


__version__ = 0.3
__author__ = "Damir Cavar <damir@cavar.me>"



import sys, re, os.path, glob
from string import *
from os import listdir, getcwd

from win32com.client import constants
import win32com.client


class Lid:
	num        = 0  # number of trigrams
	characters = 0  # number of characters
	languages  = []
	models     = []
	trigrams   = {}

	def __init__(self):
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
		# print "Loaded language models: ", self.languages
		speaker = win32com.client.Dispatch("SAPI.SpVoice")
		speaker.Speak("I loaded the following language modules:")
		for x in self.languages:
			speaker.Speak(x)


	def checkText(self, text):
		"""Check which language a text is."""
		self.createTrigrams(text)
		self.calcProb()
		result = []
		for x in range(len(self.languages)):
			result.append(0)
		for x in self.trigrams.keys():
			for i in range(len(self.models)):
				mymodel = self.models[i]
				if mymodel.has_key(x):
					value = mymodel[x] - self.trigrams[x]
					if value < 0:
						value = value * -1
					result[i] += value
				else:
					result[i] += 1
		speaker = win32com.client.Dispatch("SAPI.SpVoice")
		speaker.Speak("This text is: ")
		value = float(1.0)
		element = 0
		for x in range(len(result)):
			result[x] = float(result[x])/float(self.num)
			if value > result[x]:
				value = float(result[x])
				element = x
		speaker.Speak(self.languages[element])


	def createTrigrams(self, text):
		"""Creates trigrams from characters."""
		self.num = 0
		self.trigrams = {}
		text = re.sub(r"\n", " ", text)
		text = self.cleanTextSC(text)
		text = re.sub(r"\s+", " ", text)
		# text = lower(text)
		self.characters = len(text)

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
	myLid = Lid()
	if len(self.argv) > 1:
		for i in self.argv[1:]:
			for y in glob.glob(os.path.normcase(i)):
				try:
					myLid.checkText(open(y).read())
				except IOError:
					speaker = win32com.client.Dispatch("SAPI.SpVoice")
					speaker.Speak("I cannot open file " + y)
					pass
	else:
		speaker = win32com.client.Dispatch("SAPI.SpVoice")
		speaker.Speak("Type in your command line the following command:")
		speaker.Speak("python lid-speech.py file.txt")


