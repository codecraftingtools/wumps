# Copyright (C) 2018, 2020 Jeffrey A. Webb

"""
Wumps abstract syntax tree nodes.
"""

import pathlib

_indent_token = "  "

class Node:
    def __init__(self, src_info=None):
        self.src_info = src_info

    def _get_attribute_ast_strs(self, depth, show_src_info):
        return ""

    def get_ast_str(self, depth=0, first_depth=None, show_src_info=False):
        first_depth = depth if first_depth is None else first_depth
        s = "{}{}\n".format(_indent_token*first_depth, self.__class__.__name__)
        if show_src_info:
            indent = _indent_token*(depth+1)
            s += "{}[line: {}]\n".format(indent, self.src_info.line)
            s += "{}[column: {}]\n".format(indent, self.src_info.column)
        s += self._get_attribute_ast_strs(depth, show_src_info)
        return s

class Nothing(Node):
    def __init__(self, src_info=None):
        super().__init__(src_info=src_info)

class Operator(Node):
    def __init__(self, symbol, src_info=None):
        super().__init__(src_info=src_info)
        self.symbol = symbol

    def _get_attribute_ast_strs(self, depth, show_src_info):
        return '{}symbol: "{}"\n'.format(
            _indent_token*(depth+1), self.symbol)

class Identifier(Node):
    def __init__(self, text, src_info=None):
        super().__init__(src_info=src_info)
        self.text = text

    def _get_attribute_ast_strs(self, depth, show_src_info):
        escaped_text = self.text.replace('"','\\"')
        return '{}text: "{}"\n'.format(
            _indent_token*(depth+1), escaped_text)

class String(Node):
    def __init__(self, text, src_info=None):
        super().__init__(src_info=src_info)
        self.text = text

    def _get_attribute_ast_strs(self, depth, show_src_info):
        escaped_text = self.text.replace('"','\\"')
        escaped_text = escaped_text.replace('\n','\\n')
        return '{}text: "{}"\n'.format(
            _indent_token*(depth+1), escaped_text)

class Integer(Node):
    def __init__(self, value, src_info=None):
        super().__init__(src_info=src_info)
        self.value = value

    def _get_attribute_ast_strs(self, depth, show_src_info):
        return "{}value: {}\n".format(_indent_token*(depth+1), self.value)

class Float(Node):
    def __init__(self, value, src_info=None):
        super().__init__(src_info=src_info)
        self.value = value

    def _get_attribute_ast_strs(self, depth, show_src_info):
        return "{}value: {}\n".format(_indent_token*(depth+1), self.value)

class Named_Expression(Node):
    def __init__(self, name, expression, src_info=None):
        super().__init__(src_info=src_info)
        self.name = name
        self.expression = expression

    def _get_attribute_ast_strs(self, depth, show_src_info):
        s = "{}name: ".format(_indent_token*(depth+1))
        s += self.name.get_ast_str(depth+1, 0, show_src_info)
        s += "{}expression: ".format(_indent_token*(depth+1))
        s += self.expression.get_ast_str(depth+1, 0, show_src_info)
        return s

class Call(Node):
    def __init__(self, callee, arguments, src_info=None):
        super().__init__(src_info=src_info)
        self.callee = callee
        if not isinstance(arguments, Sequence):
            arguments = Sequence(arguments, src_info=src_info)
        self.arguments = arguments

    def _get_attribute_ast_strs(self, depth, show_src_info):
        s = "{}callee: ".format(_indent_token*(depth+1))
        s += self.callee.get_ast_str(depth+1, 0, show_src_info)
        s += "{}arguments: ".format(_indent_token*(depth+1))
        s += self.arguments.get_ast_str(depth+1, 0, show_src_info)
        return s

class Elements(Node):
    def __init__(self, elements=[], src_info=None):
        super().__init__(src_info=src_info)
        self.elements = tuple(elements)

    def _get_attribute_ast_strs(self, depth, show_src_info):
        s = "{}elements:\n".format(_indent_token*(depth+1))
        for a in self.elements:
            try:
                s += a.get_ast_str(depth+2, None, show_src_info)
            except:
                s += str(a)
        return s

class File(Elements):
    def __init__(self, elements, file_name=None, path_root=None,
                 src_info=None):
        super().__init__(elements, src_info=src_info)
        if file_name is None:
            self.path = self.src_info.file_name
        else:
            self.path = file_name
        if self.path is None:
            self.path_wrt_root = None
        elif path_root is None:
            self.path_wrt_root = pathlib.Path(self.path).name
        else:
            self.path_wrt_root = pathlib.Path(self.path).relative_to(
                path_root)

    def _get_attribute_ast_strs(self, depth, show_src_info):
        path_str = "Nothing" if self.path is None else '"{}"'.format(
            self.path)
        s = '{}path: {}\n'.format(_indent_token*(depth+1), path_str)
        path_wrt_root_str = "Nothing" if self.path_wrt_root is None else \
            '"{}"'.format(self.path_wrt_root)
        s += '{}path_wrt_root: {}\n'.format(_indent_token*(depth+1),
                                            path_wrt_root_str)
        s += super()._get_attribute_ast_strs(depth, show_src_info)
        return s

class Sequence(Elements):
    pass
