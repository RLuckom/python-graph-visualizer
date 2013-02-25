#!/usr/bin/env python


class FieldCombiner(object):

    def __init__(self, fields, join_string=''):
        if type(fields) is str:
            fields = [fields]
        self._field_names = fields
        self._join_string = join_string

    def join_fields(self, dict):
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
