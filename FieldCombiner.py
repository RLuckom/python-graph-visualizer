#!/usr/bin/env python


class FieldCombiner(object):
    """class to take dictionaries and join fields with string."""

    def __init__(self, fields, join_string=''):
        """Constructor

        @type fields: list or str
        @param fields: list of fields to be joined in order, e.g ['F Name', 'L Name']
                       If str, is turned to single-item list automatically.
        @type join_string: str
        @param join_string: string with which to join fields
        """
        if type(fields) is str:
            fields = [fields]
        self._field_names = fields
        self._join_string = join_string

    def join_fields(self, dict):
        """returns selfs fields from row_dict, joined.

        @type row_dict: dict
        @param row_dict: dictionary of row as returned by csv.DictReader
        @rtype: str
        @return: string of fields joined by join_string
        """
        try:
            return self._join_string.join([dict[field_name] for field_name in self._field_names])
        except KeyError:
            return ''

if __name__ == '__main__':
    d = {'first name': 'John', 'last name': 'Smith', 'age': 24}
    test = FieldCombiner(['first name', 'last name'], join_string=' ')
    print test.join_fields(d)
    test2 = FieldCombiner('first name')
    print test2.join_fields(d)
