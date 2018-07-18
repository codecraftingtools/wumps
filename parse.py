#!/usr/bin/env python3

# Parse input files and print the AST

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
arg_parser.add_argument(
    "--build-tree",
    action = "store_true",
    help = "use the parglare parser's build_tree option (does not work yet "
    "unless AST construction actions are commented out of grammar_actions.py)"
)
args = arg_parser.parse_args()

if args.glr:
    parser_type = GLRParser
else:
    parser_type = Parser

grammar = Grammar.from_file("grammar.pg")
parser = parser_type(
    grammar, debug=args.debug_parser, build_tree=args.build_tree,
    call_actions_during_tree_build=True)
results = parser.parse_file(args.filename)

# The GLR parser returns a list of parse trees, but the standard
# parser returns a single parse tree.
if not isinstance(results, list):
    results = [results]
n_results = len(results)

for i, tree in enumerate(results):
    maybe_glr = "GLR " if isinstance(parser, GLRParser) else ""
    maybe_tree_number = " #{}".format(i+1) if n_results > 1 else ""
    print('--- {}Parse Tree{} for "{}" ---'.format(
        maybe_glr, maybe_tree_number, args.filename))
    if args.build_tree:
        print(tree.tree_str(), end="")
    else:
        print(tree.get_ast_str(), end="")
