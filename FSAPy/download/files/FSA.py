#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
FSA.py
(C) 2007-2011 by Damir Cavar <dcavar@me.com>

General Finite State Automaton class with associated transition actions
and emitions (Transducer properties).

This automaton class represents a deterministic automaton. In addition, the
index value can be submitted to the execute method, such that the action and
emission symbols can be associated with the position in the reading tape.
"""

__author__    = "Damir Cavar <dcavar@me.com>"
__version__   = "$Revision: 1.0 $"
__date__      = "$Date: 2007/12/29 21:28:19 $"
__copyright__ = "Copyright (c) 2007-2011 Damir Ćavar"
__license__   = "GPLv3"
__credits__   = "basic idea from Skip Montanaro's suggestion: http://www.python.org/search/hypermail/python-recent/0667.html and Python Wiki: http://wiki.python.org/moin/FiniteStateMachine"



class FSA:
	"""Finite state machine with transition actions and emissions.

	The emition for the complete automaton is set as an emition to all final states.

	Actions are of the following form:
	* function(current_state, input, index)
	"""

	def __init__(self):
		self.states      = {}   #
		self.finalstates = {}   # list of final states
		self.id          = None # internal usage name of this automaton
		self.startstate  = None
		self.state       = None
		self.dbg         = None
		self.acceptingEmission = []


	def add(self, state, input, newstate, action, emission):
		"""Add a transition to the FSM."""
		self.states[(state, input)] = (newstate, action, emission)


	def accept(self, sequence):
		self.state = self.startstate
		result = []
		for i in range(len(sequence)):
			emission = self.delta(sequence[i])
			if emission:
				result.append(emission)
		print "Emission:", emission
		print "State:", self.state
		if self.isFinal(self.state):
			print result
			return self.acceptingEmission
		return None


	def hasState(self, state):
		return self.states.has_key(state)


	def getFinalStates(self):
		return self.finalstates.keys()


	def getStates(self):
		# map it such that the return is just the first element of the key tuple
		return tuple( set([ i[0] for i in self.states.keys() ] + self.finalstates.keys()) )


	def setFinal(self, state):
		self.finalstates[state] = True


	def isFinal(self, state):
		return self.finalstates.get(state, False)


	def setAcceptingEmission(self, emission):
		"""Set the emission for accepting."""
		self.acceptingEmission = [ emission ]


	def appendAcceptingEmission(self, emission):
		"""Append to the emission of accepting."""
		self.acceptingEmission.append(emission)


	def delta(self, input):
		"""Perform a transition and execute action."""

		si = (self.state, input)

		newstate = None
		emission = None

		if self.states.has_key(si):
			newstate, action, emission = self.states[si]

		if self.dbg != None:
			self.dbg.write('State: %s / Input: %s /'
				'Next State: %s / Action: %s\n' %
				(self.state, input, newstate, action, emission))

		#if action:
		#	apply(action, (self.state, input, index))
		if newstate:
			self.state = newstate
		return emission


	def setStart(self, state):
		"""Define the start state. Actually, this just resets the current state."""
		self.startstate = state
		self.state = state


	def debug(self, out):
		"""Assign a writable file to log transitions."""
		self.dbg = out

