#!/usr/bin/env python3

# Copyright (C) 2019, 2020, 2021 Jeffrey A. Webb
# Copyright (C) 2021 NTA, Inc.

import sys
from pathlib import Path

# Add the wumps package root directory to sys.path, if running as a script
if __name__ == "__main__":
    wumps_package_root = Path(sys.path[0]).parent
    sys.path.insert(1, str(wumps_package_root.parent))

import wumps.cli
import wumps.lark.cli
from wumps.processor import Processor
from wumps.lark.parser import Parser
from wumps.lark.builder import Builder

def main():
    arg_parser = wumps.cli.create_arg_parser()
    wumps.cli.add_options(arg_parser)
    wumps.lark.cli.add_options(arg_parser)

    args = arg_parser.parse_args()

    processor = Processor(Parser(args), Builder(args), args)
    processor.process_root_dirs_and_files(args.names_of_dirs_and_files)

if __name__ == "__main__":
    main()
