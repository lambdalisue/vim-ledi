nnoremap <silent><buffer> <Plug>(ledi-signature-show)
      \ :<C-u>call ledi#signature#show()<CR>

if g:ledi#enable_default_mappings
  nmap <buffer> <C-g> <Plug>(ledi-signature-show)
endif

if g:ledi#enable_default_omnifunc
  setlocal omnifunc=ledi#completion#complete
endif

if g:ledi#signature#enable_on_startup
  call ledi#signature#enable()
endif
