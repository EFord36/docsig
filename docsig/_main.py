"""
docsig._main
============

Contains package entry point.
"""
from ._config import Parser as _Parser
from ._core import docsig as _docsig
from ._core import pretty_print_error as _pretty_print_error


def main() -> int:
    """Main function for package.

    Collect config and arguments for the commandline.

    :return: Exit status for whether test failed or not.
    """
    parser = _Parser()
    _pretty_print_error()
    return _docsig(
        *parser.args.path,
        string=parser.args.string,
        check_class=parser.args.check_class,
        check_dunders=parser.args.check_dunders,
        check_overridden=parser.args.check_overridden,
        check_protected=parser.args.check_protected,
        check_property_returns=parser.args.check_property_returns,
        ignore_no_params=parser.args.ignore_no_params,
        ignore_args=parser.args.ignore_args,
        ignore_kwargs=parser.args.ignore_kwargs,
        no_ansi=parser.args.no_ansi,
        summary=parser.args.summary,
        targets=parser.args.target,
        disable=parser.args.disable
    )
