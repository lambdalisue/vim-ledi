import vim
from .util import (
    truncate,
    get_script,
    parse_docstring,
    handle_exceptions,
)


@handle_exceptions([])
def gather_candidates():
    script = get_script()
    signatures = script.call_signatures()
    description_max_length = int(
        vim.eval('g:ledi#signature#description_max_length')
    )
    candidates = [
        parse_signature(s, description_max_length)
        for s in signatures
    ]
    return candidates


def parse_signature(signature, description_max_length):
    params = [p.description.replace("\n", ' ')
              for p in signature.params]
    definitions, summaries = parse_docstring(signature.docstring() or [])

    def join_params():
        return ', '.join(filter(lambda x: x, [
            params_ltext,
            params_ctext,
            params_rtext,
        ]))

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
    params_text = ', '.join(filter(lambda x: x, [
        params_ltext,
        params_ctext,
        params_rtext,
    ]))
    params = dict(
        index=-1 if signature.index is None else signature.index,
        call_name=signature.call_name,
        description=truncate(' '.join(summaries), description_max_length),
        params=params,
        params_text=params_text,
        params_ltext=params_ltext,
        params_ctext=params_ctext,
        params_rtext=params_rtext,
    )
    return params
