"""
Actions to be taken when grammar patterns are recognized.
"""

from parglare import get_collector
from wumps import ast

action = get_collector()

action('file')                      (ast.File.create_from_nodes)
action('expressions')               (ast.Elements.create_from_nodes)
action('comma_delimited_sequence')  (ast.Sequence.
                                         create_from_comma_delimited_nodes)
action('named_expression')          (ast.Named_Expression.create_from_nodes)
action('braced_block')              (ast.Sequence.create_from_block_nodes)
action('unbracketed_indented_block_without_continuation_marker')(
                                     ast.Sequence.create_from_block_nodes)
action('call')                      (ast.Call.create_from_nodes)
action('named_argument')            (ast.Named_Expression.create_from_nodes)
action('chained_call')              (ast.Call.create_from_nodes)
action('key')                       (ast.Identifier.create_from_node)
action('simple_identifier')         (ast.Identifier.create_from_node)
action('complex_identifier')        (ast.Identifier.create_from_node)
action('string')                    (ast.String.create_from_node)
action('block_string')              (ast.String.create_from_node)
action('decimal_integer')           (ast.Integer.create_from_node)
action('hexadecimal_integer')       (ast.Integer.create_from_node)
action('binary_integer')            (ast.Integer.create_from_node)
action('octal_integer')             (ast.Integer.create_from_node)
action('float')                     (ast.Float.create_from_node)
action('binary_operation')          (ast.Call.create_from_binary_operator_nodes)

@action
def parenthesized_expression(context, nodes):
    return nodes[1]

@action
def empty_parentheses(context, nodes):
    return ast.Sequence(context=context)
