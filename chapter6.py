#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys

sys.setrecursionlimit(10000)  # set the maximum depth as 10000

def printSeq(configuration):
	def wrapper(self, *args, **kwargs):
		print("Enter configuration: %s " % (configuration.__name__))
		print("%s, %d" % (''.join(self.seq), self.idx))
		#os.system("pause")
		if self.idx < 0 or self.idx > self.maxLength - 1:
			print("cursor < 0 or cursor > maxLength(%d), quit system." % (self.maxLength))
			sys.exit(0)
		configuration(self, *args, **kwargs)
		return

	return wrapper

class TuringConfiguration(object):
	def __init__(self, seqLength = 50):
		self.maxLength = seqLength
		self.seq = ['_'] * seqLength
		self.idx = 0
		pass

	def __P(self, print_char):
		self.seq[self.idx] = print_char
		return

	def __E(self):
		self.seq[self.idx] = '_'
		return

	def __R(self, step):
		self.idx = self.idx + step
		return

	def __L(self, step):
		self.idx = self.idx - step
		return

	@printSeq
	def _configuration_b(self):
		self.__P('@')
		self.__R(1)
		self.__P('1')

		self._configuration_new()
		return

	@printSeq
	def _configuration_new(self):
		if self.seq[self.idx] == '@':
			self.__R(1)
			self._configuration_mark_digits()
		else:
			self.__L(1)
			self._configuration_new()
		return

	@printSeq
	def _configuration_mark_digits(self):
		if self.seq[self.idx] == '0' or self.seq[self.idx] == '1':
			self.__R(1)
			self.__P('x')
			self.__R(1)
			self._configuration_mark_digits()
		elif self.seq[self.idx] == '_':
			self.__R(1)
			self.__P('z')
			self.__R(2)
			self.__P('r')
			self._configuration_find_x()
		else:
			print("ERROR in mark digits")
		return

	@printSeq
	def _configuration_find_x(self):
		if self.seq[self.idx] == 'x':
			self.__E()
			self._configuration_first_r()
		elif self.seq[self.idx] == '@':
			##############   N
			self._configuration_find_digits()
		else:
			self.__L(2)
			self._configuration_find_x()

		return

	@printSeq
	def _configuration_first_r(self):
		if self.seq[self.idx] == 'r':
			self.__R(2)
			self._configuration_last_r()
		else:
			self.__R(2)
			self._configuration_first_r()

		return

	@printSeq
	def _configuration_last_r(self):
		if self.seq[self.idx] == 'r':
			self.__R(2)
			self._configuration_last_r()
		elif self.seq[self.idx] == '_':
			self.__P('r')
			self.__R(2)
			self.__P('r')
			self._configuration_find_x()
		else:
			print("ERROR in last r")

		return

	@printSeq
	def _configuration_find_digits(self):
		if self.seq[self.idx] == '@':
			self.__R(2)
			self._configuration_find_1st_digit()
		else:
			self.__L(2)
			self._configuration_find_digits()

		return

	@printSeq
	def _configuration_find_1st_digit(self):
		if self.seq[self.idx] == 'x' or self.seq[self.idx] == 'y':
			self.__L(1)
			self._configuration_found_1st_digit()
		elif self.seq[self.idx] == 'z':
			self.__L(1)
			self._configuration_found_2nd_digit()
		elif self.seq[self.idx] == '_':
			self.__R(2)
			self._configuration_find_1st_digit()
		else:
			print("ERROR in find 1st digit.")

		return

	@printSeq
	def _configuration_found_1st_digit(self):
		if self.seq[self.idx] == '0':
			self.__R(1)
			self._configuration_add_zero()
		elif self.seq[self.idx] == '1':
			self.__R(3)
			self._configuration_find_2nd_digit()
		else:
			print("ERROR in found 1st digit.")
		return

	@printSeq
	def _configuration_find_2nd_digit(self):
		if self.seq[self.idx] == 'x' or self.seq[self.idx] == 'y':
			self.__L(1)
			self._configuration_found_2nd_digit()
		elif self.seq[self.idx] == '_':
			self.__R(2)
			self._configuration_find_2nd_digit()
		else:
			print("ERROR in find 2nd digit.")

		return

	@printSeq
	def _configuration_found_2nd_digit(self):
		if self.seq[self.idx] == '0':
			self.__R(1)
			self._configuration_add_zero()
		elif self.seq[self.idx] == '1' or self.seq[self.idx] == '_':
			self.__R(1)
			self._configuration_add_one()
		else:
			print("ERROR in found 2nd digit.")
		return

	@printSeq
	def _configuration_add_zero(self):
		if self.seq[self.idx] == 'r':
			self.__P('s')
			self._configuration_add_finished()
		elif self.seq[self.idx] == 'u':
			self.__P('v')
			self._configuration_add_finished()
		else:
			self.__R(2)
			self._configuration_add_zero()
		return

	@printSeq
	def _configuration_add_one(self):
		if self.seq[self.idx] == 'r':
			self.__P('v')
			self._configuration_add_finished()
		elif self.seq[self.idx] == 'u':
			self.__P('s')
			self.__R(2)
			self._configuration_carry()
		else:
			self.__R(2)
			self._configuration_add_one()
		return

	@printSeq
	def _configuration_carry(self):
		if self.seq[self.idx] == 'r':
			self.__P('u')
			self._configuration_add_finished()
		elif self.seq[self.idx] == '_':
			self.__P('u')
			self._configuration_new_digit_is_zero()
		elif self.seq[self.idx] == 'u':
			self.__P('r')
			self.__R(2)
			self._configuration_carry()
		else:
			print("ERROR in carry.")
		return

	@printSeq
	def _configuration_add_finished(self):
		if self.seq[self.idx] == '@':
			self.__R(2)
			self._configuration_erase_old_x()
		else:
			self.__L(2)
			self._configuration_add_finished()
		return

	@printSeq
	def _configuration_erase_old_x(self):
		if self.seq[self.idx] == 'x':
			self.__E()
			self.__L(2)
			self._configuration_print_new_x()
		elif self.seq[self.idx] == 'z':
			self.__P('y')
			self.__L(2)
			self._configuration_print_new_x()
		else:
			self.__R(2)
			self._configuration_erase_old_x()
		return

	@printSeq
	def _configuration_print_new_x(self):
		if self.seq[self.idx] == '@':
			self.__R(2)
			self._configuration_erase_old_y()
		elif self.seq[self.idx] == 'y':
			self.__P('z')
			self._configuration_find_digits()
		elif self.seq[self.idx] == '_':
			self.__P('x')
			self._configuration_find_digits()
		else:
			print("ERROR in print new x.")
		return

	@printSeq
	def _configuration_erase_old_y(self):
		if self.seq[self.idx] == 'y':
			self.__E()
			self.__L(2)
			self._configuration_print_new_y()
		else:
			self.__R(2)
			self._configuration_erase_old_y()
		return

	@printSeq
	def _configuration_print_new_y(self):
		if self.seq[self.idx] == '@':
			self.__R(1)
			self._configuration_new_digit_is_one()
		else:
			self.__P('y')
			self.__R(1)
			self._configuration_reset_new_x()
		return

	@printSeq
	def _configuration_reset_new_x(self):
		if self.seq[self.idx] == '_':
			self.__R(1)
			self.__P('x')
			self._configuration_flag_result_digits()
		else:
			self.__R(2)
			self._configuration_reset_new_x()
		return

	@printSeq
	def _configuration_flag_result_digits(self):
		if self.seq[self.idx] == 's':
			self.__P('t')
			self.__R(2)
			self._configuration_unflag_result_digits()
		elif self.seq[self.idx] == 'v':
			self.__P('w')
			self.__R(2)
			self._configuration_unflag_result_digits()
		else:
			self.__R(2)
			self._configuration_flag_result_digits()
		return

	@printSeq
	def _configuration_unflag_result_digits(self):
		if self.seq[self.idx] == 's':
			self.__P('r')
			self.__R(2)
			self._configuration_unflag_result_digits()
		elif self.seq[self.idx] == 'v':
			self.__P('u')
			self.__R(2)
			self._configuration_unflag_result_digits()
		else:
			################# N
			self._configuration_find_digits()
		return

	@printSeq
	def _configuration_new_digit_is_zero(self):
		if self.seq[self.idx] == '@':
			self.__R(1)
			self._configuration_print_zero_digit()
		else:
			self.__L(1)
			self._configuration_new_digit_is_zero()
		return

	@printSeq
	def _configuration_print_zero_digit(self):
		if self.seq[self.idx] == '0' or self.seq[self.idx] == '1':
			self.__R(1)
			self.__E()
			self.__R(1)
			self._configuration_print_zero_digit()
		elif self.seq[self.idx] == '_':
			self.__P('0')
			self.__R(3)
			self._configuration_cleanup()
		else:
			print("ERROR in print zero digit.")
		return

	@printSeq
	def _configuration_new_digit_is_one(self):
		if self.seq[self.idx] == '@':
			self.__R(1)
			self._configuration_print_one_digit()
		else:
			self.__L(1)
			self._configuration_new_digit_is_one()
		return

	@printSeq
	def _configuration_print_one_digit(self):
		if self.seq[self.idx] == '0' or self.seq[self.idx] == '1':
			self.__R(1)
			self.__E()
			self.__R(1)
			self._configuration_print_one_digit()
		elif self.seq[self.idx] == '_':
			self.__P('1')
			self.__R(3)
			self._configuration_cleanup()
		else:
			print("ERROR in print zero digit.")
		return

	@printSeq
	def _configuration_cleanup(self):
		if self.seq[self.idx] == '_':
			############# N
			self._configuration_new()
		else:
			self.__E()
			self.__R(2)
			self._configuration_cleanup()

	def start(self):
		self._configuration_b()

if __name__=='__main__':  
	testTuring = TuringConfiguration()
	testTuring.start()