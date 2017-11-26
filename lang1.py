#!/usr/bin/env python3

from parglare_mod import Parser, Grammar
import re

input_string = r"""
f b \
  a d
  b c ... # comment
    d e
  a
    b
  a
    f g
      h i
    j k;
L1 a b c
  # comment 1
   L2 d e f # comment 2
       L3 g h i;
       J;
     m # not a block
L4 j k l;
L5 m n o;
"""

grammar = r"""
file:
    statements EOF;
statements:
    statement_separators? statement+[statement_separators]
    statement_separators?;
statement_separators:
    statement_separator+;
statement_separator:
    align
  | ";";
statement:
    call;
call:
    command positional_argument*;
command:
    identifier;
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
    discardable+;
discardable:
    insignificant_spaces
  | escaped_newline
  | hash_comment
  | hash_comment_line
  | continuation_line_marker
  | continuation_line_indent
  | continuation_line_align
  | blank_line
  | EMPTY;
insignificant_spaces: / */;
escaped_newline: /\\ *\n/;
hash_comment: / *#.*(?=\n)/;
hash_comment_line: /\n *#.*(?=\n)/;
continuation_line_marker:; // custom recognizer function
continuation_line_indent:; // custom recognizer function
continuation_line_align:; // custom recognizer function
blank_line:; // custom recognizer function
"""

class State:
    def __init__(self):
        self.indent_stack = [""]
        self.starting_continuation = False
        self.in_continuation = False
state = State()

new_line_re = re.compile(r"\n *")
def align_recognizer(input, pos):
    if state.starting_continuation or state.in_continuation:
        return None
    m = new_line_re.match(input, pos)
    if m:
        new_indent = input[pos+1:m.end()]
        if len(new_indent) == len(state.indent_stack[-1]):
            return input[pos:m.end()]

def block_indent_recognizer(input, pos):
    if state.starting_continuation:
        return None
    m = new_line_re.match(input, pos)
    if m:
        new_indent = input[pos+1:m.end()]
        if len(new_indent) > len(state.indent_stack[-1]):
            return input[pos:m.end()]

def block_dedent_recognizer(input, pos):
    if state.starting_continuation:
        return None
    m = new_line_re.match(input, pos)
    if m:
        new_indent = input[pos+1:m.end()]
        if len(new_indent) < len(state.indent_stack[-1]):
            return ""
            if len(new_indent) == len(state.indent_stack[-2]):
                return input[pos:m.end()]
            else:
                return ""

continuation_line_marker_re = re.compile(r"\.\.\. *(#.*)?(?=\n)")
def continuation_line_marker_recognizer(input, pos):
    m = continuation_line_marker_re.match(input, pos)
    if m:
        return input[pos:m.end()]

def continuation_line_indent_recognizer(input, pos):
    if not state.starting_continuation:
        return None
    m = new_line_re.match(input, pos)
    if m:
        new_indent = input[pos+1:m.end()]
        if len(new_indent) > len(state.indent_stack[-1]):
            return input[pos:m.end()]

def continuation_line_align_recognizer(input, pos):
    if not state.in_continuation:
        return None
    m = new_line_re.match(input, pos)
    if m:
        new_indent = input[pos+1:m.end()]
        if len(new_indent) == len(state.indent_stack[-1]):
            return input[pos:m.end()]

blank_line_re = re.compile(r"\n *(?=\n)")
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
    'continuation_line_marker': continuation_line_marker_recognizer,
    'continuation_line_indent': continuation_line_indent_recognizer,
    'continuation_line_align': continuation_line_align_recognizer,
}

class File(list):
    pass

class Call:
    def __init__(self, command, arguments):
        self.command = command
        self.arguments = arguments

class Block(list):
    pass

def block_indent_action(context, node):
    state.indent_stack.append(node[1:])
    if state.in_continuation:
        state.indent_stack.pop()
    state.in_continuation = False
    return node

def block_dedent_action(context, node):
    if state.in_continuation:
        state.indent_stack.pop()
        state.in_continuation = False
    state.indent_stack.pop()
    return node

def continuation_line_marker_action(context, node):
    state.starting_continuation = True
    return node

def continuation_line_indent_action(context, node):
    state.starting_continuation = False
    state.in_continuation = True
    state.indent_stack.append(node[1:])
    return node

actions = {
    'file': lambda _, nodes: File(nodes[0]),
    'statements': lambda _, nodes: nodes[1],
    'call': lambda _, nodes: Call(nodes[0], nodes[1]),
    'block': lambda _, nodes: Block(nodes[1]),
    'block_indent': block_indent_action,
    'block_dedent': block_dedent_action,
    'continuation_line_marker': continuation_line_marker_action,
    'continuation_line_indent': continuation_line_indent_action,
}

indent_str = "  "
def print_item(item, indent=0, first_indent=None):
    if first_indent is None:
        first_indent = indent
    if isinstance(item, File):
        for statement in item:
            print_item(statement, indent)
    elif isinstance(item, Block):
        print()
        for i, statement in enumerate(item):
            print_item(statement, indent)
    elif isinstance(item, Call):
        print("{}call {}".format(indent_str*first_indent, item.command))
        for i, arg in enumerate(item.arguments):
            print("{}{}: ".format(indent_str*(indent+1), i), end="")
            print_item(arg, indent+2, 0)
    else:
        print("{}{}".format(indent_str*first_indent, str(item)))

g = Grammar.from_string(grammar, recognizers=recognizers)
parser = Parser(g, actions=actions)
file = parser.parse(input_string)
print_item(file)
