#!/usr/bin/python
import matplotlib.pyplot as plt
import math
import networkx as nx
import itertools
import functools
import sys
from tqdm import trange

G = nx.DiGraph()
n=int(sys.argv[1])
perms = list(itertools.permutations(list(range(1,n+1))))
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

print("build subsets for graph layout")
nperms = len(perms)
subsets = [[] for _ in range(int(nperms/n))]
subsetdict = dict()
for i in trange(nperms):
    # find first perm list where dist is 1
    perm = perms[i]
    found = False
    isubset = 0
    for subset in subsets:
        if len(subset) == 0:
            subset.append(perm)
            subsetdict[perm] = isubset
            break
        for sperm in subset:
            if dist(sperm, perm) + dist(perm, sperm) == n:
                subset.append(perm)
                subsetdict[perm] = isubset
                found = True
                break
        if found:
            break
        isubset += 1

print("add graph nodes")
for i in trange(nperms):
    perm = perms[i]
    G.add_node(perm, subset=subsetdict[perm])

print("finding a path through the permutations")
seen_perms = set()
curr_perm = perms[0]
seen_perms.add(curr_perm)
superperm = name(curr_perm)
for _ in trange(nperms-1):
    min_d = n+1
    min_perm = None
    for perm in perms:
        if perm == curr_perm:
            continue
        if perm in seen_perms:
            continue
        d = dist(curr_perm, perm)
        if d < min_d:
            min_d = d
            min_perm = perm
    if min_perm is None:
        raise Exception(f"no edges found in graph for {curr_perm}")
    d1 = dist(curr_perm, min_perm)
    G.add_edge(curr_perm, min_perm, rad=(d1-1)/5, dist=d1)
    curr_perm = min_perm
    seen_perms.add(curr_perm)
    superperm += name(curr_perm)[n-min_d:]

print("making layout")
pos = nx.multipartite_layout(G)
print("draw network nodes")
nx.draw_networkx_nodes(
        G,
        pos,
        node_color=(0.9,0.9,0.9,0.5),
        node_size=800)

print("draw network edges")
edges_to_draw = list(G.edges.data())
for i in trange(len(edges_to_draw)):
    edge = edges_to_draw[i]
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[edge],
        edge_color=color_map(edge[2]["dist"]),
        connectionstyle=f'arc3, rad = {edge[2]["rad"]}')

print("draw network labels")
nx.draw_networkx_labels(
        G, pos,
        labels={ni: name(ni) for ni in G.nodes()})
print(f"Superpermutation of length {len(superperm)} found: {superperm}")
plt.show()