from tree import TreeNode
from scanner import Scanner
from token import Token


class ParserError(Exception):
    def __init__(self, line_no, identifier, expected, received):
                message = 'ID: {}; Expected {} but received {}'.format(identifier, expected, received)
                super(ParserError, self).__init__(message)


RELATIONAL_OPERATORS = set(['>', '>>', '<', '<<', '==', '=', '<>'])

tokens = list()
token_index = 0


def variables():
    global tokens, token_index
    node = TreeNode('variables')
    tk = tokens[token_index]
    # Discard keyword
    if tk.group == 'keyword' and tk.payload == 'data':
        token_index += 1
        tk = tokens[token_index]
        if tk.group == 'id':
            node.tokens.append(tk)
            token_index += 1
            tk = tokens[token_index]
            if tk.payload == '=':
                node.tokens.append(tk)
                token_index += 1
                tk = tokens[token_index]
                if tk.group == 'digit':
                    node.tokens.append(tk)
                    token_index += 1
                    tk = tokens[token_index]
                    if tk.payload == '.':
                        token_index += 1
                        node.child0 = variables()
                        return node
                    else:
                        raise ParserError(tk.line_number, tk.identifier, '.', tk.payload)
                else:
                    raise ParserError(tk.line_number, tk.identifier, 'digit', tk.group)
            else:
                raise ParserError(tk.line_number, tk.identifier, '=', tk.payload)
        else:
            raise ParserError(tk.line_number, tk.identifier, 'id', tk.group)
    return node


def r():
    global tokens, token_index
    node = TreeNode('r')
    tk = tokens[token_index]
    if tk.payload == '(':
        node.tokens.append(tk)
        token_index += 1
        tk = tokens[token_index]
        if tk.group == 'id':
            node.tokens.append(tk)
            token_index += 1
            tk = tokens[token_index]
            if tk.payload == ')':
                node.tokens.append(tk)
                token_index += 1
            else:
                raise ParserError(tk.line_number, tk.identifier, ')', tk.payload)
        else:
            raise ParserError(tk.line_number, tk.identifier, 'id', tk.group)
    elif tk.group == 'id':
        node.tokens.append(tk)
        token_index += 1
        return node
    elif tk.group == 'digit':
        node.tokens.append(tk)
        token_index += 1
        return node


def m():
    global tokens, token_index
    node = TreeNode('m')
    tk = tokens[token_index]
    if tk.payload == '*':
        node.tokens.append(tk)
        token_index += 1
        node.child0 = m()
    else:
        node.child0 = r()
    return node


def a():
    global tokens, token_index
    node = TreeNode('a')
    node.child0 = m()
    tk = tokens[token_index]
    if tk.payload == '+':
        node.tokens.append(tk)
        token_index += 1
        node.child1 = a()
    return node


def n():
    global tokens, token_index
    node = TreeNode('n')
    node.child0 = a()
    tk = tokens[token_index]
    if tk.payload in set(['/', '*']):
        node.tokens.append(tk)
        token_index += 1
        node.child1 = n()
    return node


def expr():
    global tokens, token_index
    node = TreeNode('expr')
    node.child0 = n()
    tk = tokens[token_index]
    if tk.payload == '-':
        node.tokens.append(tk)
        token_index += 1
        node.child1 = expr()
    return node



def intk():
    global tokens, token_index
    node = TreeNode('intk')
    tk = tokens[token_index]
    if tk.payload == 'in':
        token_index += 1
        tk = tokens[token_index]
        if tk.group == 'id':
            node.tokens.append(tk)
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, 'id', tk.group)
    else:
        raise ParserError(tk.line_number, tk.identifier, 'in', tk.payload)


def out():
    global tokens, token_index
    node = TreeNode('out')
    tk = tokens[token_index]
    if tk.payload == 'out':
        token_index += 1
        node.child0 = expr()
        return node
    else:
        raise ParserError(tk.line_number, tk.identifier, 'out', tk.payload)


def assign():
    global tokens, token_index
    node = TreeNode('assign')
    tk = tokens[token_index]
    if tk.group == 'id':
        node.tokens.append(tk)
        token_index += 1
        tk = tokens[token_index]
        if tk.payload == '=':
            node.tokens.append(tk)
            token_index += 1
            node.child0 = expr()
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, '=', tk.payload)
    else:
        raise ParserError(tk.line_number, tk.identifier, 'expression', tk.group)


def ro():
    global tokens, token_index
    node = TreeNode('ro')
    tk = tokens[token_index]
    if tk.payload in RELATIONAL_OPERATORS:
        node.tokens.append(tk)
        token_index += 1
        return node
    return None


def iffy():
    global tokens, token_index
    node = TreeNode('iffy')
    tk = tokens[token_index]
    if tk.payload == 'iffy':
        token_index += 1
        tk = tokens[token_index]
        if tk.payload == '[':
            token_index += 1
            node.child0 = expr()
            node.child1 = ro()
            node.child2 = expr()
            tk = tokens[token_index]
            if tk.payload == ']':
                token_index += 1
                tk = tokens[token_index]
                if tk.payload == 'then':
                    token_index += 1
                    node.child3 = stat()
                    return node
                else:
                    raise ParserError(tk.line_number, tk.identifier, 'then', tk.payload)
            else:
                raise ParserError(tk.line_number, tk.identifier, ']', tk.payload)
        else:
            raise ParserError(tk.line_number, tk.identifier, '[', tk.payload)
    else:
        raise ParserError(tk.line_number, tk.identifier, 'iffy', tk.payload)
    return None
    

def loop():
    global tokens, token_index
    node = TreeNode('loop')
    tk = tokens[token_index]
    if tk.payload == 'loop':
        token_index += 1
        tk = tokens[token_index]
        if tk.payload == '[':
            token_index += 1
            node.child0 = expr()
            node.child1 = ro()
            node.child2 = expr()
            tk = tokens[token_index]
            if tk.payload == ']':
                token_index += 1
                node.child3 = stat()
                return node
            else:
                raise ParserError(tk.line_number, tk.identifier, ']', tk.payload)
        else:
            raise ParserError(tk.line_number, tk.identifier, '[', tk.payload)
    else:
        raise ParserError(tk.line_number, tk.identifier, 'loop', tk.payload)
    return None



def stat():
    global tokens, token_index
    node = TreeNode('stat')
    tk = tokens[token_index]
    if tk.payload == 'in':
        node.child0 = intk()
        token_index += 1
        tk = tokens[token_index]
        if tk.payload == '.':
            token_index += 1
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, '.', tk.payload)
    elif tk.payload == 'out':
        node.child0 = out()
        tk = tokens[token_index]
        if tk.payload == '.':
            token_index += 1
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, '.', tk.payload)
    elif tk.payload == 'begin':
        node.child0 = block()
        return node
    elif tk.payload == 'iffy':
        node.child0 = iffy()
        tk = tokens[token_index]
        if tk.payload == '.':
            token_index += 1
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, '.', tk.payload)
    elif tk.payload == 'loop':
        node.child0 = loop()
        tk = tokens[token_index]
        if tk.payload == '.':
            token_index += 1
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, '.', tk.payload)
    elif tk.group == 'id':
        node.child0 = assign()
        tk = tokens[token_index]
        if tk.payload == '.':
            token_index += 1
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, '.', tk.payload)
    else:
        raise ParserError(tk.line_number, tk.identifier, 'body', 'none')

def mstat():
    global tokens, token_index
    node = TreeNode('mstat')
    # Just peek at the token
    tk = tokens[token_index]
    if tk.payload in set(['in', 'out', 'iffy', 'loop', 'begin']) or tk.group == 'id':
        node.child0 = stat()
        node.child1 = mstat()
        return node
    else:
        return None


def stats():
    global tokens, token_index
    node = TreeNode('stats')
    node.child0 = stat()
    node.child1 = mstat()
    return node

def block():
    global tokens, token_index
    node = TreeNode('block')
    tk = tokens[token_index]
    if tk.group == 'keyword' and tk.payload == 'begin':
        token_index += 1
        node.child0 = variables()
        node.child1 = stats()
        tk = tokens[token_index]
        if tk.payload == 'end':
            token_index += 1
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, 'end', tk.payload)
    else:
        raise ParserError(tk.line_number, tk.identifier, 'begin', tk.payload)
    return node


def program():
    global tokens
    global token_index
    tree = TreeNode('program')
    tree.child0 = variables()
    tree.child1 = block()
    return tree


def parser_func(_scanner: Scanner):
    global tokens
    for tk in _scanner.get_token():
        tokens.append(tk)
    tokens.append(Token('EOFTK', 'EOFTK', -1, -1))
    return program()