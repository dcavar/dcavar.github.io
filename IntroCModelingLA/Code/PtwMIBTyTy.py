#! /usr/bin/env python

"""
$Revision: 0.1 $
$Date: 2004/06/29 22:00:00 $
$Id: PtwMIBTyTy.py,v 0.1 2004/06/29 22:00:00 dcavar Exp $

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
from stattools import getBrownWords, puncTrim, sortNgrams, TOKEN, TYPE, getTBigrams, getTTokens, getTLRBigrams, getTWordList

PRINTWORDS = 100 # print number of most frequent words

LGRAM = TYPE
RGRAM = TYPE

bigrams      = {}	# bigram as key, frequency as value
tokens       = {}	# token as key, frequency as value
bigramsleft  = {}
bigramsright = {}
tokencount   = 0   # number of tokens
bigramcount  = 0   # number of bigrams


def PMI(token):
	"""Returns the mutual information for bigrams.
		MI = P(XY|X) log2 ( P(XY) / P(X) P(Y) )
		P(XY|X) = num of bigrams XY over num bigrams with X left
	"""

	global bigrams, tokens, bigramsleft, bigramsright, tokencount, bigramcount

	rmi = 0.0
	lmi = 0.0
	tokensleft  = []
	tokensright = []

	# all tokens left of token
	if bigramsleft.has_key(token):
		tokensleft = bigramsleft[token]
	# all tokens right of token
	if bigramsright.has_key(token):
		tokensright = bigramsright[token]

	count = 0
	for x in tokensleft:
		count += 1
		lmi += MI(x + " " + token, x, token)
	if count > 0:
		lmi = lmi/float(count)

	count = 0
	for x in tokensright:
		count += 1
		rmi += MI(token + " " + x, x, token)
	if count > 0:
		rmi = rmi/float(count)

	return rmi, lmi


def MI(bigram, token1, token2):
	"""Returns the mutual information."""
	global bigrams, tokens, bigramcount, tokencount
	pxy = float(bigrams[bigram])/float(bigramcount)
	px  = float(tokens[token1])/float(tokencount)
	py  = float(tokens[token2])/float(tokencount)
	return pxy * math.log(pxy/(px * py), 2)


if __name__ == "__main__":
	for i in sys.argv[1:]:
		for x in glob.glob(os.path.normcase(i)):
			try:
				file = open(x, "r")
				for i in file.readlines():
					i = string.lower(string.strip(i))
					if i == "":
						continue
					wordlist = getTWordList(i)
					bigrams, bigramcount = getTBigrams(wordlist, bigrams, bigramcount, TYPE, TYPE)
					tokens, tokencount = getTTokens(wordlist, tokens, tokencount, TYPE)
					bigramsleft, bigramsright = getTLRBigrams(wordlist, bigramsleft, bigramsright, TYPE, TYPE)
				file.close()
			except IOError:
				file.close()

	myTokens = sortNgrams(tokens)

	print "Left MI\tToken\tRight MI\tFrequency\tRelative Frequency"
	for x in range(min(len(myTokens), PRINTWORDS)):
		rmi, lmi = PMI(myTokens[x][0])
		print str(lmi) + "\t" + myTokens[x][0] + "\t" + str(rmi) + "\t" + str(myTokens[x][1]) + "\t" + str(float(myTokens[x][1])/float(tokencount))
