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
        s += "{}text: {}\n".format(_indent_token*(depth+1), self._text)
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
        self._arguments = arguments

    @classmethod
    def create_from_nodes(cls, context, nodes):
        callee = nodes[0]
        arguments = []
        if len(nodes) > 1:
            if isinstance(nodes[1], Expressions):                
                arguments.extend(nodes[1]._expressions)
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
        s += "{}arguments:\n".format(_indent_token*(depth+1))
        for a in self._arguments:
            try:
                s += a.tree_str(depth=depth+2)
            except:
                s += a
        return s

class Expressions:
    def __init__(self, expressions=[], context=None):
        self._context = context
        self._expressions = tuple(expressions)

    @classmethod
    def create_from_nodes(cls, context, nodes):
        expressions = []
        if len(nodes) > 1:
            expressions.extend(nodes[1])
        return cls(expressions, context=context)

    def _tree_str_attributes(self, depth):
        return ""

    def tree_str(self, depth=0, first_depth=None):
        first_depth = depth if first_depth is None else first_depth
        s = "{}{}\n".format(_indent_token*first_depth, self.__class__.__name__)
        s += self._tree_str_attributes(depth)
        s += "{}expressions:\n".format(_indent_token*(depth+1))
        for a in self._expressions:
            try:
                s += a.tree_str(depth=depth+2)
            except:
                s += a
        return s

class File(Expressions):
    def __init__(self, expressions, context=None):
        super().__init__(expressions, context=context)
        if context and hasattr(context, "file_name"):
            self._path = context.file_name
        else:
            self._path = "<None>"

    @classmethod
    def create_from_nodes(cls, context, nodes):
        return cls(nodes[0]._expressions, context=context)

    def _tree_str_attributes(self, depth):
        return "{}path: {}\n".format(_indent_token*(depth+1), self._path)

class Sequence(Expressions):
    @classmethod
    def create_from_comma_separated_nodes(cls, context, nodes):
        expressions = [nodes[0]]
        if len(nodes) > 2:
            if isinstance(nodes[2], Sequence):                
                expressions.extend(nodes[2]._expressions)
            else:
                expressions.append(nodes[2])
        return cls(expressions, context=context)

    @classmethod
    def create_from_block_nodes(cls, context, nodes):
        return cls(nodes[1]._expressions, context=context)
