#!/usr/bin/env python

"""
PSGPars.py
This is a storage and parser class for context free grammars
written in the format of reproduction or replacement rules.


(C) 2002, 2003 by Damir Cavar <dcavar@indiana.edu>

This code is written and distributed under the
GNU General Public License which means that its
source code is freely-distributed and available
to the general public.

See http://www.gnu.org/copyleft/gpl.html for details
on the license or the the file gpl.txt that should always be
distributed with this code.


A parser for context free Phrase Structure Grammars (PSG).
The grammars are restricted to:
a. only one non-terminal on the left side of a rule:
   N -> x y z
b. Non-terminals and terminals on the right side

Rules are read in with the following constraints:
i.   it is assumed that all elements on the left side of a rule
     are non-terminals
ii.  all elements that are not in the set of non-terminals
     (appear on the right side, but never on the left side) are
     assumed to be terminals


This code can be opimized. However, its main purpose is to help
students understand how simple chart parsing works. If there are any bugs,
please let me know: Damir Cavar <dcavar@indiana.edu>
"""

__author__  = "Damir Cavar"
__version__ = "0.1"

import string, re


class PSG:
  "A Phrase Structure Grammar parser and storage class."

  regexp_nont = re.compile(r"([^\s]+)\s+->\s+(.+)")
  regexp_t = re.compile(r"([^\s]+)")

  def __init__(self, filename):
    self.lhs = []           # list of left-hand-side symbols
    self.rhs = []           # list of right-hand-side symbols
    self.terminals    = []  # list of terminals
    self.nonterminals = []  # list of non-terminals
    self.lhshash = {}
    self.rhshash = {}
    self.tags         = []  # list of tags
    self.lex          = []  # list of words for tag
    self.load(filename)

  def load(self, filename):

    lines = []
    file = open(filename)
    if file:
      for i in file:
        str = string.lstrip(string.rstrip(i))
        if len(str) == 0:
          continue
        if str[0] == "#":
          continue
        else:
          lines.append(str)

    # extract nonterminals = lhs
    rhs = []
    for i in lines:
      result = self.regexp_nont.findall(i)
      if result != None:
        for k in result:
          if k[0] not in self.nonterminals:
            self.nonterminals.append(k[0])
          self.lhs.append(k[0])
          rhs.append(k[1])

    # extract terminals
    num = 0
    dellist = []
    for i in rhs:
      result = self.regexp_t.findall(i)
      if result != None:
        tmp = []
        for k in result:
          tmp.append(k)
          if k not in self.nonterminals:
            self.terminals.append(k)
            dellist.append(num)
        self.rhs.append(tmp)
        num += 1
    for i in dellist:
      if self.lhs[i] in self.tags:
        pos = self.tags.index(self.lhs[i])
        self.lex[pos].append(self.rhs[i][0])
      else:
        self.tags.append(self.lhs[i])
        self.lex.append([self.rhs[i][0]])
    dellist.reverse()
    for i in dellist:
      del self.lhs[i]
      del self.rhs[i]

    # make a hash table with LHS
    for i in range(len(self.lhs)):
      if self.lhshash.has_key(self.lhs[i]):
        if i not in self.lhshash[self.lhs[i]]:
          tmplist = self.lhshash[self.lhs[i]]
          tmplist.append(i)
          self.lhshash[self.lhs[i]] = tmplist
      else:
        self.lhshash[self.lhs[i]] = [i]
      if self.rhshash.has_key(self.rhs[i][0]):
        if i not in self.rhshash[self.rhs[i][0]]:
          tmplist = self.rhshash[self.rhs[i][0]]
          tmplist.append(i)
          self.rhshash[self.rhs[i][0]] = tmplist
      else:
        self.rhshash[self.rhs[i][0]] = [i]        

  def getTag(self, word):
    for i in range(len(self.lex)):
      if word in self.lex[i]:
        return self.tags[i]
    return "unknown"


