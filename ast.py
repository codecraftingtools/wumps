# Abstract syntax tree nodes

_indent_token = "  "

class Node:
    def __init__(self, context=None):
        self.context = context

    def _get_attribute_ast_strs(self, depth):
        return ""

    def get_ast_str(self, depth=0, first_depth=None):
        first_depth = depth if first_depth is None else first_depth
        s = "{}{}\n".format(_indent_token*first_depth, self.__class__.__name__)
        s += self._get_attribute_ast_strs(depth)
        return s

class Identifier(Node):
    def __init__(self, text, context=None):
        super().__init__(context=context)
        # The trailing colon for keys is an artifact of the way the
        # grammar is defined and needs to be removed.
        if text.endswith(':'):
            text = text[:-1].rstrip()
        self.text = text

    @classmethod
    def create_from_node(cls, context, node):
        return cls(node, context=context)

    def _get_attribute_ast_strs(self, depth):
        return '{}text: "{}"\n'.format(_indent_token*(depth+1), self.text)

class Named_Expression(Node):
    def __init__(self, name, expression, context=None):
        super().__init__(context=context)
        self.name = name
        self.expression = expression

    @classmethod
    def create_from_nodes(cls, context, nodes):
        return cls(nodes[0], nodes[1], context=context)

    def _get_attribute_ast_strs(self, depth):
        s = "{}name: ".format(_indent_token*(depth+1))
        s += self.name.get_ast_str(depth+1, first_depth=0)
        s += "{}expression: ".format(_indent_token*(depth+1))
        s += self.expression.get_ast_str(depth+1, first_depth=0)
        return s

class Call(Node):
    def __init__(self, callee, arguments, context=None):
        super().__init__(context=context)
        self.callee = callee
        if not isinstance(arguments, Sequence):
            arguments = Sequence(arguments)
        self.arguments = arguments

    @classmethod
    def create_from_nodes(cls, context, nodes):
        callee = nodes[0]
        arguments = []
        if len(nodes) > 1:
            if isinstance(nodes[1], Elements):                
                arguments.extend(nodes[1].elements)
            elif isinstance(nodes[1], list):                
                arguments.extend(nodes[1])
            else:
                arguments.append(nodes[1])
        if len(nodes) > 2:
            arguments.extend(nodes[2])
        return cls(callee, arguments, context=context)

    def _get_attribute_ast_strs(self, depth):
        s = "{}callee: ".format(_indent_token*(depth+1))
        s += self.callee.get_ast_str(depth=depth+1, first_depth=0)
        s += "{}arguments: ".format(_indent_token*(depth+1))
        s += self.arguments.get_ast_str(depth=depth+1, first_depth=0)
        return s

class Elements(Node):
    def __init__(self, elements=[], context=None):
        super().__init__(context=context)
        self.elements = tuple(elements)

    @classmethod
    def create_from_nodes(cls, context, nodes):
        elements = []
        if len(nodes) > 1:
            elements.extend(nodes[1])
        return cls(elements, context=context)

    def _get_attribute_ast_strs(self, depth):
        s = "{}elements:\n".format(_indent_token*(depth+1))
        for a in self.elements:
            try:
                s += a.get_ast_str(depth=depth+2)
            except:
                s += str(a)
        return s

class File(Elements):
    def __init__(self, elements, context=None):
        super().__init__(elements, context=context)
        if context and hasattr(context, "file_name"):
            self.path = context.file_name
        else:
            self.path = None

    @classmethod
    def create_from_nodes(cls, context, nodes):
        return cls(nodes[0].elements, context=context)

    def _get_attribute_ast_strs(self, depth):
        path_str = "Nothing" if self.path is None else '"{}"'.format(
            self.path)
        s = '{}path: {}\n'.format(_indent_token*(depth+1), path_str)
        s += super()._get_attribute_ast_strs(depth)
        return s

class Sequence(Elements):
    @classmethod
    def create_from_comma_separated_nodes(cls, context, nodes):
        elements = [nodes[0]]
        if len(nodes) > 2:
            if isinstance(nodes[2], Sequence):                
                elements.extend(nodes[2].elements)
            else:
                elements.append(nodes[2])
        return cls(elements, context=context)

    @classmethod
    def create_from_block_nodes(cls, context, nodes):
        return cls(nodes[1].elements, context=context)
