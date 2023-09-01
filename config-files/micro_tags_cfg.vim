
" use help tags for more information
" use exuberant-ctags or universal-ctags(recommended)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" <./.PROJ_TAGS> means find <.PROJ_TAGS> file @current dir first 
" <;> means or upper dir recursive, until system root directory
" <,> sepeator or two paths
" <.PROJ_TAGS> find tags @current file dir
" find sequence from up to low

" do not use ; to recursive find, may get system halt
" cation: for set, "=" opertator can not has space between LHS/RHS
" set tags=./.PROJ_TAGS;,.PROJ_TAGS   
" set tags=<PROJ_ROOT>/.PROJ_TAGS
  set tags=~/git/tinyriscv/.PROJ_TAGS

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" put it to .cshrc, then ctags_gen alias command
" ctags -f .PROJ_TAGS -R $PROJ_ROOT
" ctags -f .PROJ_TAGS -R ./
" for bash example
"export PROJ_ROOT="~/git/tinyriscv"
"alias tags_gen="cd $PROJ_ROOT;ctags -f .PROJ_TAGS -R $PROJ_ROOT"
"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nmap <Leader>ft :call V_find_tags()<CR>
" or use CTRL-] key-sequence
function V_find_tags()
    " get word under cursor
    " echo $PROJ_ROOT
    let l:str_under_cursor = expand("<cword>")
    "echo l:str_under_cursor
    exec ":tag " . l:str_under_cursor
endfunction

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
