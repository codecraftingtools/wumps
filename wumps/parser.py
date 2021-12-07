# Copyright (C) 2019, 2020, 2021 Jeffrey A. Webb
# Copyright (C) 2021 NTA, Inc.

"""
Wumps parsing front-end.
"""

from pathlib import Path
from lark import Lark
from wumps.lark import post_lex, ast
import wumps

class Parser:
    def __init__(self, args):
        wumps_package_root = Path(wumps.__file__).parent
        grammar_file = str(wumps_package_root / "lark" / "grammar.lark")
        multi_line_grammar = open(grammar_file).read()
        grammar = multi_line_grammar.replace("\\\n", "")
        self._args = args
        self._parser = self._create_lark_parser(
            grammar, filter_post_lex=True)
        self._unfiltered_post_lex_parser = self._create_lark_parser(
            grammar, filter_post_lex=False)

    def _create_lark_parser(self, grammar, filter_post_lex):
        parser = Lark(grammar,
                      start="file",
                      parser=self._args.parser,
                      lexer=self._args.lexer,
                      postlex=post_lex.Post_Lex_Processor_and_Filter(
                          filter=filter_post_lex),
                      #ambiguity="explicit",
                      debug=self._args.debug_parser,
                      propagate_positions=True,
                      )
        return parser

    def process_files_and_dirs(self, file_names):    
        for file_name in file_names:
            self.process_file_or_dir(file_name)
            
    def process_file_or_dir(self, file_name):
        file_path = Path(file_name)
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
            self.process_file(file_name)
            
    def process_file(self, file_name):
        text = open(file_name).read()
        if self._args.list_files:
            print(f'--- Processing "{file_name}"')
        if self._args.lex:
            generator = self._parser._build_lexer().lex(text)
            print(f'--- Lexer Output for "{file_name}"')
            post_lex.print_lex(generator)
            print()
        if self._args.unfiltered_post_lex:
            generator = self._unfiltered_post_lex_parser.lex(text)
            print(f'--- Unfiltered Post-Lexer Output for "{file_name}"')
            post_lex.print_lex(generator)
            print()
        if self._args.post_lex:
            generator = self._parser.lex(text)
            print(f'--- Post-Lexer Output for "{file_name}"')
            post_lex.print_lex(generator)
            print()
        if self._args.parse or self._args.ast:
            tree = self._parser.parse(text)
        if self._args.parse:
            print(f'--- Parse Tree for "{file_name}"')
            print(tree.pretty(),end="")
            print()
        if self._args.ast:
            print(f'--- Abstract Syntax Tree for "{file_name}"')
            a_tree = ast.build_ast(tree, file_name=file_name)
            print(a_tree.get_ast_str(),end="")
            print()
