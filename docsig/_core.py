"""
docsig._core
============
"""
from __future__ import annotations

from itertools import zip_longest as _zip_longest
from pathlib import Path as _Path

from ._display import Display as _Display
from ._display import Failures as _Failures
from ._function import Function as _Function
from ._module import Modules as _Modules
from ._module import Parent as _Parent
from ._report import Report as _Report
from ._repr import FuncStr as _FuncStr
from ._utils import get_index as _get_index


def _compare_args(arg: str | None, doc: str | None, kind: str) -> bool:
    if kind in ("key", "keyword") and arg is not None:
        return arg[:2] == "**"

    if isinstance(arg, str):
        arg = arg.replace("*", "")

    return arg == doc and arg is not None and doc is not None


def _construct_func(
    func: _Function, report: _Report, no_ansi: bool = False
) -> _FuncStr:
    func_str = _FuncStr(func, no_ansi)
    for count, _ in enumerate(
        _zip_longest(func.signature.args, func.docstring.args)
    ):
        longest = max([len(func.signature.args), len(func.docstring.args)])
        arg = _get_index(count, func.signature.args)
        doc = func.docstring.args.get(count)
        if _compare_args(arg, doc.name, doc.kind):
            func_str.add_param(arg, doc.name, doc.kind)
        else:
            func_str.add_param(arg, doc.name, doc.kind, failed=True)
            report.order(arg, doc.name)
            report.incorrect(arg, doc.name)
            report.misspelled(arg, doc.name)
            report.not_equal(arg, doc.name)

        if count + 1 != longest:
            func_str.add_comma()

    func_str.set_mark()
    if func.docstring.returns and func.signature.returns:
        func_str.add_return()
    elif (
        func.docstring.returns
        and not func.signature.returns
        or func.signature.returns
        and not func.docstring.returns
    ):
        func_str.add_return(failed=True)

    func_str.close_sig(func.signature.return_value)
    func_str.close_docstring()
    func_str.render()
    return func_str


def _run_check(  # pylint: disable=too-many-arguments
    parent: _Parent,
    check_class: bool = False,
    check_dunders: bool = False,
    check_overridden: bool = False,
    check_protected: bool = False,
    no_ansi: bool = False,
    targets: list[str] | None = None,
    disable: list[str] | None = None,
) -> _Failures:
    failures = _Failures()
    for func in parent:
        if not (func.kind.isoverridden and not check_overridden) and (
            not (func.kind.isprotected and not check_protected)
            and not (func.kind.isinit and not check_class)
            and not (func.kind.isdunder and not check_dunders)
        ):
            report = _Report(func, targets, disable)
            report.missing_docstring()
            if func.docstring.string is not None:
                report.exists()
                report.missing()
                report.duplicates()
                report.extra_return()
                report.return_not_typed()
                report.missing_return()
                report.property_return()
                report.class_return()

            func_str = _construct_func(func, report, no_ansi)
            if report:
                failures.append((func_str, func.lineno, report))

    return failures


def docsig(
    *path: _Path,
    string: str | None = None,
    check_class: bool = False,
    check_dunders: bool = False,
    check_overridden: bool = False,
    check_protected: bool = False,
    no_ansi: bool = False,
    summary: bool = False,
    targets: list[str] | None = None,
    disable: list[str] | None = None,
) -> int:
    """Package's core functionality.

    Populate a sequence of module objects before iterating over their
    top-level functions and classes.

    If any of the functions within the module - and methods within its
    classes - fail, print the resulting function string representation
    and report.

    :param path: Path(s) to check.
    :param string: String to check.
    :param check_class: Check class docstrings.
    :param check_dunders: Check dunder methods
    :param check_overridden: Check overridden methods
    :param check_protected: Check protected functions and classes.
    :param no_ansi: Disable ANSI output.
    :param summary: Print a summarised report.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :return: Exit status for whether test failed or not.
    """
    modules = _Modules(*path, string=string)
    display = _Display(no_ansi)
    for module in modules:
        for top_level in module:
            if not top_level.isprotected or check_protected:
                failures = _run_check(
                    top_level,
                    check_class,
                    check_dunders,
                    check_overridden,
                    check_protected,
                    no_ansi,
                    targets,
                    disable,
                )
                if failures:
                    display[top_level.path].append(failures)

    if summary:
        display.summarise()
    else:
        display.report()

    return int(bool(display))
