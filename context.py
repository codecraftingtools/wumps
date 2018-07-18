# Extra context required for parsing significant whitespace

class Extra_State:
    def __init__(self):
        self._indent_stack = [["", False, " "*999]]
        self._starting_continuation = False
        self._bracket_depth = 0
    def maximum_continuation_indent(self):
        return len(self._indent_stack[-1][2])
    def set_maximum_continuation_indent(self, max_indent):
        if len(max_indent) < len(self._indent_stack[-1][2]):
            self._indent_stack[-1][2] = max_indent
    def current_indent(self):
        return len(self._indent_stack[-1][0])
    def previous_indent(self):
        if len(self._indent_stack) > 1:
            return len(self._indent_stack[-2][0])
        else:
            return None
    def push_indent(self, indent):
        self._indent_stack.append([indent,self._starting_continuation," "*999])
        self._starting_continuation = False
    def pop_indent(self):
        self._indent_stack.pop()
    def in_continuation(self):
        return self._indent_stack[-1][1]
    def starting_continuation(self):
        return self._starting_continuation
    def start_continuation(self):
        self._starting_continuation = True
    def nest_bracket(self):
        self._bracket_depth += 1
    def unnest_bracket(self):
        if self._bracket_depth > 0:
            self._bracket_depth -= 1
    def is_bracketed(self):
        if self._bracket_depth:
            return True
        else:
            return False

state = Extra_State()
