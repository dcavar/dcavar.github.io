#! /usr/bin/env python2.4
# -*- coding: utf-8 -*-

"""
lid.py
(C) 2005, 2006 by Damir Cavar <dcavar@unizd.hr>

License:
This program is free software; you can redistribute it and/or modify
it under the terms of the Lesser GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Functionality:
1. Startup:
   Lid loads all *.dat files in the current directory, assuming that
   the files contain the tri-gram model of the language which is named
   with the file name (e.g. japanese.dat, german.dat etc.).
2. Processing:
	Lid processes all the files given as parameters to the script and prints
	out the language of the text that the file contains.

Basics:
	Lid is based on a tri-gram model of a training corpus for a given language.
	Use lidtrainer.py to generate such language models.

	The language models are sets of three character sequences (tri-grams) extracted
	from the training corpus, with their frequency. The probability of each
	tri-gram is calculated (given the frequency of the tri-gram and the number
	of all tri-grams in the corpus) and stored with the tri-gram in the language
	model.

	Lid generates all tri-grams for the test document and compares the probability
	of each tri-gram with the probabilities the corresponding tri-grams in the
	training corpus or the language model. For each tri-gram the deviation from
	the corresponding tri-gram in the language model is calculated. If a tri-gram is
	not found in the language model, the deviation is assumed to be maximal, i.e.
	equal to 1.

	The language model that has the minimal deviation score for the tri-grams in
	the tested text is assumed to represent the language of the tested text.

	This is a very simple but effective language ID strategy. It is developed for
	teaching purposes. A real world application would require much more evaluation
	of the significance of the deviations, optimization of the language models and
	many many other things.

Please send your comments and suggestions!
"""

import sys, glob, os.path, re
from os import listdir, getcwd


def loadModels(path):
	"""Load language models."""
	languages = []
	models    = []
	for x in listdir(path):
		if x[-4:] == ".dat":
			modelfile = file(x)
			languages.append(x[0].upper() + x[1:-4])
			newdict = {}
			for line in modelfile:
				tokens = line.split()
				if len(tokens) == 2:
					newdict[tokens[0]] = float(tokens[1])
			modelfile.close()
			models.append(newdict)
			modelnum = len(models)
	return languages, models


def lid(languages, models, text):
	"""Language Identification."""
	count    = float(len(text) - 2)
	trigrams = {}
	# store results
	result = [ 0.0 for i in range(len(models)) ]
	# create trigram from sample text
	for x in range(len(text) - 2):
		trigrams[text[x:x+3]] = trigrams.get(text[x:x+3], 0) + 1
	# compare with the models
	for x in trigrams.keys():
		for i in range(len(models)):
			result[i] += abs(models[i].get(x, 0.0) - (trigrams[x] / count))
	# return the identified language string
	return languages[result.index(min(result))]



if __name__ == "__main__":
	if len(sys.argv) == 1:
		sys.exit(1)
	languages, models = loadModels(getcwd())
	for i in sys.argv[1:]:
		for y in glob.glob(os.path.normcase(i)):
			print "%s\t%s" % (y, lid(languages, models, re.sub(r"\s+", r" ", re.sub(r"\n", r" ", open(y).read()))))

