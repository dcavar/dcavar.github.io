#! /usr/bin/env python

"""
$Revision: 0.1 $
$Date: 2004/06/29 22:00:00 $
$Id: stattools.py,v 0.1 2004/06/29 22:00:00 dcavar Exp $

(C) 2004 by Damir Cavar <dcavar@indiana.edu>, Indiana University

License:

	This program is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 2 of the License, or
	(at your option) any later version.

	Respect copyrights and mention the author of this tool in any
	subsequent or modified version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program; if not, write to the Free Software
	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
	or download it from http://www.gnu.org/licenses/gpl.txt

"""

import sys, re, string, math

compiled = re.compile(r'(.*)\/(.*?)$');

TOKEN = 0
TYPE  = 1

def getBrownWords(word):
	"""Returns token and type from a Brown tagged word."""
	global compiled
	brownsplit = compiled.match(word)
	if brownsplit == None:
		return [ "", ""]
	return [ brownsplit.group(1), brownsplit.group(2) ]


def puncTrim(word):
	"""Eliminates spaces and punctuation marks left and right of words."""
	word = string.strip(word)
	if len(word) > 0:
		while word[0] in string.punctuation + "1234567890":
			word = word[1:]
			if word == "":
				break
	if len(word) > 0:
		while word[-1] in string.punctuation:
			word = word[:-1]
			if word == "":
				break	
	return word


def sortNgrams(hashtable):
	"""Returns a decreasing frequency profile as list."""
	sorted = map(lambda (x, y): (y,x), hashtable.items())
	sorted.sort()     # sort on basis of frequency
	sorted.reverse()  # revert order: most frequent first
	return map(lambda (y, x): (x, y), sorted)


def RE(bigramprob, token1p, token2p):
	"""Returns the Relative Entropy.
		Relative entropy is P1*log2(P1/P2) where here P1 is P(rightword)
		and P2 is P(right word | left word)."""
	return token1p * math.log(token1p/(bigramprob/token2p), 2)


def rF(count, total):
	"""Returns the relative frequency."""
	return float(count)/float(total)


def getWordList(text):
	"""Returns a list of words."""
	tmpwordlist = string.split(text)
	wordlist = []
	for i in range(len(tmpwordlist)):
		word = puncTrim(tmpwordlist[i])
		if len(word) > 0:
			wordlist.append(word)
	return wordlist


def getTWordList(text):
	"""Returns a list of words."""
	tmpwordlist = string.split(text)
	wordlist = [ [] ]
	pos = 0
	for i in range(len(tmpwordlist)):
		word = getBrownWords(tmpwordlist[i])
		word[0] = puncTrim(word[0])
		if len(word[0]) > 0:
			wordlist[pos].append(word)
		else:
			pos += 1
			wordlist.append([])
	return wordlist


def getTokens(wordlist, tokens = {}, count = 0):
	"""Returns a table and the count of tokens from text."""

	if len(wordlist) == 0:
		return tokens, count

	for i in wordlist:
		if tokens.has_key(i):
			tokens[i] += 1
		else:
			tokens[i] = 1
		count += 1
	return tokens, count


def getTTokens(wordlist, tokens = {}, count = 0, token = TOKEN):
	"""Returns a table and the count of tokens from text."""

	if len(wordlist) == 0:
		return tokens, count

	for i in wordlist:
		for x in i:
			if tokens.has_key(x[token]):
				tokens[x[token]] += 1
			else:
				tokens[x[token]] = 1
			count += 1
	return tokens, count


def getTBigrams(wordlist, bigrams = {}, count = 0, key = TOKEN, value = TOKEN):
	"""Returns a table of bigrams and the count."""

	if len(wordlist) == 0:
		return bigrams, count

	for x in wordlist:
		for i in range(len(x) - 1):
			if bigrams.has_key(x[i][key] + " " + x[i + 1][value]):
				bigrams[x[i][key] + " " + x[i + 1][value]] += 1
			else:
				bigrams[x[i][key] + " " + x[i + 1][value]] = 1
			count += 1
			if key != value:
				if bigrams.has_key(x[i][value] + " " + x[i + 1][key]):
					bigrams[x[i][value] + " " + x[i + 1][key]] += 1
				else:
					bigrams[x[i][value] + " " + x[i + 1][key]] = 1
	return bigrams, count


def getBigrams(wordlist, bigrams = {}, count = 0):
	"""Returns a table of bigrams and the count."""

	if len(wordlist) == 0:
		return bigrams, count

	for i in range(len(wordlist) - 1):
		if bigrams.has_key(wordlist[i] + " " + wordlist[i + 1]):
			bigrams[wordlist[i] + " " + wordlist[i + 1]] += 1
		else:
			bigrams[wordlist[i] + " " + wordlist[i + 1]] = 1
		count += 1
	return bigrams, count


def getLRBigrams(wordlist, lbigrams, rbigrams):
	""" """

	if len(wordlist) == 0:
		return lbigrams, rbigrams

	for i in range(len(wordlist) - 1):
		if lbigrams.has_key(wordlist[i + 1]):
			if wordlist[i] not in lbigrams[wordlist[i + 1]]:
				tmp = lbigrams[wordlist[i + 1]]
				tmp.append(wordlist[i])
				lbigrams[wordlist[i + 1]] = tmp
		else:
			lbigrams[wordlist[i + 1]] = [ wordlist[i] ]

		if rbigrams.has_key(wordlist[i]):
			if wordlist[i + 1] not in rbigrams[wordlist[i]]:
				tmp = rbigrams[wordlist[i]]
				tmp.append(wordlist[i + 1])
				rbigrams[wordlist[i]] = tmp
		else:
			rbigrams[wordlist[i]] = [ wordlist[i + 1] ]
	return lbigrams, rbigrams


def getTLRBigrams(wordlist, lbigrams, rbigrams, key = TOKEN, value = TYPE):
	""" """

	if len(wordlist) == 0:
		return lbigrams, rbigrams

	for x in wordlist:
		for i in range(len(x) - 1):
			if lbigrams.has_key(x[i + 1][key]):
				if x[i][value] not in lbigrams[x[i + 1][key]]:
					tmp = lbigrams[x[i + 1][key]]
					tmp.append(x[i][value])
					lbigrams[x[i + 1][key]] = tmp
			else:
				lbigrams[x[i + 1][key]] = [ x[i][value] ]

			if rbigrams.has_key(x[i][key]):
				if x[i + 1][value] not in rbigrams[x[i][key]]:
					tmp = rbigrams[x[i][key]]
					tmp.append(x[i + 1][value])
					rbigrams[x[i][key]] = tmp
			else:
				rbigrams[x[i][key]] = [ x[i + 1][value] ]
	return lbigrams, rbigrams

