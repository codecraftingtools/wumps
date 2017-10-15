#!/usr/bin/env python3

from parglare_mod import Parser, Grammar
import re
from parglare.parser import default_shift_action, default_reduce_action
#from parglare.parser import NodeTerm NodeNonTerm

grammar = r"""
file: statements EOF;
statements: statement | statements new_line statement
                      | statements new_line indent statement
                      | statements new_line dedent statement
                      | statements new_line dedent dedent statement;
statement: call_statement;
call_statement: words;
words: word | words word;
word: /[a-zA-Z0-9_]+/;
new_line:; // custom recognizer function
indent:; // custom recognizer function
partial_dedent:; // custom recognizer function
dedent:; // custom recognizer function

LAYOUT: discardables;
discardables: discardable | discardables discardable;
discardable: insignificant_spaces | blank_line | EMPTY;
blank_line: /\n *(?=\n)/;
insignificant_spaces: / */;
"""

NEW_LINE = 0
INDENT = 1
DEDENT = 2
PARTIAL_DEDENT = 3
new_line_token = NEW_LINE
indent_stack = [""]
new_indent = ""

new_line_re = re.compile("\n *")
def new_line_recognizer(input, pos):
    if new_line_token != NEW_LINE:
        return None
    m = new_line_re.match(input, pos)
    if m:
        global new_indent
        new_indent = input[pos+1:m.end()]
        if len(new_indent) == len(indent_stack[-1]):
            return input[pos:m.end()]
        else:
            return ""

def new_line_action(context, node):
    global new_line_token
    if len(new_indent) == len(indent_stack[-1]):
        new_line_token = NEW_LINE
    elif len(new_indent) > len(indent_stack[-1]):
        new_line_token = INDENT
        indent_stack.append(new_indent)
    elif len(new_indent) > len(indent_stack[-2]):
        new_line_token = PARTIAL_DEDENT
        indent_stack.pop()
        indent_stack.append(new_indent)
    else:
        new_line_token = DEDENT
        indent_stack.pop()
    return default_shift_action(context, node)

def indent_recognizer(input, pos):
    if new_line_token != INDENT:
        return None
    m = new_line_re.match(input, pos)
    if m:
        return input[pos:m.end()]

def indent_action(context, node):
    global new_line_token
    new_line_token = NEW_LINE
    return default_shift_action(context, node)

def partial_dedent_recognizer(input, pos):
    if new_line_token != PARTIAL_DEDENT:
        return None
    m = new_line_re.match(input, pos)
    if m:
        return input[pos:m.end()]

def partial_dedent_action(context, node):
    global new_line_token
    new_line_token = NEW_LINE
    return default_shift_action(context, node)

def dedent_recognizer(input, pos):
    if new_line_token != DEDENT:
        return None
    m = new_line_re.match(input, pos)
    if m:
        if len(new_indent) == len(indent_stack[-1]):
            return input[pos:m.end()]
        else:
            return ""

def dedent_action(context, node):
    global new_line_token
    if len(new_indent) == len(indent_stack[-1]):
        new_line_token = NEW_LINE
    elif len(new_indent) > len(indent_stack[-1]):
        new_line_token = PARTIAL_DEDENT
        indent_stack.pop()
        indent_stack.append(new_indent)
    else:
        new_line_token = DEDENT
        indent_stack.pop()
    return default_shift_action(context, node)

recognizers = {
    'new_line': new_line_recognizer,
    'indent': indent_recognizer,
    'partial_dedent': partial_dedent_recognizer,
    'dedent': dedent_recognizer,
}

actions = {
    'new_line': new_line_action,
    'indent': indent_action,
    'partial_dedent': partial_dedent_action,
    'dedent': dedent_action,
}

g = Grammar.from_string(grammar, recognizers=recognizers)
parser = Parser(g, actions=actions)
result = parser.parse(
"""1 a b c
     2 d e f
       3 g h i
4 j k l
5 m n o""")
print(result.tree_str())
