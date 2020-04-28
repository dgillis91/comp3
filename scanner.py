# Require compatibility for python 2. Pull commmon
# changes.
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from readers import FileReader
from token import Token


class Scanner:
    def __init__(self, reader):
        self._reader = reader
        self._handlers = dict()
        self._start_state = None
        self._end_states = set()

        self._identifier_iterator = 0
        self._generator = self._reader.get_char()

    def add_state(self, name, handler, end_state=False):
        self._handlers[name] = handler
        if end_state:
            self._end_states.add(name)
        
    def set_start(self, name):
        self._start_state = name

    def _reset_fsm(self):
        try:
            handler = self._handlers[self._start_state]
        except:
            raise RuntimeError('must call .set_start() before .run()')
        if not self._end_states:
            raise RuntimeError('at least one state must be an end_state')
        return handler

    def __iter__(self):
        self._identifier_iterator = 0
        return self

    def __next__(self):
        handler = self._reset_fsm()
        buffer = list()
        while True:
            char = next(self._generator)
            if char.character == '':
                return Token('keyword', 'eof', self._identifier_iterator, char.line_number)
            buffer.append(char.character)
            new_state = handler(char.character)
            if new_state in self._end_states:
                self._identifier_iterator += 1
                return Token(new_state, ''.join(buffer).strip(), self._identifier_iterator, char.line_number)
            else:
                handler = self._handlers[new_state]

    # Support for python 3
    def next(self):
        handler = self._reset_fsm()
        buffer = list()
        while True:
            char = next(self._generator)
            if char.character == '':
                return Token('keyword', 'eof', self._identifier_iterator, char.line_number)
            buffer.append(char.character)
            new_state = handler(char.character)
            if new_state in self._end_states:
                self._identifier_iterator += 1
                return Token(new_state, ''.join(buffer).strip(), self._identifier_iterator, char.line_number)
            else:
                handler = self._handlers[new_state]
