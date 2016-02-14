import sys
from simulation_manager import SimulationManager


def read_num_cats_from_stdin():
	try:
		print 'Enter number of cats:'
		num_cats = sys.stdin.readline()
		num_cats = int(num_cats)
		valid_input = True
	except ValueError:
		print 'Number of cats must be an iteger'
		num_cats = sys.stdin.readline()
		num_cats = int(num_cats)
		valid_input = True

	return num_cats


def run():

	num_cats = read_num_cats_from_stdin()

	sim_mgr = SimulationManager(
		num_cats,
		'data/tfl_stations.csv',
		'data/tfl_connections.csv'
	)
	sim_mgr.run_simulation()


if __name__ == '__main__':
	run()
