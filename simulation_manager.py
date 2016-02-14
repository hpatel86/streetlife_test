import csv
import sys
import random

from station_connections import StationConnections
from owner import Owner
from cat import Cat

class SimulationManager(object):

	def __init__(self, num_owners, stations_file, connections_file):
		self.num_cats = num_owners
		self.read_data(stations_file, connections_file)
		self.create_owners_and_cats()
		self.max_iters = 100000
		self.total_cats_found = 0
		self.number_of_moves = []


	def read_data(self, stations_file, connections_file):

		with open(stations_file) as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			self.tfl_stations = {int(row[0]): row[1] for row in reader}

		self.tfl_connections = StationConnections()
		with open(connections_file) as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				self.tfl_connections.add_connection(row)


	def create_owners_and_cats(self):
		self.owners = []
		self.cats = []

		station_ids = self.tfl_connections.get_all_stations()

		for idx in range(1, self.num_cats+1):
			owner_posn, cat_posn = random.sample(station_ids, 2)

			cat = Cat(idx, cat_posn)
			owner = Owner(idx, owner_posn, cat)

			self.owners.append(owner)
			self.cats.append(cat)


	def run_simulation(self):
		iters = 0
		owner_idxs = range(self.num_cats)
		idx_to_skip = set([])

		while iters < self.max_iters and \
			self.total_cats_found < self.num_cats:

			closed_station_ids = set([])

			for i in owner_idxs:

				connecting_stations_cat = self.tfl_connections.get_connecting_stations(
					self.cats[i].cur_posn
				)

				connecting_stations_owner = self.tfl_connections.get_connecting_stations(
					self.owners[i].cur_posn
				)
				self.cats[i].move(connecting_stations_cat)
				self.owners[i].move(connecting_stations_owner)

				if self.cats[i].trapped or self.owners[i].trapped:
					owner_idxs.remove(i)

				if self.cats[i].get_current_position() == \
					self.owners[i].get_current_position():
					owner_idxs.remove(i)

					self._process_owner_found_cat(
						self.owners[i],
						self.cats[i],
						iters
					)
					closed_station_ids.add(
						self.owners[i].get_current_position()
					)

			if closed_station_ids:
				self.tfl_connections.remove_closed_stations(closed_station_ids)

			iters += 1

		self._print_simulation_statistics()


	def _process_owner_found_cat(self, owner, cat, num_moves):
		self.total_cats_found += 1
		self.number_of_moves.append(num_moves)

		owner.found_cat = True
		cat.found = True

		station_id = owner.get_current_position()
		print '%s found %s - %s is now closed'% \
			(owner, cat, self.tfl_stations[owner.get_current_position()])


	def _print_simulation_statistics(self):
		print 'Total number of cats %s'%self.num_cats
		print 'Number of cats found %s'%self.total_cats_found
		print 'Average number of movements required to find a cat %s'\
			%int(sum(self.number_of_moves)/float(self.total_cats_found))
