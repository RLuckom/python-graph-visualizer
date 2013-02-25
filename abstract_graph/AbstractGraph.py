#!/usr/bin/env python

from Vertex import Vertex
from Edge import Edge
import random


class AbstractGraph(object):

    def __init__(self, name=None):
        self.directed = False
        self.vertex_dict = {}
        self.edge_dict = {}
        self.name = name

    def __str__(self):
        printstr = 'GRAPH: {0}\n\n\n'.format(self.name)
        for vertex in self.vertex_dict:
            printstr += str(self.vertex_dict[vertex])
        return printstr

    def add_vertex(self, vertex_name, vertex_type=None):
        self.vertex_dict[vertex_name] = Vertex(vertex_name, vertex_type)

    def add_undirected_edge(self, vertex_one, vertex_two, weight=None):
        self.edge_dict[vertex_one, vertex_two] = Edge(vertex_one, vertex_two, weight)
        self.edge_dict[vertex_two, vertex_one] = Edge(vertex_two, vertex_one, weight)
        self.vertex_dict[vertex_two].add_edge(vertex_one, weight)
        self.vertex_dict[vertex_one].add_edge(vertex_two, weight)

    def add_directed_edge(self, from_vertex, to_vertex, weight=None):
        self.directed = True
        self.edge_dict[from_vertex, to_vertex] = Edge(from_vertex, to_vertex, weight)
        self.vertex_dict[from_vertex].add_edge(to_vertex, weight)

    def minimum_spanning_tree(self):
        if self.directed:
            raise Exception('Current implementation of minimum spanning tree does not work for directed graphs')
        tree = {'vertices': [self.vertex_dict[random.choice([x for x in self.vertex_dict])]], 'edges': []}
        while len(tree['vertices']) < len(self.vertex_dict):
            best_edge_number = None
            best_edge = None
            best_vertex = None
            vertex_names = [vertex.label for vertex in tree['vertices']]
            for vertex in tree['vertices']:
                for edge in vertex.edges:
                    if edge not in vertex_names and (vertex.edges[edge] < best_edge_number or best_edge is None):
                        best_edge_number = vertex.edges[edge]
                        best_edge = self.edge_dict[vertex.label, edge]
                        best_vertex = edge
            tree['vertices'].append(self.vertex_dict[best_vertex])
            tree['edges'].append(best_edge)
        return tree['edges']

if __name__ == '__main__':
    graph = AbstractGraph('wikipedia example')
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_vertex('C')
    graph.add_vertex('D')
    graph.add_vertex('E')
    graph.add_vertex('F')
    graph.add_vertex('G')
    graph.add_undirected_edge('A', 'D', 5)
    graph.add_undirected_edge('A', 'B', 7)
    graph.add_undirected_edge('B', 'C', 8)
    graph.add_undirected_edge('B', 'D', 9)
    graph.add_undirected_edge('B', 'E', 7)
    graph.add_undirected_edge('C', 'E', 5)
    graph.add_undirected_edge('D', 'E', 15)
    graph.add_undirected_edge('D', 'F', 6)
    graph.add_undirected_edge('E', 'F', 8)
    graph.add_undirected_edge('E', 'G', 9)
    graph.add_undirected_edge('F', 'G', 11)
    print [str(edge) for edge in graph.minimum_spanning_tree()]
