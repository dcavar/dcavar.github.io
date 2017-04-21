#!/usr/bin/env python

"""
BUAParser.py
(C) 2005 by Damir Cavar

	This code is free; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 2 of the License, or
	(at your option) any later version.

This is an implementation of a simple agenda-based buttom-up parser with
backtracking.

You can change the behavior of the parser by setting the value in the code
line:

strategy = FIFO

to the LIFO or FIFO. This simulates breadth first or depth first, respectively.
"""

import sys, grammar

LIFO = -1
FIFO = 0
strategy = LIFO

def parse(input, grammar, rootsymbol):
	"""Simple non-recursive bottom up parser."""
	agenda = []
	while True:
		print "Input: %s" % (input,)
		if input == rootsymbol:
			print "Success!"
			break
		else:
			for i in range(1, len(input) + 1):     # window
				for j in range(len(input) - i + 1): # movement
					for lhs in grammar.RHS.get(tuple(input[j:i + j]), []):
						newhyp = input[:j] + [lhs] + input[i + j:]
						if newhyp not in agenda:
							agenda.append(newhyp)
			if len(agenda) > 0:
				input = agenda.pop(strategy)
				print "Backing up to: ", input
			else:
				if input == rootsymbol:  print "Success!"
				else:  print "Failure! No more backtracking!"
				break


if __name__ == "__main__":
	if len(sys.argv[1:]) > 0:
		parse(sys.argv[1:], grammar.PSG("PSG1.txt"), ['S'])
	else:
		print "Example parse:"
		input=["the", "cat", "chases", "a", "mouse"]
		parse(input, grammar.PSG("PSG1.txt"), ['S'])
