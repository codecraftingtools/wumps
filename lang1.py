#!/usr/bin/env python3

from parglare_mod import Parser, Grammar
import re
from parglare.parser import default_shift_action

grammar = r"""
file: statements EOF;
statements: statement | statements statement;
//statement: words endl align |
//           words ellipsis continuation_li
statement: words statement_end;
words: word | words word;
word: /[a-zA-Z0-9_]+/;
statement_end: endl endl;
endl:; // custom recognizer function

LAYOUT: discardables;
discardables: discardable | discardables discardable;
discardable: insignificant_spaces | blank_line | EMPTY;
insignificant_spaces:; // custom recognizer function
//ws: / +/;
blank_line: /\n *(?=\n)/;
"""

INDENTING = 1
INSIGNIFICANT = 2
#ws_mode = INDENTING
ws_mode = INSIGNIFICANT
indent_stack = [0]
insignificant_spaces_re = re.compile(" +")
def insignificant_spaces_recognizer(input, pos):
    if ws_mode == INSIGNIFICANT:
        m = insignificant_spaces_re.match(input, pos)
        if m:
            return input[pos:m.end()]

endl_re = re.compile("\n")
endl_count = 0
def endl_recognizer(input, pos):
    if input[pos] == "\n":
        if endl_count == 0:
            return ""
        else:
            return "\n"
    #m = insignificant_spaces_re.match(input, pos)
    #if m:
    #    return input[pos:m.end()]
def endl_action(context, node):
    global endl_count
    if endl_count == 0:
        endl_count = 1
    else:
        endl_count = 0
    #endl_count += 1
    return default_shift_action(context, node)

recognizers = {
    'insignificant_spaces': insignificant_spaces_recognizer,
    'endl': endl_recognizer,
}

actions = {
    'endl': endl_action,
}

g = Grammar.from_string(grammar, recognizers=recognizers)
parser = Parser(g, actions=actions)
result = parser.parse(
"""1 a b c
2 d e
3 f
""")
print(result.tree_str())
