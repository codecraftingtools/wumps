# Copyright (C) 2019, 2020, 2021 Jeffrey A. Webb
# Copyright (C) 2021 NTA, Inc.

"""
Command-line interface for Wumps processor.
"""

import argparse
import wumps

def create_arg_parser(description="Process wumps input files.", **kw):
    arg_parser = argparse.ArgumentParser(description=description, **kw)
    arg_parser.add_argument(
        "names_of_dirs_and_files",
        nargs = "+",
        metavar = "DIR_OR_FILE",
        help = "names of root directories and files to process")
    return arg_parser

def add_general_options(arg_parser):
    arg_parser.add_argument(
        "--dsl",
        default = None,
        help = "specify a custom domain-specific language (DSL) processing "
        "module (default: %(default)s)")

def add_phase_options(arg_parser):
    arg_parser.add_argument(
        "--partial-parse",
        action = "store_const",
        dest = "stop_after_phase",
        const = wumps.Phase.PARTIAL_PARSE,
        default = wumps.Phase.ALL,
        help = "Exit after executing any requested partial-parsing steps, "
        "but before executing the final step in the parsing phase")
    arg_parser.add_argument(
        "--parse",
        action = "store_const",
        dest = "stop_after_phase",
        const = wumps.Phase.PARSE,
        help = "Exit after parsing the specified input files")
    arg_parser.add_argument(
        "--build",
        action = "store_const",
        dest = "stop_after_phase",
        const = wumps.Phase.BUILD,
        help = "Exit after building the abstract syntax tree (AST)")

def add_output_options(arg_parser):
    arg_parser.add_argument(
        "--show-src-info",
        action = "store_true",
        help = "show source information when printing AST nodes")
    arg_parser.add_argument(
        "--print-file-name",
        action = "store_true",
        help = "print the name of each file as it is processed")
    arg_parser.add_argument(
        "--print-ast",
        action = "store_true",
        help = "print the abstract syntax tree for each file")
    arg_parser.add_argument(
        "--print-path",
        action = "store_true",
        help = "print the path of each collected source file (in order of "
        "processing)")
    arg_parser.add_argument(
        "--print-path-wrt-root",
        action = "store_true",
        help = "print the relative path of each collected source file "
        "with respect to the corresponding source root specified on the "
        "command line (in order of processing)")

def add_options(arg_parser):
    arg_parser._optionals.title = "general options"
    add_general_options(arg_parser)

    arg_parser.phases = arg_parser.add_argument_group('processing phases')
    add_phase_options(arg_parser.phases)

    arg_parser.output = arg_parser.add_argument_group('processing output')
    add_output_options(arg_parser.output)
