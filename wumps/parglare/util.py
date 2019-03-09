"""
Utility routines used in multiple source files.
"""

import re

new_line_and_possible_indent_re = re.compile(r"\n *")

def match_new_line_and_possible_indent(input, pos):
    match = new_line_and_possible_indent_re.match(input, pos)
    if match is None:
        return None
    return input[pos:match.end()]
