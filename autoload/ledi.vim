function! ledi#throw(msg) abort
  throw 'ledi: ' . a:msg
endfunction

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

