import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sys, os
from utils import *


def format_matrix_as_input(adj_matrix):
	out_str = ""
	for i in adj_matrix:
		for j in i:
			if j < 0.001:
				out_str = out_str + "x "
			else:
				#keep first 3 decimal digits of lengths
				out_str = out_str + str(j + 0.001)[0:5] + " "
		out_str = out_str + "\n"
	return out_str

def sep_list(l):
	out_str = ""
	for i in l:
		out_str = out_str + i + " "
	return out_str


# the different problem sizes to generate
problem_size = (50, 100, 200)

#x, y coordinates of vertices 1 ... n in a problem
locations = [np.random.rand(n, 2) for n in problem_size]

for p in range(len(problem_size)):
	G = nx.Graph()
	G.add_nodes_from([1, 2, 3, 4, 5])
	while not nx.is_connected(G):
		G = nx.erdos_renyi_graph(problem_size[p], .1)
		A = nx.adjacency_matrix(G)


	G_np = nx.convert_matrix.to_numpy_matrix(G).A.tolist()

	for i in range(len(G_np)):
		for j in range(len(G_np)):
			if G_np[i][j] != 0:
				#if edge i, j exists in the graph, set the length to the norm2 dist between them in locations matrix
				G_np[i][j] = np.linalg.norm(locations[p][i] - locations[p][j])

	#each vertex will be named "loc i" if it is the ith vertex in the adjacency matrix
	loc_names = ["loc" + str(i) for i in range(problem_size[p])]
	#choose n/5 integers between 0 and n, these are the dropoffs
	#cannot drop off at vertex zero
	dropoffs = np.random.choice(problem_size[p] - 1, int(problem_size[p]/5), replace=False) + 1
	dropoffs = [loc_names[i] for i in dropoffs]

	write_to_file(str(problem_size[p]) + ".in", "")
	write_to_file(str(problem_size[p]) + ".in", str(problem_size[p]) + "\n", append=True)
	write_to_file(str(problem_size[p]) + ".in", str(len(dropoffs)) + "\n", append=True)
	write_to_file(str(problem_size[p]) + ".in", sep_list(loc_names) + "\n", append=True)
	write_to_file(str(problem_size[p]) + ".in", sep_list(dropoffs) + "\n", append=True)
	write_to_file(str(problem_size[p]) + ".in", loc_names[0] + "\n", append=True)
	write_to_file(str(problem_size[p]) + ".in", format_matrix_as_input(G_np), append=True)