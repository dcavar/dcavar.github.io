#! /usr/bin/env python

"""
$Revision: 0.1 $
$Date: 2004/06/29 22:00:00 $
$Id: REBToTy.py,v 0.1 2004/06/29 22:00:00 dcavar Exp $

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

from stattools import getBrownWords, puncTrim, sortNgrams, RE, rF, TOKEN, TYPE, getTWordList, getTBigrams, getTTokens, getTLRBigrams


PRINTWORDS = 1000 # print number of most frequent words

bigrams      = {}	# bigram as key, frequency as value
tokens       = {}	# token as key, frequency as value
types        = {}
bigramsleft  = {}
bigramsright = {}
tokencount   = 0   # number of tokens
typecount    = 0   # number of tokens
bigramcount  = 0   # number of bigrams


def PRE(token):
	"""Relative entropy is P1*log2(P1/P2) where here P1 is P(rightword)
		and P2 is P(right word | left word)."""

	global bigrams, tokens, bigramsleft, bigramsright, tokencount, bigramcount

	rre = 0.0
	lre = 0.0
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
		lre += RE(rF(bigrams[x+" "+token], bigramcount), rF(tokens[token], tokencount), rF(types[x], typecount))

	count = 0
	for x in tokensright:
		count += 1
		rre += RE(rF(bigrams[token+" "+x], bigramcount), rF(tokens[token], tokencount), rF(types[x], typecount))

	return rre, lre



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
					bigrams, bigramcount = getTBigrams(wordlist, bigrams, bigramcount, TOKEN, TYPE)
					tokens, tokencount = getTTokens(wordlist, tokens, tokencount, TOKEN)
					types, typecount = getTTokens(wordlist, types, typecount, TYPE)
					bigramsleft, bigramsright = getTLRBigrams(wordlist, bigramsleft, bigramsright, TOKEN, TYPE)
				file.close()
			except IOError:
				file.close()

	myTokens = sortNgrams(tokens)

	print "Left RE\tToken\tRight RE\tFrequency\tRelative Frequency"
	for x in range(min(len(myTokens), PRINTWORDS)):
		rre, lre = PRE(myTokens[x][0])
		print str(lre) + "\t" + myTokens[x][0] + "\t" + str(rre) + "\t" + str(myTokens[x][1]) + "\t" + str(rF(myTokens[x][1], tokencount))
