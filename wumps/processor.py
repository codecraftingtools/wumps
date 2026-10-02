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

    def process_root_dirs_and_files(self, names_of_dirs_and_files,
                                    filter_extensions=None):
        args = self._args

        asts = self.build_asts_from_root_dirs_and_files(
            names_of_dirs_and_files, filter_extensions)

        if args.stop_after_phase < wumps.Phase.AST:
            return

        if args.print_path:
            print(f'--- Source File Paths')
            for ast in asts:
                print(f'{ast.path}')
            print()
        if args.print_path_wrt_root:
            print(f'--- Source File Paths wrt Root')
            for ast in asts:
                print(f'{ast.path_wrt_root}')
            print()

    def build_asts_from_root_dirs_and_files(self, names_of_dirs_and_files,
                                            filter_extensions=None):
        asts = []
        for name_of_dir_or_file in names_of_dirs_and_files:
            path = Path(name_of_dir_or_file)
            if path.is_dir():
                asts += self.build_asts_from_dir(
                    name_of_dir_or_file, name_of_dir_or_file, filter_extensions)
            else:
                ast = self.build_ast_from_file(
                    name_of_dir_or_file, path.parent, filter_extensions)
                if ast:
                    asts.append(ast)
        return asts

    def build_asts_from_dir(self, dir_name, path_root=None, filter_extensions=None):
        path_root = dir_name if path_root is None else path_root
        dir_path = Path(dir_name)
        asts = []
        subdirs = []
        subpaths = dir_path.iterdir()
        for subpath in sorted(subpaths):
            if subpath.is_dir():
                subdirs.append(subpath)
            else:
                ast = self.build_ast_from_file(subpath, path_root, filter_extensions)
                if ast:
                    asts.append(ast)
        for subdir in subdirs:
            asts += self.build_asts_from_dir(subdir, path_root, filter_extensions)
        return asts

    def build_ast_from_file(self, file_name, path_root=None, filter_extensions=None):
        if filter_extensions:
            file_ext = Path(file_name).suffix
            if not file_ext:
                return None
            if not file_ext[1:] in filter_extensions:
                return None

        path_root = '' if path_root is None else path_root
        file_name_str = f'"{file_name}"'
        args = self._args

        if args.print_file_name:
            print(f'--- Processing {file_name_str}')
            print()

        text = open(file_name).read()
        parse_tree = self.parse(text, file_name)

        if args.stop_after_phase < wumps.Phase.AST:
            return None

        ast = self.build_ast_from_parse_tree(
            parse_tree, text, file_name, path_root)
        if args.print_ast:
            print(f'--- Abstract Syntax Tree for {file_name_str}')
            print(ast.get_ast_str(show_src_info=args.show_src_info), end="")
            print()

        return ast

    def parse(self, text, file_name=None):
        parse_tree = self._parser.parse(text, file_name)
        return parse_tree

    def build_ast_from_parse_tree(self, parse_tree, file_text=None,
                                  file_name=None, path_root=None):
        ast = self._builder.build_ast(
            parse_tree, file_text, file_name, path_root)
        return ast
