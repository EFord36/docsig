"""
docsig._function
================
"""
from __future__ import annotations

import re as _re
import textwrap as _textwrap
import typing as _t
from collections import Counter as _Counter

import astroid as _ast
import sphinxcontrib.napoleon as _s

from ._objects import MutableSequence as _MutableSequence
from ._utils import isprotected as _isprotected


class _GoogleDocstring(str):
    def __new__(cls, string: str) -> _GoogleDocstring:
        return super().__new__(cls, str(_s.GoogleDocstring(string)))


class _NumpyDocstring(str):
    def __new__(cls, string: str) -> _NumpyDocstring:
        return super().__new__(cls, str(_s.NumpyDocstring(string)))


class _DocFmt(str):
    def __new__(cls, string: str) -> _DocFmt:
        return super().__new__(
            cls,
            _textwrap.dedent("\n".join(string.splitlines()[1:])).replace(
                "*", ""
            ),
        )


class _RawDocstring(str):
    def __new__(cls, string: str) -> _RawDocstring:
        return super().__new__(
            cls, _NumpyDocstring(_GoogleDocstring(_DocFmt(string)))
        )


class Param(_t.NamedTuple):
    """A tuple of param types and their names."""

    kind: str = "param"
    name: str | None = None
    description: str | None = None
    indent: int = 0


class _Matches(_MutableSequence[Param]):
    _pattern = _re.compile(":(.*?):")

    def __init__(self, string: str) -> None:
        super().__init__()
        for line in string.splitlines():
            strip_line = line.lstrip()
            indent = len(line) - len(strip_line)
            match = self._pattern.split(strip_line)[1:]
            if match:
                name = description = None
                kinds = match[0].split()
                if kinds:
                    if len(kinds) > 1:
                        name = kinds[1]

                    if len(match) > 1:
                        description = match[1]

                    super().append(Param(kinds[0], name, description, indent))


class _Params(_MutableSequence[Param]):

    _param = "param"
    _keys = ("key", "keyword")
    _kwarg_value = "(**)"

    def insert(self, index: int, value: Param) -> None:
        if value.kind == self._param:
            super().insert(index, value)

        elif value.kind in self._keys and not any(
            i in y for y in self for i in self._keys
        ):
            super().insert(
                index, Param(value.kind, self._kwarg_value, value.description)
            )

    def get(self, index: int) -> Param:
        """Get a param.

        If the index does not exist return a `Param` with None as
        `Param.name`.

        :param index: Index of param to get.
        :return: Param belonging to the index.
        """
        try:
            return self[index]
        except IndexError:
            return Param()

    @property
    def duplicated(self) -> bool:
        """Boolean value for whether there are duplicate parameters."""
        return any(k for k, v in _Counter(self).items() if v > 1)


class _Signature:
    def __init__(
        self,
        arguments: _ast.Arguments,
        returns: _ast.Module,
        ismethod: bool = False,
        isstaticmethod: bool = False,
    ) -> None:
        self._arguments = arguments
        self._args = _Params(
            Param(name=a.name)
            for a in self._arguments.args
            if not _isprotected(a.name)
        )
        self._return_value = self._get_returns(returns)
        self._returns = (
            self._return_value is not None and self._return_value != "None"
        )
        self._get_args_kwargs()
        if ismethod and not isstaticmethod and self._args:
            self._args.pop(0)

    def _get_args_kwargs(self) -> None:
        vararg = self._arguments.vararg
        if vararg is not None and not _isprotected(vararg):
            self._args.append(Param(name=f"*{vararg}"))

        if self._arguments.kwonlyargs:
            self._args.extend(
                Param(name=k.name) for k in self._arguments.kwonlyargs
            )

        kwarg = self._arguments.kwarg
        if kwarg is not None and not _isprotected(kwarg):
            self._args.append(Param(name=f"**{kwarg}"))

    def _get_returns(self, returns: _ast.NodeNG | None) -> str | None:
        if isinstance(returns, _ast.Name):
            return returns.name

        if isinstance(returns, _ast.Attribute):
            return returns.attrname

        if isinstance(returns, _ast.Const):
            return str(returns.kind)

        if isinstance(returns, _ast.Subscript):
            return "{}[{}]".format(
                self._get_returns(returns.value),
                self._get_returns(returns.slice),
            )

        if isinstance(returns, _ast.BinOp):
            return "{} | {}".format(
                self._get_returns(returns.left),
                self._get_returns(returns.right),
            )

        return None

    @property
    def args(self) -> _Params:
        """Tuple of signature parameters."""
        return self._args

    @property
    def return_value(self) -> str | None:
        """Function's return value.

        If a function is typed to return None, return str(None). If no
        typehint exists then return None (NoneType).
        """
        return self._return_value

    @property
    def returns(self) -> bool:
        """Check that a function returns a value."""
        return self._returns


class _Docstring:
    def __init__(self, node: _ast.Const | None = None) -> None:
        self._string = None
        self._args = _Params()
        if node is not None:
            self._string = _RawDocstring(node.value)
            matches = _Matches(self._string)
            self._args.extend(matches)

    @property
    def string(self) -> _RawDocstring | None:
        """The raw documentation string, if it exists, else None."""
        return self._string

    @property
    def args(self) -> _Params:
        """Docstring args."""
        return self._args

    @property
    def returns(self) -> bool:
        """Check that docstring return is documented."""
        return (
            False
            if self._string is None
            else any(i in self._string for i in (":return:", ":returns:"))
        )


class Function:
    """Represents a function with signature and docstring parameters.

    :param node: Function's abstract syntax tree.
    """

    def __init__(self, node: _ast.FunctionDef) -> None:
        self._name = node.name
        self._parent = node.parent.frame()
        self._parent_name = self._parent.name
        self._lineno = node.lineno or 0
        self._decorators = node.decorators
        doc_node = node.doc_node
        if self.isinit:
            doc_node = self._parent.doc_node

        self._signature = _Signature(
            node.args, node.returns, self.ismethod, self.isstaticmethod
        )
        self._docstring = _Docstring(doc_node)

    def __len__(self) -> int:
        """Length of the longest sequence of args."""
        return max([len(self.signature.args), len(self.docstring.args)])

    def _by_decorated(self, name: str) -> bool:
        decorators = self._decorators
        if decorators is not None:
            for dec in decorators.nodes:
                if isinstance(dec, _ast.Name) and dec.name == name:
                    return True

        return False

    @property
    def ismethod(self) -> bool:
        """Boolean value for whether function is a method."""
        return isinstance(self._parent, _ast.ClassDef)

    @property
    def isproperty(self) -> bool:
        """Boolean value for whether function is a property."""
        return self.ismethod and self._by_decorated("property")

    @property
    def isinit(self) -> bool:
        """Boolean value for whether function is a class constructor."""
        return self.ismethod and self.name == "__init__"

    @property
    def isoverridden(self) -> bool:
        """Boolean value for whether function is overridden."""
        if self.ismethod and not self.isinit:
            for ancestor in self._parent.ancestors():
                if self.name in ancestor and isinstance(
                    ancestor[self.name], _ast.nodes.FunctionDef
                ):
                    return True

        return False

    @property
    def isprotected(self) -> bool:
        """Boolean value for whether function is protected."""
        return (
            _isprotected(self.name) and not self.isinit and not self.isdunder
        )

    @property
    def isstaticmethod(self) -> bool:
        """Boolean value for whether function is a static method."""
        return self.ismethod and self._by_decorated("staticmethod")

    @property
    def isdunder(self) -> bool:
        """Boolean value for whether function is a dunder method."""
        return (
            self.ismethod
            and not self.isinit
            and self.name[:2] + self.name[-2:] == "____"
        )

    @property
    def name(self) -> str:
        """The name of the function."""
        return self._name

    @property
    def parent_name(self) -> str:
        """The name of the function's parent."""
        return self._parent_name

    @property
    def lineno(self) -> int:
        """Line number of function declaration."""
        return self._lineno

    @property
    def signature(self) -> _Signature:
        """The function's signature parameters."""
        return self._signature

    @property
    def docstring(self) -> _Docstring:
        """The function's docstring."""
        return self._docstring
