"""
tests
=====

Test package for ``docsig``.
"""
# pylint: disable=too-many-lines
import typing as t
from pathlib import Path

from templatest import BaseTemplate as _BaseTemplate
from templatest import templates as _templates

from docsig import messages

MockMainType = t.Callable[..., int]
InitFileFixtureType = t.Callable[[str], Path]

CHECK = "\u2713"
CROSS = "\u2716"

MULTI = "multi"
NAME = "name"
TEMPLATE = "template"
ERR_GROUP = "f-e-1-0"
FUNC = "func"
E10 = "e-1-0"
CHECK_CLASS = "--check-class"
CHECK_PROTECTED = "--check-protected"
FAIL_PROTECT = "f-protect"
CHECK_OVERRIDDEN = "--check-overridden"
FAIL_OVERRIDE = "f-override"
CHECK_DUNDERS = "--check-dunders"
FAIL = "f"


@_templates.register
class _PassParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :param param3: Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FParamDocsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2) -> None:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"
"""


@_templates.register
class _FParamSigS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _FNoDocNoRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    pass
"""

    @property
    def expected(self) -> str:
        return messages.H104


@_templates.register
class _PassNoParamsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function() -> None:
    \"\"\"No params.\"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassUnderscoreParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, _) -> None:
    \"\"\"Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FOutOfOrderS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CROSS}param1, {CROSS}param2, {CROSS}param3)?:
    \"\"\"...

    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"
"""


@_templates.register
class _PassRetTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :param param3: Passes.
    :return: Passes.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CHECK}param3) -> {CROSS}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FRetTypeSigS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CHECK}param3) -> {CROSS}int:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE109NoRetNoTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :param param3: Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E109


@_templates.register
class _FNoRetDocsNoTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3):
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CHECK}param3)?:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FRetDocsAttrTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
import typing as t

def function(param1) -> t.Optional[str]:
    \"\"\"Proper docstring.

    :param param1: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1) -> {CROSS}Optional[str]:
    \"\"\"...

    :param param1: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FRetDocsNameTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
from typing import Optional

def function(param1) -> Optional[str]:
    \"\"\"Proper docstring.

    :param param1: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1) -> {CROSS}Optional[str]:
    \"\"\"...

    :param param1: {CHECK}
    :return: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE101OutOfOrder1SumS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return messages.E101


@_templates.register
class _FIncorrectDocS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1) -> None:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CROSS}None) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE102ParamDocs1SumS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2) -> None:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E102


@_templates.register
class _FE103ParamSig1SumS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E103


@_templates.register
class _FE104RetTypeDocs1SumS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E104


@_templates.register
class _FE105RetTypeSig1SumS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> int:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return messages.E105


@_templates.register
class _FDupesSumS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E106


@_templates.register
class _FIncorrectDocSumS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E107


@_templates.register
class _PassWithArgsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, *args) -> None:
    \"\"\"Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    :param args: Pass
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWithArgsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, *args) -> None:
    \"\"\"Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CROSS}*args) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _PassWithKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, **kwargs) -> None:
    \"\"\"Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    :param kwargs: Pass
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWithKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, **kwargs) -> None:
    \"\"\"Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function({CHECK}param1, {CHECK}param2, {CROSS}**kwargs) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _MultiFailS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function_1(param1, param2, param3) -> None:
    \"\"\"Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    \"\"\"
    return 0
    
def function_2(param1, param2) -> None:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
    
def function_3(param1, param2, param3) -> None:
    \"\"\"Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def function_1({CROSS}param1, {CROSS}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"...

    :param param2: {CROSS}
    :param param3: {CROSS}
    :param param1: {CROSS}
    \"\"\"

{messages.E101}


def function_2({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

{messages.E102}


def function_3({CHECK}param1, {CHECK}param2, {CROSS}param3) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"

{messages.E103}
"""


@_templates.register
class _FClassS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        \"\"\"Proper docstring.

        :param param1: Pass.
        :param param2: Pass.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def method({CHECK}param1, {CHECK}param2, {CROSS}**kwargs) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _PassClassSelfS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    def method(self, param1) -> None:
        \"\"\"Proper docstring.

        :param param1: Pass.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassClassPropertyS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    @property
    def method(self) -> int:
        \"\"\"Proper docstring.\"\"\"
        return self._method
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassWithKwargsKeyS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    :param param1: Passes
    :key kwarg1: Pass
    :keyword kwarg2: Pass
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWithKwargsOutOfOrderS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, **kwargs) -> None:
    \"\"\"Proper docstring.

    :keyword kwarg1: Fail
    :keyword kwarg3: Fail
    :param param1: Fail
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassDualColonS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(attachments, sync, **kwargs) -> None:
    \"\"\"Proper docstring.

    Note: Keyword args (dict) to pass to ``attachments``:

        See ``flask_mail.Message.attach``.

        * filename:     filename of attachment
        * content_type: file mimetype
        * data:         the raw file data

    :param attachments: Iterable of kwargs to construct attachment.
    :param sync: Don't thread if True: Defaults to False.
    :param kwargs: Keyword args to pass to ``Message``:
        See ``flask_mail.Message``.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassOnlyParamsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(reduce: bool = False) -> _t.Tuple[str, ...]:
    \"\"\"Proper docstring.

    :param reduce: :func:`~lsfiles.utils._Tree.reduce`
    :return: Tuple of `Path` objects or str repr.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassReturnAnyS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    \"\"\"Proper docstring.

    :param args: Manipulate string(s).
    :key format: Return a string instead of a tuple if strings are
        passed as tuple.
    :return: Colored string or None.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FMsgPoorIndentS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_post(
        id: int, version: t.Optional[int] = None, checkauthor: bool = True
) -> Post:
    \"\"\"Get post by post's ID or abort with ``404: Not Found.``

    Standard behaviour would be to return None, so do not bypass
     silently.

     :param id: The post's ID.
     :param version: If provided populate session object with
        version.
     :param checkauthor: Rule whether to check for author ID.
     :return: Post's connection object.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.H101


@_templates.register
class _FE103NoSpaceS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1) -> None:
    \"\"\"Proper docstring.

    :param param1:Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E103


@_templates.register
class _PassBinOpS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_index(index: int, seq: _t.Sequence[_T]) -> _T | None:
    \"\"\"Fet index without throwing an error if index does not exist.

    :param index: Index to get.
    :param seq: Sequence object that can be indexed.
    :return: Item from index else None.
    \"\"\"
    try:
        return seq[index]
    except IndexError:
        return None
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FBinOpReprS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_index(index: int) -> _T | None:
    \"\"\"Get index without throwing an error if index does not exist.

    :return: Item from index else None.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""
def get_index({CROSS}index) -> {CHECK}_T | None:
    \"\"\"...

    :param None: {CROSS}
    :return: {CHECK}
    \"\"\"
"""


@_templates.register
class _PassDoubleUnderscoreParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, __) -> None:
    \"\"\"Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassUnderscoreArgsKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(*_, **__) -> None:
    \"\"\"Proper docstring.\"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassPropertyNoReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    @property
    def function(*_, **__) -> int:
        \"\"\"Proper docstring.\"\"\"
        return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FPropertyReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    @property
    def function(*_, **__) -> int:
        \"\"\"Proper docstring.
        
        :return: Returncode.
        \"\"\"
        return 0
"""

    @property
    def expected(self) -> str:
        return messages.E108


@_templates.register
class _FHintMissingReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def get_post() -> Post:
    \"\"\"Proper docstring.

     return: Post's connection object.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.H103


@_templates.register
class _FOverrideS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
import typing as _t

T = _t.TypeVar("T")


class MutableSet(_t.MutableSet[T]):
    \"\"\"Set objet to inherit from.\"\"\"

    def __init__(self) -> None:
        self._set: _t.Set[T] = set()

    def add(self, value: T) -> None:
        self._set.add(value)

    def discard(self, value: T) -> None:
        self._set.discard(value)

    def __contains__(self, x: object) -> bool:
        return self._set.__contains__(x)

    def __len__(self) -> int:
        return self._set.__len__()

    def __iter__(self) -> _t.Iterator[T]:
        return self._set.__iter__()
"""

    @property
    def expected(self) -> str:
        return messages.E103


@_templates.register
class _FNoDocRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function() -> int:
    pass
"""

    @property
    def expected(self) -> str:
        return messages.H104


@_templates.register
class _PassInconsistentSpaceS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@pytest.fixture(name="main")
def fixture_main(monkeypatch) -> t.Callable[..., None]:
    \"\"\"Function for passing mock ``main`` commandline arguments
    to package's main function.

    :param monkeypatch: ``pytest`` fixture for mocking attributes.
    :return:            Function for using this fixture.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FE109WRetQuestionS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function():
    \"\"\"Docstring.
    
    :return: Does it?
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E109


@_templates.register
class _FE109WORetQuestionS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function():
    \"\"\"Docstring.\"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E109


@_templates.register
class _FE110NES(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(arg, param2) -> None:
    \"\"\"Docstring.
    
    :param param1: not equal.
    :param para2: not equal.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E110


@_templates.register
class _FClassHeaderS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    def method(param1, param2, **kwargs) -> None:
        \"\"\"Proper docstring.

        :param param1: Pass.
        :param param2: Pass.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return "module/file.py::Klass::4"


@_templates.register
class _PassKWOnlyArgsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def docsig(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    \"\"\"...

    :param path: Path(s) to check.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :return: Boolean value for whether there were any failures or not.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return """"""


@_templates.register
class _FInitS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
    
    def __init__(self, param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return f"""\
class Klass:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"

    def __init__({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
"""


@_templates.register
class _PassPropNoRetTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:
    @property
    def method(self):
        \"\"\"Proper docstring.\"\"\"
        return self._method
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassInitNoRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"

    def __init__(self, param1, param2):
        pass
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassInitBadRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    \"\"\"

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        pass
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FInitRetNoneS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :return: Fails
    \"\"\"

    def __init__(self, param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return f"""
class Klass:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :return: {CROSS}
    \"\"\"

    def __init__({CHECK}param1, {CHECK}param2) -> {CROSS}None:
"""


@_templates.register
class _FE111S(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :return: Fails
    \"\"\"

    def __init__(param1, param2) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return messages.E111


@_templates.register
class _FProtectFuncS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def _function(param1, param2) -> None:
    \"\"\"...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def _function({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"
"""


@_templates.register
class _FFuncPropS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def function(self) -> int:
    \"\"\"Docstring.
    
    :param self: Fails.
    \"\"\"
    return self._method
"""

    @property
    def expected(self) -> str:
        return messages.E105


@_templates.register
class _PassFuncPropReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def function(*_, **__) -> int:
    \"\"\"Docstring.

    :return: Returncode.
    \"\"\"
    return 0
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncPropNoRetTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
@property
def method(self):
    \"\"\"Docstring.
    
    :param self: Fails.
    \"\"\"
    return self._method
"""

    @property
    def expected(self) -> str:
        return messages.E109


@_templates.register
class _FProtectNInitS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def __init__(param1, param2) -> None:
    pass
"""

    @property
    def expected(self) -> str:
        return messages.E103


@_templates.register
class _PassStaticSelfS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
    class Klass:
        @staticmethod
        def method(self, param1) -> None:
            \"\"\"Proper docstring.

            :param self: Pass.
            :param param1: Pass.
            \"\"\"
    """

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PassClassNoSelfS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class Klass:

    # against convention but not up to this package to decide
    def method(no_self) -> None:
        \"\"\"Docstring.\"\"\"
        return None
"""

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FProtectClsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """

class _Klass:
    def method(self, param1, param2, **kwargs) -> None:
        \"\"\"Proper docstring.

        :param param1: Pass.
        :param param2: Pass.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def method({CHECK}param1, {CHECK}param2, {CROSS}**kwargs) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param None: {CROSS}
    \"\"\"
"""


@_templates.register
class _FDunderS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class MutableSet:
    \"\"\"Set objet to inherit from.\"\"\"

    def __init__(self) -> None:
        self._set: _t.Set[T] = set()

    def __contains__(self, x: object) -> bool:
        return self._set.__contains__(x)

    def __len__(self) -> int:
        return self._set.__len__()

    def __iter__(self) -> _t.Iterator[T]:
        return self._set.__iter__()
"""

    @property
    def expected(self) -> str:
        return messages.E103


@_templates.register
class _FDunderParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:
    def __dunder__(self, param1, param2) -> None:
        \"\"\"...

        :param param1: Fails.
        :param param2: Fails.
        :param param3: Fails.
        \"\"\"
"""

    @property
    def expected(self) -> str:
        return f"""\
def __dunder__({CHECK}param1, {CHECK}param2, {CROSS}None) -> {CHECK}None:
    \"\"\"...

    :param param1: {CHECK}
    :param param2: {CHECK}
    :param param3: {CROSS}
    \"\"\"
"""


@_templates.register
class _FE112S(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param) -> None:
    \"\"\"Docstring.

    :param pram: Misspelled.
    \"\"\"
"""

    @property
    def expected(self) -> str:
        return messages.E112
