# Require compatibility for python 2. Pull commmon
# changes.
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


KEYWORD_PATH = 'keywords.kwds'
with open(KEYWORD_PATH, 'r') as keyword_file:
    keyword_list = keyword_file.read().split()
KEYWORD_SET = set(keyword_list)


class Token:
    def __init__(self, group, payload, identifier, line_number):
        if group == 'id' and self._is_keyword(payload):
            self._group = 'keyword'
        else:
            self._group = group

        self._payload = payload
        self._identifier = identifier
        self._line_number = line_number

    def _is_keyword(self, payload):
        if payload in KEYWORD_SET:
            return True
        return False

    @property
    def group(self):
        return self._group

    @property
    def payload(self):
        return self._payload
    
    @property
    def identifier(self):
        return self._identifier

    @property
    def line_number(self):
        return self._line_number

    def __repr__(self):
        return '< {} >'.format(self.__str__())

    def __str__(self):
        return 'id: {}; type: {}; line_number: {}; token: {};'.format(self.identifier, self.group, self.line_number, self.payload)
