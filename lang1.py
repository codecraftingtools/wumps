#!/usr/bin/env python3

from parglare_mod import Parser, Grammar
import re
from parglare_mod import default_shift_action, default_reduce_action

input_string = r"""
f b \
  a d
  b c
L1 a b c
  # comment 1
   L2 d e f # comment 2
       L3 g h i
     m # not a block
L4 j k l
L5 m n o
"""

grammar = r"""
file:
    statements EOF
  | statement_separator statements EOF;
statements:
    statement
  | statements statement_separator statement;
statement:
    call_statement;
statement_separators:
    statement_separator
  | statement_separators statement_separator;
statement_separator:
    align
  | ";";
call_statement:
    callable
  | callable arguments;
callable:
    identifier;
arguments:
    positional_arguments;
positional_arguments:
    positional_argument
  | positional_arguments positional_argument;
positional_argument:
    identifier
  | block;
block:
    block_start statements block_end;
block_start:
    block_indent;
block_end:
    block_dedent;
identifier: /[a-zA-Z_]+[a-zA-Z0-9_]*/;
align:; // custom recognizer function
block_indent:; // custom recognizer function
block_dedent:; // custom recognizer function

LAYOUT:
    discardables;
discardables:
    discardable
  | discardables discardable;
discardable:
    insignificant_spaces
  | escaped_newline
  | line_continuation
  | hash_comment
  | hash_comment_line
  | blank_line
  | EMPTY;
line_continuation: ellipsis "\n";
insignificant_spaces: / */;
escaped_newline: /\\ *\n/;
ellipsis: "...";
hash_comment: / *#.*(?=\n)/;
hash_comment_line: /\n *#.*(?=\n)/;
blank_line:; // custom recognizer function
"""

class State:
    def __init__(self):
        self.indent_stack = [""]
state = State()

new_line_re = re.compile("\n *")
def align_recognizer(input, pos):
    m = new_line_re.match(input, pos)
    if m:
        new_indent = input[pos+1:m.end()]
        if len(new_indent) == len(state.indent_stack[-1]):
            return input[pos:m.end()]

def block_indent_recognizer(input, pos):
   m = new_line_re.match(input, pos)
   if m:
       new_indent = input[pos+1:m.end()]
       if len(new_indent) > len(state.indent_stack[-1]):
           return input[pos:m.end()]

def block_indent_action(context, node):
    state.indent_stack.append(node[1:])
    return default_shift_action(context, node)

def block_dedent_recognizer(input, pos):
    m = new_line_re.match(input, pos)
    if m:
        new_indent = input[pos+1:m.end()]
        if len(new_indent) < len(state.indent_stack[-1]):
            return ""
            if len(new_indent) == len(state.indent_stack[-2]):
                return input[pos:m.end()]
            else:
                return ""

def block_dedent_action(context, node):
    state.indent_stack.pop()
    return default_shift_action(context, node)

blank_line_re = re.compile("\n *(?=\n)")
def blank_line_recognizer(input, pos):
    m = blank_line_re.match(input, pos)
    if m:
        return input[pos:m.end()]
    m = new_line_re.match(input, pos)
    if m:
        if m.end() == len(input):
            return input[pos:m.end()]

recognizers = {
    'align': align_recognizer,
    'block_indent': block_indent_recognizer,
    'block_dedent': block_dedent_recognizer,
    'blank_line': blank_line_recognizer,
}

actions = {
    'block_indent': block_indent_action,
    'block_dedent': block_dedent_action,
}

g = Grammar.from_string(grammar, recognizers=recognizers)
parser = Parser(g, actions=actions)
result = parser.parse(input_string)
print(result.tree_str())
