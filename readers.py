# Require compatibility for python 2. Pull commmon
# changes.
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from character import Character, COMMENT_CHARACTER

DEFAULT_FILE_EXT = '.sp2020'


class InvalidCommentError(Exception):
    pass


class FileReader:
    def __init__(self, filename):
        self._filename = filename + DEFAULT_FILE_EXT
        self._data = None
        self._line_number = 1
        self._character_index = 0

    @property
    def line_number(self):
        return self._line_number

    @property
    def character_number(self):
        return self._character_index

    def get_char(self):
        in_comment = False
        for char in self._get_next():
            self._character_index += 1
            if char == COMMENT_CHARACTER:
                in_comment = not in_comment
                continue
            if in_comment:
                continue
            yield Character(char, self.character_number, self.line_number)
            if char == '\n':
                self._line_number += 1
                self._character_index = 0
        if in_comment:
            raise InvalidCommentError('unclosed comment block')

    def _get_next(self):
        if not self._data:
            self._initialize_data()
        for char in self._data:
            yield char
        yield '\n'

    def _initialize_data(self):
        with open(self._filename, 'r') as input_file:
            self._data = list(input_file.read())
            self._data.append('\n')
            self._data.append('')
