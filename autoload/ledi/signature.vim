let s:NUMBER_T = 0


function! ledi#signature#gather_candidates(...) abort
  let options = extend({
        \}, get(a:000, 0, {})
        \)
  return ledi#python#exec(
        \ 'ledi.signature.gather_candidates()',
        \)
endfunction

function! ledi#signature#show(...) abort
  let signatures = get(a:000, 0, 0)
  if type(signatures) == s:NUMBER_T
    unlet signatures
    let signatures = ledi#signature#gather_candidates()
  endif

  let signature = get(signatures, 0, {})
  if empty(signature)
    echo
    return
  endif

  echohl Function
  echon signature.call_name
  echohl None
  echon '('
  echohl lediSignatureParams
  echon signature.params_ltext
  echohl lediSignatureParamsBold
  echon signature.params_ctext
  echohl lediSignatureParams
  echon signature.params_rtext
  echohl None
  echon ') : '
  echon signature.description
endfunction

function! ledi#signature#enable_indicator() abort
  augroup vim-ledi-signature-indicator
    autocmd! *
    autocmd InsertEnter  * call ledi#signature#show()
    autocmd CursorMovedI * call ledi#signature#show()
    autocmd CompleteDone * call ledi#signature#show()
  augroup END
  redraw | echo ''
endfunction

function! ledi#signature#disable_indicator() abort
  augroup vim-ledi-signature-indicator
    autocmd! *
  augroup END
  redraw | echo ''
endfunction

function! s:register_highlights() abort
  highlight default link lediSignatureParams     Comment
  highlight default link lediSignatureParamsBold String
endfunction

call s:register_highlights()
