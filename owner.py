from collections import defaultdict

class Owner(object):

	def __init__(self, owner_id, initial_posn, cat):
		self.owner_id = owner_id
		self.cat = cat
		self.cur_posn = initial_posn
		self.visited = defaultdict(int)
		self.visited[self.cur_posn] += 1
		self.prev_posn = None
		self.found_cat = False
		self.trapped = False


	def move(self, edges):
		if self.found_cat or self.trapped:
			return

		if not edges:
			self.trapped = True
			return

		else:
			self.prev_posn = self.cur_posn
			min_visited_node = None
			min_visited_cnt = None

			if len(edges) == 1:
				self.cur_posn = edges[0]

			else:
				for edge in sorted(edges):
					if edge in self.visited:
						if min_visited_node is None or \
							self.visited[edge] < min_visited_cnt:
							min_visited_node = edge
							min_visited_cnt = self.visited[edge]
						continue

					self.cur_posn = edge
					break

			if self.cur_posn == self.prev_posn:
				self.cur_posn = min_visited_node

			self.visited[self.cur_posn] += 1

		self.found_cat = self.cat.cur_posn == self.cur_posn
		self.cat.found = self.found_cat

		return self.found_cat


	def __str__(self):
		return 'Owner %d'%self.owner_id
