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
        "file_and_dir_names",
        nargs = "+",
        help = "names of the input files and directories to process")
    arg_parser.phases = arg_parser.add_argument_group('phases')
    arg_parser.output_control = arg_parser.add_argument_group(
        'output control')
    return arg_parser

def add_general_options(arg_parser):
    arg_parser.add_argument(
        "--dsl",
        default = None,
        help = "specify a custom domain-specific language (DSL) processing "
        "module (default: %(default)s)")

def add_phase_options(arg_parser):
    arg_parser.add_argument(
        "--build",
        action = "store_const",
        dest = "stop_after_phase",
        const = wumps.Phase.BUILD,
        default = wumps.Phase.ALL,
        help = "Exit after building the abstract syntax tree")
    arg_parser.add_argument(
        "--parse",
        action = "store_const",
        dest = "stop_after_phase",
        const = wumps.Phase.PARSE,
        help = "Exit after parsing the specified input files")

def add_output_control_options(arg_parser):
    arg_parser.add_argument(
        "--show-src-info",
        action = "store_true",
        help = "show source information when printing AST nodes")
    arg_parser.add_argument(
        "--print-file-names",
        action = "store_true",
        help = "print the name of each file as it is processed")
    arg_parser.add_argument(
        "--print-ast",
        action = "store_true",
        help = "print the abstract syntax tree")

def add_options(arg_parser):
    add_general_options(arg_parser)
    add_phase_options(arg_parser.phases)
    add_output_control_options(arg_parser.output_control)
