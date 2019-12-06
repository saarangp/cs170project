import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils

from student_utils import *
from graph_reduction import *
from sp_solver import *
from tsp_mcmc.traveling_salesman_MCMC import mcmc_solver
"""
======================================================================
  Complete the following function.
======================================================================
"""

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
    G = adjacency_matrix_to_graph(adjacency_matrix)[0]
    house_ind = convert_locations_to_indices(list_of_homes,list_of_locations)
    G = add_node_attributes(G, house_ind)
    #cc,lv = modified_voronoi(G, house_ind,len(list_of_locations))
    start = convert_locations_to_indices([starting_car_location],list_of_locations)[0]
    centroids = cost_clustering(G, start)
    print(centroids)
    #turn into fully connected graph of dropoffs
    G_prime = nx.Graph()
    G_prime.add_nodes_from(centroids)
    for v in centroids:
        for u in centroids:
            if u > v:
                G_prime.add_edge(u, v)
                G_prime[u][v]['weight'] = nx.dijkstra_path_length(G, u, v)
    #G_prime is fully connected graph to feed into mcmc
    abbrev_path = mcmc_solver(G_prime)
    path = [abbrev_path[0]]
    for i in range(len(abbrev_path) - 1):
        rt = nx.dijkstra_path(G, abbrev_path[i], abbrev_path[i + 1])
        path = path + rt[1:]
    dropoffs = find_nearest_centroid(G, centroids)
    #dropoffs = [(v, clusters[v]) for v in clusters.keys()]
    #start = convert_locations_to_indices([starting_car_location],list_of_locations)[0]
    # path,dropoffs = find_path(G, house_ind,len(list_of_locations),lv,start)
    return path, dropoffs
    

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
        output_filename = utils.input_to_output(input_file).split('/')[1]
        print(output_filename)
        print(os.listdir(output_directory))
        print(output_filename in os.listdir(output_directory))
        if output_filename not in os.listdir(output_directory):
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


        
