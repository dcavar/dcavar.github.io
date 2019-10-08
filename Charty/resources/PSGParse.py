#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
$Revision: 0.5 $
$Date: 2004/10/11 10:00:00 $
$Id: PSGPars.py,v 0.5 2011/06/17 12:32:00 dcavar Exp $

PSGPars.py
This is a storage and parser class for context free grammars
written in the format of reproduction or replacement rules.


(C) 2002-2011 by Damir Cavar <damir@cavar.me>

This code is written and distributed under the
Lesse GNU General Public License version 3 or newer.

See http://www.gnu.org/copyleft/lgpl.html for details
on the license or the the file lgpl-3.0.txt that should always be
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
students understand simple parsing algorithms. If there are any bugs,
please let me know:
Damir Cavar <damir@cavar.me>
"""


__author__  = "Damir Cavar <damir@cavar.me>"
__date__    = "$Jun 17, 2011 12:33:47 AM$"
__version__ = "0.5"


import sys, re, codecs


class PSG:
  """A Phrase Structure Grammar parser and storage class.

     PSG.load(fname) throws an IOException, if the file IO
     opening and reading throws one.
  """

  # symbol: [^-=>#,\s]+([-]+[^-=>#,\s]+)*
  rule_re = re.compile(r"(?P<lhssymbol>[^-=>#,\s]+([-]+[^-=>#,\s]+)*)\s+(-+|=+)>\s+(?P<rhssymbols>[^-=>#,\s]+([-]+[^-=>#,\s]+)*(\s+[^-=>#,\s]+([-]+[^-=>#,\s]+)*)*)(\s*#.*)?")

  def __init__(self, filename):
    self.terminals    = set()  # list of terminals
    self.nonterminals = set()  # list of non-terminals
    self.id2symb      = {}
    self.symb2id      = {}
    self.lhshash      = {}
    self.rhshash      = {}
    self.load(filename)

  def load(self, filename):
    rules = {}
    fp = codecs.open(filename, 'r', 'utf-8')
    line = fp.readline()
    while line:
      line = line.strip()
      res = self.rule_re.match(line)
      if res:
        lhs = res.group('lhssymbol')
        rhs = tuple(res.group('rhssymbols').split())
        ruletuple = (lhs, rhs)
        rules[ruletuple] = rules.get(ruletuple, 0) + 1
      line = fp.readline()
    fp.close()

    # make sets of terminals and non-terminals
    symbcount = 0
    for rule in rules:
      lhs = rule[0]
      rhs = rule[1]
      if lhs not in self.symb2id:
        symbcount += 1
        self.symb2id[lhs] = symbcount
      lhs = self.symb2id[lhs]
      self.nonterminals.add(lhs)
      nrhs = []
      for symb in rhs:
        if symb not in self.symb2id:
          symbcount += 1
          self.symb2id[symb] = symbcount
        nrhs.append(self.symb2id[symb])
      rhs = tuple(nrhs)
      # make lhs mapping to rhs
      res = list(self.lhshash.get(lhs, ()))
      if rhs not in res:
        res.append(rhs)
        self.lhshash[lhs] = tuple(res)
      # make rule for left-peripheral rhs symbol as key
      res = list(self.rhshash.get(rhs[0], ()))
      rule = (lhs, rhs)
      if rule not in res:
        res.append(rule)
        self.rhshash[rhs[0]] = tuple(res)
      # 
    self.id2symb = dict([ (t[1], t[0]) for t in self.symb2id.items() ])
    self.terminals = set(self.id2symb.keys()).difference(self.nonterminals)

  def id2s(self, id):
    return self.id2symb.get(id, "")

  def idl2s(self, idlist):
    return tuple( ( self.id2symb.get(i, "") for i in idlist ) )

  def s2id(self, symb):
    return self.symb2id.get(symb, 0)

  def sl2id(self, symblist):
    return tuple( ( self.symb2id.get(symb, 0) for symb in symblist ) )

  def isTerminal(self, id):
    if id in self.terminals: return True
    return False

  def isSymbol(self, id):
    if id in self.nonterminals: return True
    return False

