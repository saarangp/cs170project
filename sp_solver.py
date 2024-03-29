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
import matplotlib.pyplot as p1lt
import pprint
from graph_reduction import *


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

def modified_voronoi(G, house_ind,num_loc,min_clus_size = 2):
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

	max_len = 0
	for key,val in loc_vor.items():
		if len(val) > max_len:
			max_len = len(val)

	if max_len <= min_clus_size:
		min_clus_size = max_len-1
		print('POPOO')

	#add unclaimed houses to clusters
	unclaimed_houses = []
	for i in list(loc_vor.keys()):
		if len(loc_vor[i])<min_clus_size:
			unclaimed_houses.extend(loc_vor[i])
			loc_vor.pop(i)	
	#same clustering as above but particular to the selected ones. 
	uvor = []
	for hou in unclaimed_houses:
		h = []
		for loc in list(loc_vor.keys()):
			h.append((loc,nx.shortest_path_length(G,loc,hou,weight = 'weight')))
		uvor.append(h)

	uclosest_centroid = [min(dist, key=lambda d: d[1])[0] for dist in uvor]

	for i in range(len(uclosest_centroid)):
		loc_vor[uclosest_centroid[i]].append(unclaimed_houses[i])

	return closest_centroid,loc_vor

def cost_clustering(G, start_loc):
	neighbors_cost = []
	residents = nx.get_node_attributes(G, 'residents')
	for v in G.nodes:
		cost = [G.nodes[u]['residents'] * G[u][v]['weight'] for u in G[v]]
		cost = sum(cost)
		neighbors_cost.append(cost)
	centroids = {start_loc:True}
	# for u in G.nodes():
	# 	centroids[u] = False

	for e in G.edges():
		u,v = e[0],e[1]
		if residents[u] == 0 and residents[v] == 0:
			pass
		elif neighbors_cost[u] < neighbors_cost[v]:
			centroids[u] = True
		elif neighbors_cost[u] > neighbors_cost[v]:
			centroids[v] = True
		else:
			centroids[v] = True
			centroids[u] = True

	return centroids





def ind_list_to_loc(l,locs):
	return [locs[i] for i in l]


def find_path(G, house_ind,num_loc,lv,start):
	path = []

	dropoffs = {}

	#for some reason it works better to start greedily go to each cluster
	sorted_keys_lv = sorted(lv, key=lambda k: nx.shortest_path_length(G,start,k,weight = 'weight'),reverse = True) 

	currpos = start
	for stop in sorted_keys_lv:
		path.extend(nx.shortest_path(G,currpos,stop,weight = 'weight')[:-1])
		currpos = stop
		for i in lv[stop]:
			house_ind.remove(i)
		dropoffs[stop] = lv[stop]


	# if len(house_ind) > 0:
	# 	#sorting the remaining houses, howeever doesnt seem to help too much
	# 	# house_ind = sorted(house_ind, key = lambda h: nx.shortest_path_length(G,start,h,weight = 'weight'),reverse = True)
	# 	print('got here')
	# 	while len(house_ind) > 0:
	# 		house = house_ind.pop()
	# 		path.extend(nx.shortest_path(G,currpos,house,weight = 'weight')[:-1])
	# 		currpos = house
	# 		dropoffs[house] = [house]

	path.extend(nx.shortest_path(G,currpos,start,weight = 'weight')[:-1])
	path.extend([start])

	#get rid of walking where we drive through anyways
	for i in list(dropoffs.keys()):
		for d in dropoffs[i]:
			if d in path:
				dropoffs[i].remove(d)
				dropoffs[d] = [d]


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

if __name__ == "__main__":
	filename = 'input/50.in'

	# #Parse input file and convert to nx graph
	# input = read_file(filename)
	# num_loc, num_house, locs, houses, start_loc, adj = data_parser(input)
	# start = convert_locations_to_indices([start_loc],locs)[0]
	# G = adjacency_matrix_to_graph(adj)[0]
	# house_ind = convert_locations_to_indices(houses,locs)
	G = prepare_file(filename)
	residents = nx.get_node_attributes(G, 'residents')
	house_ind = [i for i in G.nodes if residents[i] >= 1]
	centr_cost  = cost_clustering(G, 0)
	print(centr_cost)

# # Gets modified voronoi for houses and locations to figure out optimal stops.

# cc,lv = modified_voronoi(G, house_ind,num_loc)

# path,dropoffs = find_path(G, house_ind,num_loc,lv,start)
# output_text(path,dropoffs,locs)

# # draw_network(G,house_ind,cc)



