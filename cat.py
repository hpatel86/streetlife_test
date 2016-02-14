import random

class Cat(object):

	def __init__(self, cat_id, initial_posn):
		self.cat_id = cat_id
		self.cur_posn = initial_posn
		self.prev_posn = None
		self.found = False
		self.trapped = False

	def move(self, edges):
		if self.found or self.trapped:
			return

		if edges:
			self.prev_posn = self.cur_posn
			self.cur_posn = random.choice(edges)
		else:
			self.trapped = True


	def __str__(self):
		return 'Cat %d'%self.cat_id
