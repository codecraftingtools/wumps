_indent_token = "  "

class Identifier:
    def __init__(self, text, context=None):
        self._context = context
        if text.endswith(':'):
            text = text[:-1].rstrip()
        self._text = text

    @classmethod
    def create_from_node(cls, context, node):
        return cls(node, context=context)

    def tree_str(self, depth=0, first_depth=None):
        first_depth = depth if first_depth is None else first_depth
        s = "{}Identifier\n".format(_indent_token*first_depth)
        s += '{}text: "{}"\n'.format(_indent_token*(depth+1), self._text)
        return s

class Named_Expression:
    def __init__(self, name, expression, context=None):
        self._context = context
        self._name = name
        self._expression = expression

    @classmethod
    def create_from_nodes(cls, context, nodes):
        return cls(nodes[0], nodes[1], context=context)

    def tree_str(self, depth=0, first_depth=None):
        first_depth = depth if first_depth is None else first_depth
        s = "{}Named_Expression\n".format(_indent_token*first_depth)
        s += "{}name: ".format(_indent_token*(depth+1))
        s += self._name.tree_str(depth+1, first_depth=0)
        s += "{}expression: ".format(_indent_token*(depth+1))
        s += self._expression.tree_str(depth+1, first_depth=0)
        return s

class Call:
    def __init__(self, callee, arguments, context=None):
        self._context = context
        self._callee = callee
        if not isinstance(arguments, Sequence):
            arguments = Sequence(arguments)
        self._arguments = arguments

    @classmethod
    def create_from_nodes(cls, context, nodes):
        callee = nodes[0]
        arguments = []
        if len(nodes) > 1:
            if isinstance(nodes[1], Elements):                
                arguments.extend(nodes[1]._elements)
            elif isinstance(nodes[1], list):                
                arguments.extend(nodes[1])
            else:
                arguments.append(nodes[1])
        if len(nodes) > 2:
            arguments.extend(nodes[2])
        return cls(callee, arguments, context=context)

    def tree_str(self, depth=0, first_depth=None):
        first_depth = depth if first_depth is None else first_depth
        s = "{}Call\n".format(_indent_token*first_depth)
        s += "{}callee: ".format(_indent_token*(depth+1))
        s += self._callee.tree_str(depth=depth+1, first_depth=0)
        s += "{}arguments: ".format(_indent_token*(depth+1))
        s += self._arguments.tree_str(depth=depth+1, first_depth=0)
        return s

class Elements:
    def __init__(self, elements=[], context=None):
        self._context = context
        self._elements = tuple(elements)

    @classmethod
    def create_from_nodes(cls, context, nodes):
        elements = []
        if len(nodes) > 1:
            elements.extend(nodes[1])
        return cls(elements, context=context)

    def _tree_str_attributes(self, depth):
        return ""

    def tree_str(self, depth=0, first_depth=None):
        first_depth = depth if first_depth is None else first_depth
        s = "{}{}\n".format(_indent_token*first_depth, self.__class__.__name__)
        s += self._tree_str_attributes(depth)
        s += "{}elements:\n".format(_indent_token*(depth+1))
        for a in self._elements:
            try:
                s += a.tree_str(depth=depth+2)
            except:
                s += a
        return s

class File(Elements):
    def __init__(self, elements, context=None):
        super().__init__(elements, context=context)
        if context and hasattr(context, "file_name"):
            self._path = context.file_name
        else:
            self._path = None

    @classmethod
    def create_from_nodes(cls, context, nodes):
        return cls(nodes[0]._elements, context=context)

    def _tree_str_attributes(self, depth):
        path_str = "Nothing" if self._path is None else '"{}"'.format(
            self._path)
        return '{}path: {}\n'.format(_indent_token*(depth+1), path_str)

class Sequence(Elements):
    @classmethod
    def create_from_comma_separated_nodes(cls, context, nodes):
        elements = [nodes[0]]
        if len(nodes) > 2:
            if isinstance(nodes[2], Sequence):                
                elements.extend(nodes[2]._elements)
            else:
                elements.append(nodes[2])
        return cls(elements, context=context)

    @classmethod
    def create_from_block_nodes(cls, context, nodes):
        return cls(nodes[1]._elements, context=context)
