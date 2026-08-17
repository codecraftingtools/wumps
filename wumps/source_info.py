# Copyright (C) 2026 Jeffrey A. Webb

"""
Source information for Wumps abstract syntax tree nodes.
"""

import dataclasses

@dataclasses.dataclass
class Source_Info:
    line: int = None
    column: int = None
    end_line: int = None
    end_column: int = None
    start_pos: int = None
    end_pos: int = None
    file_text: str = None
    file_name: str = None
