#!/usr/bin/env python3

# Add the project root directory to sys.path
import sys
from pathlib import Path
wumps_root = Path(sys.path[0])
sys.path.insert(1, str(wumps_root))

import argparse
from lark import Lark
from wumps.lark import post_lex

grammar_file = str(wumps_root / "wumps" / "lark" / "grammar.lark")

def create_arg_parser():
    arg_parser = argparse.ArgumentParser(
        description="Parse a wumps input file.")
    arg_parser.add_argument(
        "filenames",
        nargs = "+",
        help = "names of the input files to parse")
    arg_parser.add_argument(
        "--parser",
        default = "lalr",
        choices = ["lalr", "earley"],
        help = "specify the parsing algorithm to use")
    arg_parser.add_argument(
        "--lexer",
        default = "standard",
        choices = ["standard", "contextual"],
        help = "specify the lexer to use (contextual only works with lalr "
        "parser")
    arg_parser.add_argument(
        "--lex",
        action = "store_true",
        help = "print the output of the lexer before post-lexing and parsing")
    arg_parser.add_argument(
        "--post-lex",
        action = "store_true",
        help = "print the output of the post-lexer before parsing")
    arg_parser.add_argument(
        "--parse",
        action = "store_true",
        help = "print the output of the parser")
    arg_parser.add_argument(
        "--ast",
        action = "store_true",
        help = "print the abstract syntax tree")
    arg_parser.add_argument(
        "--debug",
        action = "store_true",
        help = "debug parser")
    return arg_parser

def main():
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    grammar = open(grammar_file).read()
    grammar = grammar.replace("\\\n", "")
    parser = Lark(grammar,
                  start=["file", "unused_terminals"],
                  parser=args.parser,
                  lexer=args.lexer,
                  postlex=post_lex.Post_Lex_Processor(),
                  #ambiguity="explicit",
                  debug=args.debug,
                  )

    # Process each file specified on the command line.
    for file_name in args.filenames:
        text = open(file_name).read()
        if args.lex:
            generator = parser._build_lexer().lex(text)
            print(f'--- Lexer output for "{file_name}" ---')
            post_lex.print_lex(generator)
            print()
        if args.post_lex:
            generator = parser.lex(text)
            print(f'--- Post-Lexer output for "{file_name}" ---')
            post_lex.print_lex(generator)
            print()
        if args.parse or args.ast:
            tree = parser.parse(text, start="file")
        if args.parse:
            print(f'--- Parse Tree for "{file_name}" ---')
            print(tree.pretty(),end="")
            print()
        if args.ast:
            print("not implemented")
            print()
            
        #for item in tree.children:
        #    print(type(item))
            
if __name__ == "__main__":
    main()
