import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from student_utils import *
from utils import *




def ind_path_to_locs(path,locs):
	return [locs[i] for i in path]

def trivial_stops(houses):
	hlist = []
	for house in houses:
		hlist.append([house, house])
	return hlist




def get_output(filename):
	input = read_file(filename)
	output = input_to_output(filename)
	num_loc, num_house, locs, houses, start_loc, adj = data_parser(input)
	G = adjacency_matrix_to_graph(adj)[0]

	house_ind = convert_locations_to_indices(houses,locs)
	start_loc_ind = convert_locations_to_indices([start_loc],locs)
	path_inds = start_loc_ind + house_ind + start_loc_ind
	nx.draw(G)
	

	# print(nx.find_cycle(G))

	#Find a greedy-ish path that goes to every house 
	path = []
	for i in range(len(path_inds)-1):
		path.extend(nx.shortest_path(G,path_inds[i],path_inds[i+1])[:-1])
	path.extend(start_loc_ind)

	loc_path = ind_path_to_locs(path,locs) #convert the path from indicies to names of locations
	stops = trivial_stops(houses) #get stops for every house

	write_data_to_file(output, loc_path, ' ', append = False)
	write_to_file(output,'\n',append = True)
	write_to_file(output,str(num_house) + '\n',append = True)
	for stop in stops:
		write_data_to_file(output,stop,' ', append = True)
		write_to_file(output,'\n',append = True)

	plt.show()

files = ('input/50.in','input/100.in', 'input/200.in')

for file in files:
	get_output(file)


