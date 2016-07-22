let s:Python = vital#ledi#import('Vim.Python')
let s:Path   = vital#ledi#import('System.Filepath')
let s:root   = expand('<sfile>:p:h:h:h')


function! ledi#python#init(...) abort
  let major_version = get(a:000, 0, s:Python.get_major_version())
  call s:Python.set_major_version(major_version)
  if !exists(printf('s:python%s_ready', major_version))
    let lib = s:Path.join([s:root, 'scripts'])
    let code = [
          \ 'import sys',
          \ printf('if "%s" not in sys.path:', lib),
          \ printf('  sys.path.insert(0, "%s")', lib),
          \ 'import ledi',
          \]
    execute s:Python.exec_code(code)
    execute printf('let s:python%s_ready = 1', major_version)
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


call ledi#python#init()
