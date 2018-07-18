# This file contains the original parts of parglare that were modified
# in parglare_mod.py (for comparision purposes).

class Parser(object):
    def _token_recognition(self, input_str, position, actions, finish_flags):
        tokens = []
        last_prior = -1
        for idx, symbol in enumerate(actions):
            if symbol.prior < last_prior and tokens:
                break
            last_prior = symbol.prior
            tok = symbol.recognizer(input_str, position)
            if tok:
                tokens.append(Token(symbol, tok))
                if finish_flags[idx]:
                    break
        return tokens
