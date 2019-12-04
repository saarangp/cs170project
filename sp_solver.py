#TRY INSTALING python-louvain
from collections import OrderedDict
import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
from utils import *
import networkx as nx
from student_utils import *
import matplotlib.pyplot as plt
import pprint





def draw_network(G, house_ind,cc):
	_,weights = zip(*nx.get_edge_attributes(G,'weight').items())
	pos = nx.spring_layout(G)
	nx.draw_networkx_nodes(G, pos, 
	                   node_color='r',
	                   node_size=50,
	               alpha=0.8)
	nx.draw_networkx_nodes(G, pos, 
	                   nodelist=house_ind,
	                   node_color=cc,
	                   node_size=50,
	               alpha=0.8)
	nx.draw_networkx_edges(G,pos,width=1.0, edge_color=weights,edge_cmap=plt.cm.Blues)
	plt.show()
	# print(G.edges.data())

def modified_voronoi(G, house_ind,num_loc):
	#returns array where ith house is closest to A[i] location
	#returns dictionary keyed by locations and houses closest to them
	loc_vor = {}
	vor = []
	locs = [i for i in range(num_loc) if i not in house_ind]
	for l in locs:
		loc_vor[l] = []

	for hou in house_ind:
		h = []
		for loc in locs:
			h.append((loc,nx.shortest_path_length(G,loc,hou,weight = 'weight')))
		vor.append(h)
	closest_centroid = [min(dist, key=lambda d: d[1])[0] for dist in vor]

	for i in range(len(closest_centroid)):
		loc_vor[closest_centroid[i]].append(house_ind[i])

	return closest_centroid,loc_vor

def find_path(G, house_ind,num_loc,lv,start):
	#shrink lv
	[lv.pop(i) for i in list(lv.keys()) if len(lv[i])<1]
	path = []
	dropoffs = {}
	sorted_keys_lv = sorted(lv, key=lambda k: len(lv[k]), reverse=True)
	currpos = start
	for stop in sorted_keys_lv:
		path.extend(nx.shortest_path(G,currpos,stop,weight = 'weight')[:-1])
		currpos = stop
		for i in lv[stop]:
			house_ind.remove(i)
		dropoffs[stop] = lv[stop]

	if len(house_ind) > 0:
		for house in house_ind:
			path.extend(nx.shortest_path(G,currpos,house,weight = 'weight')[:-1])
			currpos = house
			house_ind.pop(house)
			dropoffs[house] = house

	path.extend(nx.shortest_path(G,currpos,start,weight = 'weight')[:-1])
	path.extend([start])
	return path,dropoffs

def ind_path_to_locs(path,locs):
	return [locs[i] for i in path]

def stops_to_text(dropoffs, locs):
	text = ''
	for key in dropoffs.keys():
		text += locs[key] + ' '
		text += ' '.join(ind_path_to_locs(dropoffs[key],locs))
		text+= '\n'
	return text

def output_text(path,dropoffs,locs):
	pathtext = ind_path_to_locs(path,locs)
	print(' '.join(pathtext))
	print(len(dropoffs.keys()))
	print(stops_to_text(dropoffs,locs))





filename = '50.in'

#Parse input file and convert to nx graph
input = read_file(filename)
num_loc, num_house, locs, houses, start_loc, adj = data_parser(input)
start = convert_locations_to_indices([start_loc],locs)[0]
G = adjacency_matrix_to_graph(adj)[0]
house_ind = convert_locations_to_indices(houses,locs)

# Gets modified voronoi for houses and locations to figure out optimal stops.
cc,lv = modified_voronoi(G, house_ind,num_loc)

path,dropoffs = find_path(G, house_ind,num_loc,lv,start)
print(path)
print(dropoffs)


output_text(path,dropoffs,locs)


# draw_network(G,house_ind,cc)



