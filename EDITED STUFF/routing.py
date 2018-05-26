# -*- coding: utf-8 -*-

import math

def dijkstra_predecessor_and_distance(graph, source, weight='weight'):
    """
    Shortest paths via Dijkstra's algorithm,
    consistent with pseudocode on Slide 5-14.
    """
    import math

    # Definitions consistent with Kurose & Ross
    u = source
    def c(x, y):
        return graph[x][y][weight]
    N = frozenset(graph.nodes())
    NPrime = {u}  # i.e. "set([u])"
    D = dict.fromkeys(N, math.inf)
    P = {} # create predecessor dictionary, to return

    # Initialization
    for v in N:
        P[v] = []
        if graph.has_edge(u, v):
            D[v] = c(u, v)
            P[v] = [u] # add all the nodes directly connected to the source, with their predecessor being the source, to the
                        # output predecessor dictionary

    D[u] = 0  # over-write inf entry for source

    # Loop
    while NPrime != N:
        candidates = {w: D[w] for w in N if w not in NPrime}
        w, Dw = min(candidates.items(), key=lambda item: item[1])
        NPrime.add(w)

        for v in graph[w]:
            if v not in NPrime:
                DvNew = D[w] + c(w, v)
                if DvNew < D[v]:
                    D[v] = DvNew
                    # add node and its predecessor to the predecessor dictionary
                    P[v] = [w]
    return P, D

"""==========================================================================="""


"""==========================================================================="""

def predecessor_to_forwarding(predecessor, source):
    """
    Compute a forwarding table from a predecessor list.
    """

    # Create variable to return (forwarding-table dictionary)
    FT = {}

    ## Loop over all nodes that AREN'T the source
    for ( key, value ) in predecessor.items():
        if (key != source):
            # Add all node pairs, where the immediate predecessor is the source
            if (value[0] == source):
                FT[key] = (value[0], key)
            # If immediate predecessor is not source, follow predecessors
            # until source is found, and isolate that link, to add to the dictionary
            else:
                newKey = key
                newValue = value[0]
                while (newValue != source):
                    newKey = newValue
                    newValue = predecessor[newKey][0]
                FT[key] = (newValue, newKey)
    return FT

"""==========================================================================="""

import json
import os
from pprint import pprint  # "pretty print"
filename = os.path.join('.', 'KuroseRoss5-15.json')  # modify as required
netjson = json.load(open(filename))
pprint(netjson)


import networkx as nx  # saves typing later on
graph = nx.Graph()
graph.add_nodes_from((
    (node['id'], node['properties'])  # node-attributes
        for node in netjson['nodes']))
graph.add_edges_from((
    (link['source'], link['target'], {'cost': link['cost']})  # source-target-attributes
        for link in netjson['links']))

for node, data in graph.nodes(data=True):
    pprint((node, data))

for source, target, data in graph.edges(data=True):
    pprint((source, target, data))  # edges & attributes

for node in graph:
    pprint((node, dict(graph[node])))  # neighbours

node_positions = nx.get_node_attributes(graph, name='pos')
# node_positions = nx.spring_layout(graph) # <--- uses Fruchterman-Reingold force-directed algorithm
edge_label_positions = nx.draw_networkx_edge_labels(
        graph,
        pos=node_positions,
        node_labels=nx.get_node_attributes(graph, name='name'),
        edge_labels=nx.get_edge_attributes(graph, name='cost'))
nx.draw_networkx(graph, pos=node_positions)

node_positions = nx.spring_layout(graph)

P, D = dijkstra_predecessor_and_distance(graph, source = 'u', weight = 'cost')
forwarding_table = predecessor_to_forwarding(P, 'u')

sp_tree = nx.convert.from_dict_of_lists(P).edges()
print(sp_tree)
nx.draw_networkx_edges(
        graph,
       pos=node_positions,
        edgelist=sp_tree,
       edge_color='r',
       width=3)

"""==========================================================================="""

def dijkstra_generalized(graph, source, weight='cost',
                         infinity = math.inf,
                         plus = lambda x, y : x + y, # each "None" to be replaced with suitable default
                         less = lambda x, y : x < y,
                         min = min,
                         sourcedist = 0): # this is a suitable default
    """
    Least-cost or widest paths via Dijkstra's algorithm.
    """

    # WPP: for the widest path problem, the parameters should be set as follows:
    # infinity = 0
    # plus = min
    # less = lambda x, y : x > y
    # min = max

    # Copy-paste the following arguments into the parameters, to solve the widest-path problem

    """
    graph, source, weight='cost',
                         infinity = 0,
                         plus = min, # each "None" to be replaced with suitable default
                         less = lambda x, y : x > y,
                         min = max,
                         sourcedist = 0
    """

    #SPP: for the shortest path problem, the parameters should be set as follows:
    # infinity = math.inf
    # plus = lambda x, y : x + y
    # less= lambda x, y : x < y
    # min = min

    # Copy-paste the following arguments into the parameters, to solve the shortest-path problem

    """
    graph, source, weight='cost',
                         infinity = math.inf,
                         plus = lambda x, y : x + y, # each "None" to be replaced with suitable default
                         less = lambda x, y : x < y,
                         min = min,
                         sourcedist = 0
    """

    # Definitions consistent with Kurose & Ross
    u = source
    def c(x, y):
        return graph[x][y][weight]
    N = frozenset(graph.nodes()) # creates set of nodes from graph
    NPrime = {u}  # i.e. "set([u])"
    D = dict.fromkeys(N, infinity) # sets all weights to infinity initially
    P = {} # create predecessor dictionary, to return

    # Initialization
    for v in N:
        P[v] = []
        if graph.has_edge(u, v): # checks if a node is connected to the source
            D[v] = c(u, v)
            P[v] = [u] # add all the nodes directly connected to the source, with their predecessor being the source, to the
                        # output predecessor dictionary
    D[u] = sourcedist  # over-write inf entry for source

    # Loop
    while NPrime != N: # while (not all nodes have been visited)
        candidates = {w: D[w] for w in N if w not in NPrime} # all estimates thus far
        w, Dw = min(candidates.items(), key=lambda item: item[1]) # isolate smallest distance weighting thus far
        NPrime.add(w) # add corresponding node to 'visited' set

        for v in graph[w]:
            if v not in NPrime: # check all nodes adjacent to chosen node
                DvNew = plus(D[w], c(w, v)) # calculate a new path value for all nodes (wrt chosen node), and
                if less(DvNew, D[v]):
                    D[v] = DvNew
                    # add node and its predecessor to the predecessor dictionary
                    P[v] = [w]
    return P, D

"""==========================================================================="""

