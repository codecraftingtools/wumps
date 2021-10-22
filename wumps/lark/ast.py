# Copyright 2020 Jeffrey A. Webb
# Copyright 2021 NTA, Inc.

"""
Abstract syntax tree nodes (lark extension).
"""

import wumps.ast
import lark
import textwrap

def build_ast(parse_tree_node, file_name=None):
    if isinstance(parse_tree_node, lark.Tree):
        t = parse_tree_node
        if t.data == "file":
            elements = [build_ast(child) for child in t.children]
            ast_node = wumps.ast.File(elements)
            if file_name is not None:
                ast_node.path = file_name
        elif (t.data == "sequence" or
              t.data == "braced_block"):
            elements = [build_ast(child) for child in t.children]
            ast_node = wumps.ast.Sequence(elements)
        elif t.data == "binary_operation":
            callee = build_ast(t.children[1])
            argument1 = build_ast(t.children[0])
            argument2 = build_ast(t.children[2])
            arguments = wumps.ast.Sequence([argument1, argument2])
            ast_node = wumps.ast.Call(callee, arguments)
        elif t.data == "call":
            callee = build_ast(t.children[0])
            if len(t.children) == 2:
                arguments = build_ast(t.children[1])
                if not isinstance(arguments, wumps.ast.Sequence):
                    arguments = wumps.ast.Sequence([arguments])
            else:
                arguments = [build_ast(child) for child in t.children[1:]]
                arguments = wumps.ast.Sequence(arguments)
            ast_node = wumps.ast.Call(callee, arguments)
        elif (t.data == "named_expression" or
              t.data == "named_argument"):
            name = build_ast(t.children[0])
            if len(t.children) > 1:
                expression = build_ast(t.children[1])
            else:
                expression = wumps.ast.Nothing()
            ast_node = wumps.ast.Named_Expression(name, expression)
        elif t.data == "empty_parentheses":
            ast_node = wumps.ast.Sequence()
        else:
            raise Exception(f"unknown parse tree data field: {t.data}")
    elif isinstance(parse_tree_node, lark.Token):
        t = parse_tree_node
        if (t.type == "SIMPLE_IDENTIFIER" or
            t.type == "COMPLEX_IDENTIFIER"):
            ast_node = wumps.ast.Identifier(fix_up_identifier(t))
        elif (t.type == "HEXADECIMAL_INTEGER" or
              t.type == "OCTAL_INTEGER" or
              t.type == "BINARY_INTEGER" or
              t.type == "DECIMAL_INTEGER"):
            ast_node = wumps.ast.Integer(fix_up_integer(t))
        elif t.type == "FLOAT":
            ast_node = wumps.ast.Float(fix_up_float(t))
        elif (t.type == "SIMPLE_STRING" or
              t.type == "BLOCK_STRING"):
            ast_node = wumps.ast.String(fix_up_string(t))
        elif t.type == "MEMBER_OPERATOR":
            ast_node = wumps.ast.Operator(t)
        else:
            raise Exception(f"unknown token type: {t.type}")
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
