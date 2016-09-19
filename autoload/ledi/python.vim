let s:Python = vital#ledi#import('Vim.Python')
let s:Path   = vital#ledi#import('System.Filepath')
let s:root   = expand('<sfile>:p:h:h:h')
let s:status = {
      \ '2': '',
      \ '3': '',
      \}


function! ledi#python#init(...) abort
  let major_version = get(a:000, 0, s:Python.get_major_version())
  if get(s:status, major_version) !=# 'ready'
    let code = [
          \ 'try:',
          \ '  import jedi',
          \ '  import ledi',
          \ '  ledi_response = ""',
          \ 'except Exception as e:',
          \ '  ledi_response = str(e)',
          \]
    execute s:Python.exec_code(code, major_version)
    let response = s:Python.eval_expr('ledi_response')
    execute s:Python.exec_code('del ledi_response')
    if empty(response)
      let s:status[major_version] = 'ready'
      call s:Python.set_major_version(major_version)
    else
      let s:status[major_version] = 'failed'
      echohl ErrorMsg
      echomsg printf(
            \ 'ledi: %s - Failed to initialize ledi on Python %s',
            \ substitute(response, '^\%(\r\?\n\)\+\|\%(\r\?\n\)\+$', '', 'g'),
            \ major_version, 
            \)
      echohl None
    endif
  endif
endfunction


function! ledi#python#exec(code, ...) abort
  let code = type(a:code) == 3 ? join(a:code, "\n") : a:code
  let code = a:0 > 0 ? call('printf', [code] + a:000) : code
  let code = printf('ledi_response = %s', code)
  execute s:Python.exec_code(code)
  let response = s:Python.eval_expr('ledi_response')
  execute s:Python.exec_code('del ledi_response')
  return response
endfunction


function! ledi#python#status() abort
  let major_version = s:Python.get_major_version()
  return s:status[major_version]
endfunction


call ledi#python#init()
