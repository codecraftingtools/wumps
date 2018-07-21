"""
Custom recognizers for grammar terminals.
"""

import re
from parglare import get_collector
from wumps.context import state
from wumps.util import match_new_line_and_possible_indent

recognizer = get_collector()

@recognizer
def unbracketed_aligned_indent(input, pos):
    if (not state.is_bracketed() and
        not state.starting_continuation() and 
        not state.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) == state.current_indent():
                return new_line_and_possible_indent

@recognizer
def unbracketed_increased_indent(input, pos):
    if (not state.is_bracketed() and
        not state.starting_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) > state.current_indent():
                return new_line_and_possible_indent

@recognizer
def unbracketed_decreased_indent_one_level(input, pos):
    if (not state.is_bracketed() and
        not state.starting_continuation() and
        not state.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) < state.current_indent():
                return ""

@recognizer
def bracketed_new_line(input, pos):
    if state.is_bracketed():
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            return new_line_and_possible_indent

continuation_marker_re = re.compile(r"\.\.\. *(#.*)?(?=\n)")

@recognizer
def unbracketed_continuation_marker(input, pos):
    if state.is_bracketed():
        return None
    if state.in_continuation():
        return None
    match = continuation_marker_re.match(input, pos)
    if match:
        return input[pos:match.end()]

@recognizer
def unbracketed_increased_indent_after_continuation_marker(input, pos):
    if (not state.is_bracketed() and
        state.starting_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if (len(new_indent) > state.current_indent() and
                len(new_indent) <= state.maximum_continuation_indent()):
                return new_line_and_possible_indent

@recognizer
def unbracketed_aligned_indent_in_continuation(input, pos):
    if (not state.is_bracketed() and
        state.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) == state.current_indent():
                return new_line_and_possible_indent

@recognizer
def unbracketed_decreased_indent_one_level_in_continuation(input, pos):
    if (not state.is_bracketed() and
        state.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) < state.current_indent():
                return ""
