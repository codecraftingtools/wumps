"""
Extra context required for parsing significant whitespace.
"""

import parglare.parser

from wumps.context import Context as Extra_Context

class Context(parglare.parser.Context):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.extra = Extra_Context()


