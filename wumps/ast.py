"""
Abstract syntax tree nodes.
"""

_indent_token = "  "

class Node:
    def __init__(self, context=None):
        self.file_name = context.file_name
        self.input_str = context.input_str
        self.start_position = context.start_position
        self.end_position = context.end_position

    def _get_attribute_ast_strs(self, depth):
        return ""

    def get_ast_str(self, depth=0, first_depth=None):
        first_depth = depth if first_depth is None else first_depth
        s = "{}{}\n".format(_indent_token*first_depth, self.__class__.__name__)
        s += self._get_attribute_ast_strs(depth)
        return s

class Nothing(Node):
    def __init__(self, context=None):
        super().__init__(context=context)

class Operator(Node):
    def __init__(self, symbol, context=None):
        super().__init__(context=context)
        self.symbol = symbol

    def _get_attribute_ast_strs(self, depth):
        return '{}symbol: "{}"\n'.format(
            _indent_token*(depth+1), self.symbol)

class Identifier(Node):
    def __init__(self, text, context=None):
        super().__init__(context=context)
        self.text = text

    def _get_attribute_ast_strs(self, depth):
        escaped_text = self.text.replace('"','\\"')
        return '{}text: "{}"\n'.format(
            _indent_token*(depth+1), escaped_text)

class String(Node):
    def __init__(self, text, context=None):
        super().__init__(context=context)
        self.text = text

    def _get_attribute_ast_strs(self, depth):
        escaped_text = self.text.replace('"','\\"')
        escaped_text = escaped_text.replace('\n','\\n')
        return '{}text: "{}"\n'.format(
            _indent_token*(depth+1), escaped_text)

class Integer(Node):
    def __init__(self, value, context=None):
        super().__init__(context=context)
        self.value = value

    def _get_attribute_ast_strs(self, depth):
        return "{}value: {}\n".format(_indent_token*(depth+1), self.value)

class Float(Node):
    def __init__(self, value, context=None):
        super().__init__(context=context)
        self.value = value

    def _get_attribute_ast_strs(self, depth):
        return "{}value: {}\n".format(_indent_token*(depth+1), self.value)

class Named_Expression(Node):
    def __init__(self, name, expression, context=None):
        super().__init__(context=context)
        self.name = name
        self.expression = expression

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
            arguments = Sequence(arguments, context=context)
        self.arguments = arguments

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

    def _get_attribute_ast_strs(self, depth):
        path_str = "Nothing" if self.path is None else '"{}"'.format(
            self.path)
        s = '{}path: {}\n'.format(_indent_token*(depth+1), path_str)
        s += super()._get_attribute_ast_strs(depth)
        return s

class Sequence(Elements):
    pass
