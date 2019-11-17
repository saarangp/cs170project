import networkx as nx
import matplotlib.pyplot as plt

G = nx.erdos_renyi_graph(10,.5)
A = nx.adjacency_matrix(G)

print(A)
print(nx.find_cycle(G))
nx.draw(G)
plt.show()

