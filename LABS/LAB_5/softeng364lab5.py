#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 10:21:58 2018

@author: cyrus
"""

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
"""node_positions = nx.spring_layout(graph) <--- uses Fruchterman-Reingold force-directed algorithm"""
edge_label_positions = nx.draw_networkx_edge_labels(
        graph,
        pos=node_positions,
        node_labels=nx.get_node_attributes(graph, name='name'),
        edge_labels=nx.get_edge_attributes(graph, name='cost'))
nx.draw_networkx(graph, pos=node_positions)

node_positions = nx.spring_layout(graph)

P, D = nx.dijkstra_predecessor_and_distance(graph, source = 'u', weight = 'cost')

sp_tree = nx.convert.from_dict_of_lists(P).edges()

nx.draw_networkx_edges(
        graph,
        pos=node_positions,
        edgelist=sp_tree,
        edge_color='r',
        width=3)
