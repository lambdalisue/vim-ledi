function! ledi#signature#gather_candidates() abort
  return ledi#python#exec(
        \ 'ledi.signature.gather_candidates()',
        \)
endfunction

function! ledi#signature#show() abort
  let signatures = ledi#signature#gather_candidates()
  if empty(signatures)
    return
  endif
  let signature = signatures[0]
  echohl Function
  echon signature.call_name
  echohl None
  echon '('
  if signature.index == -1
    echohl lediSignatureParams
    echon signature.params_text
  else
    echohl lediSignatureParams
    echon signature.params_ltext
    echohl lediSignatureParamsBold
    echon signature.params_ctext
    echohl lediSignatureParams
    echon signature.params_rtext
  endif
  echohl None
  echon ') : '
  echon signature.description
endfunction

function! ledi#signature#enable() abort
  let s:enabled = 1
  augroup vim-ledi-signature-indicator
    autocmd! * <buffer>
    autocmd InsertEnter  <buffer> call ledi#signature#show()
    autocmd CursorMovedI <buffer> call ledi#signature#show()
    autocmd CompleteDone <buffer> call ledi#signature#show()
  augroup END
  redraw | echo ''
endfunction

function! ledi#signature#disable() abort
  let s:enabled = 0
  augroup vim-ledi-signature-indicator
    autocmd! * <buffer>
  augroup END
  redraw | echo ''
endfunction

function! ledi#signature#toggle() abort
  if get(s:, 'enabled', 0)
    call ledi#signature#disable()
    return 0
  else
    call ledi#signature#enable()
    return 1
  endif
endfunction


function! s:register_highlights() abort
  highlight default link lediSignatureParams     Comment
  highlight default link lediSignatureParamsBold String
endfunction

augroup vim-ledi-signature-syntax
  autocmd! *
  autocmd Syntax * call s:register_highlights()
augroup END

call s:register_highlights()
call ledi#define_variables('signature', {
      \ 'enable_on_startup': 1,
      \ 'description_max_length': 80,
      \})
