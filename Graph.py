#!/usr/bin/env python

from collections import namedtuple
import random
import vtk

from abstract_graph.Vertex import Vertex
from abstract_graph.Edge import Edge
from Interactor import MouseAndKeysInteractor


class Graph(object):
    """Class to represent a graph for purposes of analysis and manipulation."""

    vertex_tuple = namedtuple('vertex_tuple', ['abstract_vertex', 'visual_vertex'])

    def __init__(self, name=None):
        """Constructor

        @type name: str
        @param name: Graph name, defaults to None
        """
        self._name = name
        self._directed = False
        self._vertex_dict = {}
        self._edge_dict = {}
        self._weights = vtk.vtkDoubleArray()
        self._weights.SetName('Weights')
        self._weights.SetNumberOfComponents(1)
        self._labels = vtk.vtkStringArray()
        self._labels.SetNumberOfComponents(1)
        self._labels.SetName('labels')
        self._graph = vtk.vtkMutableDirectedGraph()
        self._color_picker = vtk.vtkColorSeries()
        self._color_dict = {}
        self._colors = []
        self._vertex_types = 1

    def __str__(self):
        """printstr

        @rtype: str
        @return: printstring
        """
        printstr = 'GRAPH: {0}\n\n\n'.format(self.name)
        for vertex in self.vertex_dict:
            printstr += str(self.vertex_dict[vertex])
        return printstr

    def add_vertex(self, vertex_name, vertex_type=None):
        """add a vertex to the graph

        vertex is of Vertex type

        @type vertex_name: str
        @param vertex_name: name for the vertex. will be used as a label in the visualization.
        @type vertex_type: str
        @param vertex_type: Optional field for a type string, like 'donor', or 'contributor'. Defaults to None
        """
        if vertex_name not in self._vertex_dict:
            self._labels.InsertNextValue(vertex_name)
            self._vertex_dict[vertex_name] = self.vertex_tuple(Vertex(vertex_name, vertex_type),
                                                               self._graph.AddVertex())
            if vertex_type not in self._color_dict:
                self._color_dict[vertex_type] = self._vertex_types
                self._vertex_types += 1
            self._colors.append(self._color_dict[vertex_type])

    def add_undirected_edge(self, vertex_one, vertex_two, weight=None):
        """Adds directed edges of the same weight between two nodes

        @type vertex_one: str
        @param vertex_one: str of the name of the first vertex
        @type vertex_two: str
        @param vertex_two: str of the name of the second vertex. Order doesn't matter.
        @type weight: number
        @param weight: weight of the edge, defaults to None
        """
        self._edge_dict[vertex_one, vertex_two] = Edge(vertex_one, vertex_two, weight)
        self._edge_dict[vertex_two, vertex_one] = Edge(vertex_two, vertex_one, weight)
        self._vertex_dict[vertex_two].abstract_vertex.add_edge(vertex_one, weight)
        self._vertex_dict[vertex_one].abstract_vertex.add_edge(vertex_two, weight)
        from_vertex = self._vertex_dict[vertex_one].visual_vertex
        to_vertex = self._vertex_dict[vertex_two].visual_vertex
        self._graph.AddGraphEdge(from_vertex, to_vertex)
        self._weights.InsertNextValue(weight)
        to_vertex = self._vertex_dict[vertex_one].visual_vertex
        from_vertex = self._vertex_dict[vertex_two].visual_vertex
        self._graph.AddGraphEdge(from_vertex, to_vertex)
        self._weights.InsertNextValue(weight)

    def add_directed_edge(self, from_vertex, to_vertex, weight=None):
        """adds a single directed edge from from_vertex to to_vertex.

        @type from_vertex: str
        @param from_vertex: vertex from which the directed edge originates
        @type to_vertex: str
        @param to_vertex: vertex at which the directed edge terminates
        @type weight: number
        @param weight: weight of the edge, defaults to None
        """
        self._directed = True
        self._vertex_dict[from_vertex].abstract_vertex.add_edge(to_vertex, weight)
        from_vertex = self._vertex_dict[from_vertex].visual_vertex
        to_vertex = self._vertex_dict[to_vertex].visual_vertex
        self._graph.AddGraphEdge(from_vertex, to_vertex)
        self._weights.InsertNextValue(weight)

    def visualize_graph(self):
        """shows a visualization of the graph"""
        self._graph.GetVertexData().AddArray(self._labels)
        self._graph.GetEdgeData().AddArray(self._weights)
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(1)
        colors.SetName('Colors')
        types = int(245 / len(self._color_dict))
        for c in self._colors:
            colors.InsertNextValue(int(c * types))
        self._graph.GetVertexData().AddArray(colors)
        graphLayoutView = vtk.vtkGraphLayoutView()
        graphLayoutView.AddRepresentationFromInput(self._graph)
        graphLayoutView.SetLayoutStrategy(vtk.vtkSpanTreeLayoutStrategy())
        graphLayoutView.GetLayoutStrategy().SetEdgeWeightField("Weights")
        graphLayoutView.GetLayoutStrategy().SetWeightEdges(1)
        graphLayoutView.GetRenderer().GetActiveCamera().ParallelProjectionOff()
        graphLayoutView.SetEdgeLabelArrayName("Weights")
        graphLayoutView.SetEdgeLabelVisibility(1)
        graphLayoutView.SetVertexLabelArrayName('labels')
        graphLayoutView.SetVertexLabelVisibility(1)
        graphLayoutView.SetVertexColorArrayName('Colors')
        graphLayoutView.SetColorVertices(1)
        graphLayoutView.SetInteractorStyle(MouseAndKeysInteractor(graphLayoutView))
        graphLayoutView.ResetCamera()
        graphLayoutView.Render()
        graphLayoutView.GetInteractor().Start()

    def minimum_spanning_tree(self):
        """Calculate mst of graph

        only works on undirected graphs.

        @type Exception:
        @throws Exception: if graph is directed
        @rtype: list
        @return: list of Edge objects in the mst
        """
        if self._directed:
            raise Exception('Current implementation of minimum spanning tree does not work for directed graphs')
        vertices = [self._vertex_dict[x].abstract_vertex for x in self._vertex_dict]
        tree = {'vertices': [random.choice(vertices)], 'edges': []}
        while len(tree['vertices']) < len(vertices):
            best_edge_number = None
            best_edge = None
            best_vertex = None
            vertex_names = [vertex.label for vertex in tree['vertices']]
            for vertex in tree['vertices']:
                for edge in vertex.edges:
                    if edge not in vertex_names and (vertex.edges[edge] < best_edge_number or best_edge is None):
                        best_edge_number = vertex.edges[edge]
                        best_edge = self._edge_dict[vertex.label, edge]
                        best_vertex = edge
            tree['vertices'].append(self._vertex_dict[best_vertex].abstract_vertex)
            tree['edges'].append(best_edge)
        return tree['edges']

if __name__ == '__main__':
    graph = Graph('wikipedia example')
    graph.add_vertex('A', 1)
    graph.add_vertex('B', 2)
    graph.add_vertex('C', 3)
    graph.add_vertex('D', 2)
    graph.add_vertex('E', 1)
    graph.add_vertex('F', 4)
    graph.add_vertex('G', 1)
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
    graph.visualize_graph()
