#!/usr/bin/env python

from collections import namedtuple
import csv
from decimal import Decimal
from re import sub

from FieldCombiner import FieldCombiner
from Graph import Graph


class ContributionList(list):
    """list subclass that reads donation info from a file and converts it into a form that can be graphed."""

    standard_fields = ['donor', 'recipient', 'amount']
    Contribution = namedtuple('Contribution', standard_fields)

    def __init__(self, contribution_file_name, delim,
                 quotecharacter, contributor_name_combiner,
                 recipient_name_combiner, amount_column_name):
        """Constructor

        @type contribution_file_name: str
        @param contribution_file_name: full path to filename of contributions
        @type delim: str
        @param delim: delimiter between fields in contribution list. comma, tab etc.
        @type quotechar: str
        @param quotechar: string used to represent quotes in the contribution file.
        @type contributor_name_combiner: FieldCombiner
        @param contributor_name_combiner: object that given a row will return the contributor name.
        @type recipient_name_combiner: FieldCombiner
        @param recipient_name_combiner: object that given a row will return the contributor name.
        @type amount_column_name: str
        @param amount_column_name: title of amount column in contribution file
        """

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
        """converts an amount string into a Decimal

        strips $ and ,s

        @type amount_string: str
        @param amount_string: string of amount as found from contribution file.
        @rtype: Decimal
        @return: decimal of amount
        """
        return Decimal(sub('[^\d.]', '', amount_string))

    def create_graph(self):
        """visualize graph from contributions in self

        @rtype: Graph
        @return: graph visualization
        """
        graph = Graph()
        for contrib in self:
            graph.add_vertex(contrib.donor, 'donor')
            graph.add_vertex(contrib.recipient, 'recipient')
            graph.add_directed_edge(contrib.donor, contrib.recipient, contrib.amount)
        graph.visualize_graph()


def mass_contribution_list_creator(contribution_file_name):
    """function to set up a ContributionList from a Massachusetts public disclosure.

    @type contribution_file_name: str
    @param contribution_file_name: full path to file
    @rtype: ContributionList
    @return: contributionlist from file
    """
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
