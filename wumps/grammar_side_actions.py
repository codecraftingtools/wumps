"""
Side-effect actions to be taken when grammar patterns are recognized.
"""

from parglare import get_collector
from wumps.util import match_new_line_and_possible_indent

side_action = get_collector()

def open_bracket(context, node):
    context.extra.nest_bracket()
    return node
side_action('open_parenthesis')(open_bracket)
side_action('open_brace')(open_bracket)

def close_bracket(context, node):
    context.extra.unnest_bracket()
    return node
side_action('close_parenthesis')(close_bracket)
side_action('close_brace')(close_bracket)

@side_action
def unbracketed_increased_indent_without_continuation_marker(context, node):
    context.extra.push_indent(node[1:])
    return node

@side_action
def unbracketed_decreased_indent_outside_continuation(context, node):
    partial_indent = False
    new_line_and_possible_indent = match_new_line_and_possible_indent(
        context.input_str, context.start_position)
    if new_line_and_possible_indent is not None:
        new_indent = new_line_and_possible_indent[1:]
        if len(new_indent) > context.extra.previous_indent():
            partial_indent = True
    context.extra.pop_indent()
    if partial_indent:
        context.extra.start_continuation()
    return node

@side_action
def unbracketed_continuation_marker(context, node):
    context.extra.start_continuation()
    return node

@side_action
def unbracketed_increased_indent_after_continuation_marker(context, node):
    context.extra.push_indent(node[1:])
    context.extra.set_maximum_continuation_indent(
        " "*context.extra.current_indent())
    return node

@side_action
def unbracketed_decreased_indent_inside_continuation(context, node):
    partial_indent = False
    new_line_and_possible_indent = match_new_line_and_possible_indent(
        context.input_str, context.start_position)
    if new_line_and_possible_indent is not None:
        new_indent = new_line_and_possible_indent[1:]
        if len(new_indent) > context.extra.previous_indent():
            partial_indent = True
    context.extra.pop_indent()
    if partial_indent:
        context.extra.start_continuation()
    return node

@side_action
def unbracketed_partially_decreased_indent(context, node):
    return node
