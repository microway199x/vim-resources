
" Only do this when not done yet for this buffer
if exists("b:loaded_hdl") 
    finish 
endif


if v:version <700
    echoerr "HDL:this plugin requires version > 700"
    finish
endif

" Don't load another plugin for this buffer
let b:loaded_hdl = 1

" Save the compatibility options and temporarily switch to vim defaults
let s:cpo_save = &cpoptions
set cpoptions&vim

" init options
function! s:InitVar(var,value)
    echo a:value
    if !exists(a:var)
        exec 'let' . ' ' . a:var . '=' . "'" . a:value . "'"
	return 1
    endif
    return 0
endfunction

call s:InitVar('g:IrunOption',' ')
call s:InitVar('g:SlintOption',' ')

" get module 
function! s:Getmodule()
    for line in getline(1,line('$'))
        if line =~# '^\s*module\s\+\w+'
	    let l:module = matchlist(line,'\s*module\s\+\(\w+\)')[1]
            return l:module
	endif
    endfor
endfunction

function! s:RunIrun(...)
    " get command input filelist 
    let l:filelist=join(a:000,' ')
    " get current file module name 
    let l:module = s:Getmodule()
    if empty(l:module)
        echohl ErrorMSG | Echo “no module specified” | echohl None
	return 
    endif
    exec 'cclose'
    exec 'compiling..
    "set compiler, correspond to compiler/ncverilog.vim
    exec 'compiler ncverilog'
    " execute compiling
    silent execute 'make' . g:IrunOption . ' ' . l:filelist . ' ' . expand(%) . '-top' . l:module
    let l:ret=system('rm ./INCA_libs -rf')
    exec 'copen'
endfunction

au BufRead,BufNewFile *.v,*.sv command! -complete=file -nargs=* IRUN call S:RunIrun(<f-args>)

let &cpoptions = s:cpo_save
unlet s:cpo_save
