#!/usr/bin/env python3

from parglare_mod import Parser, GLRParser, Grammar
import re

indent_token = "  "

class Identifier:
    def __init__(self, id_string, context=None):
        self._context = context
        if id_string.endswith(':'):
            id_string = id_string[:-1].rstrip()
        self._string = id_string

    @classmethod
    def parse_action(cls, context, node):
        return cls(node, context=context)

    def print(self, indent=0, first_indent=None):
        first_indent = indent if first_indent is None else first_indent
        print("{}{}".format(indent_token*first_indent, self._string))

class Named_Expression:
    def __init__(self, name, expression, context=None):
        self._context = context
        self._name = name
        self._expression = expression

    @classmethod
    def parse_action(cls, context, nodes):
        return cls(nodes[0], nodes[1], context=context)

    def print(self, indent=0, first_indent=None):
        first_indent = indent if first_indent is None else first_indent
        print("{}Named_Expression".format(indent_token*first_indent))
        print("{}name: ".format(indent_token*(indent+1)), end="")
        self._name.print(first_indent=0)
        print("{}expression: ".format(indent_token*(indent+1)), end="")
        self._expression.print(indent+1, first_indent=0)

class Call:
    def __init__(self, callee, arguments, context=None):
        self._context = context
        self._callee = callee
        self._arguments = arguments

    @classmethod
    def parse_action(cls, context, nodes):
        callee = nodes[0]
        arguments = []
        if len(nodes) > 1:
            if isinstance(nodes[1], list):                
                arguments.extend(nodes[1])
            else:
                arguments.append(nodes[1])
        if len(nodes) > 2:
            arguments.extend(nodes[2])
        return cls(callee, arguments, context=context)

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

class Expressions:
    def __init__(self, expressions, context=None):
        self._context = context
        self._expressions = tuple(expressions)

    @classmethod
    def parse_action(cls, context, nodes):
        expressions = []
        if len(nodes) > 1:
            expressions.extend(nodes[1])
        return cls(expressions, context=context)

    def _print_attributes(self, indent):
        pass

    def print(self, indent=0, first_indent=None):
        first_indent = indent if first_indent is None else first_indent
        print("{}{}".format(indent_token*first_indent,
                            self.__class__.__name__))
        self._print_attributes(indent)
        print("{}expressions:".format(
            indent_token*(indent+1)))
        for a in self._expressions:
            try:
                a.print(indent=indent+2)
            except:
                print(a)

class File(Expressions):
    def __init__(self, expressions, context=None):
        super().__init__(expressions, context=context)
        if context and hasattr(context, "file_name"):
            self._path = context.file_name
        else:
            self._path = "<None>"

    @classmethod
    def parse_action(cls, context, nodes):
        return cls(nodes[0]._expressions, context=context)

    def _print_attributes(self, indent):
        print("{}path: {}".format(indent_token*(indent+1), self._path))

class Comma_Separated_Expressions(Expressions):
    @classmethod
    def parse_action(cls, context, nodes):
        expressions = [nodes[0]]
        if isinstance(nodes[2], Comma_Separated_Expressions):                
            expressions.extend(nodes[2]._expressions)
        else:
            expressions.append(nodes[2])
        return cls(expressions, context=context)

input_string = r"""
a
a, b, f a : c d e b: d e
"""
#f2 (b k1: a k2: b c)

grammar = r"""
file:
    expressions
    EOF;
expressions:
    expression_separators?
    expression+[expression_separators]
    expression_separators? |
    expression_separators?;
expression_separators:
    expression_separator+;
expression_separator:
    indent | ";";
indent: "\n";
expression:
    non_sequence_expression |
    named_expression |
    comma_separated_expressions;
non_sequence_expression:
    identifier |
    call |
    parenthesized_expression;
identifier: /[a-zA-Z_]+[a-zA-Z0-9_]*/;
call:
    identifier named_expression+ |
    identifier inner_expression named_expression*;
named_expression:
    key inner_expression;
key: /[a-zA-Z_]+[a-zA-Z0-9_]* *:/;
inner_expression:
    identifier |
    inner_call |
    parenthesized_expression;
inner_call:
    identifier inner_expression;
parenthesized_expression:
    "(" expression ")";
comma_separated_expressions:
    non_sequence_expression comma comma_separated_expressions |
    non_sequence_expression comma non_sequence_expression;
comma: ",";

LAYOUT:
    discardable+ | EMPTY;
discardable:
    spaces;
spaces: / +/;
"""

actions = {
    'file': File.parse_action,
    'expressions': Expressions.parse_action,
    'identifier': Identifier.parse_action,
    'call': Call.parse_action,
    'named_expression': Named_Expression.parse_action,
    'key': Identifier.parse_action,
    'inner_call': Call.parse_action,
    'parenthesized_expression': lambda context, nodes: nodes[1],
    'comma_separated_expressions': Comma_Separated_Expressions.parse_action,
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
