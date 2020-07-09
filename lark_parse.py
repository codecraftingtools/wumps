#!/usr/bin/env python3

# Add the project root directory to sys.path
import sys
from pathlib import Path
wumps_root = Path(sys.path[0])
sys.path.insert(1, str(wumps_root))

from lark import Lark
from wumps.lark import post_lex

grammar_file = str(wumps_root / "wumps" / "lark" / "grammar.lark")

def main():
    #parser_type = "earley"
    parser_type = "lalr"
    grammar = open(grammar_file).read()
    grammar = grammar.replace("\\\n", "")
    parser = Lark(grammar, start="file", parser=parser_type,
                  lexer="standard",
                  #lexer="contextual",
                  postlex=post_lex.Post_Lex_Processor(),
                  #ambiguity="explicit",
                  #debug=True,
                  )
    text = open(sys.argv[1]).read()
    #post_lex.print_lex(parser, text)
    #return
    try:
        tree = parser.parse(text)
        for item in tree.children:
            print(type(item))
            #print(dir(item))
            #print()
        print(tree.pretty(),end="")
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    main()
