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
		['b',                    '_',    'P@ R P1',        'new'],
		['new',                  '@',    'R',              'mark_digits'],
		['new',                  'else', 'L',              'new'],
		['mark_digits',          '0',    'R Px R',         'mark_digits'],
		['mark_digits',          '1',    'R Px R',         'mark_digits'],
		['mark_digits',          '_',    'R Pz R R Pr',    'find_x'],
		['find_x',               'x',    'E',              'first_r'],
		['find_x',               '@',    '',               'find_digits'],
		['find_x',               'else', 'L L',            'find_x'],
		['first_r',              'r',    'R R',            'last_r'],
		['first_r',              'else', 'R R',            'first_r'],
		['last_r',               'r',    'R R',            'last_r'],
		['last_r',               '_',    'Pr R R Pr',      'find_x'],
		['find_digits',          '@',    'R R',            'find_1st_digit'],
		['find_digits',          'else', 'L L',            'find_digits'],
		['find_1st_digit',       'x',    'L',              'found_1st_digit'],
		['find_1st_digit',       'y',    'L',              'found_1st_digit'],
		['find_1st_digit',       'z',    'L',              'found_2nd_digit'],
		['find_1st_digit',       '_',    'R R',            'find_1st_digit'],
		['found_1st_digit',      '0',    'R',              'add_zero'],
		['found_1st_digit',      '1',    'R R R',          'find_2nd_digit'],
		['find_2nd_digit',       'x',    'L',              'found_2nd_digit'],
		['find_2nd_digit',       'y',    'L',              'found_2nd_digit'],
		['find_2nd_digit',       '_',    'R R',            'find_2nd_digit'],
		['found_2nd_digit',      '0',    'R',              'add_zero'],
		['found_2nd_digit',      '1',    'R',              'add_one'],
		['found_2nd_digit',      '_',    'R',              'add_one'],
		['add_zero',             'r',    'Ps',             'add_finished'],
		['add_zero',             'u',    'Pv',             'add_finished'],
		['add_zero',             'else', 'R R',            'add_zero'],
		['add_one',              'r',    'Pv',             'add_finished'],
		['add_one',              'u',    'Ps R R',         'carry'],
		['add_one',              'else', 'R R',            'add_one'],
		['carry',                'r',    'Pu',             'add_finished'],
		['carry',                '_',    'Pu',             'new_digit_is_zero'],
		['carry',                'u',    'Pr R R',         'carry'],
		['add_finished',         '@',    'R R',            'erase_old_x'],
		['add_finished',         'else', 'L L',            'add_finished'],
		['erase_old_x',          'x',    'E L L',          'print_new_x'],
		['erase_old_x',          'z',    'Py L L',         'print_new_x'],
		['erase_old_x',          'else', 'R R',            'erase_old_x'],
		['print_new_x',          '@',    'R R',            'erase_old_y'],
		['print_new_x',          'y',    'Pz',             'find_digits'],
		['print_new_x',          '_',    'Px',             'find_digits'],
		['erase_old_y',          'y',    'E L L',          'print_new_y'],
		['erase_old_y',          'else', 'R R',            'erase_old_y'],
		['print_new_y',          '@',    'R',              'new_digit_is_one'],
		['print_new_y',          'else', 'Py R',           'reset_new_x'],
		['reset_new_x',          '_',    'R Px',           'flag_result_digits'],
		['reset_new_x',          'else', 'R R',            'reset_new_x'],
		['flag_result_digits',   's',    'Pt R R',         'unflag_result_digits'],
		['flag_result_digits',   'v',    'Pw R R',         'unflag_result_digits'],
		['flag_result_digits',   'else', 'R R',            'flag_result_digits'],
		['unflag_result_digits', 's',    'Pr R R',         'unflag_result_digits'],
		['unflag_result_digits', 'v',    'Pu R R',         'unflag_result_digits'],
		['unflag_result_digits', 'else', '',               'find_digits'],
		['new_digit_is_zero',    '@',    'R',              'print_zero_digit'],
		['new_digit_is_zero',    'else', 'L',              'new_digit_is_zero'],
		['print_zero_digit',     '0',    'R E R',          'print_zero_digit'],
		['print_zero_digit',     '1',    'R E R',          'print_zero_digit'],
		['print_zero_digit',     '_',    'P0 R R R',       'cleanup'],
		['new_digit_is_one',     '@',    'R',              'print_one_digit'],
		['new_digit_is_one',     'else', 'L',              'new_digit_is_one'],
		['print_one_digit',      '0',    'R E R',          'print_one_digit'],
		['print_one_digit',      '1',    'R E R',          'print_one_digit'],
		['print_one_digit',      '_',    'P1 R R R',       'cleanup'],
		['cleanup',              '_',    '',               'new'],
		['cleanup',              'else', 'E R R',          'cleanup']
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
			if item[0] == currentState and (item[1] == self.seq[self.idx] or item[1] == "else"):
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