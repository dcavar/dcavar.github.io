#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ngram.py
(C) 2005 by Damir Cavar

ngram class

License:

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.


Description:

Generates frequency profiles over ngrams.
Serializes ngram models to files.
"""

import sys, pickle, os.path
from operator import itemgetter

class Ngrams:
	"""Ngram class for counting ngrams and storing ngram models."""

	def __init__(self, n = 2):
		"""Constructor."""
		self.ngrams = {}
		self.ngrams["__count__"] = 0
		self.ngrams["__n__"] = n
		self.__ngramrel = {}
		self.__changed = False


	def getNgramFrequency(self, ngram):
		"""Returns the absolute frequency of an ngram."""
		if self.ngrams.has_key(ngram):
			return self.ngrams[ngram]
		return 0


	def getNgramRelativeFrequency(self, ngram):
		"""Returns the relative frequency of an ngram."""
		if self.ngrams["__count__"] > 0:
			return float(self.getNgramFrequency(ngram))/float(self.ngrams["__count__"])
		else:
			return 0.0


	def getNumberTokens(self):
		"""Return number of tokens."""
		return self.ngrams["__count__"]


	def getNumberTypes(self):
		"""return number of types."""
		return len(self.ngrams.keys()) - 2


	def addNgram(self, ngram):
		"""Adds an ngram to the collection."""
		if len(ngram) == self.ngrams["__n__"]:
			self.ngrams[ngram] = self.ngrams.get(ngram, 0) + 1
			self.ngrams["__count__"] += 1
			self.__changed = True
		# else:
			# raise some exception


	def removeNgram(self, ngram):
		"""Removes one occurrence of an ngram from the collection by decreasing
		   its counter. If the counter equals 0 after decreasing, the ngram is
		   removed from the collection.
		"""
		if self.ngrams.has_key(ngram):
			if self.ngrams[ngram] > 1:
				self.ngrams[ngram] -= 1
			else:
				del self.ngrams[ngram]
			self.ngrams["__count__"] -= 1
			self.__changed = True
		# else
			# raise an error


	def frequencyProfile(self, increasing = True):
		"""Returns the frequency profile of the ngram items. If increasing is
		   set to True, the returned frequency profile will be increasing,
		   if it is set to False, the returned frequency profile is
		   decreasing.
		"""
		e = self.ngrams.copy()
		del e["__count__"]
		del e["__n__"]
		if increasing == True:
			return sorted(e.items(), key=itemgetter(1))
		items = e.items()
		items.sort(key = itemgetter(1), reverse=True)
		return items


	def relativeFrequencyProfile(self, increasing = True):
		"""Returns the relative frequency profile of the ngram items. If increasing
		   is set to True, the returned profile will be increasing, if it is set to
		   False, it is decreasing.
		"""
		if changed == True:
			self.__ngramrel = self.ngrams.copy()
			del self.__ngramrel["__count__"]
			del self.__ngramrel["__n__"]
			for i in self.__ngramrel.keys():
				self.__ngramrel[i] = self.getNgramRelativeFrequency(i)
			self.__changed = False
		return self.frequencyProfile(increasing, self.__ngramrel)


	def getMostFrequent(self, ngram):
		"""Returns the most frequent ngram."""
		return self.frequencyProfile()[-1]


	def getLeastFrequent(self, ngram):
		"""Returns the least frequent ngram."""
		return self.frequencyProfile()[0]


	def serialize(self, filename = "ngrams"):
		"""Dump the ngram model to a file."""
		try:
			if filename == "ngrams":
				filename = filename + str(self.ngrams["__n__"]) + ".p"
			pickle.dump(self.ngrams, open(filename, "w"))
			self.__changed = True
		except Exception, e:
			print "Exception %s" % e


	def deSerialize(self, filename = "ngrams"):
		"""Read ngram model from filename."""
		try:
			if filename == "ngrams":
				filename = filename + str(self.ngrams["__n__"]) + ".p"
			if os.path.exists(filename):
				self.ngrams = pickle.load(open(filename))
				self.__changed = True
		except Exception, e:
			print "Exception %s" % e
		# sparcify ngram dictionary for speed increase
		e = self.ngrams.copy()
		self.ngrams.update(e)


