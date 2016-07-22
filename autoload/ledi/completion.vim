function! ledi#completion#gather_candidates(...) abort
  let options = extend({
        \ 'base': '',
        \ 'include_signatures': 0,
        \}, get(a:000, 0, {})
        \)
  return ledi#python#exec(
        \ 'ledi.completion.gather_candidates("%s", %s)',
        \ options.base,
        \ options.include_signature ? 'True' : 'False',
        \)
endfunction

function! ledi#completion#complete(findstart, base) abort
  if a:findstart
    let col  = col('.')
    let part = getline('.')[col : ]
    return col + strlen(substitute(part, '[^a-zA-Z0-9]*$', '', ''))
  else
    let [candidates, signatures] = ledi#completion#gather_candidates({
          \ 'base': a:base,
          \ 'include_signature': g:ledi#completion#show_signatures,
          \})
    if len(signatures)
      call ledi#signature#show(signatures)
    endif
    return candidates
  endif
endfunction


call ledi#define_variables('completion', {
      \ 'show_signatures': 1,
      \ 'menu_max_length': 80,
      \ 'type_indicators': {
      \    'class':    '[c] ',
      \    'instance': '[i] ',
      \    'function': '[f] ',
      \    'module':   '[m] ',
      \    'keyword':  '[k] ',
      \    'other':    '    ',
      \ },
      \})
