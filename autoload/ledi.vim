function! ledi#define_variables(prefix, defaults) abort
  let prefix = empty(a:prefix) ? 'g:ledi' : 'g:ledi#' . a:prefix
  for [key, value] in items(a:defaults)
    let name = prefix . '#' . key
    if !exists(name)
      execute 'let ' . name . ' = ' . string(value)
    endif
    unlet value
  endfor
endfunction

function! ledi#complete() abort
  if pumvisible()
    return "\<C-n>"
  else
    return "\<C-x>\<C-o>\<C-p>\<CR>"
  endif
endfunction

call ledi#define_variables('', {
      \ 'force_py_version': has('python3') ? 3 : has('python') ? 2 : 0,
      \ 'enable_default_mappings': 1,
      \ 'enable_default_omnifunc': 1,
      \ 'enable_signature_indicator': 0,
      \})

