#!/usr/bin/env python3

from parglare import *
from parglare.parser import *

Parser_ = Parser
class Parser(Parser_):
    def _next_token(self, state, input_str, position):
        """
        For the current position in the input stream and actions in the current
        state find next token.
        """
        #print("start----------------")
        actions = state.actions
        finish_flags = state.finish_flags

        in_len = len(input_str)

        # Find the next token in the input
        if position == in_len and EMPTY not in actions \
           and STOP not in actions:
            # Execute EOF action at end of input only if EMTPY and
            # STOP terminals are not in actions as this might call
            # for reduction.
            ntok = EOF_token
        else:
            tokens = []
            if position < in_len:
                for idx, symbol in enumerate(actions):
                    #print(symbol.recognizer)
                    tok = symbol.recognizer(input_str, position)
                    #print('here', type(tok), "<{}>".format(tok))
                    #raise "JEFF"
                    if tok is not None:
                        #print('there')
                        tokens.append(Token(symbol, tok))
                        if finish_flags[idx]:
                            break
            #print('tokens:', tokens)
            if not tokens:
                if STOP in actions:
                    ntok = STOP_token
                else:
                    ntok = EMPTY_token
            elif len(tokens) == 1:
                ntok = tokens[0]
            else:
                ntok = self._lexical_disambiguation(tokens)

        #print('returning', ntok)
        return ntok
