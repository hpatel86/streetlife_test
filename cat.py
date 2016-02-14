""" Cat class """

import random

class Cat(object):

	def __init__(self, cat_id, initial_posn):
		self.__cat_id = cat_id
		self.__cur_posn = initial_posn
		self.found = False
		self.trapped = False

	def move(self, edges):
		if self.found or self.trapped:
			return

		if edges:
			self.__cur_posn = random.choice(edges)
		else:
			self.trapped = True


	def get_current_position(self):
		return self.__cur_posn


	def __str__(self):
		return 'Cat %d'%self.__cat_id
