import sys
import unittest
import mock
from collections import defaultdict

sys.path += ['../']

from simulation_manager import SimulationManager


class TestSimulationManager(unittest.TestCase):

	def setUp(self):
		self.num_cats = 10
		self.station_file = '../data/tfl_stations.csv'
		self.connection_file = '../data/tfl_connections.csv'
		self.obj = SimulationManager(
			self.num_cats,
			self.station_file,
			self.connection_file
		)


	def tearDown(self):
		self.obj = SimulationManager(
			self.num_cats,
			self.station_file,
			self.connection_file
		)


	def test_create_owners_and_cats_num_owners(self):
		self.assertEqual(len(self.obj.owners), self.num_cats)


	def test_create_owners_and_cats_num_cats(self):
		self.assertEqual(len(self.obj.cats), self.num_cats)


	def test_create_owners_and_cats_unique_starting_positions(self):
		for i in range(self.num_cats):
			self.assertNotEqual(
				self.obj.owners[i].get_current_position(),
				self.obj.cats[i].get_current_position()
			)


if __name__ == '__main__':
	unittest.main()
