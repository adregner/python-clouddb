#!/usr/bin/env python

class Hm(object):

	def __init__(self):
		print 'init'
		self._data = {}
		print self, self.__dict__
		print 'init done'

	def __setattr__(self, k, v):
		print 'setattr', k, v
		#self._data[k] = v
		getattr(self, '_data')[k] = v
		print 'done setting attr'

	def __getattr__(self, k):
		print 'getattr', k
		#return self._data[k]
		return getattr(self, k)


obj = Hm()
print obj
