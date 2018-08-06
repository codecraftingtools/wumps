"""
Custom recognizers for grammar terminals.
"""

import re
from parglare import get_collector
from wumps.util import match_new_line_and_possible_indent

recognizer = get_collector()

@recognizer
def unbracketed_aligned_indent_outside_continuation(context, input, pos):
    if (not context.extra.is_bracketed() and
        not context.extra.starting_continuation() and 
        not context.extra.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) == context.extra.current_indent():
                return new_line_and_possible_indent

@recognizer
def unbracketed_increased_indent_without_continuation_marker(
        context, input, pos):
    if (not context.extra.is_bracketed() and
        not context.extra.starting_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) > context.extra.current_indent():
                return new_line_and_possible_indent

@recognizer
def unbracketed_decreased_indent_outside_continuation(context, input, pos):
    if (not context.extra.is_bracketed() and
        not context.extra.starting_continuation() and
        not context.extra.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) < context.extra.current_indent():
                if len(new_indent) > context.extra.previous_indent():
                    # partial unindent
                    return new_line_and_possible_indent
                else:
                    return ""

@recognizer
def bracketed_new_line(context, input, pos):
    if context.extra.is_bracketed():
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            return new_line_and_possible_indent

continuation_marker_re = re.compile(r"\.\.\. *(#.*)?(?=\n)")

@recognizer
def unbracketed_continuation_marker(context, input, pos):
    if context.extra.is_bracketed():
        return None
    match = continuation_marker_re.match(input, pos)
    if match:
        return input[pos:match.end()]

@recognizer
def unbracketed_increased_indent_after_continuation_marker(context, input, pos):
    if (not context.extra.is_bracketed() and
        context.extra.starting_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if (len(new_indent) > context.extra.current_indent()):
                return new_line_and_possible_indent

@recognizer
def unbracketed_aligned_indent_inside_continuation(context, input, pos):
    if (not context.extra.is_bracketed() and
        context.extra.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) == context.extra.current_indent():
                return new_line_and_possible_indent

@recognizer
def unbracketed_decreased_indent_inside_continuation(context, input, pos):
    if (not context.extra.is_bracketed() and
        not context.extra.starting_continuation() and
        context.extra.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) < context.extra.current_indent():
                if len(new_indent) > context.extra.previous_indent():
                    # partial unindent
                    return new_line_and_possible_indent
                else:
                    return ""
