#!/usr/bin/env python

"""
Charty.py
This is a small incremental bottom-up chart parser for context free grammars.

(C) 2005 by Damir Cavar

This code is written and distributed under the
GNU General Public License which means that its
source code is freely-distributed and available
to the general public.

See http://www.gnu.org/copyleft/gpl.html for details
on the license or the the file gpl.txt that should always be
distributed with this code.


Used data structures:

chart:
	list of edges

edge:
	list of integers and symbols
	[start, end, dotindex, LHS, RHS]
	start:    integer, start of the edge
	end:      integer, end of the edge
	dotindex: integer, position of the dot in the RHS
	LHS:      string, left-hand side symbol
	RHS:      list of strings, symbols in right-hand side


Properties:
Incremental (left-to-right) bottom-up chart parser.
Select only potentially appropriate rules from grammar
	- length of RHS is less or equal to remaining words/symbols


Processing steps:
	Word by word:
		Initialise chart with word (add edge for word)
		Do until no further improvement:
			Add new rules from grammar that consume inactive edges
			Apply the fundamental rule to induce new edges


This code can be opimized. However, its main purpose is to help
students understand how simple chart parsing works. If there are any bugs,
please let me know: Damir Cavar <dcavar@indiana.edu>"""

__author__  = "Damir Cavar"
__version__ = "0.2"

import sys, PSGPars
from copy import copy

grammarfile = "PSG1.txt"              # name of the CFG file
DEBUG = 1       # set this to 0 if you do not want tracing

grammar = PSGPars.PSG(grammarfile) # initialization of the grammar
chart  = []     # storage for edges
inputlength = 0 # storage for number of tokens in input


def isActive(edge):
	"""Return 1 if edge is active, else return 0."""
	if edge[2] < len(edge[4]): return 1
	return 0


def isInactive(edge):
	"""Return 1 if edge is active, else return 0."""
	if edge[2] >= len(edge[4]): return 1
	return 0


def match(aedge, iedge):
	"""Returns 1 if the active edge and the inactive edge match,
	   otherwise 0."""
	if aedge[1] == iedge[0]:
		if aedge[4][aedge[2]] == iedge[3]: return 1
	return 0


def getParse(inputlength, chart):
	"""Returns a list of all parses in bracketing notation."""
	parses = []
	for i in range(len(chart)):
		if not isActive(chart[i]):
			if chart[i][0] == 0 and chart[i][1] == inputlength: # got spanning edge
				parses.append(structToStr([i]))
	return parses


def structToStr(edges):
	"""Returns a string representation of the parse with
	   labled brackets."""
	tmpstr = ""
	for i in edges:
		if chart[i][5]:
			tmpstr = tmpstr + "[" + chart[i][3] + " " + structToStr(chart[i][5]) + " ] "
		else:
			tmpstr = tmpstr + "[" + chart[i][3] + " "
			for x in chart[i][4]:
				tmpstr = " ".join([tmpstr, x])
			tmpstr = tmpstr + " ] "
	return tmpstr


def ruleInvocation(lststart):
	"""Add all the rules of the grammar to the chart that
	   are relavant:
		Find the rule with the LHS of edge as the leftmost RHS
		symbol and maximally the remaining length of the input."""
	global chart
	change = 0
	for i in range(lststart, len(chart)):
		if chart[i][2] >= len(chart[i][4]): # only inactive edge
			(start, end, index, lhs, rhs, consumed) = chart[i]
			if grammar.rhshash.has_key(lhs):
				for k in grammar.rhshash[lhs]:
					if len(grammar.rhs[k]) > inputlength - start:
						continue
					newedge = [ start, end, 1, grammar.lhs[k], grammar.rhs[k], [i] ]
					if newedge in chart:
						continue
					chart.append(copy(newedge))
					change = 1
					if DEBUG:
						print "RI Adding edge:", newedge
	return change


def fundamentalRule():
	"""The fundamental rule of chart parsing generates new edges by
	   combining fitting active and inactive edges."""
	global chart
	change = 0
	for aedge in chart:
		if isActive(aedge):
			for k in range(len(chart)):
				if isInactive(chart[k]):
					if match(aedge, chart[k]):
						newedge = aedge[:]
						newedge[5] = aedge[5][:]
						newedge[5].append(k)
						newedge[1] = chart[k][1]
						newedge[2] = newedge[2] + 1
						if newedge not in chart:
							chart.append(copy(newedge))
							change = 1
							if DEBUG:
								print "FR Adding edge:", newedge
	return change


def parse(input):
	"""Parse a list of tokens.
	"""
	global chart, inputlength
	chart = []
	inputlength = len(input)

	chartpos = 0  # remember start-position in chart
	for i in range(len(input)):
		# initialize with input token
		chart.append([ i, i + 1, 1, grammar.getTag(input[i]), [ input[i] ], [] ])
		if DEBUG:
			print "Adding edge:", chart[len(chart) - 1]
		change = 1
		while change:
			change = 0
			chartlen = len(chart)
			if ruleInvocation(chartpos):
				change = 1
			chartpos = chartlen  # set pointer to new edge in chart
			if fundamentalRule():
				change = 1
	if DEBUG:
		print "Chart:"
		for i in range(len(chart)):
			if isActive(chart[i]):
				print i, "Active:  ",
			else:
				print i, "Inactive:",
			print chart[i]
	for i in getParse(inputlength, chart):
		print "Parse:"
		print i



if __name__ == "__main__":
	if len(sys.argv) > 1:
		parse(sys.argv[1:])
	else:
		print "Parsing: John kissed Mary"
		parse(["John", "kissed", "Mary"])
		print "-----------------------------------------------------------"
		print "Parsing: John kissed Mary"
		parse(["the", "green", "man", "killed", "the", "blue", "man", "with", "the", "tie"])

