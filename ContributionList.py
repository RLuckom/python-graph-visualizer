#!/usr/bin/env python

from collections import namedtuple
import csv
from decimal import Decimal
from re import sub

from FieldCombiner import FieldCombiner
from abstract_graph.Vertex import Vertex
from abstract_graph.Edge import Edge
from Graph import Graph


class ContributionList(list):

    standard_fields = ['donor', 'recipient', 'amount']
    Contribution = namedtuple('Contribution', standard_fields)

    def __init__(self, contribution_file_name, delim,
                 quotecharacter, contributor_name_combiner,
                 recipient_name_combiner, amount_column_name):

        super(ContributionList, self).__init__()

        self._contribution_reader = csv.DictReader(open(contribution_file_name, 'rb'),
                                                   delimiter=delim,
                                                   quotechar=quotecharacter)

        for row in self._contribution_reader:
            donor = contributor_name_combiner.join_fields(row).upper()
            recipient = recipient_name_combiner.join_fields(row)
            amount = self._convert_str_to_amount(row[amount_column_name])
            self.append(self.Contribution(donor, recipient, amount))
        self._vertices = {}

    def _convert_str_to_amount(self, amount_string):
        return Decimal(sub('[^\d.]', '', amount_string))

    def create_graph(self):
        edges = []
        for contrib in self:
            self._add_vertex(contrib.donor, 'donor')
            self._add_vertex(contrib.recipient, 'recipient')
            edges.append(Edge(contrib.donor, contrib.recipient, contrib.amount))
        return Graph([self._vertices[x] for x in self._vertices], edges)

    def _add_vertex(self, vertex_name, vertex_type):
        if vertex_name not in self._vertices:
            self._vertices[vertex_name] = Vertex(vertex_name, vertex_type)
        return self._vertices[vertex_name]


def mass_contribution_list_creator(contribution_file_name):
    contributor_name_combiner = FieldCombiner(['F Name', 'L Name'], ' ')
    recipient_name_combiner = FieldCombiner('Recipient Full Name')
    amount_column_name = 'Amount'
    delim = '\t'
    quotecharacter = '"'
    contrib_list = ContributionList(contribution_file_name,
                                    delim, quotecharacter,
                                    contributor_name_combiner,
                                    recipient_name_combiner,
                                    amount_column_name)
    return contrib_list

if __name__ == '__main__':
    contribution_file_name = 'contribs.txt'
    contrib_list = mass_contribution_list_creator(contribution_file_name)
    print len(contrib_list)
    contrib_list.create_graph()
