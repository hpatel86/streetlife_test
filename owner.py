""" Owner class """

from collections import defaultdict

class Owner(object):

	def __init__(self, owner_id, initial_posn):
		self.__owner_id = owner_id
		self.__cur_posn = initial_posn
		self.__visited = defaultdict(int)
		self.__visited[self.__cur_posn] += 1
		self.found_cat = False
		self.trapped = False


	def move(self, edges):
		""" 1. Move to an edge we haven't visited with the minimum value
									OR
			2. If visited all the edges, then visit the one we have visited
				the least
		"""

		if self.found_cat or self.trapped:
			return

		if not edges:
			self.trapped = True
			return

		min_cost = None

		for edge in sorted(edges):
			if edge not in self.__visited:
				self.__cur_posn = edge
				break

			else:
				if min_cost is None or self.__visited[edge] < min_cost:
					min_cost = self.__visited[edge]
					self.__cur_posn = edge

		self.__visited[self.__cur_posn] += 1


	def get_current_position(self):
		return self.__cur_posn


	def __str__(self):
		return 'Owner %d'%self.__owner_id
