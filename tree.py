from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


class TreeNode:
    def __init__(self, label, child0=None, child1=None, child2=None, child3=None):
        self.label = label
        self.tokens = list()
        self.children = list()


def print_tree(node, level=0):
    if node is not None:
        padding = ' ' * level * 4
        print('{} {}'.format(padding, node.label))
        print('{} {}'.format(padding, '|'.join([str(tk) for tk in node.tokens])))
        for child in node.children:
            print_tree(child, level + 1)
