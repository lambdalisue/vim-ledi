function! ledi#completion#gather_candidates(base) abort
  return ledi#python#exec(
        \ 'ledi.completion.gather_candidates("%s")',
        \ a:base,
        \)
endfunction

function! ledi#completion#complete(findstart, base) abort
  if a:findstart
    let col  = col('.')
    let part = getline('.')[col : ]
    return col + strlen(substitute(part, '[^a-zA-Z0-9]*$', '', ''))
  else
    return ledi#completion#gather_candidates(a:base)
  endif
endfunction


call ledi#define_variables('completion', {
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
