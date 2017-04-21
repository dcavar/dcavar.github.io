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



def createUnigrams(text, ngrams, count):
	"""Creates unigrams."""
	for i in text:
		i = lower(i)
		if i == "\t":
			i = "\\t"
		if i == "\n":
			i = "\\n"
		count += 1
		if ngrams.has_key(i):
			ngrams[i] += 1
		else:
			ngrams[i] = 1
	return ngrams, count


def sort_by_value(d):
	""" Returns the keys of dictionary d sorted by their values """
	items=d.items()
	backitems=[ [v[1],v[0]] for v in items]
	backitems.sort()
	backitems.reverse()
	return [ backitems[i][1] for i in range(0,len(backitems))]


def main(x, ngrams, count):
	try:
		file = open(x)
		ngrams, count = createUnigrams(file.read(), ngrams, count)
		file.close()
	except : # hmm, except something ;-)
		file.close()
	return ngrams, count


if __name__ == "__main__":
	ngram = {}
	count = 0
	for x in sys.argv[1:]:
		for y in glob.glob(os.path.normcase(x)):
			ngram, count = main(y, ngram, count)
	for i in sort_by_value(ngram):
		print str(i) + "\t" + str(float(ngram[i])/count)
