# Actions to be taken when grammar patterns are recognized

from parglare import get_collector
from context import state
from util import match_new_line_and_possible_indent

action = get_collector()

# Parsing side-effects

@action
def open_bracket(context, node):
    state.nest_bracket()
    return node

@action
def close_bracket(context, node):
    state.unnest_bracket()
    return node

@action
def unbracketed_increased_indent(context, node):
    state.push_indent(node[1:])
    return node

@action
def unbracketed_decreased_indent_one_level(context, node):
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

@action
def unbracketed_continuation_marker(context, node):
    state.start_continuation()
    return node

@action
def unbracketed_increased_indent_after_continuation_marker(context, node):
    state.push_indent(node[1:])
    state.set_maximum_continuation_indent(" "*state.current_indent())
    return node

@action
def unbracketed_decreased_indent_one_level_in_continuation(context, node):
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

# AST construction actions
import ast

action('file')                      (ast.File.create_from_nodes)
action('expressions')               (ast.Elements.create_from_nodes)
action('comma_delimited_sequence')  (ast.Sequence.
                                         create_from_comma_separated_nodes)
action('named_expression')          (ast.Named_Expression.create_from_nodes)
action('key')                       (ast.Identifier.create_from_node)
action('braced_block')              (ast.Sequence.create_from_block_nodes)
action('unbracketed_indented_block')(ast.Sequence.create_from_block_nodes)
action('simple_identifier')         (ast.Identifier.create_from_node)
action('complex_identifier')        (ast.Identifier.create_from_node)
action('call')                      (ast.Call.create_from_nodes)
action('named_argument')            (ast.Named_Expression.create_from_nodes)
action('chained_call')              (ast.Call.create_from_nodes)
action('string')                    (ast.String.create_from_node)
action('decimal_integer')           (ast.Integer.create_from_node)
action('hexadecimal_integer')       (ast.Integer.create_from_node)
action('binary_integer')            (ast.Integer.create_from_node)
action('octal_integer')             (ast.Integer.create_from_node)
action('float')                     (ast.Float.create_from_node)

@action
def parenthesized_expression(context, nodes):
    return nodes[1]

@action
def empty_parentheses(context, nodes):
    return ast.Sequence()
