from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


class TreeNode:
    def __init__(self, label, child0=None, child1=None, child2=None, child3=None):
        self.label = label
        self.tokens = list()
        self.child0 = child0
        self.child1 = child1
        self.child2 = child2
        self.child3 = child3


def print_tree(node, level=0):
    if node is not None:
        padding = ' ' * level * 4
        print('{} {}'.format(padding, node.label))
        print('{} {}'.format(padding, '|'.join([str(tk) for tk in node.tokens])))
        print_tree(node.child0, level + 1)
        print_tree(node.child1, level + 1)
        print_tree(node.child2, level + 1)
        print_tree(node.child3, level + 1)
