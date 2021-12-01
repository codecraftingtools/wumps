#!/usr/bin/env python3

# Copyright 2019, 2020, 2021 Jeffrey A. Webb
# Copyright 2021 NTA, Inc.

# Add the project root directory to sys.path
import sys
from pathlib import Path
wumps_root = Path(sys.path[0])
sys.path.insert(1, str(wumps_root))

import argparse
from lark import Lark
from wumps.lark import post_lex, ast

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
        default = "basic",
        choices = ["basic", "contextual"],
        help = "specify the lexer to use (contextual only works with lalr "
        "parser")
    arg_parser.add_argument(
        "--list-files",
        action = "store_true",
        help = "list the names of the files being processed, in order")
    arg_parser.add_argument(
        "--lex",
        action = "store_true",
        help = "print the output of the lexer before post-lexing and parsing")
    arg_parser.add_argument(
        "--unfiltered-post-lex",
        action = "store_true",
        help = "print the output of the post-lexer before filtering and "
        "parsing")
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
        "--debug-parser",
        action = "store_true",
        help = "debug lark parser")
    return arg_parser

def create_lark_parser(grammar, args, filter_post_lex=True):
    parser = Lark(grammar,
                  start="file",
                  parser=args.parser,
                  lexer=args.lexer,
                  postlex=post_lex.Post_Lex_Processor_and_Filter(
                      filter=filter_post_lex),
                  #ambiguity="explicit",
                  debug=args.debug_parser,
                  propagate_positions=True,
                  )
    return parser

def main():
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    multi_line_grammar = open(grammar_file).read()
    grammar = multi_line_grammar.replace("\\\n", "")
    
    parser = create_lark_parser(grammar, args)
    unfiltered_post_lex_parser = create_lark_parser(
        grammar, args, filter_post_lex=False)

    for file_name in args.filenames:
        parse_file_or_dir(file_name, args, parser, unfiltered_post_lex_parser)
        
def parse_file_or_dir(file_name, args, parser, unfiltered_post_lex_parser):
    file_path = Path(file_name)
    if file_path.is_dir():
        subdirs = []
        subpaths = file_path.iterdir()
        for subpath in sorted(subpaths):
            if subpath.is_dir():
                subdirs.append(subpath)
            else:
                parse_file(subpath, args, parser, unfiltered_post_lex_parser)
        for subdir in subdirs:
            parse_file_or_dir(
                subdir, args, parser, unfiltered_post_lex_parser)
    else:
        parse_file(file_name, args, parser, unfiltered_post_lex_parser)
        
def parse_file(file_name, args, parser, unfiltered_post_lex_parser):
    text = open(file_name).read()
    if args.list_files:
        print(f'--- Processing "{file_name}"')
    if args.lex:
        generator = parser._build_lexer().lex(text)
        print(f'--- Lexer Output for "{file_name}"')
        post_lex.print_lex(generator)
        print()
    if args.unfiltered_post_lex:
        generator = unfiltered_post_lex_parser.lex(text)
        print(f'--- Unfiltered Post-Lexer Output for "{file_name}"')
        post_lex.print_lex(generator)
        print()
    if args.post_lex:
        generator = parser.lex(text)
        print(f'--- Post-Lexer Output for "{file_name}"')
        post_lex.print_lex(generator)
        print()
    if args.parse or args.ast:
        tree = parser.parse(text)
    if args.parse:
        print(f'--- Parse Tree for "{file_name}"')
        print(tree.pretty(),end="")
        print()
    if args.ast:
        print(f'--- Abstract Syntax Tree for "{file_name}"')
        a_tree = ast.build_ast(tree, file_name=file_name)
        print(a_tree.get_ast_str(),end="")
        print()
            
if __name__ == "__main__":
    main()
