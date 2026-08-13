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
from wumps.lark.parser import Parser
            
def main():
    arg_parser = wumps.cli.create_arg_parser()
    args = arg_parser.parse_args()

    parser = Parser(args)
    parser.process_files_and_dirs(args.filenames)

if __name__ == "__main__":
    main()
