from tree import TreeNode
from scanner import Scanner
from token import Token


class ParserError(Exception):
    def __init__(self, line_no, identifier, expected, received):
                message = 'ID: {}; Expected {} but received {}'.format(identifier, expected, received)
                super(ParserError, self).__init__(message)


RELATIONAL_OPERATORS = set(['>', '>>', '<', '<<', '==', '=', '<>'])


scan = None
tk = None

def variables():
    global scan, tk
    node = TreeNode('variables')
    # Discard keyword
    if tk.group == 'keyword' and tk.payload == 'data':
        tk = next(scan)
        if tk.group == 'id':
            node.tokens.append(tk)
            tk = next(scan)
            if tk.payload == '=':
                node.tokens.append(tk)
                tk = next(scan)
                if tk.group == 'digit':
                    node.tokens.append(tk)
                    tk = next(scan)
                    if tk.payload == '.':
                        tk = next(scan)
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
    global tk, scan
    node = TreeNode('r')
    if tk.payload == '(':
        node.tokens.append(tk)
        tk = next(scan)
        if tk.group == 'id':
            node.tokens.append(tk)
            tk = next(scan)
            if tk.payload == ')':
                node.tokens.append(tk)
                tk = next(scan)
            else:
                raise ParserError(tk.line_number, tk.identifier, ')', tk.payload)
        else:
            raise ParserError(tk.line_number, tk.identifier, 'id', tk.group)
    elif tk.group == 'id':
        node.tokens.append(tk)
        tk = next(scan)
        return node
    elif tk.group == 'digit':
        node.tokens.append(tk)
        tk = next(scan)
        return node


def m():
    global tk, scan
    node = TreeNode('m')
    if tk.payload == '*':
        node.tokens.append(tk)
        tk = next(scan)
        node.child0 = m()
    else:
        node.child0 = r()
    return node


def a():
    global tk, scan
    node = TreeNode('a')
    node.child0 = m()
    if tk.payload == '+':
        node.tokens.append(tk)
        tk = next(scan)
        node.child1 = a()
    return node


def n():
    global tk, scan
    node = TreeNode('n')
    node.child0 = a()
    if tk.payload in set(['/', '*']):
        node.tokens.append(tk)
        tk = next(scan)
        node.child1 = n()
    return node


def expr():
    global tk, scan
    node = TreeNode('expr')
    node.child0 = n()
    if tk.payload == '-':
        node.tokens.append(tk)
        tk = next(scan)
        node.child1 = expr()
    return node



def intk():
    global tk, scan
    node = TreeNode('intk')
    if tk.payload == 'in':
        tk = next(scan)
        if tk.group == 'id':
            node.tokens.append(tk)
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, 'id', tk.group)
    else:
        raise ParserError(tk.line_number, tk.identifier, 'in', tk.payload)


def out():
    global tk, scan
    node = TreeNode('out')
    if tk.payload == 'out':
        tk = next(scan)
        node.child0 = expr()
        return node
    else:
        raise ParserError(tk.line_number, tk.identifier, 'out', tk.payload)


def assign():
    global tk, scan
    node = TreeNode('assign')
    if tk.group == 'id':
        node.tokens.append(tk)
        tk = next(scan)
        if tk.payload == '=':
            node.tokens.append(tk)
            tk = next(scan)
            node.child0 = expr()
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, '=', tk.payload)
    else:
        raise ParserError(tk.line_number, tk.identifier, 'expression', tk.group)


def ro():
    global tk, scan
    node = TreeNode('ro')
    if tk.payload in RELATIONAL_OPERATORS:
        node.tokens.append(tk)
        tk = next(scan)
        return node
    return None


def iffy():
    global tk, scan
    node = TreeNode('iffy')
    if tk.payload == 'iffy':
        tk = next(scan)
        if tk.payload == '[':
            tk = next(scan)
            node.child0 = expr()
            node.child1 = ro()
            node.child2 = expr()
            if tk.payload == ']':
                tk = next(scan)
                if tk.payload == 'then':
                    tk = next(scan)
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
    global tk, scan
    node = TreeNode('loop')
    if tk.payload == 'loop':
        tk = next(scan)
        if tk.payload == '[':
            tk = next(scan)
            node.child0 = expr()
            node.child1 = ro()
            node.child2 = expr()
            if tk.payload == ']':
                tk = next(scan)
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
    global tk, scan
    node = TreeNode('stat')
    if tk.payload == 'in':
        node.child0 = intk()
        tk = next(scan)
        if tk.payload == '.':
            tk = next(scan)
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, '.', tk.payload)
    elif tk.payload == 'out':
        node.child0 = out()
        if tk.payload == '.':
            tk = next(scan)
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, '.', tk.payload)
    elif tk.payload == 'begin':
        node.child0 = block()
        return node
    elif tk.payload == 'iffy':
        node.child0 = iffy()
        if tk.payload == '.':
            tk = next(scan)
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, '.', tk.payload)
    elif tk.payload == 'loop':
        node.child0 = loop()
        if tk.payload == '.':
            tk = next(scan)
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, '.', tk.payload)
    elif tk.group == 'id':
        node.child0 = assign()
        if tk.payload == '.':
            tk = next(scan)
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, '.', tk.payload)
    else:
        raise ParserError(tk.line_number, tk.identifier, 'body', 'none')

def mstat():
    global tk, scan
    node = TreeNode('mstat')
    if tk.payload in set(['in', 'out', 'iffy', 'loop', 'begin']) or tk.group == 'id':
        node.child0 = stat()
        node.child1 = mstat()
        return node
    else:
        return None


def stats():
    global tk, scan
    node = TreeNode('stats')
    node.child0 = stat()
    node.child1 = mstat()
    return node

def block():
    global tk, scan
    node = TreeNode('block')
    if tk.group == 'keyword' and tk.payload == 'begin':
        tk = next(scan)
        node.child0 = variables()
        node.child1 = stats()
        if tk.payload == 'end':
            tk = next(scan)
            return node
        else:
            raise ParserError(tk.line_number, tk.identifier, 'end', tk.payload)
    else:
        raise ParserError(tk.line_number, tk.identifier, 'begin', tk.payload)
    return node


def program():
    global tk, scan
    tree = TreeNode('program')
    tree.child0 = variables()
    tree.child1 = block()
    return tree


def parser_func(_scanner):
    global scan, tk
    scan = _scanner
    tk = next(scan)
    tree = program()
    if tk.payload == 'eof':
        return tree
    else:
        raise ParserError(tk.line_number, tk.identifier, 'eof', tk.payload)
