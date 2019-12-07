# -*- coding: utf-8 -*-
"""
Created on Sat Jan 09 13:36:18 2016

@author: Zhongxiang Dai
"""
import numpy as np
import matplotlib.pyplot as plt
import copy
import networkx as nx
import random
import math



# MCMC (Simulated Annealing) solution for Traveling Salesman problem
# start from city 1 to city N

#N = 50 # the number of cities

# simulate a distance matrix
# distance = np.random.rand(N, N)
# distance = (distance + distance.T) / 2.0
# ind_diag = range(N)
# distance[ind_diag, ind_diag] = 0
#print(distance)

'''CHANGE THESE BOIZ RIGHT HERE'''
ITER0 = 30
ITER1 = 4000
ITER2 = 2000

'''Keep ITER0 relatively low, and ITER1 about two times as much as ITER2
For reference, 500 : 100000 : 50000 took about 1.5 mintues for a random input of size 200
while 50 : 10000 : 5000 took about 12 seconds for a random input of size 200


I'm guessing that 30 : 10000 : 5000 is optimal for decent time, 
but feel free to reduce them or increase the last two values if you want for time
'''


'''

MAKE SURE THAT
the input is a fully connected graph that has weighted edges

returns list of edges that solver will travel to starting and ending with location 0 (which should be soda hall)
(we can also return the distance if necessary)
'''

# Calculate total distance for a given sequence
def mcmc_solver(G, start):
    distance = nx.to_numpy_matrix(G)

    node_names = list(G.nodes)
    start_index = 0
    for i in range(len(node_names)):
        if node_names[i] == start:
            start_index = i
            break

    soda = list(G.nodes)[start_index]
    print(start_index, soda)


    def swap_weights(a,b):
        nl = list(G.nodes)
        nl.remove(a)
        nl.remove(b)
        for v in nl:
            repl_weight = G.edges[a, v]['weight']
            G.edges[a, v]['weight'] = G.edges[b, v]['weight']
            G.edges[b, v]['weight'] = repl_weight

    #print(distance)

    if len(G.nodes()) == 1:
        return node_names[start_index]
    if len(G.nodes()) == 2:
        return [node_names[start_index], node_names[1 - start_index], node_names[start_index]]

    def cal_dist(distance, L):

        d = 0
        for i in range(len(L)):
            d = d + distance[L[i % N], L[(i + 1) % N]]
        return d

    T = float(pow(2, -8)) # free parameters, inversely related to the probability of rejection if the direction is wrong
    N = len(G.nodes())

    swap_weights(0, start_index)

    L = np.append(np.arange(N), [0]) # initial route sequence

    print(L)
    print (cal_dist(distance, L)) # initial distance
    dist_all = []




    for i in range(ITER0):
        c = np.random.choice(math.ceil((N - 1)/2), size = 1, replace=False)
        a = np.random.randint(1, N - 1, size = c)
        b = np.random.randint(1, N - 1, size = c)
        d_t = cal_dist(distance, L)
        dist_all.append(d_t)
        L_tmp = copy.copy(L)
        for k in range(c[0]):
            L_tmp[[a[k], b[k]]] = L_tmp[[b[k], a[k]]]
        delta_d = cal_dist(distance, L_tmp) - d_t
        p = min(1, np.exp(-1 * delta_d / T))
        u = np.random.rand()
        if u < p:
            L = L_tmp

    for i in range(ITER1):
        a = np.random.randint(1, N - 1)
        b = np.random.randint(1, N - 1)
        if a == b:
            b = (a + 1)%N
        d_t = cal_dist(distance, L)
        dist_all.append(d_t)
        L_tmp = copy.copy(L)
        L_tmp[[a, b]] = L_tmp[[b, a]]
        delta_d = cal_dist(distance, L_tmp) - d_t
        p = min(1, np.exp(-1 * delta_d / T))
        u = np.random.rand()
        if u < p:
            L = L_tmp
    for j in range(ITER2):
        a = np.random.randint(1, N - 1)
        b = (a + 1)%N
        d_t = cal_dist(distance, L)
        dist_all.append(d_t)
        L_tmp = copy.copy(L)
        L_tmp[[a, b]] = L_tmp[[b, a]]
        delta_d = cal_dist(distance, L_tmp) - d_t
        p = min(1, np.exp(-1 * delta_d / T))
        u = np.random.rand()
        if u < p:
            L = L_tmp

    #swap_weights(0, start_index)
    soda_index = list(L).index(soda)
    L[0] = soda
    L[len(L) - 1] = soda
    L[soda_index] = 0


    print(list(L))
    print (cal_dist(distance, L)) # final distance
    plt.plot(dist_all)
    plt.show()

    return([node_names[i] for i in L])

# def christo_solver(G):
#     distance_matrix = list(nx.to_numpy_matrix(G))
#     TSP = christofides.compute(distance_matrix)



'''Uncomment this for testing purposes'''
# N = 25
# G = nx.complete_graph(N)
# for (u, v) in G.edges():
#     G.edges[u, v]['weight'] = random.randint(0, 10)
# mcmc_solver(G, N%9)



# print(christo_solver(G))