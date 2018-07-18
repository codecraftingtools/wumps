new_line_and_possible_indent_re = re.compile(r"\n *")
def match_new_line_and_possible_indent(input, pos):
    match = new_line_and_possible_indent_re.match(input, pos)
    if match is None:
        return None
    return input[pos:match.end()]

def unbracketed_aligned_indent_recognizer(input, pos):
    if (not state.is_bracketed() and
        not state.starting_continuation() and 
        not state.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) == state.current_indent():
                return new_line_and_possible_indent

def unbracketed_increased_indent_recognizer(input, pos):
    if (not state.is_bracketed() and
        not state.starting_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) > state.current_indent():
                return new_line_and_possible_indent

def unbracketed_decreased_indent_one_level_recognizer(input, pos):
    if (not state.is_bracketed() and
        not state.starting_continuation() and
        not state.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) < state.current_indent():
                return ""

def bracketed_new_line_recognizer(input, pos):
    if state.is_bracketed():
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            return new_line_and_possible_indent

continuation_marker_re = re.compile(r"\.\.\. *(#.*)?(?=\n)")
def unbracketed_continuation_marker_recognizer(input, pos):
    if state.is_bracketed():
        return None
    match = continuation_marker_re.match(input, pos)
    if match:
        return input[pos:match.end()]

def unbracketed_increased_indent_after_continuation_marker_recognizer(
        input, pos):
    if (not state.is_bracketed() and
        state.starting_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if (len(new_indent) > state.current_indent() and
                len(new_indent) <= state.maximum_continuation_indent()):
                return new_line_and_possible_indent

def unbracketed_aligned_indent_in_continuation_recognizer(input, pos):
    if (not state.is_bracketed() and
        state.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) == state.current_indent():
                return new_line_and_possible_indent

def unbracketed_decreased_indent_one_level_in_continuation_recognizer(
        input, pos):
    if (not state.is_bracketed() and
        state.in_continuation()):
        new_line_and_possible_indent = match_new_line_and_possible_indent(
            input, pos)
        if new_line_and_possible_indent is not None:
            new_indent = new_line_and_possible_indent[1:]
            if len(new_indent) < state.current_indent():
                return ""

recognizers = {
    'unbracketed_aligned_indent': unbracketed_aligned_indent_recognizer,
    'unbracketed_increased_indent': unbracketed_increased_indent_recognizer,
    'unbracketed_decreased_indent_one_level':
        unbracketed_decreased_indent_one_level_recognizer,

    'bracketed_new_line': bracketed_new_line_recognizer,
    'unbracketed_continuation_marker':
        unbracketed_continuation_marker_recognizer,
    'unbracketed_increased_indent_after_continuation_marker':
        unbracketed_increased_indent_after_continuation_marker_recognizer,
    'unbracketed_aligned_indent_in_continuation':
        unbracketed_aligned_indent_in_continuation_recognizer,
    'unbracketed_decreased_indent_one_level_in_continuation':
        unbracketed_decreased_indent_one_level_in_continuation_recognizer,
}
