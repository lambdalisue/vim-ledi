from .docstring import parse_docstring
from .util import (
    flatten,
    truncate,
    get_script,
)


def gather_candidates():
    script = get_script()
    signatures = script.call_signatures()
    candidates = [parse_signature(s) for s in signatures]
    return candidates


def parse_signature(signature):
    params = [p.description.replace("\n", ' ') for p in signature.params]

    definitions, summaries = parse_docstring(signature.docstring() or [])

    if signature.index is not None:
        index = signature.index
        params_ltext = ', '.join(params[:index])
        params_ctext = params[index]
        params_rtext = ', '.join(params[index+1:])
        if params_rtext and params_ctext:
            params_ctext += ', '
        if params_ctext and params_ltext:
            params_ltext += ', '
    else:
        params_ltext = ''
        params_ctext = ''
        params_rtext = ', '.join(params)
    params_text = ', '.join(map(lambda x: x, [
        params_ltext,
        params_ctext,
        params_rtext,
    ]))
    params = dict(
        call_name=signature.call_name,
        description=truncate(' '.join(summaries), 100),
        params=params,
        params_text=params_text,
        params_ltext=params_ltext,
        params_ctext=params_ctext,
        params_rtext=params_rtext,
    )
    return params
