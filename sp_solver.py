#TRY INSTALING python-louvain


import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
from utils import *
import networkx as nx
from student_utils import *
import matplotlib.pyplot as plt

def draw_network(G, house_ind):
	_,weights = zip(*nx.get_edge_attributes(G,'weight').items())
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
	nx.draw_networkx_edges(G,pos,width=1.0, edge_color=weights,edge_cmap=plt.cm.Blues)
	plt.show()
	# print(G.edges.data())

def modified_voronoi(G, house_ind,num_loc):
	dic = {}
	vordic = {}
	locs = [i for i in range(num_loc) if i not in house_ind]
	for i in locs:
		dic[i] = nx.single_source_shortest_path_length(G,i)
		vordic[i] = locs

	for v in vordic.keys():
		for l in locs:
			for d in dic.keys():
				if dic[v][l] > dic[d][l]:
					print(v,d)
					print(dic[v][l], dic[d][l])
					vordic[v].remove(l)
					break

	print(vordic)
	return dic    




filename = '50.in'

#Parse input file and convert to nx graph
input = read_file(filename)
num_loc, num_house, locs, houses, start_loc, adj = data_parser(input)
G = adjacency_matrix_to_graph(adj)[0]
house_ind = convert_locations_to_indices(houses,locs)

# print(house_ind)
print(modified_voronoi(G, house_ind,num_loc))

#Voronoi algorithm on each of the houses, 
# cells = nx.voronoi_cells(G, house_ind)
# print(cells)

# draw_network(G,house_ind)


