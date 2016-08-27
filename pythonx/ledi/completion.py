import vim
from .util import (
    flatten,
    truncate,
    get_script,
    parse_docstring,
    handle_exceptions,
)


@handle_exceptions([])
def gather_candidates(base=''):
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
        parse_completion(c, menu_max_length, type_indicators)
        for c in completions
    ]
    return candidates


def parse_completion(completion, menu_max_length, type_indicators):
    type_ = completion.description.split(':')[0]
    indicator = type_indicators.get(type_, '')

    docstring = completion.docstring() or None
    if docstring:
        definitions, summaries = parse_docstring(docstring)
        menu = ' '.join(summaries)
        info = docstring
    else:
        menu = flatten(completion.description.replace('%s:' % type_, ''))
        info = completion.description

    params = dict(
        word=completion.complete,
        abbr=completion.name,
        menu='%s%s' % (indicator, truncate(menu, menu_max_length)),
        info=info,
        icase=1,
    )
    return params
