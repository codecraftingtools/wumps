#!/usr/bin/env python3

import argparse
from parglare_mod import Parser, GLRParser, Grammar

arg_parser = argparse.ArgumentParser(
    description="Parse an input file and print the AST.")
arg_parser.add_argument(
    "filename",
    help = "name of the input file to parse")
arg_parser.add_argument(
    "--glr",
    action = "store_true",
    help = "use the GLR parser instead of the default LR parser")
arg_parser.add_argument(
    "--debug-parser",
    action = "store_true",
    help = "put the parser in debug mode")
args = arg_parser.parse_args()

if args.glr:
    parser_type = GLRParser
else:
    parser_type = Parser

grammar = Grammar.from_file("grammar.pg")
parser = parser_type(grammar, debug=args.debug_parser)
result = parser.parse_file(args.filename)

if isinstance(parser, GLRParser):
    # The GLR parser returns a list of parse trees
    for tree in result:
        tree.print()
else:
    # The LR parser return a single parse tree
    result.print()
