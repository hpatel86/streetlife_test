import sys
import unittest
import mock

sys.path += ['../']

from cat import (
	Cat,
	random
)


class TestCat(unittest.TestCase):

	def setUp(self):
		self.cat_id = 1
		self.initial_posn = 1
		self.obj = Cat(self.cat_id, self.initial_posn)


	def tearDown(self):
		self.obj = Cat(self.cat_id, self.initial_posn)


	def test_get_current_position(self):
		self.assertEqual(self.obj.get_current_position(), self.initial_posn)


	def test_set_cat_move_found(self):
		edges = {self.initial_posn: [2, 3, 4]}
		self.obj.found = True
		self.obj.move(edges)
		self.assertEqual(self.obj.get_current_position(), self.initial_posn)


	def test_set_cat_move_trapped(self):
		edges = {self.initial_posn: [2, 3, 4]}
		self.obj.trapped = True
		self.obj.move(edges)
		self.assertEqual(self.obj.get_current_position(), self.initial_posn)


	def test_set_cat_move_not_trapped(self):
		edges = [2, 3, 4]
		self.obj.move(edges)
		self.assertFalse(self.obj.trapped)


	@mock.patch('cat.random')
	def test_cat_new_position(self, random_mock):
		edges = [2, 3, 4]
		random_mock.choice.return_value = edges[1]
		self.obj.move(edges)
		self.assertEqual(self.obj.get_current_position(), edges[1])


	def test_cat_trapped_no_edges(self):
		edges = []
		self.obj.move(edges)
		self.assertTrue(self.obj.trapped)


if __name__ == '__main__':
	unittest.main()

