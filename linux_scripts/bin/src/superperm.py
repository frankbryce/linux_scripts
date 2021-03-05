#!/usr/bin/python
import matplotlib.pyplot as plt
import math
import networkx as nx
import itertools
import functools
import sys
from tqdm import trange

G = nx.DiGraph()
n = 4
if len(sys.argv) > 1:
    n=int(sys.argv[1])
filter_len = 0
if len(sys.argv) > 2:
    filter_len=int(sys.argv[2])
perms = set(itertools.permutations(list(range(1,n+1))))
nodes = []

def dist(n1, n2):
    if len(n1) != len(n2):
        raise Exception("only support dist(n1, n2) where n1 and n2 are the same length")
    n = len(n1)
    for i in range(n+1):
        if n1[i:] == n2[:n-i]:
            return i
    raise Exception("shouldn't happen")

def mindist(n1,n2):
    return min(dist(n1,n2), dist(n2,n1))

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

print("finding a path through the permutations")
nperms = math.factorial(n)
seen_perms = set()
curr_perm = tuple([i+1 for i in range(n)]) # next(iter(perms))
subset_ys = [n] * int(nperms/n)
subset = 0
superperm = ''
def add_node(G, perm, chars2add):
    global superperm
    G.add_node(perm, pos=(subset, subset_ys[subset]))
    subset_ys[subset] -= 1
    seen_perms.add(perm)
    superperm += name(perm)[n-chars2add:]
add_node(G, curr_perm, n)
for _ in trange(nperms-1):
    min_d = n+1
    min_perm = None
    for perm in sorted(perms.difference(seen_perms)):
        d = dist(curr_perm, perm)
        if d < min_d:
            min_d = d
            min_perm = perm
    if min_perm is None:
        raise Exception(f"no edges found in graph for {curr_perm}")
    d1 = dist(curr_perm, min_perm)
    # G.add_edge(curr_perm, min_perm, rad=(d1-1)/5, dist=d1)
    G.add_edge(curr_perm, min_perm, rad=0.0, dist=d1)
    curr_perm = min_perm
    if min_d != 1:
        subset += 1
    add_node(G, curr_perm, min_d)

print("making layout")
pos = nx.get_node_attributes(G, 'pos')

print("draw network nodes")
nx.draw_networkx_nodes(
        G,
        pos,
        node_color=[(0.9,0.9,0.9,0.5)],
        node_size=0)

print("draw network edges")
edges_to_draw = list(filter(lambda e: e[2]['dist'] > filter_len, G.edges.data()))
for i in trange(len(edges_to_draw)):
    edge = edges_to_draw[i]
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[edge],
        edge_color=color_map(edge[2]["dist"]),
        connectionstyle=f'arc3, rad = {edge[2]["rad"]}')

if len(sys.argv) < 3 or sys.argv[3].tolower() == "true":
    print("draw network labels")
    nx.draw_networkx_labels(
            G, pos,
            labels={ni: name(ni) for ni in G.nodes()})

print(f"Superpermutation of length {len(superperm)} found: {superperm}")
plt.show()
