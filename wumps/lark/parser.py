# Copyright (C) 2019, 2020, 2021 Jeffrey A. Webb
# Copyright (C) 2021 NTA, Inc.

"""
Wumps parsing implementation.
"""

from pathlib import Path
from lark import Lark
from wumps.lark import post_lex
import wumps

class Parser:
    def __init__(self, args):
        self._args = args
        wumps_package_root = Path(wumps.__file__).parent
        grammar_file = str(wumps_package_root / "lark" / "grammar.lark")
        multi_line_grammar = open(grammar_file).read()
        grammar = multi_line_grammar.replace("\\\n", "")
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

    def parse(self, text, file_name=None):
        if file_name is None:
            file_name_str = "input text"
        else:
            file_name_str = f'"{file_name}"'
        args = self._args

        if args.print_lex:
            if args.lexer == "contextual":
                print(f'--- Lexer output not available for contextual lexer')
            else:
                stream = self._parser.parser._make_lexer_thread(text)
                tokens = list(stream.lex(None))
                print(f'--- Lexer Output for {file_name_str}')
                post_lex.print_lex(tokens)
            print()
        if args.print_unfiltered_post_lex:
            generator = self._unfiltered_post_lex_parser.lex(text)
            print(f'--- Unfiltered Post-Lexer Output for {file_name_str}')
            post_lex.print_lex(generator)
            print()
        if args.print_post_lex:
            generator = self._parser.lex(text)
            print(f'--- Post-Lexer Output for {file_name_str}')
            post_lex.print_lex(generator)
            print()

        if args.stop_after_phase < wumps.Phase.PARSE:
            return None

        parse_tree = self._parser.parse(text)
        if args.print_parse_tree:
            print(f'--- Parse Tree for {file_name_str}')
            print(parse_tree.pretty(), end="")
            print()
        return parse_tree
