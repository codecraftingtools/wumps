# Copyright (C) 2026 Jeffrey A. Webb

"""
Widely-Useful Macro Programming Syntax (Wumps).
"""

from enum import IntEnum

class Phase(IntEnum):
    PARTIAL_PARSE = 0
    PARSE = 1
    AST = 2
    ALL = 3
