#!/usr/bin/env python


class Edge(object):

    def __init__(self, from_vertex, to_vertex, weight=None):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight

    def __str__(self):
        return "Edge {0}{1}, weight {2}.".format(self.from_vertex, self.to_vertex, self.weight)


if __name__ == '__main__':
    x = Edge('A', 'B', 5)
    print x
