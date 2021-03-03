#!/usr/bin/python
import matplotlib.pyplot as plt
import networkx as nx
import itertools
import functools

G = nx.Graph()
n=3
perms = itertools.permutations(list(range(1,n+1)))
nodes = []

def dist(n1, n2):
    if len(n1) != len(n2):
        raise Exception("only support dist(n1, n2) where n1 and n2 are the same length")
    n = len(n1)
    for i in range(n+1):
        if n1[i:] == n2[:n-i]:
            return i
    raise Exception("shouldn't happen")

def name(n1):
    return functools.reduce(lambda nm, i: nm+str(i), n1, '')

def color_map(w):
    if w == 1:
        return 'r'
    if w == 2:
        return 'g'
    if w == 3:
        return 'b'
    if w == 4:
        return 'm'
    if w == 5:
        return 'c'
    if w == 6:
        return 'y'
    return 'k'

for perm in perms:
    for node in nodes:
        d1,d2 = dist(perm, node), dist(node, perm)
        G.add_edge(perm, node, dist=d1, weight=1.0/min(d1,d2))
        G.add_edge(node, perm, dist=d2, weight=1.0/min(d1,d2))
    nodes.append(perm)

pos = nx.spring_layout(G, iterations=1000)
nx.draw_networkx_nodes(G, pos, node_size=1000)
nx.draw_networkx_labels(G, pos, labels={ni: name(ni) for ni in G.nodes()})

all_edges = G.edges()
nx.draw_networkx_edges(
        G,
        pos,
        edgelist=all_edges,
        edge_color=list(map(lambda e: color_map(min(dist(e[0],e[1]),
            dist(e[1],e[0]))), all_edges)))
plt.show()
