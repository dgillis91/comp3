# Require compatibility for python 2. Pull commmon
# changes.
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from readers import FileReader
from token import Token


class Scanner:
    def __init__(self, reader: FileReader):
        self._reader = reader
        self._handlers = dict()
        self._start_state = None
        self._end_states = set()

    def add_state(self, name, handler, end_state=False):
        self._handlers[name] = handler
        if end_state:
            self._end_states.add(name)
        
    def set_start(self, name):
        self._start_state = name

    def run(self):
        buffer = list()
        for character in self._reader.get_char():
            buffer.append(character)

    def _reset_fsm(self):
        try:
            handler = self._handlers[self._start_state]
        except:
            raise RuntimeError('must call .set_start() before .run()')
        if not self._end_states:
            raise RuntimeError('at least one state must be an end_state')
        return handler

    def get_token(self):
        handler = self._reset_fsm()
        buffer = list()
        identifier = 0

        for char in self._reader.get_char():
            buffer.append(char.character)
            new_state = handler(char.character)
            if new_state in self._end_states:
                yield Token(new_state, ''.join(buffer).strip(), identifier, char.line_number)
                buffer = list()
                identifier += 1
                handler = self._reset_fsm()
            else:
                handler = self._handlers[new_state]
