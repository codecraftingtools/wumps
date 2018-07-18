def process_open_bracket(context, node):
    state.nest_bracket()
    return node

def process_close_bracket(context, node):
    state.unnest_bracket()
    return node

def process_unbracketed_increased_indent(context, node):
    state.push_indent(node[1:])
    return node

def process_unbracketed_decreased_indent_one_level(context, node):
    partial_indent = False
    new_line_and_possible_indent = match_new_line_and_possible_indent(
        context.input_str, context.start_position)
    if new_line_and_possible_indent is not None:
        new_indent = new_line_and_possible_indent[1:]
        if len(new_indent) > state.previous_indent():
            partial_indent = True
    state.pop_indent()
    if partial_indent:
        state.start_continuation()
    return node

def process_unbracketed_continuation_marker(context, node):
    state.start_continuation()
    return node

def process_unbracketed_increased_indent_after_continuation_marker(
        context, node):
    state.push_indent(node[1:])
    state.set_maximum_continuation_indent(" "*state.current_indent())
    return node

def process_unbracketed_decreased_indent_one_level_in_continuation(
        context, node):
    partial_indent = False
    new_line_and_possible_indent = match_new_line_and_possible_indent(
        context.input_str, context.start_position)
    if new_line_and_possible_indent is not None:
        new_indent = new_line_and_possible_indent[1:]
        if len(new_indent) > state.previous_indent():
            partial_indent = True
    state.pop_indent()
    if partial_indent:
        state.start_continuation()
    return node

side_effects = {
    'open_parenthesis': process_open_bracket,
    'close_parenthesis': process_close_bracket,
    'open_brace': process_open_bracket,
    'close_brace': process_close_bracket,
    'unbracketed_increased_indent': process_unbracketed_increased_indent,
    'unbracketed_decreased_indent_one_level':
        process_unbracketed_decreased_indent_one_level,

    'unbracketed_continuation_marker': process_unbracketed_continuation_marker,
    'unbracketed_increased_indent_after_continuation_marker':
        process_unbracketed_increased_indent_after_continuation_marker,
    'unbracketed_decreased_indent_one_level_in_continuation':
        process_unbracketed_decreased_indent_one_level_in_continuation,
}

actions = {
    'file': File.create_from_nodes,
    'expressions': Expressions.create_from_nodes,
    'comma_delimited_sequence': Sequence.create_from_comma_separated_nodes,
    'named_expression': Named_Expression.create_from_nodes,
    'key': Identifier.create_from_node,
    'parenthesized_expression': lambda context, nodes: nodes[1],
    'empty_parentheses': lambda context, nodes: Sequence(),
    'braced_block': Sequence.create_from_block_nodes,
    'unbracketed_indented_block': Sequence.create_from_block_nodes,
    'identifier': Identifier.create_from_node,
    'call': Call.create_from_nodes,
    'named_argument': Named_Expression.create_from_nodes,
    'chained_call': Call.create_from_nodes,
}
actions.update(side_effects)
