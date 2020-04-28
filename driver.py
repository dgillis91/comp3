from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import argparse
from fsa import initialize_scanner
from parser import parser_func
from tree import print_tree
from staticsem import semantic_analysis


parser = argparse.ArgumentParser()
parser.add_argument('path', help='path to file. do not include ext.')
args = parser.parse_args()

scanner = initialize_scanner(args.path)

tree = parser_func(scanner)

if semantic_analysis(tree):
    print('PASSED SEMANTIC ANALYSIS')
