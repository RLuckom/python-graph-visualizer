#!/usr/bin/env python

from Vertex import Vertex
from Edge import Edge


class Graph(object):

    def __init__(self, name=None):
        self.vertex_dict = {}
        self.edge_list = []
        self.name = name

    def __str__(self):
        printstr = 'GRAPH: {0}\n\n\n'.format(self.name)
        for vertex in self.vertex_dict:
            printstr += str(self.vertex_dict[vertex])
        return printstr

    def add_vertex(self, vertex_name, vertex_type=None):
        self.vertex_dict[vertex_name] = Vertex(vertex_name, vertex_type)

    def add_undirected_edge(self, vertex_one, vertex_two, weight=None):
        self.edge_list.append(Edge(vertex_one, vertex_two, weight))
        self.edge_list.append(Edge(vertex_two, vertex_one, weight))
        self.vertex_dict[vertex_two].add_edge(vertex_one, weight)
        self.vertex_dict[vertex_one].add_edge(vertex_two, weight)

    def add_directed_edge(self, from_vertex, to_vertex, weight=None):
        self.edge_list.append(Edge(from_vertex, to_vertex, weight))
        self.vertex_dict[from_vertex].add_edge(to_vertex, weight)



if __name__ == '__main__':
    x = Graph('test')
    x.add_vertex('x', 'politician')
    x.add_vertex('y', 'donor')
    x.add_vertex('m', 'city')
    x.add_directed_edge('x', 'y', 5)
    x.add_undirected_edge('x', 'm')
    print x

