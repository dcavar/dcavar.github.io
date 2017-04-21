#! /usr/bin/env python

"""
$Revision: 0.2 $
$Date: 2004/03/09 22:00:00 $
$Id: unigramchar.py,v 0.1 2003/03/09 22:00:00 dcavar Exp $

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

Usage: python unigramchar.py textfile(s)
"""


__version__ = 0.2
__author__ = "Damir Cavar"



import sys, glob, os.path
from string import *



def createNgrams(text, ngrams, count, n):
	"""Creates ngrams."""
	for i in range(len(text) - n + 1):
		gram = ""
		for x in range(n):
			gram += text[i + x]
		count += 1
		if ngrams.has_key(gram):
			ngrams[gram] += 1
		else:
			ngrams[gram] = 1
	return ngrams, count


def sort_by_value(d):
	""" Returns the keys of dictionary d sorted by their values """
	items=d.items()
	backitems=[ [v[1],v[0]] for v in items]
	backitems.sort()
	backitems.reverse()
	return [ backitems[i][1] for i in range(0,len(backitems))]

def cleanText(text):
	for x in ["\n"]:
		if x in text:
			text = text.replace(x, "")
	for x in ["\t"]:
		if x in text:
			text = text.replace(x, " ")
	return lower(text)


def main(x, ngrams, count):
	try:
		ngrams, count = createNgrams(cleanText(open(x).read()), ngrams, count, 3)
	except : # hmm, except something ;-)
		pass
	return ngrams, count


if __name__ == "__main__":
	ngram = {}
	count = 0
	for x in sys.argv[1:]:
		for y in glob.glob(os.path.normcase(x)):
			ngram, count = main(y, ngram, count)
	for i in sort_by_value(ngram):
		print i + "\t" + str(float(ngram[i])/count)
	print "Number of Tokens:\t" + str(count)
	print "Number of Types:\t" + str(len(ngram))
	print "Type-Token Ratio:\t" + str((float(count)/len(ngram))/100)