#! /usr/bin/env python

"""
$Revision: 0.1 $
$Date: 2004/06/23 22:00:00 $
$Id: frequency.py,v 0.1 2004/06/23 22:00:00 dcavar Exp $

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
	Counting words and their length.
"""


import sys, os.path, glob, string


def countWords(words, filename):
	"""Counts words in file and returns dictionary."""
	try:
		file = open(filename, "r")
		for x in file.readlines():
			for i in string.split(x):
				i = string.strip(i)
				if len(i) == 0:
					continue
				if i[-1] in string.punctuation:
					i = i[:-1]
				if len(i) == 0:
					continue
				if i[0] in string.punctuation:
					i = i[1:]
				if words.has_key(i):
					# increment the count of this word
					words[i][0] += 1
				else:
					# append the word and its length
					words[i] = [ 1, len(i) ]
	except IOError:
		print "Cannot read from file:", filename
		file.close()
	else:
		file.close()
	return words


if __name__ == "__main__":
	words = {}
	for x in sys.argv[1:]:
		for y in glob.glob(os.path.normcase(x)):
			words = countWords(words, y)

	# sort the dictionary on frequency
	items = words.items()
	wordsort = [ [ v[1][0], v[1][1], v[0] ] for v in items ]
	wordsort.sort()
	wordsort.reverse()

	print "word\tfrequency\tlength"
	for x in wordsort:
		print x[2] + "\t" + str(x[0]) + "\t" + str(x[1])
