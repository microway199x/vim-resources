
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" verilog plugin setting 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" 1st vtags setting 
if(g:islinux)
    source ~/git/vim-resources/vtags-3.10/vtags_vim_api.vim
endif

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" verilog_systemverilog.vim setting
function V_sv_compile(...)

    if(a:0 >= 1)   " a:0 means the number of ... variable args num, a:000 is the args list
        let l:other_options = a:1 
    else 
        let l:other_options = ""
    endif

    :compiler vcs   "can use execute("compiler vcs")
    "VCS options setting
    "let vcs_cmd = "vlogan +v2k -full64 +vcs_flush+all +lint=all -sverilog +libext+.v+.sv -lva " . l:other_options . "%"
    let vcs_cmd = "vcs +v2k -full64 +vcs_flush+all +lint=all -sverilog +libext+.v+.sv -lva " . l:other_options . "%"
    let &makeprg= vcs_cmd
    echo "verilog compiler and options setted"
endfunction
"" when write buffer, do make automatic,
" autocmd BufWritePost *.v exec ":make" 
autocmd BufRead BufNew BufNewFile *.v *.sv exec ":call V_sv_compile()"


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" emacs verilog-mode setting
nmap <Leader>vm :call V_verilog_mode()<CR>
function V_verilog_mode()
    exec "w!"
    let fname = expand('%')  " get current buffer filename 
    let v_cmd = "!emacs --batch " . fname . " -f verilog-batch-auto"
    " refresh current buffer 
    :e
endfunc


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" Veriolg quick and efficent tips
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
map <F2> /^\.\w\+\s*(\1   "检查例化模块信号名是否一致
"map <F2> %s/\d\+/\=submatch(0)+1/g  "所有两位以上数字加1
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" Veriolg instance port align
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""对齐verilog instance例化
"vmap <Leader>a :'<,'>s/\(\w\+\).*(\(.*\))/\=printf("%-20s(%-20s)",submatch(1),submatch(2))<CR>
"nmap <Leader>a :s/\(\w\+\).*(\(.*\))/\=printf("%-20s(%-20s)",submatch(1),submatch(2))<CR>
"上述命令由下面函数替代，功能几乎等价，只是格式化得更好一点
vmap <Leader>vs :call V_align_inst_line()<CR>
nmap <Leader>vs :call V_align_inst_line()<CR>
function V_align_inst_line()
    let line_begin = line("'<")
    let line_end   = line("'>")
    let max_inst = 0
    let max_con = 0
    for i in range(line_begin, line_end)
        let line_str  = getline(i)
        if (line_str =~ '^\s*\..*')
            "参考函数：match matchlist subtitute
          ""let line_comp = matchlist(line_str,'\(\w\+\).*(\(.*\))\(.*\)')
           "let line_comp = matchlist(line_str,'\(\w\+\).*(\(\S*\{-}\))\(.*\)')
            let line_comp = matchlist(line_str,'\.\s*\(\w\+\S*\)\s*(\s*\(\w\|\S.*\S\|\)\s*)\s*\(,\|\)\s*\(\S*.*\|\)')
           "echo line_comp
            let inst_name = get(line_comp, 1)
            let con_name  = get(line_comp, 2)
            let comma     = get(line_comp, 3)
            let other     = get(line_comp, 4)
            let len_inst  = strlen(inst_name)
            let len_con   = strlen(con_name)

            if(len_inst > max_inst)
                let max_inst = len_inst
            endif
            if(len_con > max_con)
                let max_con = len_con
            endif
            
            if(len_inst > 30)
                echom (inst_name . "variable name too long")
            endif
            if(len_con > 30)
                echom (con_name . "variable name too long")
            endif
        endif
    endfor

    for i in range(line_begin, line_end)
        let line_str  = getline(i)
        if (line_str =~ '^\s*\..*')
            "参考函数：match matchlist subtitute
          ""let line_comp = matchlist(line_str,'\(\w\+\).*(\(.*\))\(.*\)')
           "let line_comp = matchlist(line_str,'\.\s*\(\w\+\S*\)\s*(\s*\(\w*\S*\)\s*)\s*\(\S*.*\)')
            let line_comp = matchlist(line_str,'\.\s*\(\w\+\S*\)\s*(\s*\(\w\|\S.*\S\|\)\s*)\s*\(,\|\)\s*\(\S*.*\|\)')
           "echo line_comp
            let inst_name = get(line_comp, 1)
            let con_name  = get(line_comp, 2)
            let comma     = get(line_comp, 3)
            let other     = get(line_comp, 4)
            if(max_inst < 10)
                let inst_name = printf('%-10s', inst_name)
            elseif(max_inst < 20)
                let inst_name = printf('%-20s', inst_name)
            elseif(max_inst < 25)
                let inst_name = printf('%-25s', inst_name)
            else
                let inst_name = printf('%-30s', inst_name)
            endif

            if(max_con < 10)
                let con_name = printf('%-10s', con_name)
            elseif(max_con < 20)
                let con_name = printf('%-20s', con_name)
            elseif(max_con < 25)
                let con_name = printf('%-25s', con_name)
            else
                let con_name = printf('%-30s', con_name)
            endif
           "echo max_inst . "  " . max_con

            let line_out  = printf('    .%-s(%-s)%-2s%s', inst_name, con_name, comma, other)
            call setline(i, line_out)
        endif
    endfor
endfunction

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" Veriolg input and output port align
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
vmap <Leader>vp :call V_align_io()<CR>
nmap <Leader>vp :call V_align_io()<CR>
function V_align_io()
    let line_begin = line("'<")
    let line_end   = line("'>")
    let max_len = 0
    let max_wid = 0
    let is_para = 0
    for i in range(line_begin, line_end)
        let line_str  = getline(i)
        if (line_str =~ '^\s*\(input\|inout\|output\|reg\|wire\).*')
            let is_para = 0
            "参考函数：match matchlist subtitute
            if (line_str =~ '^\s*\(input\|output\).*')
                "let line_comp = matchlist(line_str,'\(input\|output\)\s*\(reg\|wire\|\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(,\|\)\s*\(\/\/.*\|\)\s*$')
                 let line_comp = matchlist(line_str,'\(input\|output\)\s*\(reg\|wire\|\)\s*\s*\(signed\|\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(,\|\)\s*\(\/\/.*\|\)\s*$')
               "echo line_comp
                let io      = get(line_comp, 1)
                let regw    = get(line_comp, 2)
                let signed  = get(line_comp, 3)
                let width = get(line_comp, 4)
                let name  = get(line_comp, 5)
                let comma = get(line_comp, 6)
                let other = get(line_comp, 7)
            else
               "let line_comp = matchlist(line_str,'\s*\(reg\|wire\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(;\)\s*\(\/\/.*\|\)\s*$')
                let line_comp = matchlist(line_str,'\s*\(reg\|wire\)\s*\(signed\|\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(;\)\s*\(\/\/.*\|\)\s*$')
               "echo line_comp
                let io      = ""
                let regw    = get(line_comp, 1)
                let signed  = get(line_comp, 2)
                let width   = get(line_comp, 3)
                let name    = get(line_comp, 4)
                let comma   = get(line_comp, 5)
                let other   = get(line_comp, 6)
            endif
            
            let len_name = strlen(name)
            if(len_name > max_len)
                let max_len = len_name
            endif
            if(len_name > 30)
                echom(name . "variable name too long")
            endif

            let len_wid = strlen(width)
            if(len_wid > max_wid)
                let max_wid = len_wid
            endif
        elseif (line_str =~ '^\s*parameter.*')
            let is_para = 1
            let line_comp = matchlist(line_str,'\s*parameter\s*\(\w\+\)\s*=\s*\([^\/\/,]*[^\s\/,]\)\s*\(,\|\)\s*\(\/\/\+.*\|\)')
            let para       = get(line_comp, 1)
            let para_val   = get(line_comp, 2)
            let comma      = get(line_comp, 3)
            let other      = get(line_comp, 4)
            let para_val_list = matchlist(para_val,'\(.*\S\)\s*$')
            let para_val   = get(para_val_list, 1)
            "echo "test here"
            "echo para_val

            let len_name = strlen(para)
            if(len_name > max_len)
                let max_len = len_name
            endif
            if(len_name > 30)
                echom(name . "variable name too long")
            endif

            let len_wid = strlen(para_val)
            if(len_wid > max_wid)
                let max_wid = len_wid
            endif
        endif
    endfor

    if(is_para == 1) 
        for i in range(line_begin, line_end)
            let line_str  = getline(i)
            if (line_str =~ '^\s*parameter.*')
                let line_comp = matchlist(line_str,'\s*parameter\s*\(\w\+\)\s*=\s*\([^\/\/,]*[^\s\/,]\)\s*\(,\|\)\s*\(\/\/\+.*\|\)')
                    let para       = get(line_comp, 1)
                    let para_val   = get(line_comp, 2)
                    let comma      = get(line_comp, 3)
                    let other      = get(line_comp, 4)
                    let para_val_list = matchlist(para_val,'\(.*\S\)\s*$')
                    let para_val   = get(para_val_list, 1)
            endif

            if(max_len < 10)
                let para = printf('%-10s', para)
            elseif(max_len < 20)
                let para = printf('%-20s', para)
            elseif(max_len < 30)
                let para = printf('%-30s', para)
            else
                let para = printf('%-40s', para)
            endif

             if(max_wid < 10)
                 let para_val = printf('%-10s', para_val)
             elseif(max_wid < 20)
                 let para_val = printf('%-20s', para_val)
             elseif(max_wid < 25)
                 let para_val = printf('%-25s', para_val)
             else
                 let para_val = printf('%-30s', para_val)
             endif
            "echo line_comp
            let line_out  = printf('    parameter %s = %s %1s %-s', para,para_val,comma, other)
            "echo line_out
            call setline(i, line_out)
        endfor
    else
        for i in range(line_begin, line_end)
            let line_str  = getline(i)
            if (line_str =~ '^\s*\(input\|inout\|output\|reg\|wire\).*')
                "参考函数：match matchlist subtitute
                if (line_str =~ '^\s*\(input\|output\).*')
                    "let line_comp = matchlist(line_str,'\(input\|output\)\s*\(reg\|wire\|\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(,\|\)\s*\(\/\/.*\|\)\s*$')
                     let line_comp = matchlist(line_str,'\(input\|output\)\s*\(reg\|wire\|\)\s*\s*\(signed\|\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(,\|\)\s*\(\/\/.*\|\)\s*$')
                   "echo line_comp
                    let io      = get(line_comp, 1)
                    let regw    = get(line_comp, 2)
                    let signed  = get(line_comp, 3)
                    let width = get(line_comp, 4)
                    let name  = get(line_comp, 5)
                    let comma = get(line_comp, 6)
                    let other = get(line_comp, 7)
                else
                   "let line_comp = matchlist(line_str,'\s*\(reg\|wire\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(;\)\s*\(\/\/.*\|\)\s*$')
                    let line_comp = matchlist(line_str,'\s*\(reg\|wire\)\s*\(signed\|\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(;\)\s*\(\/\/.*\|\)\s*$')
                   "echo line_comp
                    let io      = ""
                    let regw    = get(line_comp, 1)
                    let signed  = get(line_comp, 2)
                    let width   = get(line_comp, 3)
                    let name    = get(line_comp, 4)
                    let comma   = get(line_comp, 5)
                    let other   = get(line_comp, 6)
                endif

                if(max_len < 10)
                    let name = printf('%-10s', name)
                elseif(max_len < 20)
                    let name = printf('%-20s', name)
                elseif(max_len < 30)
                    let name = printf('%-30s', name)
                else
                    let name = printf('%-40s', name)
                endif

                if(max_wid < 10)
                    let width = printf('%-10s', width)
                elseif(max_wid < 20)
                    let width = printf('%-20s', width)
                elseif(max_wid < 25)
                    let width = printf('%-25s', width)
                else
                    let width = printf('%-30s', width)
                endif

                if (io == "")
                    let io = ""
                else
                    let io = printf('    %-8s', io)
                endif
                "echo line_comp
                let line_out_pre  = printf(' %-6s %-6s %-s %-s %1s %-s', regw,signed, width, name, comma, other)
                let line_out = io . line_out_pre
                "echo line_out
                call setline(i, line_out)
            endif
        endfor
    endif
endfunction

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" Veriolg equalation align
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
vmap <Leader>ve :call V_align_eval()<CR>
nmap <Leader>ve :call V_align_eval()<CR>
function V_align_eval()
    let line_begin = line("'<")
    let line_end   = line("'>")
    let max_left = 0
    let max_right = 0
    let indent_s     = " "
    let name_left    = " "
    let eq_s         = " "
    let name_right   = " "
    let comment      = " "
    let assign_s     = " "
    for i in range(line_begin, line_end)
        let line_str  = getline(i)
        if (line_str =~ '^\s*\S.*')
            if (line_str =~ '^\s*assign\s+.*')
          "  "参考函数：match matchlist subtitute
                let line_comp = matchlist(line_str,'\(\s*\)assign\s\+\(\w\|\S[^;]*\S\)\s*\(=\|<=\)\s*\(\w\|\S[^;]\S\)\s*;\s*\(\S.*\)')
               "let line_comp = matchlist(line_str,'^\s*assign\s+\(\w.*\)\s*\(=\|<=\)\s*\(\w.*\)\s*;\s*\(.*\)')
               "echo line_comp
                let indent_s     = get(line_comp, 1)
                let name_left    = get(line_comp, 2)
                let eq_s         = get(line_comp, 3)
                let name_right   = get(line_comp, 4)
                let comment      = get(line_comp, 5)
                let assign_s     = "assign "
            elseif (line_str =~ '<=*')
                let line_comp = matchlist(line_str,'\(\s*\)\(\w\|\S[^;]*\S\)\s*\(<=\)\s*\(\w\|\S[^;]*\S\)\s*;\s*\(.*\)')
               "let line_comp = matchlist(line_str,'\(\s*\)\(\w\|\S.*\S\)\s*\(=\|<=\)\s*\(\w\|\S.*\S\)\s*;\s*\(.*\)')
               "let line_comp = matchlist(line_str,'^\s*\(\w.*\)\s*\(=\|<=\)\s*\(\w.*\)\s*;\s*\(.*\)')
               "echo line_comp
                let indent_s     = get(line_comp, 1)
                let name_left    = get(line_comp, 2)
                let eq_s         = get(line_comp, 3)
                let name_right   = get(line_comp, 4)
                let comment      = get(line_comp, 5)
                let assign_s     = ""
            elseif (line_str =~ '=*')
                let line_comp = matchlist(line_str,'\(\s*\)\(\w\|\S[^;]*\S\)\s*\(=\)\s*\(\w\|\S[^;]*\S\)\s*;\s*\(.*\)')
               "let line_comp = matchlist(line_str,'^\s*\(\w.*\)\s*\(=\|<=\)\s*\(\w.*\)\s*;\s*\(.*\)')
               "echo line_comp
                let indent_s     = get(line_comp, 1)
                let name_left    = get(line_comp, 2)
                let eq_s         = get(line_comp, 3)
                let name_right   = get(line_comp, 4)
                let comment      = get(line_comp, 5)
                let assign_s     = ""
            endif

            let len_left  = strlen(name_left)
            let len_right = strlen(name_right)
            if(len_left > max_left)
                let max_left = len_left
            endif
            if(len_right > max_right)
                let max_right = len_right
            endif

            if(len_left > 30)
                echom(name_left . "variable name too long")
            endif

            if(len_right > 30)
                echom(name_right . "variable name too long")
            endif
        endif
    endfor

    for i in range(line_begin, line_end)
        let line_str  = getline(i)
        if (line_str =~ '^\s*\S*.*')
            if (line_str =~ '^\s*assign\s+.*')
          "  "参考函数：match matchlist subtitute
                let line_comp = matchlist(line_str,'\(\s*\)assign\s\+\(\w\|\S[^;]*\S\)\s*\(=\|<=\)\s*\(\w\|\S[^;]*\S\)\s*;\s*\(\S.*\)')
               "let line_comp = matchlist(line_str,'^\s*assign\s+\(\w.*\)\s*\(=\|<=\)\s*\(\w.*\)\s*;\s*\(.*\)')
               "echo line_comp
                let indent_s     = get(line_comp, 1)
                let name_left    = get(line_comp, 2)
                let eq_s         = get(line_comp, 3)
                let name_right   = get(line_comp, 4)
                let comment      = get(line_comp, 5)
                let assign_s     = "assign "
            elseif (line_str =~ '<=*')
                let line_comp = matchlist(line_str,'\(\s*\)\(\w\|\S[^;]*\S\)\s*\(<=\)\s*\(\w\|\S[^;]*\S\)\s*;\s*\(.*\)')
               "let line_comp = matchlist(line_str,'\(\s*\)\(\w\|\S.*\S\)\s*\(=\|<=\)\s*\(\w\|\S.*\S\)\s*;\s*\(.*\)')
               "let line_comp = matchlist(line_str,'^\s*\(\w.*\)\s*\(=\|<=\)\s*\(\w.*\)\s*;\s*\(.*\)')
               "echo line_comp
                let indent_s     = get(line_comp, 1)
                let name_left    = get(line_comp, 2)
                let eq_s         = get(line_comp, 3)
                let name_right   = get(line_comp, 4)
                let comment      = get(line_comp, 5)
                let assign_s     = ""
            elseif (line_str =~ '=*')
                let line_comp = matchlist(line_str,'\(\s*\)\(\w\|\S[^;]*\S\)\s*\(=\)\s*\(\w\|\S[^;]*\S\)\s*;\s*\(.*\)')
               "let line_comp = matchlist(line_str,'^\s*\(\w.*\)\s*\(=\|<=\)\s*\(\w.*\)\s*;\s*\(.*\)')
               "echo line_comp
                let indent_s     = get(line_comp, 1)
                let name_left    = get(line_comp, 2)
                let eq_s         = get(line_comp, 3)
                let name_right   = get(line_comp, 4)
                let comment      = get(line_comp, 5)
                let assign_s     = ""
            endif

            if(max_left < 10)
                let name_left = printf('%-10s', name_left)
            elseif(max_left < 20)
                let name_left = printf('%-20s', name_left)
            elseif(max_left < 25)
                let name_left = printf('%-25s', name_left)
            else
                let name_left = printf('%-30s', name_left)
            endif

            if(max_right < 10)
                let name_right = printf('%-10s', name_right)
            elseif(max_right < 20)
                let name_right = printf('%-20s', name_right)
            elseif(max_right < 25)
                let name_right = printf('%-25s', name_right)
            else
                let name_right = printf('%-30s', name_right)
            endif

            let indent_s  = printf('%s',indent_s)
            let assign_s  = printf('%-s',assign_s)
            let eq_s      = printf('%-2s',eq_s)
            let comment   = printf('%-s',comment)
            "echo line_comp
            let line_out  = indent_s . assign_s . name_left . eq_s . name_right . ";" . comment
            "echo line_out
            call setline(i, line_out)
        endif
    endfor
endfunction

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" Veriolg drow simple waveform in verilog file
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
vmap <Leader>vw :Vwavedrom 
nmap <Leader>vw :Vwavedrom 
":Vwavedrom 7
command -range=% -nargs=+ Vwavedrom :call V_wavedrom(<args>) 
function V_wavedrom(n_len)
    let line_begin = line("'<")
    let line_end   = line("'>")
    let line_str   = ""
    for k in range(line_begin, line_end,2)
        let name     = ""
        let dot      = ""
        let dot_len  = 0
        let line_u   = ""
        let line_d   = ""
        let line_str  = getline(k+1)
       "if (line_str =~ 'SN\S*\s+.*SD\S*')
        if (line_str =~ 'SN:.*SD:.*')
            let line_comp = matchlist(line_str,'\(SN:\S*\)\s\+.*SD:\(\S*\)')
            let name      = line_comp[1]
            let dot       = line_comp[2]
            let dot_len   = strlen(dot)
            let dot_list  = ""
            for i_parse in range(dot_len)
                if(i_parse == 0) 
                    if(dot[0] == ".")
                        let dot_list = dot_list . "z"
                    else 
                        let dot_list = dot_list . dot[0]
                    endif
                   "echo dot_list
                else 
                    if(dot[i_parse] == ".")
                        let dot_list = dot_list . dot_list[i_parse-1]
                    else 
                        let dot_list = dot_list . dot[i_parse]
                    endif
                   "echo dot_list
                endif
            endfor
           "echo dot_list
           "
            for i_drow in range(dot_len)
                if (i_drow==0)        
                "" when wave start
                    if(dot_list[i_drow] == "0")
                        let line_u = line_u . "  "
                        let line_d = line_d . "__"
                    elseif(dot_list[i_drow] == "1")
                        let line_u = line_u . "__"
                        let line_d = line_d . "  "
                    elseif(dot_list[i_drow] == "z")
                        let line_u = line_u . "  "
                        let line_d = line_d . "--"
                    elseif((dot_list[i_drow] == "2") || (dot_list[i_drow] == "3"))
                        let line_u = line_u . "__"
                        let line_d = line_d . "__"
                    else 
                        let line_u = line_u . "??"
                        let line_d = line_d . "??"
                    endif
                else 
                    if(dot_list[i_drow] == "0")
                        if(dot_list[i_drow-1] == "0")
                            let line_u = line_u . "  "
                            let line_d = line_d . "__"
                        elseif (dot_list[i_drow-1] == "1")
                            let line_u = line_u . "  "
                            let line_d = line_d . "\\_"
                        elseif (dot_list[i_drow-1] == "z")
                            let line_u = line_u . "  "
                            let line_d = line_d . "\\_"
                        elseif((dot_list[i_drow-1] == "2") || (dot_list[i_drow-1] == "3"))
                            let line_u = line_u . "  "
                            let line_d = line_d . "\\_"
                        endif
                    elseif(dot_list[i_drow] == "1")
                        if(dot_list[i_drow-1] == "0")
                            let line_u = line_u . " _"
                            let line_d = line_d . "/ "
                        elseif (dot_list[i_drow-1] == "1")
                            let line_u = line_u . "__"
                            let line_d = line_d . "  "
                        elseif (dot_list[i_drow-1] == "z")
                            let line_u = line_u . " _"
                            let line_d = line_d . "/ "
                        elseif((dot_list[i_drow-1] == "2") || (dot_list[i_drow-1] == "3"))
                            let line_u = line_u . " _"
                            let line_d = line_d . "/ "
                        endif
                    elseif(dot_list[i_drow] == "z")
                        if(dot_list[i_drow-1] == "0")
                            let line_u = line_u . "  "
                            let line_d = line_d . "+-"
                        elseif (dot_list[i_drow-1] == "1")
                            let line_u = line_u . "  "
                            let line_d = line_d . "+-"
                        elseif (dot_list[i_drow-1] == "z")
                            let line_u = line_u . "  "
                            let line_d = line_d . "--"
                        elseif((dot_list[i_drow-1] == "2") || (dot_list[i_drow-1] == "3"))
                            let line_u = line_u . "  "
                            let line_d = line_d . "+-"
                        endif
                    elseif((dot_list[i_drow] == "2") || (dot_list[i_drow] == "3"))
                        if(dot_list[i_drow-1] == "0")
                            let line_u = line_u . " _"
                            let line_d = line_d . "/_"
                        elseif (dot_list[i_drow-1] == "1")
                            let line_u = line_u . " _"
                            let line_d = line_d . "\\_"
                        elseif (dot_list[i_drow-1] == "z")
                            let line_u = line_u . " _"
                            let line_d = line_d . "/_"
                        elseif((dot_list[i_drow-1] == "2") || (dot_list[i_drow-1] == "3"))
                            if(dot_list[i_drow] == dot_list[i_drow-1])
                                let line_u = line_u . "__"
                                let line_d = line_d . "__"
                            else
                                let line_u = line_u . " _"
                                let line_d = line_d . "X_"
                            endif
                        endif
                    endif " end else
                endif " end if i_drow
            endfor  

            if(a:n_len < 5)
                let name_u = printf("%-5s",'')
                let name_d = printf("%-5s",name)
            elseif (a:n_len < 10)
                let name_u = printf("%-10s",'')
                let name_d = printf("%-10s",name)
            elseif (a:n_len < 15)
                let name_u = printf("%-15s",'')
                let name_d = printf("%-15s",name)
            elseif (a:n_len < 20)
                let name_u = printf("%-20s",'')
                let name_d = printf("%-20s",name)
            elseif (a:n_len < 25)
                let name_u = printf("%-25s",'')
                let name_d = printf("%-25s",name)
            else
                let name_u = printf("%-30s",'')
                let name_d = printf("%-30s",name)
            endif

            let line_u_s = printf("\\\\%-s    %-s",name_u,line_u)
            let line_d_s = printf("\\\\%-s SW:%-s   SD:%-s",name_d,line_d,dot)
            call setline(k,line_u_s)
            call setline(k+1,line_d_s)
        endif " end repx
    endfor
endfunction

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" Veriolg instant from module 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
vmap <Leader>vt :call V_inst()<CR>
nmap <Leader>vt :call V_inst()<CR>
function V_inst()
   "global mark
    :w! 
    exec "normal mW"
    let cur_pos     = getcurpos()
    let cur_column  = cur_pos[2] 
    let use_cur_file = input("use current cursor file to instant(y/n): ")

    if(use_cur_file =~"y")
        exec "normal gf"
    else 
        let input_file = input("the file use for instant : ")
	let open_file_com = "e!" . input_file
	exec open_file_com
	echo input_file
    endif

    exec "normal gg"
    /^\s*module
    let line_begin = line(".")
    let module_line = getline(".")
    let line_comp = matchlist(module_line,'^\s*module\s*\(\w\+\)\s*.*')
    let module_name = get(line_comp, 1)
    /^\s*);
    let line_end = line(".")
    echo line_begin
    echo line_end
    let name_with_io = V_get_ports(line_begin,line_end)
    let name_para    = V_get_para(line_begin,line_end)
    "echo "get here"
   "global jump
    exec "normal 'W" 
    let module_name = toupper(module_name)
    let module_end = ");"
    if(empty(name_para)) " means len(name_para) == 0
        let module_inst = module_name . "  " . "U_" . module_name . "("
        exec "normal o"
        "echo name_with_io
        call setline(line("."),module_inst) 
        "exec "normal o"
    else
        let module_inst = module_name . "  " . "#("
        exec "normal o"
        "echo name_with_io
        call setline(line("."),module_inst) 
        "exec "normal o"
        for item in name_para
            exec "normal o"
            let item_out = "    " . item
            call setline(line("."),item_out)
        endfor
        let module_inst = "U_" .  module_name .  "("
        exec "normal o"
        "echo name_with_io
        call setline(line("."),module_inst) 
        "exec "normal o"
    endif
    "call setline(line("."),name_with_io)
    for item in name_with_io
        exec "normal o"
        let item_out = "    " . item
        call setline(line("."),item_out)
    endfor
    exec "normal o"
    call setline(line("."),module_end) 
    exec "normal k"
    :s/,/ /g
    :w! 
    exec "normal 'W" 
    let open_sc_file = input("open module source file for check?(y/n):")
    if(open_sc_file =~ "y")
        :sp
	if(use_cur_file =~"y")
            exec "normal 'W" 
            let go_to_column = "normal" . cur_column . "l"
            exec go_to_column
            exec "normal gf"
	else
            exec open_file_com
	endif
    endif
endfunction

function V_get_para(line_begin,line_end)
    let line_begin = str2nr(a:line_begin)  
    let line_end   = str2nr(a:line_end)
    let max_len = 0
    let name_s = ""
    let name_out = ""
    let name_list = []
    let name_list_out = []
    for i in range(line_begin, line_end)
        let line_str  = getline(i)
        if (line_str =~ '^\s*parameter.*')
            "参考函数：match matchlist subtitute
            let line_comp = matchlist(line_str,'^\s*parameter\s\+\(\w\+\)\s*=.*')
            "echo line_comp
            let name     = get(line_comp, 1)
                
            let len_name = strlen(name)
            if(len_name > max_len)
                let max_len = len_name
            endif
            echo name 
            let name_list = add(name_list,name)
            "echo name_list
        endif
    endfor

    let cur_num = 0
    let len_name_list = len(name_list)
    for item in name_list
        let name_s = item
            if(max_len < 10)
                let name_s = printf('%-10s', name_s)
            elseif(max_len < 20)
                let name_s = printf('%-20s', name_s)
            elseif(max_len < 30)
                let name_s = printf('%-30s', name_s)
            elseif(max_len < 40)
                let name_s = printf('%-40s', name_s)
            else 
                let name_s = printf('%-50s', name_s)
            endif

            if(cur_num >= len_name_list -1) 
                "echo line_comp
                let name_out = "." . name_s . "(" . "INST_PARA" . "))"
            else
                let name_out = "." . name_s . "(" . "INST_PARA" . "),"
                let cur_num = cur_num + 1
            endif
                "echo line_out
            let name_list_out = add(name_list_out,name_out)
    endfor
    return name_list_out
endfunction


function V_get_ports(line_begin,line_end)
    let line_begin = str2nr(a:line_begin)  
    let line_end   = str2nr(a:line_end)
    let max_len = 0
    let io_s = ""
    let name_s = ""
    let name_list = []
    let name_list_out = []
    for i in range(line_begin, line_end)
        let line_str  = getline(i)
        if (line_str =~ '^\s*\(input\|output\).*')
            "参考函数：match matchlist subtitute
            let line_comp = matchlist(line_str,'\(input\|output\)\s*\(reg\|wire\|\)\s*\(signed\|\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(,\|\)\s*\(\/\/.*\|\)\s*$')
            "echo line_comp
            let io     = get(line_comp, 1)
            let regw   = get(line_comp, 2)
            let signed = get(line_comp, 3)
            let width  = get(line_comp, 4)
            let name   = get(line_comp, 5)
            let comma  = get(line_comp, 6)
            let other  = get(line_comp, 7)
                
            let len_name = strlen(name)
            if(len_name > max_len)
                let max_len = len_name
            endif
            if(io == "input") 
                let io = "I_p"
            elseif(io == "output") 
                let io = "O_p"
            else 
                let io = "unknown"
            endif
            echo name 
            let name_with_io = io . "," . name
            let name_list = add(name_list,name_with_io)
            "echo name_list
        endif
    endfor

    for item in name_list
        let [io_s,name_s] = split(item,",")
            if(max_len < 10)
                let name_s = printf('%-10s', name_s)
            elseif(max_len < 20)
                let name_s = printf('%-20s', name_s)
            elseif(max_len < 30)
                let name_s = printf('%-30s', name_s)
            elseif(max_len < 40)
                let name_s = printf('%-40s', name_s)
            else 
                let name_s = printf('%-50s', name_s)
            endif

            "echo line_comp
            let name_out = "." . name_s . "(" . name_s . ")" . ",//" . io_s 
            "echo line_out
            let name_list_out = add(name_list_out,name_out)
    endfor
    return name_list_out
endfunction


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" Veriolg chk reset match 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
vmap <Leader>vc :call V_chk_rst()<CR>
nmap <Leader>vc :call V_chk_rst()<CR>

"字符串使用' ' 表示不做转义，所见即所得(特殊的为两个'，会被转义为一个')
"字符串使用" "，表示做转义
function V_chk_rst()
    exec "normal gg"
    while search("^\s*always.*rst.*","W") > 0
        let line_cur = line(".")
        let line_always = getline(line_cur)
        /^\s*if.*rst.*
        let line_rst_num = line(".")
        let line_rst    = getline(line_rst_num)
        echo line_rst
        echo line_always
        "match list shall use ' '
        let str_always_list  = matchlist(line_always,'^\s*always.*\(rst\w*\).*')
        let str_rst_list     = matchlist(line_rst   ,'^\s*if.*\(rst\w*\).*')
        echo str_rst_list
        echo str_always_list
        let str_always = get(str_always_list,1)
        let str_rst    = get(str_rst_list,1)
        if(str_always != str_rst)
            echo printf("reset violation @line %d and line %d", line_cur,line_rst_num)
        endif
    endwhile

endfunction

