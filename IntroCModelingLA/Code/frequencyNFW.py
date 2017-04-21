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


PRINTNUMBER = 30


functionWordsEN = ["a", "abroad", "about", "above", "across", "after", "again",
	"against", "ago", "ahead", "all", "almost", "alongside", "already",
	"also", "although", "always", "am", "amid", "amidst", "among", "amongst",
	"an", "and", "another", "any", "anybody", "anyone", "anything", "anywhere",
	"apart", "are", "aren't", "around", "as", "aside", "at", "away", "back",
	"backward", "backwards", "be", "because", "been", "before", "beforehand",
	"behind", "being", "below", "between", "beyond", "both", "but", "by",
	"can", "can't", "cannot", "could", "couldn't", "dare", "daren't", "despite",
	"did", "didn't", "directly", "do", "does", "doesn't", "doing", "don't",
	"done", "down", "during", "each", "either", "else", "elsewhere", "enough",
	"even", "ever", "evermore", "every", "everybody", "everyone", "everything",
	"everywhere", "except", "fairly", "farther", "few", "fewer", "for",
	"forever", "forward", "from", "further", "furthermore", "had", "hadn't",
	"half", "hardly", "has", "hasn't", "i", "have", "haven't", "having", "he",
	"hence", "her", "here", "hers", "herself", "him", "himself", "his", "how",
	"however", "if", "in", "indeed", "inner", "inside", "instead", "into",
	"is", "isn't", "it", "its", "itself", "just", "keep", "kept", "later",
	"least", "less", "lest", "like", "likewise", "little", "low", "lower",
	"many", "may", "mayn't", "me", "might", "mightn't", "mine", "minus",
	"moreover", "most", "much", "must", "mustn't", "my", "myself", "near",
	"need", "needn't", "neither", "never", "nevertheless", "next", "no",
	"no-one", "nobody", "none", "nor", "not", "nothing", "notwithstanding",
	"now", "nowhere", "of", "off", "often", "on", "once", "one", "ones",
	"only", "onto", "opposite", "or", "other", "others", "otherwise", "ought",
	"oughtn't", "our", "ours", "ourselves", "out", "outside", "over", "own",
	"past", "per", "perhaps", "please", "plus", "provided", "quite", "rather",
	"really", "round", "same", "self", "selves", "several", "shall", "shan't",
	"she", "should", "shouldn't", "since", "so", "some", "somebody", "someday",
	"someone", "something", "sometimes", "somewhat", "still", "such", "that",
	"than", "the", "their", "theirs", "them", "themselves", "then", "there",
	"therefore", "these", "they", "thing", "things", "this", "those", "though",
	"through", "throughout", "thus", "till", "to", "together", "too", "towards",
	"under", "underneath", "undoing", "unless", "unlike", "until", "up", "upon",
	"upwards", "us", "versus", "very", "via", "was", "wasn't", "way", "we",
	"well", "were", "weren't", "what", "whatever", "when", "whence", "whenever",
	"where", "whereby", "wherein", "wherever", "whether", "which", "whichever",
	"while", "whilst", "whither", "who", "whoever", "whom", "whose", "why",
	"will", "with", "within", "without", "won't", "would", "wouldn't", "yet",
	"you", "your", "yours", "yourself", "yourselves", "thou", "thee", "thy" ]




import sys, os.path, glob, string



def countWords(words, filename):
	"""Counts words in file and returns dictionary."""
	try:
		file = open(filename, "r")
		for x in file.readlines():
			for i in string.split(x):
				i = string.strip(string.lower(i))
				if len(i) == 0:
					continue
				while i[-1] in string.punctuation:
					i = i[:-1]
					if len(i) == 0:
						break
				if len(i) == 0:
					continue
				while i[0] in string.punctuation:
					i = i[1:]
					if len(i) == 0:
						break
				if i in functionWordsEN:
					continue
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
	for x in wordsort[:min(len(wordsort),PRINTNUMBER)]:
		print x[2] + "\t" + str(x[0]) + "\t" + str(x[1])
