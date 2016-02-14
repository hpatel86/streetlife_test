import sys
import unittest
import mock
from collections import defaultdict


sys.path += ['../']

from owner import Owner

class TestOwner(unittest.TestCase):

	def setUp(self):
		self.owner_id = 1
		self.initial_posn = 2
		self.obj = Owner(self.owner_id, self.initial_posn)


	def tearDown(self):
		self.obj = Owner(self.owner_id, self.initial_posn)


	def test_initial_position(self):
		self.assertEqual(self.obj.get_current_position(), self.initial_posn)


	def test_owner_move_lowest_edge_id(self):
		edges = [12, 3, 45]
		self.obj.move(edges)
		self.assertEqual(self.obj.get_current_position(), min(edges))


	def test_owner_move_visits_new_edge(self):
		edges = [12, 3, 45]
		self.obj.move(edges)
		assert self.obj.get_current_position() == 3

		self.obj.move(edges)
		self.assertEqual(self.obj.get_current_position(), 12)


	def test_owner_moves_trapped(self):
		edges = [12, 3, 45]
		self.obj.move(edges)

		new_edges = []
		self.obj.move(new_edges)

		assert self.obj.get_current_position() == 3

		self.assertTrue(self.obj.trapped)


	def test_owner_found_cat_move(self):
		edges = [12, 3, 45]
		self.obj.move(edges)
		self.obj.found_cat = True

		new_edges = [53, 2, 50]
		self.obj.move(new_edges)
		self.assertEqual(self.obj.get_current_position(), min(edges))


	def test_owner_visits_station_edge_with_min_val_after_visiting_all(self):
		edges = [12, 3, 45]

		for i in range(len(edges)+1):
			self.obj.move(edges)

		self.assertEqual(self.obj.get_current_position(), min(edges))


	def test_owner_visits_station_with_min_val_and_min_cost(self):
		edges = [12, 3, 45]

		for i in range(len(edges)+1):
			self.obj.move(edges)

		self.obj.move(edges)
		self.assertEqual(self.obj.get_current_position(), 12)


	def test_owner_visits_edge_with_min_cost(self):
		self.obj._Owner__visited = {
			3 : 3,
			20 : 4,
			40 : 2
		}

		edges = [3, 20, 40]

		self.obj.move(edges)
		self.assertEqual(self.obj.get_current_position(), 40)


	def test_owner_visits_node_not_visited_in_edges(self):
		edges = [1, 4, 6]

		self.obj._Owner__visited = defaultdict(
			int,
			{
				1: 1,
				4: 1
			}
		)

		self.obj.move(edges)
		self.assertEqual(self.obj.get_current_position(), 6)


if __name__ == '__main__':
	unittest.main()
