"""
Lark Post-Lex Processor for Wumps.
"""

from lark.lexer import Token
from wumps.context import Context

class Post_Lex_Processor:
    open_bracket_types  = ["_OPEN_BRACE", "_OPEN_PARENTHESIS"]
    close_bracket_types = ["_CLOSE_BRACE", "_CLOSE_PARENTHESIS"]
    def __init__(self):
        self.context = Context()
        
    def handle_newline_and_maybe_indent(self, token):
        new_indent = token[1:]
        if (not self.context.is_bracketed() and
            not self.context.starting_continuation() and 
            not self.context.in_continuation() and
            len(new_indent) == self.context.current_indent()):
            yield Token.new_borrow_pos(
                "_UNBRACKETED_ALIGNED_INDENT_OUTSIDE_CONTINUATION",
                token, token)
        elif (not self.context.is_bracketed() and
              not self.context.starting_continuation() and 
              len(new_indent) > self.context.current_indent()):
            self.context.push_indent(
                amount=len(new_indent), is_continuation=False)
            yield Token.new_borrow_pos(
                "_UNBRACKETED_INCREASED_INDENT_WITHOUT_CONTINUATION_MARKER",
                token, token)
        elif (not self.context.is_bracketed() and
              not self.context.starting_continuation() and 
              not self.context.in_continuation() and
              len(new_indent) < self.context.current_indent()):
            if len(new_indent) > self.context.previous_indent():
                # partial unindent
                self.context.pop_indent()
                self.context.push_indent(
                    amount=len(new_indent), is_continuation=True)
                yield Token.new_borrow_pos(
                    "_UNBRACKETED_DECREASED_INDENT_OUTSIDE_CONTINUATION",
                    token, token)
            else:
                self.context.pop_indent()
                yield Token.new_borrow_pos(
                    "_UNBRACKETED_DECREASED_INDENT_OUTSIDE_CONTINUATION",
                    "", token)
                if not self.context.in_continuation():
                    yield Token("_UNBRACKETED_ALIGNED_INDENT_OUTSIDE_CONTINUATION","")
                if len(new_indent) < self.context.current_indent():
                    # More than one level
                    for t in self.handle_newline_and_maybe_indent(token):
                        yield t
        elif (self.context.is_bracketed()):
            # Ignore BRACKETED_NEWLINE
            pass
        elif (not self.context.is_bracketed() and
              self.context.starting_continuation() and
              len(new_indent) > self.context.current_indent()):
            # UNBRACKETED_INCREASED_INDENT_AFTER_CONTINUATION_MARKER
            self.context.push_indent(
                amount=len(new_indent), is_continuation=True)
        elif (not self.context.is_bracketed() and
              self.context.in_continuation() and
              len(new_indent) == self.context.current_indent()):
            # UNBRACKETED_ALIGNED_INDENT_INSIDE_CONTINUATION
            pass
        elif (not self.context.is_bracketed() and
              not self.context.starting_continuation() and
              self.context.in_continuation() and
              len(new_indent) < self.context.current_indent()):
            # UNBRACKETED_DECREASED_INDENT_INSIDE_CONTINUATION
            yield Token("_UNBRACKETED_ALIGNED_INDENT_OUTSIDE_CONTINUATION","")
            if len(new_indent) > self.context.previous_indent():
                # partial unindent
                self.context.pop_indent()
                self.context.push_indent(
                    amount=len(new_indent), is_continuation=True)
            else:
                self.context.pop_indent()
                if len(new_indent) < self.context.current_indent():
                    # More than one level
                    for t in self.handle_newline_and_maybe_indent(token):
                        yield t
        else:
            yield token
        
    def process(self, stream):
        for token in stream:
            if token.type in self.open_bracket_types:
                self.context.nest_bracket()
                yield token
            elif token.type in self.close_bracket_types:
                self.context.unnest_bracket()
                yield token
            elif token.type == "CONTINUATION_MARKER":
                if not self.context.is_bracketed():
                    # UNBRACKETED_CONTINUATION_MARKER
                    self.context.start_continuation()
                else:
                    yield token
            elif token.type == "NEWLINE_AND_MAYBE_INDENT":
                for t in self.handle_newline_and_maybe_indent(token):
                    yield t
            elif token.type == "KEY":
                # Strip colon from end of key
                yield Token.new_borrow_pos("KEY", token[:-1], token)
            else:
                yield token
        while self.context.current_indent() > 0:
            self.context.pop_indent()
            yield Token("_UNBRACKETED_DECREASED_INDENT_OUTSIDE_CONTINUATION","")
            if not self.context.in_continuation():
                yield Token("_UNBRACKETED_ALIGNED_INDENT_OUTSIDE_CONTINUATION","")

    # XXX Hack for ContextualLexer. Maybe there's a more elegant solution?
    @property
    def always_accept(self):
        return "NEWLINE_AND_MAYBE_INDENT", "CONTINUATION_MARKER"

def print_lex(generator):
    for token in generator:
        if token.type in [
                "NEWLINE_AND_MAYBE_INDENT",
                "_UNBRACKETED_ALIGNED_INDENT_OUTSIDE_CONTINUATION",
                "_UNBRACKETED_INCREASED_INDENT_WITHOUT_CONTINUATION_MARKER",
                "_UNBRACKETED_DECREASED_INDENT_OUTSIDE_CONTINUATION",
        ]:
            print(token.type)
        else:
            print(token.type,token)
