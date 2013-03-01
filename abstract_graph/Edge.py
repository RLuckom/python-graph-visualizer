#!/usr/bin/env python


class Edge(object):
    """Class representing a graph edge"""

    def __init__(self, from_vertex, to_vertex, weight=None):
        """Constructor

        @type from_vertex: object
        @param from_vertex: conventionally a string; something unabiguously
                            representing the vertex at which the edge originates
        @type to_vertex: object
        @param to_vertex: conventionally a string; something unabiguously
                          representing the vertex at which the edge terminates
        @type weight: number
        @param weight: weight of the edge, defaults to None.
        """
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight

    def __str__(self):
        """printstring

        @rtype: str
        @return: printstring
        """
        return "Edge {0}{1}, weight {2}.".format(self.from_vertex, self.to_vertex, self.weight)


if __name__ == '__main__':
    x = Edge('A', 'B', 5)
    print x
