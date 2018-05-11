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
    def parser_action(cls, context, node):
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
    def parser_action(cls, context, nodes):
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
    def parser_action(cls, context, nodes):
        callee = nodes[0]
        arguments = []
        if len(nodes) > 1:
            if isinstance(nodes[1], Expressions):                
                arguments.extend(nodes[1]._expressions)
            elif isinstance(nodes[1], list):                
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
    def __init__(self, expressions=[], context=None):
        self._context = context
        self._expressions = tuple(expressions)

    @classmethod
    def parser_action(cls, context, nodes):
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
    def parser_action(cls, context, nodes):
        return cls(nodes[0]._expressions, context=context)

    def _print_attributes(self, indent):
        print("{}path: {}".format(indent_token*(indent+1), self._path))

class Sequence(Expressions):
    @classmethod
    def comma_parser_action(cls, context, nodes):
        expressions = [nodes[0]]
        if len(nodes) > 2:
            if isinstance(nodes[2], Sequence):                
                expressions.extend(nodes[2]._expressions)
            else:
                expressions.append(nodes[2])
        return cls(expressions, context=context)

    @classmethod
    def block_parser_action(cls, context, nodes):
        return cls(nodes[1]._expressions, context=context)

input_string = r"""
if a ...
  then:
   b (a)
 else:
   c ()
#circle ...
#   a b
#   c d
#     color: black
#     radius: four
#     outline: true
#     width: five
#c
#if a b c then: {
#     a1; a3
#     a2
# } else: (
#      )
#a
#if (a b) then: {b;c} else: {d; e()}
#a, b, f b (aa,) a : c d e b: d {e}
"""
#a d: z1 e: z3
#f2 (b k1: a k2: b c)

grammar_string = r"""
file:
    expressions
    EOF;
expressions:
    primary_delimiters? expression+[primary_delimiters] primary_delimiters? |
    primary_delimiters?;
primary_delimiters:
    primary_delimiter+;
primary_delimiter:
    unbracketed_aligned_indent |
    ";";
unbracketed_aligned_indent:; // custom recognizer
expression:
    comma_delimited_sequence |
    non_sequence;
comma_delimited_sequence:
    non_sequence comma comma_delimited_sequence |
    non_sequence comma non_sequence |
    non_sequence comma;
comma: ",";
non_sequence:
    named_expression |
    anonymous_expression;
named_expression:
    key anonymous_expression;
key: /[a-zA-Z_]+[a-zA-Z0-9_]* *:/;
anonymous_expression:
    term |
    call;
term:
    parenthesized_expression |
    empty_parentheses |
    braced_block |
    unbracketed_indented_block |
    identifier;
parenthesized_expression:
    open_parenthesis expression close_parenthesis;
open_parenthesis: "(";
close_parenthesis: ")";
empty_parentheses:
    open_parenthesis close_parenthesis;
braced_block:
    open_brace expressions close_brace;
open_brace: "{";
close_brace: "}";
unbracketed_indented_block:
    unbracketed_increased_indent
    expressions
    unbracketed_decreased_indent_one_level;
unbracketed_increased_indent:; // custom recognizer
unbracketed_decreased_indent_one_level:; // custom recognizer
identifier: /[a-zA-Z_]+[a-zA-Z0-9_]*/;
call:
    callee named_argument+ |
    callee argument named_argument*;
callee:
    identifier |
    parenthesized_expression;
named_argument:
    key argument;
argument:
    term |
    chained_call;
chained_call:
    callee argument;

LAYOUT:
    discardable+ | EMPTY;
discardable:
    hash_comment |
    hash_comment_line |
    blank_line |
    insignficant_spaces |
    escaped_newline |
    bracketed_new_line |
    unbracketed_continuation_marker |
    unbracketed_increased_indent_after_continuation_marker |
    unbracketed_aligned_indent_in_continuation |
    unbracketed_decreased_indent_one_level_in_continuation;
    // unbracketed_partially_decreased_indent
hash_comment: / *#.*(?=\n)/;
hash_comment_line: /\n *#.*(?=\n)/;
blank_line: /\n *(?=\n)/;
insignficant_spaces: / +/;
escaped_newline: /\\ *\n/;

// custom recognizers for discardable elements
bracketed_new_line:;
unbracketed_continuation_marker:;
unbracketed_increased_indent_after_continuation_marker:;
unbracketed_decreased_indent_one_level_in_continuation:;
unbracketed_aligned_indent_in_continuation:;
"""

class Extra_State:
    def __init__(self):
        self._indent_stack = [["", False, " "*999]]
        self._starting_continuation = False
        self._bracket_depth = 0
    def maximum_continuation_indent(self):
        return len(self._indent_stack[-1][2])
    def set_maximum_continuation_indent(self, max_indent):
        if len(max_indent) < len(self._indent_stack[-1][2]):
            self._indent_stack[-1][2] = max_indent
    def current_indent(self):
        return len(self._indent_stack[-1][0])
    def previous_indent(self):
        if len(self._indent_stack) > 1:
            return len(self._indent_stack[-2][0])
        else:
            return None
    def push_indent(self, indent):
        self._indent_stack.append([indent,self._starting_continuation," "*999])
        self._starting_continuation = False
    def pop_indent(self):
        self._indent_stack.pop()
    def in_continuation(self):
        return self._indent_stack[-1][1]
    def starting_continuation(self):
        return self._starting_continuation
    def start_continuation(self):
        self._starting_continuation = True
    def nest_bracket(self):
        self._bracket_depth += 1
    def unnest_bracket(self):
        if self._bracket_depth > 0:
            self._bracket_depth -= 1
    def is_bracketed(self):
        if self._bracket_depth:
            return True
        else:
            return False

state = Extra_State()

new_line_and_possible_indent_re = re.compile(r"\n *")
def match_new_line_and_possible_indent(input, pos):
    match = new_line_and_possible_indent_re.match(input, pos)
    if match is None:
        return None
    return input[pos:match.end()]

def unbracketed_aligned_indent_recognizer(input, pos):
    if (not state.is_bracketed() and
        not state.starting_continuation() and 
        not state.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) == state.current_indent():
                return new_line_and_possible_indent

def unbracketed_increased_indent_recognizer(input, pos):
    if (not state.is_bracketed() and
        not state.starting_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) > state.current_indent():
                return new_line_and_possible_indent

def unbracketed_decreased_indent_one_level_recognizer(input, pos):
    if (not state.is_bracketed() and
        not state.starting_continuation() and
        not state.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) < state.current_indent():
                return ""

def bracketed_new_line_recognizer(input, pos):
    if state.is_bracketed():
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            return new_line_and_possible_indent

continuation_marker_re = re.compile(r"\.\.\. *(#.*)?(?=\n)")
def unbracketed_continuation_marker_recognizer(input, pos):
    if state.is_bracketed():
        return None
    match = continuation_marker_re.match(input, pos)
    if match:
        return input[pos:match.end()]

def unbracketed_increased_indent_after_continuation_marker_recognizer(
        input, pos):
    if (not state.is_bracketed() and
        state.starting_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if (len(new_indent) > state.current_indent() and
                len(new_indent) <= state.maximum_continuation_indent()):
                return new_line_and_possible_indent

def unbracketed_aligned_indent_in_continuation_recognizer(input, pos):
    if (not state.is_bracketed() and
        state.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) == state.current_indent():
                return new_line_and_possible_indent

def unbracketed_decreased_indent_one_level_in_continuation_recognizer(
        input, pos):
    if (not state.is_bracketed() and
        state.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) < state.current_indent():
                return ""

recognizers = {
    'unbracketed_aligned_indent': unbracketed_aligned_indent_recognizer,
    'unbracketed_increased_indent': unbracketed_increased_indent_recognizer,
    'unbracketed_decreased_indent_one_level':
        unbracketed_decreased_indent_one_level_recognizer,

    'bracketed_new_line': bracketed_new_line_recognizer,
    'unbracketed_continuation_marker':
        unbracketed_continuation_marker_recognizer,
    'unbracketed_increased_indent_after_continuation_marker':
        unbracketed_increased_indent_after_continuation_marker_recognizer,
    'unbracketed_aligned_indent_in_continuation':
        unbracketed_aligned_indent_in_continuation_recognizer,
    'unbracketed_decreased_indent_one_level_in_continuation':
        unbracketed_decreased_indent_one_level_in_continuation_recognizer,
}

grammar = Grammar.from_string(grammar_string, recognizers=recognizers)

def open_bracket_action(context, node):
    state.nest_bracket()
    return node

def close_bracket_action(context, node):
    state.unnest_bracket()
    return node

def unbracketed_increased_indent_action(context, node):
    state.push_indent(node[1:])
    return node

def unbracketed_decreased_indent_one_level_action(context, node):
    partial_indent = False
    new_line_and_possible_indent = match_new_line_and_possible_indent(
        context.input_str, context.start_position)
    if new_line_and_possible_indent is not None:
        new_indent = new_line_and_possible_indent[1:]
        if len(new_indent) > state.previous_indent():
            partial_indent = True
    state.pop_indent()
    if partial_indent:
        state.start_continuation()
    return node

def unbracketed_continuation_marker_action(context, node):
    state.start_continuation()
    return node

def unbracketed_increased_indent_after_continuation_marker_action(
        context, node):
    state.push_indent(node[1:])
    state.set_maximum_continuation_indent(" "*state.current_indent())
    return node

def unbracketed_decreased_indent_one_level_in_continuation_action(
        context, node):
    partial_indent = False
    new_line_and_possible_indent = match_new_line_and_possible_indent(
        context.input_str, context.start_position)
    if new_line_and_possible_indent is not None:
        new_indent = new_line_and_possible_indent[1:]
        if len(new_indent) > state.previous_indent():
            partial_indent = True
    state.pop_indent()
    if partial_indent:
        state.start_continuation()
    return node

side_effects = {
    'open_parenthesis': open_bracket_action,
    'close_parenthesis': close_bracket_action,
    'open_brace': open_bracket_action,
    'close_brace': close_bracket_action,
    'unbracketed_increased_indent': unbracketed_increased_indent_action,
    'unbracketed_decreased_indent_one_level':
        unbracketed_decreased_indent_one_level_action,

    'unbracketed_continuation_marker': unbracketed_continuation_marker_action,
    'unbracketed_increased_indent_after_continuation_marker':
        unbracketed_increased_indent_after_continuation_marker_action,
    'unbracketed_decreased_indent_one_level_in_continuation':
        unbracketed_decreased_indent_one_level_in_continuation_action,
}

actions = {
    'file': File.parser_action,
    'expressions': Expressions.parser_action,
    'comma_delimited_sequence': Sequence.comma_parser_action,
    'named_expression': Named_Expression.parser_action,
    'key': Identifier.parser_action,
    'parenthesized_expression': lambda context, nodes: nodes[1],
    'empty_parentheses': lambda context, nodes: Sequence(),
    'braced_block': Sequence.block_parser_action,
    'unbracketed_indented_block': Sequence.block_parser_action,
    'identifier': Identifier.parser_action,
    'call': Call.parser_action,
    'named_argument': Named_Expression.parser_action,
    'chained_call': Call.parser_action,
}
actions.update(side_effects)

parser = Parser(grammar, actions=actions,debug=0)
#parser = GLRParser(grammar, actions=actions,debug=0)

file = parser.parse(input_string)
if isinstance(file, list):
    for f in file:
        f.print()
else:
    file.print()
