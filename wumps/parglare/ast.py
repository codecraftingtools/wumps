# Copyright 2018, 2020 Jeffrey A. Webb

"""
Abstract syntax tree nodes (parglare extension).
"""

import wumps.ast
import textwrap

class Identifier(wumps.ast.Identifier):
    @classmethod
    def create_from_node(cls, context, node):
        # The trailing colon for keys is an artifact of the way the
        # grammar is defined and needs to be removed.
        if node.endswith(':'):
            node = node[:-1].rstrip()

        # Complex identifiers need special handling.
        if node.startswith("'"):
            # Strip quotes and remove escape sequences.
            node = node[1:-1].replace("\\'","'")

        return cls(node, context=context)

class String(wumps.ast.String):
    @classmethod
    def create_from_node(cls, context, node):
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
        return cls(unescaped_text, context=context)

class Integer(wumps.ast.Integer):
    @classmethod
    def create_from_node(cls, context, node):
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
        return cls(int(node.replace("_",""), base=base), context=context)

class Float(wumps.ast.Float):
    @classmethod
    def create_from_node(cls, context, node):
        return cls(float(node.replace("_","")), context=context)

class Named_Expression(wumps.ast.Named_Expression):
    @classmethod
    def create_from_nodes(cls, context, nodes):
        if len(nodes) < 2:
            expression = wumps.ast.Nothing(context)
        else:
            expression = nodes[1]
        return cls(nodes[0], expression, context=context)

class Call(wumps.ast.Call):
    @classmethod
    def create_from_nodes(cls, context, nodes):
        callee = nodes[0]
        arguments = []
        if len(nodes) > 1:
            if isinstance(nodes[1], wumps.ast.Elements):                
                arguments.extend(nodes[1].elements)
            elif isinstance(nodes[1], list):                
                arguments.extend(nodes[1])
            else:
                arguments.append(nodes[1])
        if len(nodes) > 2:
            arguments.extend(nodes[2])
        return cls(callee, arguments, context=context)

    @classmethod
    def create_from_binary_operator_nodes(cls, context, nodes):
        callee = wumps.ast.Operator(nodes[1], context=context)
        arguments = [nodes[0], nodes[2]]
        return cls(callee, arguments, context=context)

class Elements(wumps.ast.Elements):
    @classmethod
    def create_from_nodes(cls, context, nodes):
        elements = []
        if len(nodes) > 1:
            elements.extend(nodes[1])
        return cls(elements, context=context)

class File(wumps.ast.File):
    @classmethod
    def create_from_nodes(cls, context, nodes):
        return cls(nodes[0].elements, context=context)

class Sequence(wumps.ast.Sequence):
    @classmethod
    def create_from_comma_delimited_nodes(cls, context, nodes):
        elements = [nodes[0]]
        if len(nodes) > 2:
            if isinstance(nodes[2], wumps.ast.Sequence):                
                elements.extend(nodes[2].elements)
            else:
                elements.append(nodes[2])
        return cls(elements, context=context)

    @classmethod
    def create_from_block_nodes(cls, context, nodes):
        return cls(nodes[1].elements, context=context)
