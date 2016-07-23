import sys
import itertools
import functools
import vim
import jedi


if sys.version_info.major >= 3:
    unicode = None


def to_vim(obj):
    if obj is None:
        return ''
    elif isinstance(obj, (int, float)):
        return obj
    elif isinstance(obj, bool):
        return int(obj)
    elif unicode and isinstance(obj, unicode):
        return to_vim(obj.encoding(vim.eval('&encoding') or 'latin1'))
    elif isinstance(obj, str):
        s = obj.replace('\\', '\\\\')
        s = s.replace('"', '\"')
        s = s.replace("'", "''")
        return '"%s"' % s
    elif isinstance(obj, (list, tuple)):
        return [to_vim(v) for v in obj]
    elif isinstance(obj, dict):
        return dict([
            [to_vim(k), to_vim(v)]
            for k, v in obj.items()
        ])
    else:
        raise NotImplementedError('Failed to convert %s to vim object' % obj)


def flatten(text):
    return ' '.join(map(lambda x: x.strip(), text.split("\n")))


def truncate(text, length=60):
    if len(text) > length:
        return text[:length-3] + '...'
    else:
        return text


def get_script(source=None, row=None, col=None):
    jedi.settings.additional_dynamic_modules = [
        b.name for b in vim.buffers if b.name and b.name.endswith('.py')
    ]
    if source is None:
        source = "\n".join(vim.current.buffer)
    if row is None:
        row = vim.current.window.cursor[0]
    if col is None:
        col = vim.current.window.cursor[1]
    return jedi.Script(
        source, row, col,
        path=vim.current.buffer.name,
        encoding=vim.eval('&encoding') or 'latin1',
    )


def parse_docstring(docstring):
    lines = map(lambda x: x.strip(), docstring.split("\n"))
    definitions = list(itertools.dropwhile(lambda x: x, lines))
    summaries = itertools.dropwhile(lambda x: not x, definitions)
    summaries = itertools.takewhile(lambda x: x, summaries)
    summaries = list(summaries)
    summaries = summaries if summaries else list(lines)
    return definitions, summaries


def handle_exceptions(default):
    def wrapper(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                if int(vim.eval('&verbose')) > 0:
                    vim.command('echohl ErrorMsg')
                    print(e)
                    vim.command('echohl None')
                return default
        return inner
    return wrapper
