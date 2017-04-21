#! /usr/bin/env python

"""
$Revision: 0.1 $
$Date: 2004/06/29 22:00:00 $
$Id: MI.py,v 0.1 2004/06/29 22:00:00 dcavar Exp $

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


import sys, string, glob, os.path, math
from stattools import puncTrim, sortNgrams, getWordList, getBigrams, getTokens



def MI(bigram, bigramprob, tokens, tokencount):
	"""Returns the mutual information for bigrams.
		MI = P(XY|X) log2 ( P(XY) / P(X) P(Y) )
		P(XY|X) = num of bigrams XY over num bigrams with X left
	"""
	tokenlist = string.split(bigram)

	if tokens.has_key(tokenlist[0]):
		px = float(tokens[tokenlist[0]])/float(tokencount)
	else:
		px = 0.0
	if tokens.has_key(tokenlist[1]):
		py = float(tokens[tokenlist[1]])/float(tokencount)
	else:
		py = 0.0
	if py == 0.0 or px == 0.0:
		return 0.0
	return bigramprob * math.log(bigramprob/(px * py) , 2)


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
					wordlist = getWordList(i)
					bigrams, bigramcount = getBigrams(wordlist, bigrams, bigramcount)
					tokens, tokencount = getTokens(wordlist, tokens, tokencount)
				file.close()
			except IOError:
				file.close()

	print "Got total:\nBigrams: " + str(bigramcount) + "\nTokens: " + str(tokencount)
	print "Bigram\tFrequency\tRelative Frequency\tMutual Information"
	for i in sortNgrams(bigrams):
		print i[0] + "\t" + str(i[1]) + "\t" + str(float(i[1])/float(bigramcount)) + "\t" + str(MI(i[0], float(i[1])/float(bigramcount), tokens, tokencount))
