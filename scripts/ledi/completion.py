import vim
from . import signature
from .docstring import parse_docstring
from .util import (
    flatten,
    truncate,
    get_script,
)


def gather_candidates(base, include_signature=False):
    row, col = vim.current.window.cursor
    source = []
    for i, line in enumerate(vim.current.buffer):
        if i + 1 == row:
            source.append(line[:col] + base + line[col:])
        else:
            source.append(line)
    source = "\n".join(source)
    script = get_script(
        source,
        row,
        col+len(base),
    )
    completions = script.completions()
    menu_max_length = int(vim.eval('g:ledi#completion#menu_max_length'))
    type_indicators = vim.eval('g:ledi#completion#type_indicators')
    candidates = [
        parse_completion(base, c, menu_max_length, type_indicators)
        for c in completions
    ]
    if include_signature:
        signatures = [signature.parse_signature(s)
                      for s in script.call_signatures()]
    else:
        signatures = []
    return (candidates, signatures)


def parse_completion(base, c, menu_max_length, type_indicators):
    """Parse jedi.api.classes.Completion instance to a completion candidate"""
    head = c.description.split(':')[0]
    indicator = type_indicators.get(head, type_indicators.get('other', ''))

    docstring = c.docstring() or None
    if docstring:
        definitions, summaries = parse_docstring(docstring)
        menu = ' '.join(summaries)
        info = docstring
    else:
        menu = flatten(c.description.replace('%s:' % head, ''))
        info = c.description

    params = dict(
        word=c.name[:len(base)] + c.complete,
        abbr=c.name,
        menu='%s%s' % (indicator, truncate(menu, menu_max_length)),
        info=info,
        icase=1,
    )
    return params
