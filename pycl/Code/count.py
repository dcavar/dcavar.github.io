#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, codecs, string, operator, glob, os.path, math


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



def count(filename):
	# file = codecs.open(filename, "r", "utf-8")
	file = open(filename)
	text = file.read().lower()
	file.close()

	unigrams = {}
	bigrams  = {}

	words = text.split()
	count = 0
	for i in range(len(words) - 1):
		if words[i] in string.punctuation:
			continue
		if words[i + 1] in string.punctuation:
			continue
		count += 1

		unigram = words[i]
		unigrams[unigram] = unigrams.get(unigram, 0) + 1

		bigram = tuple([words[i], words[i + 1]])
		bigrams[bigram] = bigrams.get(bigram, 0) + 1
	#if words[-1] not in string.punctuation:
	unigram = words[-1]
	count += 1
	return count, unigrams, bigrams


def printNgrams(count, ngrams):
	count = float(count)
	items = ngrams.items()
	items.sort(key=operator.itemgetter(1), reverse=True)
	for i in items:
		# print "%s\t%f" % (i.encode("utf-8"), ngrams[i]/count)
		print "%s\t%f" % (i[0], i[1]/count)


def getMI(count, unigrams, bigrams):
	count = float(count)
	items = []
	for i in bigrams.keys():
		if i[0] in functionWordsEN or i[1] in functionWordsEN:
			continue

		px = unigrams.get(i[0], 0.0000001)/count
		py = unigrams.get(i[1], 0.0000001)/count
		pxy = bigrams.get(i, 0.0000001)/(count - 1)

		items.append((i[0], i[1], pxy, px, py, pxy * math.log( pxy / (px * py) , 2)))
		# print "%s %s\t%f\t%f" % (i[0], i[1], pxy, pxy * math.log( pxy / (px * py) , 2))
	items.sort(key=operator.itemgetter(-1), reverse=True)
	for i in items:
		print "%s %s\t%f\t%f\t%f\t%f" % (i[0], i[1], i[2], i[3], i[4], i[5])



if __name__ == "__main__":
	if len(sys.argv) > 1:
		for i in sys.argv[1:]:
			for y in glob.glob(os.path.normcase(i)):
				count, unigrams, bigrams = count(y)
				# printNgrams(count, unigrams)
				getMI(count, unigrams, bigrams)

