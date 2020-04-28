class SemanticError(Exception):
    pass


declared_tokens = set()


def semantic_analysis(tree, level=0):
    if tree is None:
        return
    if tree.label == 'variables':
        for token in tree.tokens:
            if token in declared_tokens:
                raise SemanticError('{} defined here: line number {}'.format(token.payload, token.line_number))
            if token.group == 'id':
                declared_tokens.add(token)
    else:
        for token in tree.tokens:
            if token.group == 'id':
                if token not in declared_tokens:
                    raise SemanticError('{} used before declaration: line number {}'.format(token.payload, token.line_number))
    for child in tree.children:
        semantic_analysis(child, level + 1)
    return True
