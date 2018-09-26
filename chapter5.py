#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys

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

	def __printC(self, print_char):
		self.seq[self.idx] = print_char
		return

	def __earse(self):
		self.seq[self.idx] = '_'
		return

	def __right(self, step):
		self.idx = self.idx + step
		return

	def __left(self, step):
		self.idx = self.idx - step
		return

	@printSeq
	def _configuration_b(self):
		self.__printC('e')
		self.__right(1)
		self.__printC('e')
		self.__right(1)
		self.__printC('0')
		self.__right(2)
		self.__printC('0')
		self.__left(2)

		# switch to Model o
		self._configuration_o()

		return

	@printSeq
	def _configuration_o(self):
		if self.seq[self.idx] == '1':
			self.__right(1)
			self.__printC('x')
			self.__left(3)
			self._configuration_o()
		elif self.seq[self.idx] == '0':
			#switch to Model q
			self._configuration_q()
		else:
			print("ERROR status in model o.")

		return

	@printSeq
	def _configuration_q(self):
		if self.seq[self.idx] == '0' or self.seq[self.idx] == '1':
			self.__right(2)
			self._configuration_q()
		elif self.seq[self.idx] == '_':
			self.__printC('1')
			self.__left(1)
			self._configuration_p()
		else:
			print("ERROR status in model q.")

		return

	@printSeq
	def _configuration_p(self):
		if self.seq[self.idx] == 'x':
			self.__earse()
			self.__right(1)
			self._configuration_q()
		elif self.seq[self.idx] == 'e':
			self.__right(1)
			self._configuration_f()
		elif self.seq[self.idx] == '_':
			self.__left(2)
			self._configuration_p()
		else:
			print("ERROR status in model p.")

		return

	@printSeq
	def _configuration_f(self):
		if self.seq[self.idx] == '0' or self.seq[self.idx] == '1':
			self.__right(2)
			self._configuration_f()
		elif self.seq[self.idx] == '_':
			self.__printC('0')
			self.__left(2)
			self._configuration_o()
		else:
			print("ERROR status in model f.")
		
		return

	def start(self):
		self._configuration_b()

if __name__=='__main__':  
	testTuring = TuringConfiguration()
	testTuring.start()