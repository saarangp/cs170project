import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import numpy as np
import matplotlib.pyplot as plt
import copy
import networkx as nx
from student_utils import *
import random
"""
======================================================================
  Complete the following function.
======================================================================
"""

def cal_dist(distance, L):
    d = 0
    for i in range(len(L)):
        d = d + distance[L[i % N], L[(i + 1) % N]]
    return d

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A list of (location, [homes]) representing drop-offs

    """
    pass


#take make a new graph, then input
def form_tsp(reduced_graph, matrix = True):
    comp_g = nx.complete_graph(len(reduced_graph.nodes))
    for (u, v) in G.edges():
        G.edges[u, v]['weight'] = random.randint(0, 10)
    for v in list_of_homes:          #reduced_graph.nodes if v in
        for u in list_of_homes if u is not v:
            comp_g[u,v]['weight'] = nx.shortest_path_length(reduced_graph, source = u,  target = v, weight = "use")

    if matrix:
        return nx.to_numpy_matrix(comp_g).np.matrix.tolist()  # 2 dimensional adjascency list
    else:
        return comp_g   #nx complete graph with weights


def mcmc_tsp():
    #@source Zhongxiang Dai
    T = float(pow(2, -8)) # free parameters, inversely related to the probability of rejection if the direction is wrong
    ITER = 50000
    L = np.arange(N)  # initail route sequence
    print(cal_dist(distance, L))  # initial distance
    dist_all = []
    for i in range(ITER):
        a = np.random.randint(1, N - 1)
        d_t = cal_dist(distance, L)
        dist_all.append(d_t)
        L_tmp = copy.copy(L)
        L_tmp[[a, (a + 1) % N]] = L_tmp[[(a + 1) % N, a]]
        delta_d = cal_dist(distance, L_tmp) - d_t
        p = min(1, np.exp(-1 * delta_d / T))
        u = np.random.rand()
        if u < p:
            L = L_tmp

    print(cal_dist(distance, L))  # final distance
    plt.plot(dist_all)

    #take in: modified adjascency matrix
    #return: list of output verticies, distance


"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)
    
    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    output_filename = utils.input_to_output(filename)
    output_file = f'{output_directory}/{output_filename}'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)


        
