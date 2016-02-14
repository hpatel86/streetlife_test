import csv
import sys
import random


from station_connections import StationConnections
from owner import Owner
from cat import Cat

TFL_STATIONS = None
TFL_CONNECTIONS = None
OWNERS = None
CATS = None
N = 200
MAX_ITERS = 100000


class SimulationManager(object):

	def __init__(self, num_owners):
		self.num_cats = num_owners
		self.read_data()
		self.create_owners_and_cats()
		self.max_iters = 100000
		self.total_cats_found = 0
		self.number_of_moves = []


	def read_data(self):
		tfl_stations = 'data/tfl_stations.csv'
		tfl_connections = 'data/tfl_connections.csv'

		with open(tfl_stations) as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			self.tfl_stations = {int(row[0]): row[1] for row in reader}

		self.tfl_connections = StationConnections()
		with open(tfl_connections) as csvfile:
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


def read_data():
	tfl_stations = 'data/tfl_stations.csv'
	tfl_connections = 'data/tfl_connections.csv'

	global TFL_CONNECTIONS, TFL_STATIONS
	TFL_STATIONS = {}

	with open(tfl_stations) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		TFL_STATIONS = {int(row[0]): row[1] for row in reader}

	TFL_CONNECTIONS = StationConnections()
	with open(tfl_connections) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			TFL_CONNECTIONS.add_connection(row)


def create_owners_and_cats():
	global OWNERS, CATS
	OWNERS = []
	CATS = []

	station_ids = TFL_CONNECTIONS.get_all_stations()

	for _id in range(1, N+1):
		owner_posn, cat_posn = random.sample(station_ids, 2)

		cat = Cat(_id, cat_posn)
		owner = Owner(_id, owner_posn, cat)

		OWNERS.append(owner)
		CATS.append(cat)


def unleash_owners_and_cats():
	iters = 0
	cats_found = 0
	number_of_moves = []
	owner_cats_found = set([])
	trapped_cats = set([])
	trapped_owners = set([])

	while iters < MAX_ITERS and cats_found < N:
		closed_station_ids = set([])

		for i in range(N):
			if i in owner_cats_found or i in trapped_cats or i in trapped_owners:
				continue

			connecting_stations_cat = TFL_CONNECTIONS.get_connecting_stations(
				CATS[i].cur_posn
			)

			connecting_stations_owner = TFL_CONNECTIONS.get_connecting_stations(
				OWNERS[i].cur_posn
			)
			CATS[i].move(connecting_stations_cat)
			OWNERS[i].move(connecting_stations_owner)

			if CATS[i].trapped:
				trapped_cats.add(i)

			if OWNERS[i].trapped:
				trapped_owners.add(i)

			if CATS[i].get_current_position() == OWNERS[i].get_current_position():
				owner_cats_found.add(i)
				OWNERS[i].found_cat = True
				CATS[i].found = True
				cats_found += 1
				number_of_moves.append(iters)
				station_cat_found = OWNERS[i].get_current_position()
				closed_station_ids.add(station_cat_found)
				print '%s found %s - %s is now closed'% \
					(OWNERS[i], CATS[i], TFL_STATIONS[station_cat_found])


		if closed_station_ids:
			TFL_CONNECTIONS.remove_closed_stations(closed_station_ids)

		iters += 1

	print 'Total number of cats %s'%N
	print 'Number of cats found %s'%cats_found
	print 'Average number of movements required to find a cat %s'\
		%int(sum(number_of_moves)/float(cats_found))


def run():

	sim_mgr = SimulationManager(200)
	sim_mgr.run_simulation()

	#read_data()
	#create_owners_and_cats()
	#unleash_owners_and_cats()


if __name__ == '__main__':
	run()
