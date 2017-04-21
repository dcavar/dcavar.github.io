#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tokenizer.py
# (C) 2010 by Damir Cavar <dcavar@unizd.hr>
# Simple tokenization algorithm


import sys, codecs, os, os.path, glob

# workaround for piping output
sys.stdout = codecs.getwriter('utf8')(sys.stdout)


delimiterSet = u";.,!?\"()':[]\n/+-—=≤≥{}><*’”“|"
digits = u"0123456789"
chars = u"abcdefghijklmnopqrstuvwxyz"
chars = u"".join( (chars, chars.upper()) )
spaces = u" \t\n"
numberdelimiters = u",."


def main(fname):
	global delimiterSet

	if not os.path.isfile(fname):
		print "Error: Not a file", fname
		print ""
		usage()
		return

	try:
		inStream = codecs.open(fname, "r", "utf8")
		token = ""
		ch = inStream.read(1)
		lookahead = inStream.read(1)
		while True:
			if not ch:
				if token:
					print token
				break
			if ch in delimiterSet:
				if token:
					if token[-1] in digits and lookahead in digits and ch in numberdelimiters:
						token = "".join( (token, ch) )
					elif token[-1] in chars and lookahead in chars and ch in numberdelimiters:
						token = "".join( (token, ch) )
					else:
						print token
						token = ""
						if ch not in spaces:
							print ch
			elif ch in spaces:
				if token:
					print token
					token = ""
			else:
				token = "".join( (token, ch) )
			ch = lookahead
			lookahead = inStream.read(1)
		inStream.close()
	except IOError:
		print "Cannot read from file:", fname


def usage():
	pass


if __name__ == '__main__':
	for i in sys.argv[1:]:
		for j in glob.glob(i):
			main(os.path.expanduser(os.path.expandvars(j)))
	else:
		usage()
