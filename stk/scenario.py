
import numpy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
def CreateNetworkX(G_networkx, G_Matrix):
    for i in range(len(G_Matrix)):
        for j in range(len(G_Matrix)):
            if G_Matrix[i][j] == 1:
                G_networkx.add_edge(i, j)
    return G_networkx

G_sat = nx.Graph()
Adjacency_Matrix = np.loadtxt('./1Adjacency_Matrix.txt')

# Adjacency_Matrix = Get_Satellite_Network(current_time)
G_sat = CreateNetworkX(G_sat,Adjacency_Matrix)
nx.draw(G_sat, node_color="orange", edge_color="grey", with_labels=True, pos=nx.kamada_kawai_layout(G_sat))
plt.show()