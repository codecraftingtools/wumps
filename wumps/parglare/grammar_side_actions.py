# Copyright 2018, 2019 Jeffrey A. Webb

"""
Side-effect actions to be taken when grammar patterns are recognized.
"""

from parglare import get_collector
from wumps.parglare.util import match_new_line_and_possible_indent

side_action = get_collector()

def open_bracket(context, node):
    context.extra.nest_bracket()
side_action('open_parenthesis')(open_bracket)
side_action('open_brace')(open_bracket)

def close_bracket(context, node):
    context.extra.unnest_bracket()
side_action('close_parenthesis')(close_bracket)
side_action('close_brace')(close_bracket)

@side_action
def unbracketed_increased_indent_without_continuation_marker(context, node):
    context.extra.push_indent(amount=len(node[1:]), is_continuation=False)

def unbracketed_decreased_indent(context, node):
    context.extra.pop_indent()
    if node: # node is empty string unless we have a partial unindent
        context.extra.push_indent(amount=len(node[1:]), is_continuation=True)
side_action('unbracketed_decreased_indent_outside_continuation')(
    unbracketed_decreased_indent)
side_action('unbracketed_decreased_indent_inside_continuation')(
    unbracketed_decreased_indent)

@side_action
def unbracketed_continuation_marker(context, node):
    context.extra.start_continuation()

@side_action
def unbracketed_increased_indent_after_continuation_marker(context, node):
    context.extra.push_indent(amount=len(node[1:]), is_continuation=True)
