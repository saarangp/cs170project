from student_utils import *
from utils import *
import numpy as np
import networkx as nx
import sys, os
import matplotlib.pyplot as plt

def add_node_attributes(G, house_ind):
	is_house = {v:int(v in house_ind) for v in list(G.nodes)}
	# Adding node properties to graph. These will become very important with graph pruning and a node can be used as an abstraction for a subtree.
	# Trees have an analytic solution to the optimal drop off points, so the goal is to use node properties to abstract away dropoffs along a tree.
	# "Residents" refers to the number of students who live at a location or its subtree
	# "Base Walking Cost" is the base cost of all residents walking to their respective homes along a subtree T rooted at v
	# "Base Driving Cost" is the base cost of the optimal driving path along a subtree plus the cost of individual TAs walking to their homes
	# NOTE: if the root v of a subtree T is included in the driving path, we can add the Base Driving Cost to the cost of G \ T because this is the
	# lowest cost of dropping off all TAs on T. However, if v is not in the driving path, then we MUST use the Base Walking Cost, which is always
	# larger than the base driving cost
	# "Abbreviated Path" is the path we must add on to our final driving path if we use the Base Driving Cost of v
	zeros_dict = {v:0 for v in list(G.nodes)}
	none_dict = {v:None for v in list(G.nodes)}
	nx.set_node_attributes(G, is_house, 'residents')
	nx.set_node_attributes(G, zeros_dict, 'base_walking_cost')
	nx.set_node_attributes(G, zeros_dict, 'base_driving_cost')
	nx.set_node_attributes(G, [None for _ in range(len(G.nodes))], 'abbreviated_path')
	return G

def sort_list(list1, list2): #sorts elements in list1 according to values in list2
    zipped_pairs = zip(list2, list1) 
    z = [x for _, x in sorted(zipped_pairs)] 
    return z 

def prune_leaves(G):
	# This should keep updated even when graph is changed
	residents = nx.get_node_attributes(G, 'residents')
	r = sort_list(residents.keys(), residents.values())
	for v in r:
		prune_branch(G, v, residents)

def prune_branch(G, v, res):
	if len(G[v]) < 2:
		neighbor = [u for u in G[v]][0] #because I couldn't find another way of doing this
		if res[v] == 0:
			G.remove_node()
			prune_branch(G, u, res) #recursively prune along a branch
		else:
			G.node[neighbor]['residents'] += G.node[v]['residents']
			G.node[neighbor]['base_walking_cost'] += G.node[v]['base_walking_cost'] \
			+ G.node[v]['residents'] * G.edge[v][u]['weight']
			G.node[neighbor]['base_driving_cost'] += G.node[v]['base_driving_cost'] \
			+ G.node[v]['residents'] * G.edge[v][u]['weight']



def prepare_file(filename, drawn=False):
	input = read_file(filename)
	output = input_to_output(filename)
	num_loc, num_house, locs, houses, start_loc, adj = data_parser(input)
	G = adjacency_matrix_to_graph(adj)[0]
	house_ind = convert_locations_to_indices(houses,locs)
	start_loc_ind = convert_locations_to_indices([start_loc],locs)
	path_inds = start_loc_ind + house_ind + start_loc_ind
	G = add_node_attributes(G, house_ind)
	if drawn==True:
		draw_network(G, house_ind)
	return G

def find_nearest_centroid(G, centroids):
	h = [v for v in G.nodes() if G.nodes[v]['residents'] >= 1]
	cluster_dict = {v:[] for v in centroids}
	for v in h:
		if v in centroids:
			cluster_dict[v].append(v)
		else:
			#TODO: add code that finds nearest centroid
			pass
	keys = [i for i in cluster_dict.keys()]
	for c in keys:
		if cluster_dict[c] == []:
			cluster_dict.pop(c)
	return cluster_dict




def draw_network(G, house_ind):
	pos = nx.spring_layout(G)
	nx.draw_networkx_nodes(G, pos, 
                       node_color='b',
                       node_size=50,
                   alpha=0.8)
	nx.draw_networkx_nodes(G, pos, 
                       nodelist=house_ind,
                       node_color='r',
                       node_size=50,
                   alpha=0.8)
	nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)
	plt.show()
	print(G.edges.data())

prepare_file("input/50.in")