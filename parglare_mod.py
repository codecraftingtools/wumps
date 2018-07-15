#!/usr/bin/env python3

from parglare import *
from parglare.parser import *
from parglare.grammar import RegExRecognizer

Parser_ = Parser
class Parser(Parser_):
    def _token_recognition(self, input_str, position, actions, finish_flags):
        tokens = []
        last_prior = -1
        for idx, symbol in enumerate(actions):
            if symbol.prior < last_prior and tokens:
                break
            last_prior = symbol.prior
            tok = symbol.recognizer(input_str, position)
            if tok or (tok == "" and not isinstance(
                    symbol.recognizer,RegExRecognizer)):
                tokens.append(Token(symbol, tok))
                if finish_flags[idx]:
                    break
        return tokens
Parser_.Parser = Parser
import parglare
parglare.parser.Parser = Parser
