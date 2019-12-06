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

N = 50 # the number of cities

# simulate a distance matrix
# distance = np.random.rand(N, N)
# distance = (distance + distance.T) / 2.0
# ind_diag = range(N)
# distance[ind_diag, ind_diag] = 0
#print(distance)

# Calculate total distance for a given sequence

G = nx.complete_graph(N)
for (u, v) in G.edges():
    G.edges[u, v]['weight'] = random.randint(0, 10)
distance = nx.to_numpy_matrix(G)
print(distance)


#Straight up wrong
# def form_tsp(reduced_graph, matrix = True):
#     comp_g = nx.complete_graph(len(reduced_graph.nodes))
#     for (u, v) in G.edges():
#         comp_g.edges[u, v]['weight'] = random.randint(0, 10)
#
#     if matrix:
#         return nx.to_numpy_matrix(comp_g).np.matrix.tolist()  # 2 dimensional adjascency list
#     else:
#         return comp_g   #nx complete graph with weights


def cal_dist(distance, L):

    d = 0
    for i in range(len(L)):
        d = d + distance[L[i % N], L[(i + 1) % N]]
    return d

T = float(pow(2, -8)) # free parameters, inversely related to the probability of rejection if the direction is wrong

ITER0 = 100
ITER1 = 50000
ITER2 = 50000
L = np.append(np.arange(N), [0]) # initail route sequence
#np.insert(L, len(L), 0)
print(L)
print (cal_dist(distance, L)) # initial distance
dist_all = []

# for i in range(ITER0):
#     c = np.random.randint(1, math.ceil((N - 1)/2))
#     a = np.random.randint(1, N - 1, size = c)
#     b = np.random.randint(1, N - 1, c)
#     d_t = cal_dist(distance, L)
#     dist_all.append(d_t)
#     L_tmp = copy.copy(L)
#     for k in c:
#         L_tmp[[a, b]] = L_tmp[[b, a]]
#     delta_d = cal_dist(distance, L_tmp) - d_t
#     p = min(1, np.exp(-1 * delta_d / T))
#     u = np.random.rand()
#     if u < p:
#         L = L_tmp

for i in range(ITER1):
    a = np.random.randint(1, N - 1)
    #b = (a + 1)%N
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
print(L)
print (cal_dist(distance, L)) # final distance
plt.plot(dist_all)
plt.show()
