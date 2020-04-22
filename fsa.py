# Require compatibility for python 2. Pull commmon
# changes.
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import string
from scanner import Scanner
from readers import FileReader


class ParserError(Exception):
    def __init__(self, message):
        message = 'SCANNER ERROR: {}'.format(message)
        super(ParserError, self).__init__(message)


DIGITS = set(c for c in string.digits)
LETTERS = set(c for c in string.ascii_letters)
OPERATOR_STRING = '<>:+-*/%.(),{};[]'
OPERATORS = set(c for c in OPERATOR_STRING)
FULL_OPERATORS = OPERATORS.union(set(['=']))
WHITESPACE_CHARACTERS = set(c for c in string.whitespace)


def start_state_transition(character):
    if character in LETTERS:
        return 'a'
    elif character in DIGITS:
        return 'b'
    elif character in WHITESPACE_CHARACTERS:
        return 'start'
    elif character in OPERATORS:
        return 'c'
    elif character == '=':
        return 'd'
    else:
        raise ParserError('invalid character: {}'.format(character))


def a_state_transition(character):
    if character in LETTERS.union(DIGITS):
        return 'a'
    elif character in WHITESPACE_CHARACTERS.union(FULL_OPERATORS):
        return 'id'
    else:
        raise ParserError('invalid character in id: {}'.format(character))


def b_state_transition(character):
    if character in DIGITS:
        return 'b'
    elif character in LETTERS.union(WHITESPACE_CHARACTERS).union(FULL_OPERATORS):
        return 'digit'
    else:
        raise ParserError('invalid fromat in digit: {}'.format(character))


def c_state_transition(character):
    if character in LETTERS.union(WHITESPACE_CHARACTERS).union(FULL_OPERATORS):
        return 'operator'
    else:
        raise ParserError('invalid character in operator: {}'.format(character))


def d_state_transition(character):
    if character == '=':
        return 'operator'
    if character in LETTERS.union(WHITESPACE_CHARACTERS):
        return 'operator'
    else:
        raise ParserError('invalid character in operator: {}'.format(character))


def initialize_scanner(source_path):
    reader = FileReader(source_path)
    machine = Scanner(reader)
    
    machine.add_state('start', start_state_transition)
    machine.add_state('a', a_state_transition)
    machine.add_state('b', b_state_transition)
    machine.add_state('c', c_state_transition)
    machine.add_state('d', d_state_transition)
    machine.add_state('id', None, end_state=True)
    machine.add_state('digit', None, end_state=True)
    machine.add_state('operator', None, end_state=True)
    
    machine.set_start('start')

    return machine
