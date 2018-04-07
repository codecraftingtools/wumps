#!/usr/bin/env python3

from parglare_mod import Parser, GLRParser, Grammar
import re

indent_token = "  "

class File:
    def __init__(self, context, nodes):
        self._context = context
        self._statements = nodes[1]
        if hasattr(context, "file_name"):
            self._path = context.file_name
        else:
            self._path = "<None>"

    def print(self, indent=0, first_indent=None):
        first_indent = indent if first_indent is None else first_indent
        print("{}File".format(indent_token*first_indent))
        print("{}path: {}".format(indent_token*(indent+1), self._path))
        print("{}statements:".format(indent_token*(indent+1)))
        for s in self._statements:
            s.print(indent=indent+2)

class Named_Expression:
    def __init__(self, context, nodes):
        self._context = context
        self._name = nodes[0]
        self._expression = nodes[1]
        #self._expression = nodes[2]

    def print(self, indent=0, first_indent=None):
        first_indent = indent if first_indent is None else first_indent
        print("{}Named_Expression".format(indent_token*first_indent))
        print("{}name: ".format(indent_token*(indent+1)), end="")
        self._name.print(first_indent=0)
        print("{}expression: ".format(indent_token*(indent+1)), end="")
        self._expression.print(indent+1, first_indent=0)

class Call:
    def __init__(self, context, nodes):
        self._context = context
        self._callee = nodes[0]
        self._arguments = []
        if len(nodes) > 1:
            if isinstance(nodes[1], list):                
                self._arguments.extend(nodes[1])
            else:
                self._arguments.append(nodes[1])
        if len(nodes) > 2:
            self._arguments.extend(nodes[2])

    def print(self, indent=0, first_indent=None):
        first_indent = indent if first_indent is None else first_indent
        print("{}Call".format(indent_token*first_indent))
        print("{}callee: ".format(
            indent_token*(indent+1)), end="")
        self._callee.print(indent=indent+1, first_indent=0)
        print("{}arguments:".format(
            indent_token*(indent+1)))
        for a in self._arguments:
            try:
                a.print(indent=indent+2)
            except:
                print(a)

class Identifier:
    def __init__(self, context, node):
        self._context = context
        if node.endswith(':'):
            node = node[:-1].rstrip()
        self._string = node

    def print(self, indent=0, first_indent=None):
        first_indent = indent if first_indent is None else first_indent
        print("{}{}".format(indent_token*first_indent, self._string))

input_string = r"""
f a : c d e b: d e
"""

grammar = r"""
file:
    statement_separators?
    statement+[statement_separators]
    statement_separators?
    EOF;
statement_separators:
    statement_separator+;
statement_separator:
    indent | ";";
statement:
    named_expression |
    expression;
expression:
    identifier |
    complex_call;
simple_expression:
    identifier |
    simple_call;
simple_call:
    identifier simple_expression;
complex_call:
    identifier named_expression+ |
    identifier simple_expression named_expression*;
named_expression:
    key simple_expression;
identifier: /[a-zA-Z_]+[a-zA-Z0-9_]*/;
key: /[a-zA-Z_]+[a-zA-Z0-9_]* *:/;
indent: "\n";

LAYOUT:
    discardable+ | EMPTY;
discardable:
    spaces;
spaces: / +/;
"""

actions = {
    'file': File,
    'simple_call': Call,
    'complex_call': Call,
    'named_expression': Named_Expression,
    'identifier': Identifier,
    'key': Identifier,
}

g = Grammar.from_string(grammar)

parser = Parser(g, actions=actions,debug=0)
#parser = GLRParser(g, actions=actions,debug=1)

file = parser.parse(input_string)
if isinstance(file, list):
    for f in file:
        f.print()
else:
    file.print()
