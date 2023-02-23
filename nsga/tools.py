
import time
import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def CreateNetworkX(G_networkx, G_Matrix):
    for i in range(len(G_Matrix)):
        for j in range(len(G_Matrix)):
            if G_Matrix[i][j] >= 1:
                G_networkx.add_edge(i, j, weight=1)
    return G_networkx


def CreateNetworkX_delay(G_networkx, G_Matrix):
    for i in range(len(G_Matrix)):
        for j in range(len(G_Matrix)):
            if G_Matrix[i][j] >= 1:
                G_networkx.add_edge(i, j, weight=2.27 + random.random() / 10)
    return G_networkx


def CreateNetworkX_test(G_networkx, G_Matrix):
    for i in range(len(G_Matrix)):
        for j in range(len(G_Matrix)):
            if G_Matrix[i][j] > 0:
                G_networkx.add_edge(i, j, weight=1000 / (G_Matrix[i][j] + random.random() / 10))
    return G_networkx


def create_grid(raw=3, column=2, MAXRAW=100, MAXCOL=100):
    count = 0
    map = np.zeros([MAXRAW * MAXCOL, MAXRAW * MAXCOL])

    for j in range(1, raw + 1):
        count = 0
        while count < column:
            map[j + count * raw][j + count * raw + raw] = 1
            count = count + 1
    # print(map)
    i = 1
    for count in range(column):
        i = count * raw + 1
        for j in range(1, raw):
            map[i + j - 1][i + j] = 1
    count = 0
    while count < column:
        map[1 + count * raw][1 + count * raw + raw - 1] = 1
        count = count + 1
    # for i_1 in range(1, raw * column):
    #     for i_2 in range(1, raw * column):
    # print(map[i_1][i_2])
    # print("\n")
    # print("-----")
    # print(map)
    # print(map[1:raw*column+1])
    a = map[1:raw * column + 1, 1:raw * column + 1]
    for i in range(len(a)):
        for j in range(i, len(a)):
            a[j][i] = a[i][j]
    return a
