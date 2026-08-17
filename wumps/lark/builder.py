# Copyright (C) 2020 Jeffrey A. Webb
# Copyright (C) 2021 NTA, Inc.

"""
Wumps abstract syntax tree builder.
"""

import wumps.ast
import wumps.source_info
import lark
import textwrap

class Builder:
    def __init__(self, args):
        self._args = args

    def build_ast(self, *args, **kw):
        return build_ast(*args, **kw)

def build_ast(parse_tree_node, file_text=None, file_name=None):
    if isinstance(parse_tree_node, lark.Tree):
        t = parse_tree_node
        src_info = wumps.source_info.Source_Info(
            line = t.meta.line,
            column = t.meta.column,
            end_line = t.meta.end_line,
            end_column = t.meta.end_column,
            start_pos = t.meta.start_pos,
            end_pos = t.meta.end_pos,
            file_text = file_text,
            file_name = file_name,
        )
        if t.data == "file":
            elements = [build_ast(child, file_text, file_name)
                        for child in t.children]
            ast_node = wumps.ast.File(elements, src_info)
            if file_name is not None:
                ast_node.path = file_name
        elif (t.data == "sequence" or
              t.data == "braced_block"):
            elements = [build_ast(child, file_text, file_name)
                        for child in t.children]
            ast_node = wumps.ast.Sequence(elements, src_info)
        elif t.data == "binary_operation":
            callee = build_ast(t.children[1], file_text, file_name)
            argument1 = build_ast(t.children[0], file_text, file_name)
            argument2 = build_ast(t.children[2], file_text, file_name)
            arguments = wumps.ast.Sequence([argument1, argument2], src_info)
            ast_node = wumps.ast.Call(callee, arguments, src_info)
        elif t.data == "call":
            callee = build_ast(t.children[0], file_text, file_name)
            if len(t.children) == 2:
                arguments = build_ast(t.children[1], file_text, file_name)
                if not isinstance(arguments, wumps.ast.Sequence):
                    arguments = wumps.ast.Sequence([arguments], src_info)
            else:
                arguments = [build_ast(child, file_text, file_name)
                             for child in t.children[1:]]
                arguments = wumps.ast.Sequence(arguments, src_info)
            ast_node = wumps.ast.Call(callee, arguments, src_info)
        elif (t.data == "named_expression" or
              t.data == "named_argument"):
            name = build_ast(t.children[0], file_text, file_name)
            if len(t.children) > 1:
                expression = build_ast(t.children[1], file_text, file_name)
            else:
                expression = wumps.ast.Nothing(src_info)
            ast_node = wumps.ast.Named_Expression(name, expression, src_info)
        elif t.data == "empty_parentheses":
            ast_node = wumps.ast.Sequence([], src_info)
        else:
            raise Exception(f"unknown parse tree data field: {t.data}")
    elif isinstance(parse_tree_node, lark.Token):
        t = parse_tree_node
        src_info = wumps.source_info.Source_Info(
            line = t.line,
            column = t.column,
            end_line = t.end_line,
            end_column = t.end_column,
            start_pos = t.start_pos,
            end_pos = t.end_pos,
            file_text = file_text,
            file_name = file_name,
        )
        if (t.type == "SIMPLE_IDENTIFIER" or
            t.type == "COMPLEX_IDENTIFIER"):
            ast_node = wumps.ast.Identifier(fix_up_identifier(t), src_info)
        elif (t.type == "HEXADECIMAL_INTEGER" or
              t.type == "OCTAL_INTEGER" or
              t.type == "BINARY_INTEGER" or
              t.type == "DECIMAL_INTEGER"):
            ast_node = wumps.ast.Integer(fix_up_integer(t), src_info)
        elif t.type == "FLOAT":
            ast_node = wumps.ast.Float(fix_up_float(t), src_info)
        elif (t.type == "SIMPLE_STRING" or
              t.type == "BLOCK_STRING"):
            ast_node = wumps.ast.String(fix_up_string(t), src_info)
        elif t.type == "MEMBER_OPERATOR":
            ast_node = wumps.ast.Operator(t, src_info)
        elif t.type == "RANGE_OPERATOR":
            ast_node = wumps.ast.Operator(t, src_info)
        elif t.type == "EXPONENTIATION_OPERATOR":
            ast_node = wumps.ast.Operator(t, src_info)
        elif t.type == "ADDITION_OPERATOR":
            ast_node = wumps.ast.Operator(t, src_info)
        elif t.type == "SUBRACTION_OPERATOR":
            ast_node = wumps.ast.Operator(t, src_info)
        elif t.type == "MULTIPLICATION_OPERATOR":
            ast_node = wumps.ast.Operator(t, src_info)
        elif t.type == "DIVISION_OPERATOR":
            ast_node = wumps.ast.Operator(t, src_info)
        else:
            raise Exception(f"unknown parse tree token type: {t.type}")
    return ast_node

def fix_up_identifier(node):
    # Complex identifiers need special handling.
    if node.startswith("'"):
        # Strip quotes and remove escape sequences.
        node = node[1:-1].replace("\\'","'")

    return node

def fix_up_string(node):
    # If this is a block string
    if node.startswith('"""'):
        # Strip triple quotes, remove common leading whitespace
        # and remove leading/trailing newlines.  No escape
        # characters are currently implemented for block strings.
        unescaped_text = textwrap.dedent(
            node[3:-3]).strip()
    else:
        # Strip quotes and remove escape sequences.
        unescaped_text = node[1:-1].replace('\\"','"')
    return unescaped_text

def fix_up_integer(node):
    node = node.lower()
    base = 10
    if (node.startswith( "0x") or 
        node.startswith("-0x") or
        node.startswith("+0x")):
        base = 16
    elif (node.startswith( "0b") or 
          node.startswith("-0b") or
          node.startswith("+0b")):
        base = 2
    elif (node.startswith( "0o") or 
          node.startswith("-0o") or
          node.startswith("+0o")):
        base = 8
    return int(node.replace("_",""), base=base)

def fix_up_float(node):
    return float(node.replace("_",""))
