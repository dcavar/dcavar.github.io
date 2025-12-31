#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Wlist2RE.py
(C) 2007-2011 by Damir Cavar <dcavar@me.com>

This code is published under the GNU General Public Licence Version 3:
http://www.gnu.org/licenses/gpl-3.0.html
Make sure you understand the license terms before doing anything with
this code.

The code generates an FSA from a list of words and generate a DOT file
(for visualization in for example Graphviz).

The file FSA.py is required. Make sure it is in the path or next to
Wlist2RE.py.

Run with Python, having a list of words in a text-file "wordlist.txt":

python Wlist2RE.py wordlist.txt

The output will be written in the file out.dot. This file can be opened in
Graphviz for visualization.

or make Wlist2RE.py executable.

The word list is assumed to be encoded in UTF-8. This can be changed in the
code below.

Links:

For the DOT language:
http://www.graphviz.org/doc/info/lang.html

For Graphviz:
http://www.graphviz.org/

"""


__author__    = "Damir Cavar <dcavar@me.hr>"
__credits__ = ""
__version__   = "$Revision: 1.0 $"
__date__      = "$Date: 2008/01/13 13:20:01 $"
__copyright__ = "Copyright (c) 2007-2011 Damir Cavar"
__license__   = "GPLv3"


import sys, re, codecs
from FSA import FSA

finals = u"#__0__FS"


def makeFSA(wlist):
    """Returns a non-deterministic minimal automaton incrementally generated from a word list."""

    # store all the states and as value tuples of production and goal state
    # key: state
    # value: [ (to-state, emission-symbol), ... ]
    states = { 0:None, 1:[] }

    countstates = 1 # this number is the currently highest numbered state
    finalstates = [ 0 ] # list of final states

    # INIT: store all words as starting from startstate
    # suffixes is used as helping data structure to eliminate duplicates
    suffixes = {}
    for i in wlist:
        suffixes[i] = 1
    # tuple list: state, [suffix1, suffix2, ... ], history=(state1, state2, ...)
    agenda = [ (1, suffixes.keys(), tuple() ) ]
    suffixes = {} # empty suffixes!
    statesuffixes = {} # store all suffixes for a state

    while True:
        if len(agenda) == 0:
            break
        currentstate, suffixlist, history = agenda.pop()
        # get suffixes, if exist:
        tmpval = statesuffixes.get(currentstate, [])
        tmpval = tmpval + suffixlist
        tmpval.sort()
        statesuffixes[currentstate] = tmpval

        prefList = makePrefixList(suffixlist)
        for x in prefList.keys():
            val = prefList[x]
            if finals in val and len(val) == 1:
                    # link this to final state
                    transitions = states.get(currentstate, [])
                    if (x, 0) not in transitions:
                        transitions.append( (x, 0) )
                        states[currentstate] = transitions
                    # generate suffix and store in suffix list
                    tmpsuf = x
                    sto = currentstate
                    for i in range(len(history) - 1, -1, -1):
                        if history[i] in finalstates:
                            # only if the current state is not a final one too
                            break
                        outgoing = states[history[i]]
                        if len(outgoing) > 1:
                            break
                        for n in outgoing:
                            if n[1] == sto:
                                tmpsuf = n[0] + tmpsuf
                        sto = history[i]
                    tmp = suffixes.get(tmpsuf, -1)
                    if tmp == -1:
                        suffixes[tmpsuf] = sto
                    continue

            # if there is one suffix and it is in suffixes
            # link it to the state this suffix starts from
            if len(val) == 1 and suffixes.has_key(val[0]):
                transition = (x, suffixes[val[0]])
                transitions = states.get(currentstate, [])
                if transition not in transitions:
                    transitions.append(transition)
                    states[currentstate] = transitions
            else:
                # make new transition
                countstates += 1
                transition = (x, countstates)
                transitions = states.get(currentstate, [])
                if transition not in transitions:
                    transitions.append(transition)
                    states[currentstate] = transitions
                if finals in val:
                    if countstates not in finalstates:
                        finalstates.append(countstates)
                    val.remove(finals)
                agenda.append( (countstates, val, tuple(list(history) + [ currentstate ])) )

    # check for equal subpaths in the end
    merged = {}
    for key in statesuffixes.keys():
        val = tuple(statesuffixes[key])
        del statesuffixes[key]
        # hash table with transition and target state as key
        # and starting state as value
        # the target state converted to final vs. non-final
        if statesuffixes.has_key(val):
            # merge the states
            merged[key] = statesuffixes[val]
        else:
            statesuffixes[ max( (key, val) ) ] = min( (key, val) )
    statesuffixes = None

    # change the states that need to be merged
    for i in states.keys():
        newval = []
        oldval = states[i]
        if oldval == None:
            continue
        for j in oldval:
            if merged.has_key(j[1]):
                newval.append( (j[0], merged[ j[1] ]) )
            else:
                newval.append( (j[0], j[1]) )
        states[i] = newval

    myFSA = FSA() # new FSA

    # eliminate unnecessary states by traversing
    agenda = []
    for i in states[1]:
        agenda.append( i )
        myFSA.add(1, i[0], i[1], None, None)

    while True:
        if not agenda:
            break
        inp, state = agenda.pop()
        val = states[state]
        if val:
            for i in val:
                agenda.append( i )
                myFSA.add(state, i[0], i[1], None, None)
    # erase unnecessary data
    states = None

    existingstates = myFSA.getStates()
    for i in finalstates:
        if i in existingstates:
            myFSA.setFinal(i)
    myFSA.setFinal(0)
    myFSA.setStart(1)

    return myFSA


def makeDOT(myFSA):
    """Return DOT representation for graphviz."""

    buffer = "digraph fsa {\nrankdir=LR;\nnode [shape=doublecircle];\n"
    for i in myFSA.getFinalStates():
        buffer = u" ".join((buffer, str(i)))
    buffer += u";\nnode [shape = circle];\n"
    for i in myFSA.states.keys():
        val = myFSA.states[i]
        buffer = u" ".join( (buffer, str(i[0]), u"->", str(val[0]), u"[ label=\"", i[1], u"\" ];\n") )
    return "".join((buffer, "\n}"))



def makePrefixList(wlist):
    # print wlist
    prefdict = {}
    for i in wlist:
        if not i:
            continue
        value = prefdict.get(i[0], [])
        if len(i) == 1:
            rest = finals
        else:
            rest = i[1:]
        if rest in value:
            continue
        value.append(rest)
        value.sort()
        prefdict[i[0]] = value
    return prefdict


def loadWlist(fname):
    """Return a list of words from a text file (in UTF-8 encoding).
       The word list is genereted by whitespace tokenization, i.e.
        it could be a floating text, a list of words line by line,
        word by word, etc. Duplicate words are removed."""
    try:
        fp = codecs.open(fname, "r", "utf-8")
        tmp = fp.read()
        fp.close()
        words = tmp.split()
    except ValueError:
        fp.close()
    words = list(set(words))
    words.sort()
    return tuple(words)


if __name__ == "__main__":
    for i in sys.argv[1:]:
        myFSA = makeFSA(loadWlist(i))
        myFSA.setAcceptingEmission("verb")
        ret = makeDOT(myFSA)
        fp = codecs.open("out.dot", "w", "utf-8")
        fp.write(ret)
        fp.close()
        # test some word in the FSA (accepting)
        # print myFSA.accept("pospavaju")
