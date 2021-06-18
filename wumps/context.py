# Copyright 2018, 2019 Jeffrey A. Webb

"""
Extra context required for parsing significant whitespace.
"""

from collections import namedtuple

Indented_Block = namedtuple('Indented_Block', ['amount', 'is_continuation'])

class Context:
    def __init__(self):
        self._indent_stack = [Indented_Block(amount=0, is_continuation=False)]
        self._starting_continuation = False
        self._bracket_depth = 0

    def current_indent(self):
        return self._indent_stack[-1].amount

    def previous_indent(self):
        if len(self._indent_stack) > 1:
            return self._indent_stack[-2].amount
        else:
            return None

    def push_indent(self, amount, is_continuation):
        self._indent_stack.append(
            Indented_Block(amount=amount, is_continuation=is_continuation))
        self._starting_continuation = False

    def pop_indent(self):
        self._indent_stack.pop()

    def in_continuation(self):
        return self._indent_stack[-1].is_continuation

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
