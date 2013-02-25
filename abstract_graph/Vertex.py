#!/usr/bin/env python


class Vertex(object):

    def __init__(self, label, type=None):
        self.type = type
        self.label = label
        self.edges = {}

    def __str__(self):
        printstr = "Vertex {0}\n\tType: {1}\n".format(self.label, self.type)
        for edge in self.edges:
            printstr += '\n\tConnected to vertex {0} by an edge of weight {1}'.format(edge, self.edges[edge])
        return printstr + '\n\n'

    def add_edge(self, other_vertex, weight=None):
        if other_vertex in self.edges:
            raise Exception("Vertex {0} already connected to vertex {1}. Support for multiple connections between vertices not implemented.".format(other_vertex, self.label))
        else:
            self.edges[other_vertex] = weight


if __name__ == '__main__':
    x = Vertex('x')
    y = Vertex('y', 'donor')
    x.add_edge('y', 5)
    print x
    print y
