import csv
import sys
import random

from collections import defaultdict

from owner import Owner
from cat import Cat

TFL_STATIONS = None
TFL_CONNECTIONS = None
OWNERS = None
CATS = None
N = 10
MAX_ITERS = 100000


def read_data():
	tfl_stations = 'data/tfl_stations.csv'
	tfl_connections = 'data/tfl_connections.csv'

	global TFL_CONNECTIONS, TFL_STATIONS
	TFL_STATIONS = {}

	with open(tfl_stations) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		TFL_STATIONS = {int(row[0]): row[1] for row in reader}

	TFL_CONNECTIONS = defaultdict(set)
	with open(tfl_connections) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			TFL_CONNECTIONS[int(row[0])].add(int(row[1]))
			TFL_CONNECTIONS[int(row[1])].add(int(row[0]))


def create_owners_and_cats():
	global OWNERS, CATS
	OWNERS = []
	CATS = []

	virtices = TFL_CONNECTIONS.keys()

	for _id in range(1, N+1):
		owner_posn, cat_posn = random.sample(virtices, 2)

		cat = Cat(_id, cat_posn)
		owner = Owner(_id, owner_posn, cat)

		OWNERS.append(owner)
		CATS.append(cat)


def unleash_owners_and_cats():
	iters = 0
	cats_found = 0
	number_of_moves = []

	while iters < MAX_ITERS and cats_found < N:
		stations_cats_found = set([])

		for i in range(N):
			CATS[i].move(list(TFL_CONNECTIONS[CATS[i].cur_posn]))
			found = OWNERS[i].move(list(TFL_CONNECTIONS[OWNERS[i].cur_posn]))

			if found:
				cats_found += 1
				number_of_moves.append(iters+1)
				station_cat_found = OWNERS[i].cur_posn
				stations_cats_found.add(station_cat_found)
				print '%s found %s - %s is now closed'% \
					(OWNERS[i], CATS[i], TFL_STATIONS[station_cat_found])

		if len(stations_cats_found):
			for station in stations_cats_found:
				edges = TFL_CONNECTIONS.pop(station)
				for edge in edges:
					TFL_CONNECTIONS[edge].remove(station)

		iters += 1

	print 'Total number of cats %s'%N
	print 'Number of cats found %s'%cats_found


def run():
	read_data()
	create_owners_and_cats()
	unleash_owners_and_cats()


if __name__ == '__main__':
	run()
