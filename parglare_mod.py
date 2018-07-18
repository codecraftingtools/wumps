# This file contains the required modifications to parglare.

from parglare import *

class Parser_Overrides:
    def _token_recognition(self, input_str, position, actions, finish_flags):
        tokens = []
        last_prior = -1
        for idx, symbol in enumerate(actions):
            if symbol.prior < last_prior and tokens:
                break
            last_prior = symbol.prior
            tok = symbol.recognizer(input_str, position)
            # Empty string matches are required for handling
            # significant whitespace.
            if tok is not None:
                tokens.append(Token(symbol, tok))
                if finish_flags[idx]:
                    break
        return tokens

Parser._token_recognition = Parser_Overrides._token_recognition
GLRParser._token_recognition = Parser_Overrides._token_recognition
