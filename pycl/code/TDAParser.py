#!/usr/bin/env python

"""
TDAParser.py
(C) 2005 by Damir Cavar

	This code is free; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 2 of the License, or
	(at your option) any later version.

This code is a simple implementation of an agenda-based top-down parser
with backtracking.

In the code you can control the behavior of the parser, i.e. simulate
depth-first or breadth-first by changing the element that is taken from the
agenda, the first or the last one.
"""

import sys, grammar

LIFO = -1
FIFO = 0
strategy = FIFO

def tdparse(input, goal, grammar, agenda):
	"""Recursive top-down parse function with weak generative capacity."""

	#print "Got : %s\tinput: %s\nwith agenda:\n%s" % (goal, input, agenda)
	print "Got : %s\tinput: %s" % (goal, input)

	if goal == input == []:  print "Success"
	elif goal == [] or input == []:
		if agenda == []:  print "Fail: Agenda empty!"
		else:
			entry = agenda.pop(strategy)
			print "Backing up to: %s with %s" % (entry[0], entry[1])
			tdparse(entry[1], entry[0], grammar, agenda)
	else: # there is something in goal and input
		if goal[0] == input[0]: # if initial symbols match, reduce lists, parse
			tdparse(input[1:], goal[1:], grammar, agenda)
		else:
			for i in grammar.LHS.get(goal[0], []):
				if [list(i) + goal[1:], input] not in agenda:
					agenda.append([list(i) + goal[1:], input])
			if len(agenda) > 0:
				entry = agenda.pop(strategy)
				tdparse(entry[1], entry[0], grammar, agenda)
			else:  print "Fail: Agenda empty!"


if __name__ == "__main__":
	if len(sys.argv[1:]) > 0:
		myGrammar = grammar.PSG("PSG1.txt")
		print myGrammar
		tdparse(sys.argv[1:], ["S"], grammar.PSG("PSG1.txt"), [])
	else:
		print "Example parse:"
		input = ["Mary", "kissed", "John"]
		tdparse(input, ["S"], grammar.PSG("PSG1.txt"), [])
