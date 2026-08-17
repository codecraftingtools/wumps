# Copyright (C) 2019, 2020, 2021 Jeffrey A. Webb
# Copyright (C) 2021 NTA, Inc.

"""
Lark-specific command-line options for Wumps parser.
"""

import argparse
import wumps

def add_phase_options(arg_parser):
    arg_parser.add_argument(
        "--partial-parse",
        action = "store_const",
        dest = "stop_after_phase",
        const = wumps.Phase.PARTIAL_PARSE,
        help = "Exit after any requested partial-parsing steps, but before "
        "the final step in the parsing phase")

def add_output_control_options(arg_parser):
    arg_parser.add_argument(
        "--print-parse-tree",
        action = "store_true",
        help = "print the parse tree")
    arg_parser.add_argument(
        "--print-post-lex",
        action = "store_true",
        help = "print the output of the post-lexer before parsing")
    arg_parser.add_argument(
        "--print-unfiltered-post-lex",
        action = "store_true",
        help = "print the output of the post-lexer before filtering and "
        "parsing")
    arg_parser.add_argument(
        "--print-lex",
        action = "store_true",
        help = "print the output of the lexer before post-lexing and parsing")

def add_parsing_options(arg_parser):
    arg_parser.add_argument(
        "--parser",
        default = "lalr",
        choices = ["lalr", "earley"],
        help = "specify the parsing algorithm to use (default: %(default)s)")
    arg_parser.add_argument(
        "--lexer",
        default = "basic",
        choices = ["basic", "contextual"],
        help = "specify the lexer to use (default: %(default)s)")
    arg_parser.add_argument(
        "--debug-parser",
        action = "store_true",
        help = "debug the parsing implementation")

def add_options(arg_parser):
    add_phase_options(arg_parser.phases)
    add_output_control_options(arg_parser.output_control)
    arg_parser.parsing = arg_parser.add_argument_group('parsing options')
    add_parsing_options(arg_parser.parsing)
