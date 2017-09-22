#!/usr/bin/env python3

from parglare import Parser, Grammar
from parglare.parser import default_shift_action

#E: E '+' E  {left, 1}
# | E '-' E  {left, 1}
# | E '*' E  {left, 2}
# | E '/' E  {left, 2}
# | E '^' E  {right, 3}
# | '(' E ')'
# | number;
#number: /\d+(\.\d+)?/;

grammar = r"""
file: block EOF;
block: stmts;
stmts: stmts stmt | stmt;
stmt: number | cr_aligned | cr_indent | cr_unindent | cr_partial_unindent;
number: /\d+/;
cr_aligned:;
cr_indent:;
cr_unindent:;
cr_partial_unindent:;

LAYOUT: LayoutItem | LAYOUT LayoutItem;
LayoutItem: WS | EMPTY;
WS: / +/;
"""

grammar = r"""
//file: file_start stmt_list EOF | file_start stmt_list cr_aligned EOF;
file: file_start stmt_list file_end EOF;
file_start: cr_aligned | EMPTY;
file_end: cr_aligned | cr_indent | cr_unindent | EMPTY;
//file_end: end_of_file | EOF;
//end_of_file:;
stmt_list: stmt_list cr_aligned stmt |
           stmt;
stmt: stmt item | item; // | stmt cr_indent stmt
item: number;
sep: cr_aligned | cr_indent | cr_unindent | cr_partial_unindent;
number: /\d+/;
cr_aligned:;
cr_indent:;
cr_unindent:;
cr_partial_unindent:;

LAYOUT: LayoutItem | LAYOUT LayoutItem;
LayoutItem: WS | EMPTY| empty_line;
empty_line:;
WS: / +/;
"""

import re
cr_space_re = re.compile("\n *")
indent_stack = [0]
def cr_recognizer(input, pos):
    m  = cr_space_re.match(input, pos)
    if m:
        #print(m.end() - m.start() - 1)
        return m.end() - m.start() - 1
def cr_aligned(input, pos):
    indent = cr_recognizer(input, pos)
    if indent == indent_stack[-1]:
        #if pos < len(input) - 1: # distinguish from end_of_file
        return input[pos:pos+indent+1]
def cr_indent(input, pos):
    indent = cr_recognizer(input, pos)
    if indent is not None and indent > indent_stack[-1]:
        return input[pos:pos+indent+1]
def cr_unindent(input, pos):
    indent = cr_recognizer(input, pos)
    if (indent is not None and
        len(indent_stack) > 1 and 
        indent == indent_stack[-2]):
        return input[pos:pos+indent+1]
def cr_partial_unindent(input, pos):
    indent = cr_recognizer(input, pos)
    if (indent is not None and
        indent < indent_stack[-1] and
        len(indent_stack) > 1 and 
        indent > indent_stack[-2]):
        return input[pos:pos+indent+1]
def end_of_file(input, pos):
    if input[pos] == "\n" and pos == len(input)-1:
        return "\n"

empty_line_re = re.compile("\n *\n")
def empty_line(input, pos):
    m = empty_line_re.match(input, pos)
    if m:
        return input[m.start():m.end()-1]

recognizers = {
    'cr_aligned': cr_aligned,
    'cr_indent': cr_indent,
    'cr_unindent': cr_unindent,
    'cr_partial_unindent': cr_partial_unindent,
    'empty_line': empty_line,
#    'end_of_file': end_of_file,
}

def cr_indent_action(context, node):
    indent_stack.append(len(node)-1)
    #print("cr_indent: <{}>".format(node),type(node),indent_stack)
    return default_shift_action(context, node)

def cr_unindent_action(context, node):
    indent_stack.pop()
    return default_shift_action(context, node)

def cr_partial_unindent_action(context, node):
    indent_stack.pop()
    indent_stack.append(len(node)-1)
    return default_shift_action(context, node)

actions = {
    'cr_indent': cr_indent_action,
    'cr_unindent': cr_unindent_action,
    'cr_partial_unindent': cr_partial_unindent_action,
}

# recognizers for incr_indent, dedent, partial_dedent, newline
# cr_aligned cr_indent cr_unindent cr_partial_unindent

g = Grammar.from_string(grammar, recognizers=recognizers)
#parser = Parser(g, debug=True)
parser = Parser(g, actions=actions)

result = parser.parse("""
5
6
7
""")

#result = parser.parse("""5
#1113 456
#  22
# 3333
# 7
#2
#""")

print(result.tree_str())
