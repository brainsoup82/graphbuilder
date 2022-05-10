# -*- coding: utf-8 -*-
"""
Created on Thu May  5 20:37:48 2022

@author: chris

Code that will create graph given a link from one node to another

Graphs are dictionaries with nodes as the keys
Paths are the list items within list for each key with format
['end_node', distance]
"""

# copy needed to copy the graph whilst working on it
# math needed to compare floats

import copy
import math

class Graph:
    '''
    Graphs are dictionaries with nodes as the keys
    Paths are the list items within list for each key with format
    ['end_node', distance]
    '''
    def __init__(self):
        '''
        Creates new empty graph

        Returns
        -------
        None.

        '''
        self.graph = {}
        self.oneway = False

    def __str__(self):
        message = ''
        for node in self.graph.keys():
            message += f'the node {node} connects to :\n'
            for path in self.graph[node]:
                message += f'\tnode {path[0]} with distance {path[1]}\n'
            message += '\n'
        return message

    def create_node(self,node_name):
        '''
        Adds a node to the graph if it does not yet exist

        Parameters
        ----------
        node_name : name of node

        Returns
        -------
        None.

        '''

        # Check if node already in graph, if so then pass
        # Otherwise add a key with a blank list ready to append connections to
        if node_name in self.graph.keys():
            pass
        else:
            self.graph[node_name]=[]

    def add_path(self,start_node, end_node, distance, oneway=False):
        '''
        Adds a path to the graph - will add new nodes as found

        Parameters
        ----------
        start_node : start node name
        end_node : end node name
        distance : distance
        oneway : TYPE, optional
            Is the path One-Way? The default is False.

        Returns
        -------
        None.

        '''
        # Ensure that both nodes are created in the graph
        self.create_node(start_node)
        self.create_node(end_node)

        #append the new connection from start node to end node
        self.graph[start_node].append([end_node, distance])

        # If the link is one way then the link is added.
        # Otherwise add the reverse link
        if oneway is False:
            self.graph[end_node].append([start_node, distance])
        else:
            self.oneway = True

    def paths_at_node(self,node):
        '''
        Creates a list of paths at a node

        Parameters
        ----------
        node : node to find paths for
        Returns
        -------
        If no paths found then empty list
        if paths found then returns nested list - [[node_name, distance]]

        '''
        if node in self.graph.keys():
            return self.graph[node]
        return []

    def add_paths(self,path_list):
        '''
        adds a list of paths to the graph
        pass graphs as nested list [[start,end, distance, one_way]]
        if one_way not passed then will default to False
        '''
        for path in path_list:
            # Check if one_way parameter has been passed for the link
            # If not assume false
            if len(path) == 4:
                one_way = path[3]
            else:
                one_way = False
            self.add_path(path[0],path[1],path[2],one_way)

    def node_degree(self,node):
        '''
        returns how many paths leave node
        '''
        return len(self.paths_at_node(node))

    def is_eulerian(self):
        '''
        checks if an Eulerian path is possible on the graph
        Returns Boolean
        '''
        odd_vertices = len(self.odd_vertices())
        return (odd_vertices in {0,2})

    def odd_vertices(self):
        '''
        returns a list of vertices that are have odd degree
        '''
        odd_vertex_list = []
        for node in self.graph:
            if self.node_degree(node)%2 == 1:
                odd_vertex_list.append(node)
        return odd_vertex_list

    def remove_path(self,start_node, end_node, length=0):
        '''
        Function looks for path from start node to end node
        Removes path and reverse.
        Finds first path if no length passed, or path matching length otherwise
        '''

        # get paths to iterate through
        possible_paths = self.paths_at_node(start_node)
        # Search for path with correct end node and distance
        # use first found path if distance = 0
        for path in possible_paths:
            if ((path[0] == end_node and length == path[1])
                or (path[0] == end_node and length == 0)):
                self.graph[start_node].remove(path)
                break

        # now look for reverse path
        possible_paths = self.paths_at_node(end_node)
        for path in possible_paths:
            if ((path[0] == start_node and length == path[1])
                or (path[0] == start_node and length == 0)):
                self.graph[end_node].remove(path)
                break

    def reachable_nodes(self,node):
        '''
        Returns a list of nodes that are reachable from given node
        '''
        reachable_nodes = {node}
        for path in self.paths_at_node(node):
            reachable_nodes.add(path[0])
        return reachable_nodes

    def connected_nodes(self,node_list):
        '''
        Creates a list of nodes that are connected to all the nodes passed

        Parameters
        ----------
        node_list : list of nodes

        Returns
        -------
        reachable_nodes : list of reachable nodes

        '''
        reachable_nodes = set(node_list)
        for node in node_list:
            for path in self.paths_at_node(node):
                reachable_nodes.add(path[0])
        return reachable_nodes

    def eulerian_path(self):
        '''
        Function creates an Eulerian path on the graph

        Returns
        -------
        current_path : string detailing the path
        total_distance : length of path

        '''
        # Determine start and finish point as a list
        start_finish_vertex = self.odd_vertices()
        if start_finish_vertex == []:
            start_finish_vertex.append(list(self.graph.keys)[0])
            start_finish_vertex.append(list(self.graph.keys)[0])

        #create a copy of the graph to work with during algorithm
        current_graph = Graph()
        current_graph.graph = copy.deepcopy(self.graph)

        current_path = ''
        paths_exist = True
        total_distance = 0
        current_vertex = start_finish_vertex[0]

        while paths_exist:
            next_vertex = current_graph.graph[current_vertex][0][0]
            # check if next node is a bridge,
            # if it is then try to move to next vertex
            # if no more vertices exist then this must be last path to cross
            if current_graph.node_degree(next_vertex) == 1:
                try:
                    next_vertex = current_graph.graph[current_vertex][1][0]
                except IndexError:
                    paths_exist = False

            current_path += (f'Travel from {current_vertex} ' +
                             f'to {next_vertex}\n')
            current_graph.remove_path(current_vertex, next_vertex)
            current_vertex = next_vertex
        return (current_path, total_distance)

    def fully_connected(self):
        '''
        Checks if a grapgh is fully connected.

        Returns
        -------
        bool - if graph fully connected then True

        '''
        all_nodes = set(self.graph.keys())
        start_node = list(all_nodes)[0]
        current_nodes = set(start_node)

        while True:
            current_nodes.update(self.connected_nodes(current_nodes))
            if current_nodes == all_nodes:
                return True
            if current_nodes == self.connected_nodes(current_nodes):
                return False

    def dijkstra(self, start_node, end_node):
        '''
        Performs Djikstra's algorithm on the graph to find shortest path
        between two nodes

        Parameters
        ----------
        start_node : starting node for path
        end_node : ending node for path

        Returns
        -------
        message : string detailing path

        '''
        # Create list to hold all nodes.
        # [Node name, current distance, current node, finalised?]
        all_nodes = {}
        for node in self.graph.keys():
            all_nodes.update({node: [float('inf'),False, False]})
        all_nodes.update({start_node:[0, True, True]})

        # Keep going until end_node is finalised
        while all_nodes[end_node][2] is False:
            for node in all_nodes:
                # look at the current node
                if all_nodes[node][1] is True:
                    # look at all paths from this node
                    for path in self.paths_at_node(node):
                        # see if new distance is less than current distance
                        # if it is then update with new value
                        if all_nodes[node][0] + path[1] < all_nodes[path[0]][0]:
                            all_nodes[path[0]][0] = all_nodes[node][0] + path[1]
                    # current node no longer current
                    all_nodes[node][1] = False

            lowest_distance = float('inf')
            lowest_node = ''
            for node in all_nodes:
                if (all_nodes[node][2] is False
                        and all_nodes[node][0]<lowest_distance):
                    lowest_distance = all_nodes[node][0]
                    lowest_node = node
            all_nodes[lowest_node][1] = True
            all_nodes[lowest_node][2] = True

        print(all_nodes)
        message = f'\nTotal Distance {all_nodes[end_node][0]}'
        while all_nodes[start_node][2]:
            for node in all_nodes:
                if all_nodes[node][1] is True:
                    for path in self.paths_at_node(node):
                        value_1 = float(all_nodes[path[0]][0])
                        value_2 = float(all_nodes[node][0] - path[1])

                        if math.isclose(value_1 , value_2):
                            message = (f'\nGo from {path[0]} to {node} '
                                       f'- distance: {path[1]}'+ message)
                            all_nodes[path[0]][1]=True
                            all_nodes[node][1] = False
                            all_nodes[path[0]][2] = False
                            print('breaking')
                            break
        return message

if __name__ == '__main__':
    my_graph = Graph()
    my_graph.add_path('A','B',3)
    my_graph.add_path('B','C',1)
    my_graph.add_paths([['A','C', 2],['D','C',9],['D','A',5.2],['A','B',4]])

    print(my_graph.node_degree('A'))
    print(my_graph)
    print(my_graph.is_eulerian())
    print(my_graph.odd_vertices())
    print(my_graph.eulerian_path()[0])
    print(my_graph)

    my_graph = Graph()
    my_graph.add_paths([['A','C', 2],['D','C',9],['D','A',5.2],['A','B',4],
                        ['C','E',3],['F','G',1],['G','A',19]])
    print(my_graph)
    print('nodes connected to C and D')
    print(my_graph.connected_nodes(['D','C']))
    print('and is the graph fully connected')
    print(my_graph.fully_connected())
    print(my_graph.dijkstra('B', 'E'))
    my_graph = Graph()
    my_graph.add_paths([['A','B',4],['A','D',7],['A','C',3],['D','B',1],
                        ['C','D',3],['B','F',4],['C','E',5],['D','E',2],
                        ['D','F',2],['D','G',7],['E','G',2],['F','G',4]])
    print(my_graph)
    print(my_graph.dijkstra('A','G'))
