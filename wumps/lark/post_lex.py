# Copyright 2020, 2021 Jeffrey A. Webb
# Copyright 2021 NTA, Inc.

"""
Lark Post-Lex Processor for Wumps.
"""

from lark.lexer import Token
from wumps.context import Context

class Post_Lex_Processor:
    open_bracket_types  = ["_OPEN_BRACE", "_OPEN_PARENTHESIS",
                           "_OPEN_SQUARE_BRACKET"]
    close_bracket_types = ["_CLOSE_BRACE", "_CLOSE_PARENTHESIS",
                           "_CLOSE_SQUARE_BRACKET"]
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
                yield Token.new_borrow_pos(
                    "_UNBRACKETED_DECREASED_INDENT_OUTSIDE_CONTINUATION",
                    token, token)
                self.context.push_indent(
                    amount=len(new_indent), is_continuation=True)
                # The following yield could be omitted -- the token is
                # removed by the post-lex filter
                yield Token.new_borrow_pos(
                    "IMPLICIT_CONTINUATION_INDENT",
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
            # The following yield could be omitted -- the token is
            # removed by the post-lex filter
            yield Token.new_borrow_pos(
                "BRACKETED_NEWLINE",
                token, token)
        elif (not self.context.is_bracketed() and
              self.context.starting_continuation() and
              len(new_indent) > self.context.current_indent()):
            self.context.push_indent(
                amount=len(new_indent), is_continuation=True)
            # The following yield could be omitted -- the token is
            # removed by the post-lex filter
            yield Token.new_borrow_pos(
                "UNBRACKETED_INCREASED_INDENT_AFTER_CONTINUATION_MARKER",
                token, token)
        elif (not self.context.is_bracketed() and
              self.context.in_continuation() and
              len(new_indent) == self.context.current_indent()):
            # The following yield could be omitted -- the token is
            # removed by the post-lex filter
            yield Token.new_borrow_pos(
                "UNBRACKETED_ALIGNED_INDENT_INSIDE_CONTINUATION",
                token, token)
        elif (not self.context.is_bracketed() and
              not self.context.starting_continuation() and
              self.context.in_continuation() and
              len(new_indent) < self.context.current_indent()):
            if len(new_indent) > self.context.previous_indent():
                # partial unindent
                self.context.pop_indent()
                # The following yield could be omitted -- the token is
                # removed by the post-lex filter
                yield Token.new_borrow_pos(
                    "UNBRACKETED_DECREASED_INDENT_INSIDE_CONTINUATION",
                token, token)
                self.context.push_indent(
                    amount=len(new_indent), is_continuation=True)
                # The following yield could be omitted -- the token is
                # removed by the post-lex filter
                yield Token.new_borrow_pos(
                    "IMPLICIT_CONTINUATION_INDENT",
                    token, token)
            else:
                self.context.pop_indent()
                # The following yield could be omitted -- the token is
                # removed by the post-lex filter
                yield Token.new_borrow_pos(
                    "UNBRACKETED_DECREASED_INDENT_INSIDE_CONTINUATION",
                    token, token)
                yield Token(
                    "_UNBRACKETED_ALIGNED_INDENT_OUTSIDE_CONTINUATION","")
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
                    self.context.start_continuation()
                    # The following yield could be omitted -- the token is
                    # removed by the post-lex filter
                    yield Token.new_borrow_pos(
                        "UNBRACKETED_CONTINUATION_MARKER",
                        token, token)
                else:
                    yield token
            elif token.type == "NEWLINE_AND_MAYBE_INDENT":
                for t in self.handle_newline_and_maybe_indent(token):
                    yield t
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

class Post_Lex_Processor_and_Filter:
    always_accept = Post_Lex_Processor.always_accept

    def __init__(self, filter=True):
        self._filter = filter
        
    def process(self, stream):
        generator = Post_Lex_Processor().process(stream)
        for token in generator:
            if token.type in [
                    "IMPLICIT_CONTINUATION_INDENT",
                    "BRACKETED_NEWLINE",
                    "UNBRACKETED_ALIGNED_INDENT_INSIDE_CONTINUATION",
                    
                    "UNBRACKETED_CONTINUATION_MARKER",
                    "UNBRACKETED_INCREASED_INDENT_AFTER_CONTINUATION_MARKER",
                    "UNBRACKETED_DECREASED_INDENT_INSIDE_CONTINUATION",
            ] and self._filter:
                continue
            else:
                yield token

def print_lex(generator):
    for token in generator:
        if token.type in [
                "NEWLINE_AND_MAYBE_INDENT",
                
                "_UNBRACKETED_ALIGNED_INDENT_OUTSIDE_CONTINUATION",
                "_UNBRACKETED_INCREASED_INDENT_WITHOUT_CONTINUATION_MARKER",
                "_UNBRACKETED_DECREASED_INDENT_OUTSIDE_CONTINUATION",

                "IMPLICIT_CONTINUATION_INDENT",
                "BRACKETED_NEWLINE",
                "UNBRACKETED_ALIGNED_INDENT_INSIDE_CONTINUATION",

                "UNBRACKETED_INCREASED_INDENT_AFTER_CONTINUATION_MARKER",
                "UNBRACKETED_DECREASED_INDENT_INSIDE_CONTINUATION",
        ]:
            print(token.type)
        else:
            print(token.type,token)
