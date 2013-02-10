#!/usr/bin/env python


class Edge(object):

    def __init__(self, from_vertex, to_vertex, weight=None):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight

    def __str__(self):
        return "Edge of weight {0} connnecting vertex {1} to vertex {2}.".format(self.weight, self.from_vertex, self.to_vertex)


if __name__ == '__main__':
    x = Edge('A', 'B', 5)
    print x
