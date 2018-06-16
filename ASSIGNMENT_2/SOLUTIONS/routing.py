# -*- coding: utf-8 -*-

import math


def dijkstra_predecessor_and_distance(graph, source, weight='cost'):
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
    P = {}  # create predecessor dictionary, to return

    # Initialization
    for v in N:
        P[v] = []
        if graph.has_edge(u, v):
            D[v] = c(u, v)
            P[v] = [u]  # add coresponding predecessor

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
                    # add node and its predecessor to predecessor dictionary
                    P[v] = [w]
    return P, D


def predecessor_to_forwarding(predecessor, source):
    """
    Compute a forwarding table from a predecessor list.
    """

    # Create variable to return (forwarding-table dictionary)
    FT = {}

    # Loop over all nodes that AREN'T the source
    for (key, value) in predecessor.items():
        if (key != source):
            # Add all node pairs, where the immediate predecessor is the source
            if (value[0] == source):
                FT[key] = (value[0], key)
            # If immediate predecessor is not source, follow predecessors
            # until source is found, and isolate that link, to add to the dict
            else:
                newKey = key
                newValue = value[0]
                while (newValue != source):
                    newKey = newValue
                    newValue = predecessor[newKey][0]
                FT[key] = (newValue, newKey)
    return FT


def dijkstra_generalized(graph, source, weight='cost',
                         infinity=math.inf,
                         plus=lambda x, y: x + y,
                         less=lambda x, y: x < y,
                         min=min,
                         sourcedist=0):  # this is a suitable default
    """
    Least-cost or widest paths via Dijkstra's algorithm.
    """

    # WPP: for the widest path problem the parameters should be as follows:
    # infinity = 0
    # plus = min
    # less = lambda x, y : x > y
    # min = max

    # SPP: for the shortest path problem the parameters should be as follows:
    # infinity = math.inf
    # plus = lambda x, y : x + y
    # less= lambda x, y : x < y
    # min = min

    # Definitions consistent with Kurose & Ross
    u = source

    def c(x, y):
        return graph[x][y][weight]
    N = frozenset(graph.nodes())  # creates set of nodes from graph
    NPrime = {u}  # i.e. "set([u])"
    D = dict.fromkeys(N, infinity)  # sets all weights to infinity initially
    P = {}  # create predecessor dictionary, to return

    # Initialization
    for v in N:
        P[v] = []
        if graph.has_edge(u, v):  # checks if a node is connected to the source
            D[v] = c(u, v)
            P[v] = [u]  # add predecessor of node, to pred dict
    D[u] = sourcedist  # over-write inf entry for source

    # Loop
    while NPrime != N:
        candidates = {w: D[w] for w in N if w not in NPrime}
        w, Dw = min(candidates.items(), key=lambda item: item[1])
        NPrime.add(w)

        for v in graph[w]:
            if v not in NPrime:
                DvNew = plus(D[w], c(w, v))
                if less(DvNew, D[v]):
                    D[v] = DvNew
                    # add node and its predecessor to the predecessor dict
                    P[v] = [w]
    return P, D
