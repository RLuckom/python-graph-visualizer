#!/usr/bin/env python

from collections import namedtuple

import vtk


class Graph(object):

    vertex_tuple = namedtuple('vertex_tuple', ['label', 'type', 'vertex'])

    def __init__(self, vertices, edges):
        self._graph = vtk.vtkMutableDirectedGraph()
        self._weights = vtk.vtkDoubleArray()
        self._weights.SetNumberOfComponents(1)
        self._weights.SetName('Weights')
        self._labels = vtk.vtkStringArray()
        self._labels.SetNumberOfComponents(1)
        self._labels.SetName('labels')
        self._vertex_dict = self._populate_vertex_dict(vertices)
        self._populate_edges(edges)
        self._graph.GetVertexData().AddArray(self._labels)
        self._graph.GetEdgeData().AddArray(self._weights)

        graphLayoutView = vtk.vtkGraphLayoutView()
        graphLayoutView.AddRepresentationFromInput(self._graph)
        graphLayoutView.SetLayoutStrategy("Simple 2D")
        graphLayoutView.GetLayoutStrategy().SetEdgeWeightField("Weights")
        graphLayoutView.GetLayoutStrategy().SetWeightEdges(1)
        graphLayoutView.SetEdgeLabelArrayName("Weights")
        graphLayoutView.SetEdgeLabelVisibility(1)
        graphLayoutView.SetVertexLabelArrayName('labels')
        graphLayoutView.SetVertexLabelVisibility(1)
        graphLayoutView.ResetCamera()
        graphLayoutView.Render()
        graphLayoutView.GetLayoutStrategy().SetRandomSeed(0)
        graphLayoutView.GetInteractor().Start()

    def _populate_vertex_dict(self, vertices):
        vertex_dict = {}
        for v in vertices:
            label = v.label
            self._labels.InsertNextValue(label)
            vertex = self._graph.AddVertex()
            typ = v.type
            vertex_dict[label] = self.vertex_tuple(label, typ, vertex)
        return vertex_dict

    def _populate_edges(self, edges):
        for edge in edges:
            from_vertex = self._vertex_dict[edge.from_vertex]
            to_vertex = self._vertex_dict[edge.to_vertex]
            weight = edge.weight
            self._graph.AddGraphEdge(from_vertex.vertex, to_vertex.vertex)
            self._weights.InsertNextValue(weight)
