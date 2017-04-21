#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-

"""
lid.py
(C) 2005, 2006 by Damir Cavar <dcavar@unizd.hr>

License:
This program is free software; you can redistribute it and/or modify
it under the terms of the Lesser GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Usage:
python2.4 lidtrain.py text1.txt text2.txt text3.txt ... > English.dat

Please send your comments and suggestions!
"""


__version__ = 0.3
__author__ = "Damir Cavar"

import sys, re, os.path, glob
# from operator import itemgetter

if __name__ == "__main__":
	trigrams = {}
	count = 0.0
	if len(sys.argv) == 1:
		print "Usage:"
		print "python lidtrainer.py [document1] ..."
		sys.exit(1)
	for x in sys.argv[1:]:
		for y in glob.glob(os.path.normcase(x)):
			text = re.sub(r"\s+", r" ", re.sub(r"\n", r" ", open(y).read()))
			count += (len(text) - 2)
			for i in range(len(text) - 2):
				trigrams[text[i:i+3]] = trigrams.get(text[i:i+3], 0) + 1
	for i in trigrams.keys():
		trigrams[i] = trigrams[i] / count
	# pairs = sorted(trigrams.items(), key = itemgetter(1), reverse=True)
	for i in pairs:
		print "%s\t%s" % i

