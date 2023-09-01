""map <leader>m ^hhR//
map <leader>m  :call Commented()<cr>
map <leader>u  :call UnCommented()<cr>
function Commented()
   exe "normal ^"
   let cur_pos     = getcurpos()
   let cur_column  = cur_pos[2] 
   if cur_column == 1
     exe "normal i//"
   elseif cur_column ==2
     exe "normal hxi//"
   elseif cur_column >2
     exe "normal hhR//"
   endif
endf

function UnCommented()
    exe "normal ^R  "
endf

""mapÖ´ÐÐshellÃüÁî
"map <leader>c :silent !start cmd.exe /C echo HAHAHA &pause 

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Quickly Run
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

map <Leader>mc :call CompileRunGcc()<CR>

func! CompileRunGcc()
    exec "w!" 
    if &filetype == 'c' 
        exec '!g++ % -o %<'
        exec '!time ./%<'
    elseif &filetype == 'cpp'
        exec '!g++ % -o %<'
        exec '!time ./%<'
    elseif &filetype == 'python'
        "exec '!time python %'
         exec '!python %'
    elseif &filetype == 'sh'
        :!time bash %
    endif                                                                              
endfunc 

source $VIMRUNTIME/macros/matchit.vim 
runtime! macros/matchit.vim 
"if not work well,use autocmd BufNweFile,BufRead *   let b:match_wrods 
let b:match_words='\<begin\>:\<end\>' .
                \ '\<module\>:\<endmodule\>' .
                \ '\<case\>:\<endcase\>' "can added any pairs like this 

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Quickly replace
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
map <Leader>mr :call V_quick_replace()<CR>

func! V_quick_replace()
    let old_word = expand("<cword>")
    let new_word = input("replace " . old_word .  " by:")
    let range_r = input("replace @all file? if yes, input /gg/:")
    if(range_r =~ ".*gg.*")
        let replace_range = "normal " . range_r
        exec replace_range
    endif
    let cur_pos   = getcurpos()
    let cur_line  = cur_pos[1] 
   "let replace_cmd = printf('%%s/%s/%s/gc',old_word,new_word)
    let replace_cmd = cur_line . ",$" . "s/" . "\\<" . old_word . "\\>" . "/" . new_word . "/gc"
    exec replace_cmd
  " do the command like : normal gg | 1,$s/old/new/gc
endfunc 


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" Veriolg add increase or decrease sequence 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

nmap <Leader>vs :Vseq
"command -range=% -nargs=+ Vseq :call V_seq(<f-args>) 
" <f-args>会自动转换格式为函数需要的格式
":Vseq xxx<seq>yyy<seq> 0 16 2 此处不建议，因为插入序列中肯定有空格，空格认为是参数分割符
"command -range=% -nargs=+ Vseq :call V_seq(<q-args>) 
":Vseq 'xxx<seq>yyy<seq>',0,16,2
":Vseq 'xxx<seq>yyy<seq>',0,16,-2
command -range=% -nargs=1 Vseq :call V_seq(<args>) 

function! V_seq(seq_str,start,num,step)
    let seq_str = a:seq_str
    
    let num     = str2nr(a:num)  
    let step    = str2nr(a:step)
    if(a:start =~ '[a-zA-Z]')
        let is_char_seq = 1
    else
        let is_char_seq = 0
    endif
    if(is_char_seq == 1)
       let start = char2nr(a:start)
    else
       let start = str2nr(a:start)
    endif
       
    let end_num = start + num *step
    let str_start = printf("%d",start)
    let str_end = printf("%d",end_num)
    let str_len_s = strlen(str_start)
    let str_len_e = strlen(str_end)
    if(is_char_seq == 1)
        let str_len = 1
    else
        if(str_len_s > str_len_e)
            let str_len = str_len_s
        else
            let str_len = str_len_e
        endif
    endif
    
    let line_out = ''

    for i_s in range(num)
        let num_str = ''
        let num_str_s = []
        let num_str_l = 0
        let num_str_o = ''
        let num_dec = start + step * i_s
        if(is_char_seq == 1)
            let num_str_o = nr2char(num_dec)
        else
            let num_str = printf('%d',num_dec)
            let num_str = '0000' . num_str
            let num_str_l = strlen(num_str)
            let num_str_p = num_str_l - str_len
           "let num_str_o = num_str[num_str_l-3] . num_str[num_str_l-2] . num_str[num_str_l-1]
            let num_str_o = strcharpart(num_str,num_str_p,str_len)
        endif
        let line_out = substitute(seq_str,"<seq>",num_str_o,"g")
        call append((line('.')+i_s),line_out)
    endfor

endfunction


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" Veriolg signal and module find quickfix
"" if use emacs, use "M-x compile" run command,and auto open compile mode 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nmap <Leader>fs :Vgrep 
command -range=% -nargs=* Vgrep :call V_grep_str_top(<args>) 
" 1st: the grep directory,default current dir
" 2ed: "mod", use for module define only?, 
" 3rd: strict mode, word not use regex grep

function V_grep_str_sub(g_option,g_str,g_dir)
    let grep_str = a:g_str
    let grep_dir = a:g_dir
    let grep_option = a:g_option
    let grep_command = "grep " .grep_option . " \"" . grep_str . "\" ". grep_dir 
    echo grep_command
    exec grep_command
    " use :copen open quickfix window for quick jump
    exec "copen"
endfunction

" use "..." as args list means unceration number of args , it is a list 
function V_grep_str_top(...)
    if(a:0 >= 1)   " a:0 means the number of ... variable args num, a:000 is the args list
        let l:grep_dir = a:1
    else 
        let l:grep_dir = "./*"
    endif

    if(a:0 >= 2)   " a:0 means the number of ... variable args num, a:000 is the args list
        let l:grep_mode = a:2
    else 
        let l:grep_mode = ""
    end 

    if(a:0 >= 3)   " a:0 means the number of ... variable args num, a:000 is the args list
        let l:grep_option = "-nirw"
    else 
        let l:grep_option = "-nir"
    end

    " get word under cursor
    let l:str_under_cursor = expand("<cword>")
   "let str_under_cursor = "<cword>"
    echo l:str_under_cursor

    if(l:grep_mode == "")
        let l:grep_string = str_under_cursor
    else 
        let l:grep_string = substitute(l:grep_mode,"<w>",l:str_under_cursor,"g")
    endif
    call V_grep_str_sub(l:grep_option, l:grep_string, grep_dir)
endfunction


