import sys
import vim
import jedi


PY_VERSION = sys.version_info[0]
VIM_ENCODING = vim.eval('&encoding') or 'latin1'


def to_vim(obj):
    if obj is None:
        return ''
    elif isinstance(obj, (int, float)):
        return obj
    elif isinstance(obj, bool):
        return int(obj)
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
        encoding=VIM_ENCODING,
    )
