#!/usr/bin/env python3

from parglare_mod import Parser, Grammar
import re
from parglare_mod import default_shift_action, default_reduce_action

grammar = r"""
file: statements EOF |
      align statements EOF;
statements: statement | statements align statement;
statement: call_statement;
call_statement: callable | callable arguments;
callable: identifier;
arguments: argument | arguments argument;
argument: identifier | block;
block: indent statements dedent;
identifier: /[a-zA-Z_]+[a-zA-Z0-9_]*/;
ellipsis: "...";
align:; // custom recognizer function
indent:; // custom recognizer function
dedent:; // custom recognizer function

LAYOUT: discardables;
discardables: discardable | discardables discardable;
discardable: insignificant_spaces | blank_line | hash_comment |
             hash_comment_line | EMPTY;
blank_line:; // custom recognizer function
hash_comment: / *#.*(?=\n)/;
hash_comment_line: /\n *#.*(?=\n)/;
insignificant_spaces: / */;
"""

indent_stack = [""]

new_line_re = re.compile("\n *")
def align_recognizer(input, pos):
    m = new_line_re.match(input, pos)
    if m:
        new_indent = input[pos+1:m.end()]
        if len(new_indent) == len(indent_stack[-1]):
            return input[pos:m.end()]

def indent_recognizer(input, pos):
   m = new_line_re.match(input, pos)
   if m:
       new_indent = input[pos+1:m.end()]
       if len(new_indent) > len(indent_stack[-1]):
           return input[pos:m.end()]

def indent_action(context, node):
    indent_stack.append(node[1:])
    return default_shift_action(context, node)

def dedent_recognizer(input, pos):
    m = new_line_re.match(input, pos)
    if m:
        new_indent = input[pos+1:m.end()]
        if len(new_indent) < len(indent_stack[-1]):
            return ""
            if len(new_indent) == len(indent_stack[-2]):
                return input[pos:m.end()]
            else:
                return ""

def dedent_action(context, node):
    indent_stack.pop()
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
    'indent': indent_recognizer,
    'dedent': dedent_recognizer,
    'blank_line': blank_line_recognizer,
}

actions = {
    'indent': indent_action,
    'dedent': dedent_action,
}

g = Grammar.from_string(grammar, recognizers=recognizers)
parser = Parser(g, actions=actions)
result = parser.parse(
"""

L1 a b c
  # comment 1
   L2 d e f # comment 2
       L3 g h i
     m
L4 j k l
L5 m n o


""")
print(result.tree_str())
