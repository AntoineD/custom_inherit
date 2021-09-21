"""This module handles sections with items."""

import inspect
import re
from collections import OrderedDict

try:
    from textwrap import indent
except ImportError:
    # for Python < 3.3
    def indent(text, padding):
        return "".join(padding + line for line in text.splitlines(True))

try:
    from inspect import getfullargspec
except ImportError:
    # for python 2.7
    from inspect import getargspec as getfullargspec


_RE_PATTERN_ITEMS = re.compile(r"(\**\w+)(.*?)(?:$|(?=\n\**\w+))", flags=re.DOTALL)

_STYLE_TO_PADDING = {
    "numpy": "",
    "google": " " * 4,
}

_ARGS_SECTION_NAMES = {
    "Parameters",
    "Other Parameters",
    "Args",
    "Arguments",
}

SECTION_NAMES = _ARGS_SECTION_NAMES | {
    "Attributes",
    "Methods",
    "Keyword Args",
    "Keyword Arguments",
}


def _render(body, style):
    """Render the items of a section.

    Parameters
    ----------
    body: OrderedDict[str, Optional[str]]
        The items of a section.
    style: str
        The doc style.

    Returns
    -------
    str
    """
    padding = _STYLE_TO_PADDING[style]
    section = []
    for key, value in body.items():
        section += [indent("{}{}".format(key, value), padding)]
    return "\n".join(section)


def set_defaults(doc_sections):
    """Set the defaults for the sections with items in place.

    Parameters
    ----------
    doc_sections: OrderedDict[str, Optional[str]]
    """
    for section_name in SECTION_NAMES:
        doc_sections[section_name] = OrderedDict()


def parse(doc_sections):
    """Parse the sections with items in place.

    Parameters
    ----------
    doc_sections: OrderedDict[str, Optional[str]]
    """
    for section_name in SECTION_NAMES:
        section_content = doc_sections[section_name]
        if section_content:
            # inspect.cleandoc indentation determination starts from the second line,
            # so we prepend an empty line.
            doc_sections[section_name] = OrderedDict(
                _RE_PATTERN_ITEMS.findall(inspect.cleandoc("\n"+section_content))
            )


def merge(child_func, section_name, prnt_sec, child_sec, merge_within_sections, style):
    """Merge the doc-sections of the parent's and child's attribute with items.

    Parameters
    ----------
    child_func: FunctionType
        The child function which doc is being merged.
    prnt_sec: OrderedDict[str, str]
    child_sec: OrderedDict[str, str]
    merge_within_sections: bool
        Wheter to merge the items.
    style: str
        The doc style.

    Returns
    -------
    OrderedDict[str, str]
        The merged items.
    """
    if merge_within_sections:
        body = prnt_sec.copy()
        body.update(child_sec)
    else:
        body = prnt_sec if not child_sec else child_sec

    if section_name in _ARGS_SECTION_NAMES:
        args, varargs, varkw, _, kwonlyargs = getfullargspec(child_func)[:5]

        if "self" in args:
            args.remove("self")

        if varargs is not None:
            args += ["*" + varargs]

        args += kwonlyargs

        if varkw is not None:
            args += ["**" + varkw]

        ordered_body = OrderedDict()
        for arg in args:
            if arg in body:
                ordered_body[arg] = body[arg]

        body = ordered_body

    body = _render(body, style)
    return body
