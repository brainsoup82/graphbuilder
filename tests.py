# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:05:20 2022

@author: chris
"""

from Graphs import graphbuilder

my_graph = graphbuilder.Graph()
my_graph.add_path('A', 'B', 3)
my_graph.add_path('B', 'C', 1)
my_graph.add_paths([['A', 'C', 2], ['D', 'C', 9], ['D', 'A', 5.2], ['A', 'B', 4]])

print(my_graph.node_degree('A'))
print(my_graph)
print(my_graph.is_eulerian())
print(my_graph.odd_vertices())
print(my_graph.eulerian_path[0])
print(my_graph)

my_graph = graphbuilder.Graph()
my_graph.add_paths([['A', 'C', 2], ['D', 'C', 9], ['D', 'A', 5.2], ['A', 'B', 4],
                    ['C', 'E', 3], ['F', 'G', 1], ['G', 'A', 19]])
print(my_graph)
print('nodes connected to C and D')
print(my_graph.connected_nodes(['D', 'C']))
print('and is the graph fully connected')
print(my_graph.fully_connected())
print(my_graph.dijkstra('B', 'E'))
my_graph = graphbuilder.Graph()
my_graph.add_paths([['A', 'B', 4], ['A', 'D', 7], ['A', 'C', 3], ['D', 'B', 1],
                    ['C', 'D', 3], ['B', 'F', 4], ['C', 'E', 5], ['D', 'E', 2],
                    ['D', 'F', 2], ['D', 'G', 7], ['E', 'G', 2], ['F', 'G', 4]])
print(my_graph)
print(my_graph.dijkstra('A', 'F'))
