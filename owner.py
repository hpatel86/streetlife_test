from collections import defaultdict

class Owner(object):

	def __init__(self, owner_id, initial_posn, cat):
		self.owner_id = owner_id
		self.cat = cat
		self.cur_posn = initial_posn
		self.visited = defaultdict(int)
		self.visited[self.cur_posn] += 1
		self.found_cat = False
		self.trapped = False


	def move(self, edges):
		if self.found_cat or self.trapped or not edges:
			if not edges:
				self.trapped = True

			return None

		min_cost = None

		for edge in sorted(edges):
			if edge not in self.visited:
				self.cur_posn = edge
				break

			else:
				if min_cost is None or self.visited[edge] < min_cost:
					min_cost = self.visited[edge]
					self.cur_posn = edge


		self.visited[self.cur_posn] += 1


	def get_current_position(self):
		return self.cur_posn


	def __str__(self):
		return 'Owner %d'%self.owner_id
