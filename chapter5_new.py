#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys

def printSeq(configuration):
	def wrapper(self, *args, **kwargs):
		print("Enter configuration: %s " % (args[0]))
		print("%s, %d" % (''.join(self.seq), self.idx))

		if self.idx < 0 or self.idx > self.maxLength - 1:
			print("cursor < 0 or cursor > maxLength(%d), quit system." % (self.maxLength))
			sys.exit(0)
		return configuration(self, *args, **kwargs)
	return wrapper

class TuringConfiguration(object):
	def __init__(self, seqLength = 50):
		# 0 - Start state, 1 - Input, 2 - Action, 3 - End state
		self.stateMachine = [
		['b', '_', 'Pe R Pe R P0 R R P0 L L', 'o'],
		['o', '1', 'R Px L L L',              'o'],
		['o', '0', '',                        'q'],
		['q', '0', 'R R',                     'q'],
		['q', '1', 'R R',                     'q'],
		['q', '_', 'P1 L',                    'p'],
		['p', 'x', 'E R',                     'q'],
		['p', 'e', 'R',                       'f'],
		['p', '_', 'L L',                     'p'],
		['f', '0', 'R R',                     'f'],
		['f', '1', 'R R',                     'f'],
		['f', '_', 'P0 L L',                  'o']
		]
		self.maxLength = seqLength
		self.seq = ['_'] * seqLength
		self.idx = 0
		return

	def __P(self, print_char):
		self.seq[self.idx] = print_char
		return

	def __E(self):
		self.seq[self.idx] = '_'
		return

	def __R(self):
		self.idx = self.idx + 1
		return

	def __L(self):
		self.idx = self.idx - 1
		return

	def __action(self, actionStr):
		actionList = actionStr.split(" ")

		for idx, action in enumerate(actionList):
			if action == "":
				continue
			elif action == "E":
				self.__E()
			elif action == "R":
				self.__R()
			elif action == "L":
				self.__L()
			elif action.startswith("P"):
				self.__P(action[1:])
			else:
				print("Wrong action: %s" % (action))
		return

	@printSeq
	def __stateMachineRunning(self, currentState):
		for idx, item in enumerate(self.stateMachine):
			if item[0] == currentState and item[1] == self.seq[self.idx]:
				self.__action(item[2])
				return item[3]

		print("StateMachine error in state: %s" % (currentState))
		sys.exit(0)

	def start(self):
		state = "b"
		while 1:
			state = self.__stateMachineRunning(state)

if __name__=='__main__':  
	testTuring = TuringConfiguration()
	testTuring.start()