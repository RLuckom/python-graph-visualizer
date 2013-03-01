#!/usr/bin/env python


class Vertex(object):
    """Class to represent a vertex."""

    def __init__(self, label, type=None):
        """Constructor

        @type label: str
        @param label: label for the vertex in the visualization of the graph
        @type type: str
        @param type: type of the vertex if applicable, like 'donor'. defaults to None.
        """
        self.type = type
        self.label = label
        self.edges = {}

    def __str__(self):
        """printstring

        @rtype: str
        @return: printstring
        """
        printstr = "Vertex {0}\n\tType: {1}\n".format(self.label, self.type)
        for edge in self.edges:
            printstr += '\n\tConnected to vertex {0} by edge(s) of weight {1}'.format(edge, self.edges[edge])
        return printstr + '\n\n'

    def add_edge(self, other_vertex, weight=None):
        """adds outgoing edge to vertex

        adding incoming edges is unsupported.

        @type weight: number
        @param weight: weight of edge, defaults to None
        """
        if other_vertex in self.edges:
            self.edges[other_vertex].append(weight)
        else:
            self.edges[other_vertex] = [weight]


if __name__ == '__main__':
    x = Vertex('x')
    y = Vertex('y', 'donor')
    x.add_edge('y', 5)
    print x
    print y
