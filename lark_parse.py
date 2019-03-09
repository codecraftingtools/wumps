#!/usr/bin/env python3

from lark import Lark

my_grammar = """
    start: _expressions
    _expressions: _PRIMARY_DELIMITER* expression _PRIMARY_DELIMITER*
               | _expressions _PRIMARY_DELIMITER _expressions
    expression: IDENTIFIER
    _PRIMARY_DELIMITER: ";"
                     | "\\n"
    IDENTIFIER: /[a-zA-Z_]+[a-zA-Z0-9_]*/
    %ignore " "
"""

def main():
    parser = Lark(my_grammar)
    text = """
;; a;; 
b;;
  c;"""
    tree = parser.parse(text)
    print(tree.pretty())

if __name__ == '__main__':
    main()
