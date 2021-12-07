#!/usr/bin/env python3

# Copyright (C) 2019, 2020, 2021 Jeffrey A. Webb
# Copyright (C) 2021 NTA, Inc.

import sys
from pathlib import Path

# Add the wumps package root directory to sys.path, if running as a script
if __name__ == "__main__":
    wumps_package_root = Path(sys.path[0]).parent
    sys.path.insert(1, str(wumps_package_root.parent))

import argparse
from wumps.parser import Parser

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

            
def main():
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    parser = Parser(args)
    parser.process_files_and_dirs(args.filenames)

if __name__ == "__main__":
    main()
