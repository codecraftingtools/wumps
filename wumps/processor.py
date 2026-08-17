# Copyright (C) 2019, 2020, 2021 Jeffrey A. Webb
# Copyright (C) 2021 NTA, Inc.

"""
Wumps processing interface.
"""

from pathlib import Path
import wumps

class Processor:
    def __init__(self, parser, builder, args):
        self._parser = parser
        self._builder = builder
        self._args = args

    def process_files_and_dirs(self, file_and_dir_names):
        for file_or_dir_name in file_and_dir_names:
            self.process_file_or_dir(file_or_dir_name)

    def process_file_or_dir(self, file_or_dir_name):
        file_path = Path(file_or_dir_name)
        if file_path.is_dir():
            subdirs = []
            subpaths = file_path.iterdir()
            for subpath in sorted(subpaths):
                if subpath.is_dir():
                    subdirs.append(subpath)
                else:
                    self.process_file(subpath)
            for subdir in subdirs:
                self.process_file_or_dir(subdir)
        else:
            self.process_file(file_or_dir_name)

    def process_file(self, file_name):
        file_name_str = f'"{file_name}"'
        args = self._args

        if args.print_file_names:
            print(f'--- Processing {file_name_str}')
            print()

        text = open(file_name).read()

        parse_tree = self.parse(text, file_name)
        if args.stop_after_phase <= wumps.Phase.PARSE:
            return

        ast = self.build_ast(parse_tree, text, file_name)
        if args.print_ast:
            print(f'--- Abstract Syntax Tree for {file_name_str}')
            print(ast.get_ast_str(show_src_info=args.show_src_info), end="")
            print()
        if args.stop_after_phase <= wumps.Phase.BUILD:
            return

    def parse(self, text, file_name=None):
        parse_tree = self._parser.parse(text, file_name)
        return parse_tree

    def build_ast(self, parse_tree, file_text=None, file_name=None):
        ast = self._builder.build_ast(parse_tree, file_text, file_name)
        return ast
