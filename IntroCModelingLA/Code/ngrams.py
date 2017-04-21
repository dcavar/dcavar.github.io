#! /usr/bin/env python

"""
$Revision: 0.1 $
$Date: 2004/06/29 22:00:00 $
$Id: bigrams.py,v 0.1 2004/06/29 22:00:00 dcavar Exp $

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

Functionality:
	Creation of bi-grams in python.
"""


import sys, string, glob, os.path, re
from stattools import sortNgrams


def getNGrams(text, ngrams, ngramcount, n):
	"""Creates an n-gram table and returns it together with the count."""

	if text == "":
		return ngrams, ngramcount

	wordlist = string.split(text)

	for x in range(len(wordlist) - n + 1):
		# skip punctuation marks
		if wordlist[x] in string.punctuation:
			continue

		# increment the total n-gram count
		ngramcount += 1

		# create n-gram
		if n == 1:
			ngram = wordlist[x]
		else:
			for i in range(n - 1):
				ngram = wordlist[x + i] + " "
			ngram = ngram + wordlist[x + n - 1]

		# add n-gram to n-gram table
		if ngrams.has_key(ngram):
			# increment the number for this n-gram
			ngrams[ngram] += 1
		else:
			# append the n-gram
			ngrams[ngram] = 1
	return ngrams, ngramcount


if __name__ == "__main__":
	bigrams     = {}	# bigram as key, frequency as value
	tokens      = {}	# token as key, frequency as value
	tokencount  = 0   # number of tokens
	bigramcount = 0   # number of bigrams

	for i in sys.argv[1:]:
		for x in glob.glob(os.path.normcase(i)):
			try:
				file = open(x, "r")
				for i in file.readlines():
					i = string.lower(string.strip(i))
					if i == "":
						continue
					bigrams, bigramcount = getNGrams(i, bigrams, bigramcount, 2)
					tokens, tokencount = getNGrams(i, tokens, tokencount, 1)
				file.close()
			except IOError:
				file.close()

	print "Got total:\nBigrams: " + str(bigramcount) + "\nTokens: " + str(tokencount)
	print "Bigram\tFrequency"
	for i in sortNgrams(bigrams):
		print i[0] + "\t" + str(i[1])
	print "Token\tFrequency"
	for i in sortNgrams(tokens):
		print i[0] + "\t" + str(i[1])
	print "Bigram\tRelative Frequency"
	for i in sortNgrams(bigrams):
		print i[0] + "\t" + str(float(i[1])/float(bigramcount))
	print "Token\tRelative Frequency"
	for i in sortNgrams(tokens):
		print i[0] + "\t" + str(float(i[1])/float(tokencount))
