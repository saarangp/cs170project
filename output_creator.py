import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

n = 50
h = 25

G = nx.erdos_renyi_graph(n,.5)
houses = np.random.choice(range(n), h, replace=False)
print(houses)

cycle = nx.find_cycle(G,source = 0)
print(cycle)
cycle_path  = [c[0] for c in cycle]
cycle_path.append(0)
print(cycle_path)
