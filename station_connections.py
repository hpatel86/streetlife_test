""" Station connections class - mange adding and deleting stations """

from collections import defaultdict

class StationConnections(object):

	def __init__(self):
		self.__connections = defaultdict(set)
		self.__closed_stations = {}


	def add_connection(self, edges):
		edge1, edge2 = map(int, edges)
		self.__connections[edge1].add(edge2)
		self.__connections[edge2].add(edge1)


	def get_all_stations(self):
		return list(self.__connections.keys())


	def get_connecting_stations(self, station_id):
		try:
			return list(self.__connections[station_id])
		except KeyError:
			return []


	def remove_closed_stations(self, closed_station_ids):
		if type(closed_station_ids) not in (list, set):
			raise TypeError('Closed station ids must be a list')

		for station_id in closed_station_ids:
			connected_station_ids = self.__connections.pop(station_id)
			self.__closed_stations[station_id] = connected_station_ids
			for connected_station_id in connected_station_ids:
				self.__connections[connected_station_id].remove(station_id)

