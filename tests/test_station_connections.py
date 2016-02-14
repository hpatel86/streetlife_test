import sys
import unittest
import mock
from collections import defaultdict

sys.path += ['../']

from station_connections import StationConnections

class TestStationConnections(unittest.TestCase):

	def setUp(self):
		self.edges = [
			(1, 2),
			(3, 4),
			(3, 5),
		]

		self.obj = StationConnections()
		for edge in self.edges:
			self.obj.add_connection(edge)


	def tearDown(self):
		self.obj = StationConnections()
		for edge in self.edges:
			self.obj.add_connection(edge)


	def test_add_connection(self):
		self.assertEqual(
			self.obj._StationConnections__connections[3],
			set([4, 5])
		)


	def test_get_all_connections(self):
		all_stations = set([])
		for edge in self.edges:
			all_stations.add(edge[0])
			all_stations.add(edge[1])

		self.assertListEqual(self.obj.get_all_stations(), list(all_stations))


	def test_remove_closed_stations_raise_typeerror_integer(self):
		self.assertRaises(TypeError, lambda: self.obj.remove_closed_stations(1))


	def test_remove_closed_stations_raise_typeerror_nonetype(self):
		self.assertRaises(
			TypeError,
			lambda: self.obj.remove_closed_stations(None)
		)


	def test_remove_closed_stations(self):
		self.obj.remove_closed_stations([1])
		self.assertNotIn([1], self.obj.get_all_stations())


if __name__ == '__main__':
	unittest.main()
