
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" verilog plugin setting 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" 1st vtags setting 
"if(g:islinux)
    "source ~/git/vim-resources/micro-config-files/micro-plugin/vtags-3.10/vtags_vim_api.vim
"endif

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
"autocmd BufRead BufNew BufNewFile *.v, *.sv exec ":call V_sv_compile()"


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
    let max_con_vec = 0
    for i in range(line_begin, line_end)
        let line_str  = getline(i)
        if (line_str =~ '^\s*\..*')
            "参考函数：match matchlist subtitute
          ""let line_comp = matchlist(line_str,'\(\w\+\).*(\(.*\))\(.*\)')
           "let line_comp = matchlist(line_str,'\(\w\+\).*(\(\S*\{-}\))\(.*\)')
            let line_comp = matchlist(line_str,'^\s*\.\s*\(\S\+\S*\)\s*(\s*\(\w\|\S.*\S\|\)\s*)\s*\(,\|\)\s*\(\S*.*\|\)$')
           "echo line_comp
            let inst_name = get(line_comp, 1)
            let con_name  = get(line_comp, 2)
            let comma     = get(line_comp, 3)
            let other     = get(line_comp, 4)

            if(con_name =~ '^\s*\w[a-zA-Z0-9_]*\s*\(\[.*\]\)\s*$') 
                let con_name_vec = matchlist(con_name,'^\s*\(\w[a-zA-Z0-9_]*\)\s*\(\[.*\]\)\s*$') 
                let con_name     = get(con_name_vec,1)
                let con_vec      = get(con_name_vec,2)
            else 
                let con_name_vec = matchlist(con_name,'^\s*\(\w\|\S.*\S\|\)\s*$') 
                let con_name     = get(con_name_vec,1)
                let con_vec      = ""
            endif
            
            let con_name = con_name . " " . con_vec

            let len_inst     = strlen(inst_name)
            let len_con      = strlen(con_name)


            if(len_inst > max_inst)
                let max_inst = len_inst
            endif
            if(len_con > max_con)
                let max_con = len_con
            endif

            
            if(len_inst > 40)
                echom (inst_name . "variable name too long")
            endif
            if(len_con > 40)
                echom (con_name . "variable name too long")
            endif
        endif
    endfor

    ""can use string as format, string can dynamic generate
    if(max_inst > 60) 
        let max_inst = 60
    endif
    let max_inst = max_inst + 4
    let inst_name_format = "%-" . max_inst . "s"

    if(max_con > 60) 
        let max_con = 60
    endif
    let max_con = max_con + 4
    let con_name_format = "%-" . max_con . "s"

    for i in range(line_begin, line_end)
        let line_str  = getline(i)
        if (line_str =~ '^\s*\..*')
            "参考函数：match matchlist subtitute
          ""let line_comp = matchlist(line_str,'\(\w\+\).*(\(.*\))\(.*\)')
           "let line_comp = matchlist(line_str,'\.\s*\(\w\+\S*\)\s*(\s*\(\w*\S*\)\s*)\s*\(\S*.*\)')
            let line_comp = matchlist(line_str,'^\s*\.\s*\(\S\+\S*\)\s*(\s*\(\w\|\S.*\S\|\)\s*)\s*\(,\|\)\s*\(\S*.*\|\)$')
           "echo line_comp
            let inst_name = get(line_comp, 1)
            let con_name  = get(line_comp, 2)
            let comma     = get(line_comp, 3)
            let other     = get(line_comp, 4)

            if(con_name =~ '^\s*\w[a-zA-Z0-9_]*\s*\(\[.*\]\)\s*$') 
                let con_name_vec = matchlist(con_name,'^\s*\(\w[a-zA-Z0-9_]*\)\s*\(\[.*\]\)\s*$') 
                let con_name     = get(con_name_vec,1)
                let con_vec      = get(con_name_vec,2)
            else 
                let con_name_vec = matchlist(con_name,'^\s*\(\w\|\S.*\S\|\)\s*$') 
                let con_name     = get(con_name_vec,1)
                let con_vec      = ""
            endif

            let con_name     = con_name . " " . con_vec
            let con_name = printf(con_name_format, con_name)

            let inst_name = printf(inst_name_format, inst_name)

           "echo max_inst . "  " . max_con

            let line_out  = printf('    .%-s(%-s% )%-2s%s', inst_name, con_name,comma, other)
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
    let max_vec = 0
    let max_wid = 0
    let is_para = 0
    for i in range(line_begin, line_end)
        let line_str  = getline(i)
        if (line_str =~ '^\s*\(input\|inout\|output\|reg\|wire\).*')
            let is_para = 0
            "参考函数：match matchlist subtitute
            if (line_str =~ '^\s*\(input\|output\).*')
                "let line_comp = matchlist(line_str,'\(input\|output\)\s*\(reg\|wire\|\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(,\|\)\s*\(\/\/.*\|\)\s*$')
                 let line_comp = matchlist(line_str,'\s*\(input\|output\)\s*\(reg\|wire\|\)\s*\s*\(signed\|\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(,\|\)\s*\(\/\/.*\|\)\s*$')
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
               "let line_comp = matchlist(line_str,'\s*\(reg\|wire\)\s*\(signed\|\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(;\)\s*\(\/\/.*\|\)\s*$')
                let line_comp = matchlist(line_str,'\s*\(reg\|wire\)\s*\(signed\|\)\s*\(\[.*\]\|\)\s*\(\w[^;]*\)\s*\(;\)\s*\(\S.*\|\)\s*$')
               "echo line_comp
                let io      = ""
                let regw    = get(line_comp, 1)
                let signed  = get(line_comp, 2)
                let width   = get(line_comp, 3)
                let name    = get(line_comp, 4)
                let comma   = get(line_comp, 5)
                let other   = get(line_comp, 6)
            endif

            if(name =~ '^\s*\w[a-zA-Z0-9_]*\s*\(\[.*\]\)\s*$') 
                let name_vec = matchlist(name,'^\s*\(\w[a-zA-Z0-9_]*\)\s*\(\[.*\]\)\s*$') 
                let name     = get(name_vec,1)
                let vec      = get(name_vec,2)
            else 
                let name_vec = matchlist(name,'^\s*\(\w[a-zA-Z0-9_]*\)\s*$') 
                let name     = get(name_vec,1)
                let vec      = ""
            endif

            let name = name . " " . vec
            
            let len_name = strlen(name)

            if(len_name > max_len)
                let max_len = len_name
            endif

            if(len_name > 40)
                echom(name . "variable name too long")
            endif

            let len_wid = strlen(width)
            if(len_wid > max_wid)
                let max_wid = len_wid
            endif
        elseif (line_str =~ '^\s*parameter.*')
            let is_para = 1
            let line_comp = matchlist(line_str,'^\s*parameter\s*\(\w\+\)\s*=\s*\([^\/,;]*[^\s\/,;]\)\s*\(,\|;\|\)\s*\(\/\/\+.*\|\)')
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
        if(max_len > 60) 
            let max_len = 60
        endif 

        let max_len = max_len + 4
        let para_format = "%-" . max_len . "s"

        if(max_wid > 60) 
            let max_wid = 60
        endif 

        let max_wid = max_wid + 4
        let para_val_format = "%-" . max_wid . "s"

        for i in range(line_begin, line_end)
            let line_str  = getline(i)
            if (line_str =~ '^\s*parameter.*')
                let line_comp = matchlist(line_str,'^\s*parameter\s*\(\w\+\)\s*=\s*\([^\/,;]*[^\s\/,;]\)\s*\(,\|;\|\)\s*\(\/\/\+.*\|\)')
                let para       = get(line_comp, 1)
                let para_val   = get(line_comp, 2)
                let comma      = get(line_comp, 3)
                let other      = get(line_comp, 4)
                let para_val_list = matchlist(para_val,'\(.*\S\)\s*$')
                let para_val   = get(para_val_list, 1)
            

                let para = printf(para_format , para)
   
                let para_val = printf(para_val_format, para_val)
                "echo line_comp
                let line_out  = printf('    parameter %s = %s %1s %-s', para,para_val,comma, other)
                "echo line_out
                call setline(i, line_out)
            endif
        endfor
    else   
    "if not paramenter , input /output 

        if(max_len > 60) 
            let max_len = 60
        endif 

        let max_len = max_len + 4
        let name_format = "%-" . max_len . "s"

        if(max_wid > 60) 
            let max_wid = 60
        endif 

        let max_wid = max_wid + 4
        let width_format = "%-" . max_wid . "s"

        for i in range(line_begin, line_end)
            let line_str  = getline(i)
            if (line_str =~ '^\s*\(input\|inout\|output\|reg\|wire\).*')
                "参考函数：match matchlist subtitute
                if (line_str =~ '^\s*\(input\|output\).*')
                    "let line_comp = matchlist(line_str,'\(input\|output\)\s*\(reg\|wire\|\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(,\|\)\s*\(\/\/.*\|\)\s*$')
                     let line_comp = matchlist(line_str,'\s*\(input\|output\)\s*\(reg\|wire\|\)\s*\s*\(signed\|\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(,\|\)\s*\(\/\/.*\|\)\s*$')
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
                   "let line_comp = matchlist(line_str,'\s*\(reg\|wire\)\s*\(signed\|\)\s*\(\[.*\]\|\)\s*\(\w[a-zA-Z0-9\[\]:_]*\)\s*\(;\)\s*\(\/\/.*\|\)\s*$')
                    let line_comp = matchlist(line_str,'\s*\(reg\|wire\)\s*\(signed\|\)\s*\(\[.*\]\|\)\s*\(\w[^;]*\)\s*\(;\)\s*\(\S.*\|\)\s*$')
                   "echo line_comp
                    let io      = ""
                    let regw    = get(line_comp, 1)
                    let signed  = get(line_comp, 2)
                    let width   = get(line_comp, 3)
                    let name    = get(line_comp, 4)
                    let comma   = get(line_comp, 5)
                    let other   = get(line_comp, 6)
                endif

                if(name =~ '^\s*\w[a-zA-Z0-9_]*\s*\(\[.*\]\)\s*$') 
                    let name_vec = matchlist(name,'^\s*\(\w[a-zA-Z0-9_]*\)\s*\(\[.*\]\)\s*$') 
                    let name     = get(name_vec,1)
                    let vec      = get(name_vec,2)
                else 
                    let name_vec = matchlist(name,'^\s*\(\w[a-zA-Z0-9_]*\)\s*$') 
                    let name     = get(name_vec,1)
                    let vec      = ""
                endif
                
                let name = name . " " . vec
                
                let name = printf(name_format, name)

                let width = printf(width_format, width)

                if (io == "")
                    let io = ""
                else
                    let io = printf('    %-8s', io)
                endif
                "echo io
                let line_out_pre  = printf(' %-6s %-6s %-s %-s %1s %-s', regw,signed, width, name,comma, other)
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
    let max_len_left = 0
    let max_len_right = 0
    let max_len_vec_left = 0
    let max_len_vec_right = 0
    let indent_s     = " "
    let name_left    = " "
    let eq_s         = " "
    let name_right   = " "
    let comment      = " "
    let assign_s     = " "
    for i in range(line_begin, line_end)
        let line_str  = getline(i)
        if (line_str =~ '^\s*\S\+.*')
            if (line_str =~ '^\s*assign\s\+.*')
          "  "参考函数：match matchlist subtitute
                let line_comp = matchlist(line_str,'^\(\s*\)assign\s\+\(\w\|\S[^;<=]*\S\)\s*\(=\|<=\)\s*\(\w\|\S[^;]*\S\)\s*;\s*\(.*\)$')
               "let line_comp = matchlist(line_str,'^\s*assign\s+\(\w.*\)\s*\(=\|<=\)\s*\(\w.*\)\s*;\s*\(.*\)')
               "echo line_comp
                let indent_s     = get(line_comp, 1)
                let name_left    = get(line_comp, 2)
                let eq_s         = get(line_comp, 3)
                let name_right   = get(line_comp, 4)
                let comment      = get(line_comp, 5)
                let assign_s     = "assign "
            elseif (line_str =~ '<=')
                let line_comp = matchlist(line_str,'^\(\s*\)\(\w\|\S[^;<=]*\S\)\s*\(<=\)\s*\(\w\|\S[^;]*\S\)\s*;\s*\(.*\)$')
               "let line_comp = matchlist(line_str,'\(\s*\)\(\w\|\S.*\S\)\s*\(=\|<=\)\s*\(\w\|\S.*\S\)\s*;\s*\(.*\)')
               "let line_comp = matchlist(line_str,'^\s*\(\w.*\)\s*\(=\|<=\)\s*\(\w.*\)\s*;\s*\(.*\)')
               "echo line_comp
                let indent_s     = get(line_comp, 1)
                let name_left    = get(line_comp, 2)
                let eq_s         = get(line_comp, 3)
                let name_right   = get(line_comp, 4)
                let comment      = get(line_comp, 5)
                let assign_s     = ""
            elseif (line_str =~ '=')
                let line_comp = matchlist(line_str,'^\(\s*\)\(\w\|\S[^;=]*\S\)\s*\(=\)\s*\(\w\|\S[^;]*\S\)\s*;\s*\(.*\)$')
               "let line_comp = matchlist(line_str,'^\s*\(\w.*\)\s*\(=\|<=\)\s*\(\w.*\)\s*;\s*\(.*\)')
               "echo line_comp
                let indent_s     = get(line_comp, 1)
                let name_left    = get(line_comp, 2)
                let eq_s         = get(line_comp, 3)
                let name_right   = get(line_comp, 4)
                let comment      = get(line_comp, 5)
                let assign_s     = ""
            endif

            if(name_left =~ '^\s*\w[a-zA-Z0-9_]*\s*\(\[.*\]\)\s*$') 
                let name_left_vec = matchlist(name_left,'^\s*\(\w[a-zA-Z0-9_]*\)\s*\(\[.*\]\)\s*$') 
                let name_left     = get(name_left_vec,1)
                let vec_left      = get(name_left_vec,2)
            else 
                let name_left_vec = matchlist(name_left,'^\s*\(\w\|\S.*\S\)\s*$') 
                let name_left     = get(name_left_vec,1)
                let vec_left      = ""
            endif

            if(name_right =~ '^\s*\w[a-zA-Z0-9_]*\s*\(\[.*\]\)\s*') 
                let name_right_vec  = matchlist(name_right,'^\s*\(\w[a-zA-Z0-9_]*\)\s*\(\[.*\]\)\s*$') 
                let name_right      = get(name_right_vec,1)
                let vec_right       = get(name_right_vec,2)
            else 
                let name_right_vec = matchlist(name_right,'^\s*\(\w\|\S.*\S\)\s*$') 
                let name_right     = get(name_right_vec,1)
                let vec_right      = ""
            endif

            let len_left  = strlen(name_left)
            let len_right = strlen(name_right)

            let len_vec_left  = strlen(vec_left)
            let len_vec_right = strlen(vec_right)

            if(len_left > max_len_left)
                let max_len_left = len_left
            endif
            if(len_right > max_len_right)
                let max_len_right = len_right
            endif

            if(len_vec_left > max_len_vec_left)
                let max_len_vec_left = len_vec_left
            endif

            if(len_vec_right > max_len_vec_right)
                let max_len_vec_right = len_vec_right
            endif

            if(len_left > 40)
                echom(name_left . "variable name too long")
            endif

            if(len_right > 40)
                echom(name_right . "variable name too long")
            endif
        endif
    endfor

    if(max_len_left > 60)
        let max_len_left = 60
    endif

    let name_left_format = "%-" . max_len_left . "s"

    if(max_len_right > 60)
        let max_len_right = 60
    endif

    let name_right_format = "%-" . max_len_right . "s"

    if(max_len_vec_left > 30)
        let max_len_vec_left = 30
    endif
    let name_vec_left_format = "%-" . max_len_vec_left . "s"

    if(max_len_vec_right > 30)
        let max_len_vec_right = 30
    endif
    let name_vec_right_format = "%-" . max_len_vec_right . "s"

    for i in range(line_begin, line_end)
        let line_str  = getline(i)
        if (line_str =~ '^\s*\S\+.*')
            if (line_str =~ '^\s*assign\s\+.*')
          "  "参考函数：match matchlist subtitute
                let line_comp = matchlist(line_str,'^\(\s*\)assign\s\+\(\w\|\S[^;<=]*\S\)\s*\(=\|<=\)\s*\(\w\|\S[^;]*\S\)\s*;\s*\(.*\)$')
               "let line_comp = matchlist(line_str,'^\s*assign\s+\(\w.*\)\s*\(=\|<=\)\s*\(\w.*\)\s*;\s*\(.*\)')
               "echo line_comp
                let indent_s     = get(line_comp, 1)
                let name_left    = get(line_comp, 2)
                let eq_s         = get(line_comp, 3)
                let name_right   = get(line_comp, 4)
                let comment      = get(line_comp, 5)
                let assign_s     = "assign "
            elseif (line_str =~ '<=')
                let line_comp = matchlist(line_str,'^\(\s*\)\(\w\|\S[^;<=]*\S\)\s*\(<=\)\s*\(\w\|\S[^;]*\S\)\s*;\s*\(.*\)$')
               "let line_comp = matchlist(line_str,'\(\s*\)\(\w\|\S.*\S\)\s*\(=\|<=\)\s*\(\w\|\S.*\S\)\s*;\s*\(.*\)')
               "let line_comp = matchlist(line_str,'^\s*\(\w.*\)\s*\(=\|<=\)\s*\(\w.*\)\s*;\s*\(.*\)')
               "echo line_comp
                let indent_s     = get(line_comp, 1)
                let name_left    = get(line_comp, 2)
                let eq_s         = get(line_comp, 3)
                let name_right   = get(line_comp, 4)
                let comment      = get(line_comp, 5)
                let assign_s     = ""
            elseif (line_str =~ '=')
                let line_comp = matchlist(line_str,'^\(\s*\)\(\w\|\S[^;<=]*\S\)\s*\(=\)\s*\(\w\|\S[^;]*\S\)\s*;\s*\(.*\)$')
               "let line_comp = matchlist(line_str,'^\s*\(\w.*\)\s*\(=\|<=\)\s*\(\w.*\)\s*;\s*\(.*\)')
               "echo line_comp
                let indent_s     = get(line_comp, 1)
                let name_left    = get(line_comp, 2)
                let eq_s         = get(line_comp, 3)
                let name_right   = get(line_comp, 4)
                let comment      = get(line_comp, 5)
                let assign_s     = ""
            endif

            if(name_left =~ '^\s*\w[a-zA-Z0-9_]*\s*\(\[.*\]\)\s*$') 
                let name_left_vec = matchlist(name_left,'^\s*\(\w[a-zA-Z0-9_]*\)\s*\(\[.*\]\)\s*$') 
                let name_left     = get(name_left_vec,1)
                let vec_left      = get(name_left_vec,2)
            else 
                let name_left_vec = matchlist(name_left,'^\s*\(\w\|\S.*\S\)\s*$') 
                let name_left     = get(name_left_vec,1)
                let vec_left      = ""
            endif

            if(name_right =~ '^\s*\w[a-zA-Z0-9_]*\s*\(\[.*\]\)\s*$') 
                let name_right_vec  = matchlist(name_right,'^\s*\(\w[a-zA-Z0-9_]*\)\s*\(\[.*\]\)\s*$') 
                let name_right      = get(name_right_vec,1)
                let vec_right       = get(name_right_vec,2)
            else 
                let name_right_vec = matchlist(name_right,'^\s*\(\w\|\S.*\S\)\s*$') 
                let name_right     = get(name_right_vec,1)
                let vec_right      = ""
            endif

            let name_left = printf(name_left_format, name_left)

            let name_right = printf(name_right_format, name_right)

            let vec_left = printf(name_vec_left_format, vec_left)

            let vec_right = printf(name_vec_right_format, vec_right)

            let indent_s  = printf('%s',indent_s)
            let assign_s  = printf('%-s',assign_s)
            let eq_s      = printf('%-2s',eq_s)
            let comment   = printf('%-s',comment)
            "echo line_comp
            "let line_out  = indent_s . assign_s . name_left .vec_left . "  " .  eq_s . "  " . name_right . vec_right . "  ;" . comment
             let line_out  = "    " . assign_s . name_left .vec_left . "  " .  eq_s . "  " . name_right . vec_right . "  ;" . comment
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

            let name_len = a:n_len + 2
            let name_format = "%-" . name_len . "s"

            let name_u = printf(name_format,'')
            let name_d = printf(name_format,name)

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
    
    if(max_len > 60)
        let max_len = 60
    endif
    let max_len = max_len + 4

    let name_s_format = "%-" . max_len ."s"

    for item in name_list
        let name_s = item
            let name_s = printf(name_s_format, name_s)

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

    if(max_len > 60)
        let max_len = 60
    endif
    let max_len = max_len + 4

    let name_s_format = "%-" . max_len ."s"

    for item in name_list
        let [io_s,name_s] = split(item,",")
        let name_s = printf(name_s_format, name_s)

        "echo line_comp
        let name_out = "." . name_s . "(" . name_s . ")" . ",//" . io_s 
        "echo line_out
        let name_list_out = add(name_list_out,name_out)
    endfor
    return name_list_out
endfunction


"'''''''''''''''''''''''''''''''''''''''''''''''''''''''
"get module output port
"'''''''''''''''''''''''''''''''''''''''''''''''''''''''
function V_get_output_ports()
    exec "normal gg"
    /^\s*module
    let line_begin = line(".")
    /^\s*);
    let line_end = line(".")
    echo line_begin
    echo line_end

    let name_list = []
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
                
            if(io == "output") 
                echo name 
                let name_list = add(name_list,name)
                "echo name_list
             endif
        endif
    endfor

    return name_list
endfunction

"'''''''''''''''''''''''''''''''''''''''''''''''''''''''
"get module input port
"'''''''''''''''''''''''''''''''''''''''''''''''''''''''
function V_get_input_ports()
    exec "normal gg"
    /^\s*module
    let line_begin = line(".")
    /^\s*);
    let line_end = line(".")
    echo line_begin
    echo line_end

    let name_list = []
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
                
            if(io == "input") 
                echo name 
                let name_list = add(name_list,name)
                "echo name_list
             endif
        endif
    endfor

    return name_list
endfunction

"'''''''''''''''''''''''''''''''''''''''''''''''''''''''
"get module variable def(reg/wire)
"'''''''''''''''''''''''''''''''''''''''''''''''''''''''
function V_get_variable_def(line_begin,line_end)

    let line_begin = str2nr(a:line_begin)
    let line_end = str2nr(a:line_end)

    let name_list = []
    for i in range(line_begin, line_end)
        let line_str  = getline(i)
            "参考函数：match matchlist subtitute
        if (line_str =~ '^\s*\(reg\|wire\).*')
                let line_comp = matchlist(line_str,'\s*\(reg\|wire\)\s*\(signed\|\)\s*\(\[.*\]\|\)\s*\(\w\+\)\W*.*\s*\(;\)\s*\(\S.*\|\)\s*$')
               "echo line_comp
                let io      = ""
                let regw    = get(line_comp, 1)
                let signed  = get(line_comp, 2)
                let width   = get(line_comp, 3)
                let name    = get(line_comp, 4)
                let comma   = get(line_comp, 5)
                let other   = get(line_comp, 6)
                echo name 
                let name_list = add(name_list,name)
        endif
    endfor
    return name_list
endfunction


"'''''''''''''''''''''''''''''''''''''''''''''''''''''''
"get module all variable def with width information
"'''''''''''''''''''''''''''''''''''''''''''''''''''''''
function V_get_all_var_with_wid()
    exec "normal gg"
    /^\s*module
    let line_begin = line(".")
    /^\s*);
    let line_end = line(".")
    echo line_begin
    echo line_end

    let name_list = []
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

            let name_wid = name . width
            let name_wid_s = substitute(name_wid, " ", "", "g")
                
            let name_list = add(name_list,name_wid_s)
        elseif (line_str =~ '^\s*\(reg\|wire\).*')
                let line_comp = matchlist(line_str,'\s*\(reg\|wire\)\s*\(signed\|\)\s*\(\[.*\]\|\)\s*\(\w\+\)\W*.*\s*\(;\)\s*\(\S.*\|\)\s*$')
               "echo line_comp
                let io      = ""
                let regw    = get(line_comp, 1)
                let signed  = get(line_comp, 2)
                let width   = get(line_comp, 3)
                let name    = get(line_comp, 4)
                let comma   = get(line_comp, 5)
                let other   = get(line_comp, 6)

                let name_wid = name . width
                let name_wid_s = substitute(name_wid, " ", "", "g")
                    
                let name_list = add(name_list,name_wid_s)
        endif
    endfor

    return name_list
endfunction



"'''''''''''''''''''''''''''''''''''''''''''''''''''''''
"function use for module define wire/reg
"all use unsigned variable
"uw: unsigned wire
"ur: unsigned reg
" ///{auto-port-define-begin
"     ...port...
" ///}user-port-define-begin
"
" ///{user-variable-define-end
"    ... user define variable ...
" ///}user-variable-define-end
" 
" ///{auto-variable-define-begin
"    ... auto define variable ...
" ///}auto-variable-define-end
"
" assign xxx = yyy; ///{uw99}
" assign xxx = yyy; ///{uw<parameter>}
" assign xxx = yyy; ///user-deine-variable
" always ...
"  xxx = yyy; ///{ur99}
"  xxx = yyy; ///{ur<parameter>}
"  xxx = yyy; ///{uro99}
"  xxx = yyy; ///{uro<parameter>}
" always @(posedge ...
"  xxx <= yyy; ///{ur99}
"  xxx <= yyy; ///{ur<parameter>}
"  .a (xxxx), ///{uwi99}
"  .a (xxxx), ///{uwi<parameter>}
"  .a (xxxx), ///{uwo99}
"  .a (xxxx), ///{uwo<parameter>}
"
"  for more compilcate expression shall do user define "  ......   ///{user-define:option-width-info} "'''''''''''''''''''''''''''''''''''''''''''''''''''''''

nmap <Leader>vd :call V_module_variable_def()<CR>

function V_module_variable_def()
    ""delete auto output list =============================
    /^\s*\/\/\/{.*auto.*port.*define.*begin
    let line_def_begin = line(".")
    let line_def_begin_add1 = line_def_begin + 1
    /^\s*\/\/\/}.*auto.*port.*define.*end
    let line_def_end = line(".")
    exec ":" . line_def_begin_add1 . "," . line_def_end . "d"
    call append(line_def_begin, "\/\/\/}auto-port-define-end")

    ""delete auto variable list ===========================
    /^\s*\/\/\/{.*auto.*variable.*define.*begin
    let line_def_begin = line(".")
    let line_def_begin_add1 = line_def_begin + 1
    /^\s*\/\/\/}.*auto.*variable.*define.*end
    let line_def_end = line(".")
    exec ":" . line_def_begin_add1 . "," . line_def_end . "d"
    call append(line_def_begin, "\/\/\/}auto-variable-define-end")

    " get user-define signal list==========================
    let module_output_port_list = []
    let module_output_port_list = V_get_output_ports()
    let module_input_port_list = []
    let module_input_port_list = V_get_input_ports()

    /^\s*\/\/\/{.*user.*variable.*define.*begin
    let line_begin = line(".")
    /^\s*\/\/\/}.*user.*variable.*define.*end
    let line_end = line(".")
    let module_user_def_var = []
    let module_user_def_var = V_get_variable_def(line_begin, line_end)

    echo module_input_port_list
    echo module_output_port_list
    echo module_user_def_var

    ""signal generate =====================================
    exec "normal gg"
    let line_begin = line(".")
    exec "normal G"
    let line_end = line(".")
    echo line_begin
    echo line_end
    let name_s = ""
    let v_type = ""
    let name_list = []
    let name_list_output_port = []
    let name_list_input_port = []
    " get all variable define information
    for i in range(line_begin, line_end)
        let line_str = getline(i)
        ""assign express 1==========================================
        if(line_str =~ '^\s*assign.*=.*{uw\d\+}.*')
            let line_comp = matchlist(line_str, '^\s*assign\s\+\(\w\+\)\W*.*=.*.*\/\/.*{uw\(\d\+\)}.*')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,2)
            let v_type = "wire"

            let width_nr = str2nr(width)
            if(width_nr ==1)
                let width_str = ""
            else 
                let width_out = width_nr -1
                let width_str = printf("[%3s:0]",width_out)
            endif

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            " if (index(module_output_port_list, name_s) == -1)
            if (index(module_user_def_var, name_s) >= 0)
                echo name_s . ":: is already user defined"
            else 
                let name_s = printf('%-5s %-20s %-40s ;',v_type, width_str, name_s)
                call add(name_list,name_s)
            endif
        ""assign express 2: parameter ==============================
        elseif(line_str =~ '^\s*assign.*=.*{uw<.*>}.*')
            let line_comp = matchlist(line_str, '^\s*assign\s\+\(\w\+\)\W*.*=.*.*\/\/.*{uw<\(.*\)>}.*')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,2)
            let v_type = "wire"

            let width_str = printf("[%5s -1:0]",width)

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_user_def_var, name_s) >= 0)
                echo name_s . ":: is already user defined"
            else 
                let name_s = printf('%-5s %-20s %-40s ;',v_type, width_str, name_s)
                call add(name_list,name_s)
            endif
        ""assign express 3: output    ==============================
        elseif(line_str =~ '^\s*assign.*=.*{uwo\d\+}.*')
            let line_comp = matchlist(line_str, '^\s*assign\s\+\(\w\+\)\W*.*=.*.*\/\/.*{uwo\(\d\+\)}.*')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,2)
            let v_type = ""

            let width_nr = str2nr(width)
            if(width_nr ==1)
                let width_str = ""
            else 
                let width_out = width_nr -1
                let width_str = printf("[%3s:0]",width_out)
            endif

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            " if (index(module_output_port_list, name_s) == -1)
            if (index(module_output_port_list, name_s) >= 0)
                echo name_s . ":: is already output port"
            else 
                let name_s = printf('output %-5s %-20s %-40s ,',v_type, width_str, name_s)
                call add(name_list_output_port,name_s)
            endif
        ""assign express 3: output with parameter ==================
        elseif(line_str =~ '^\s*assign.*=.*{uwo<.*>}.*')
            let line_comp = matchlist(line_str, '^\s*assign\s\+\(\w\+\)\W*.*=.*.*\/\/.*{uwo<\(.*\)>}.*')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,2)
            let v_type = "wire"

            let width_str = printf("[%5s -1:0]",width)

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_output_port_list, name_s) >= 0)
                echo name_s . ":: is alreasy output port"
            else 
                let name_s = printf('output %-5s %-20s %-40s ,',v_type, width_str, name_s)
                call add(name_list_output_port,name_s)
            endif
        ""always express 1: ========================================
        "expression as follow not supported
        "aaa:d21_x[WID*A-1:0]  <=   xxxx  ;//{ur....}
        elseif(line_str =~ '^.*[:]\s*\w\+\s*[<]*=.*{ur\d\+}.*')
            let line_comp = matchlist(line_str, '^.*[:]\s*\(\w\+\)\s*\(=\|<=\).*.*\/\/.*{ur\(\d\+\)}.*')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,3)
            let v_type = "reg"

            let width_nr = str2nr(width)
            if(width_nr ==1)
                let width_str = ""
            else 
                let width_out = width_nr -1
                let width_str = printf("[%3s:0]",width_out)
            endif

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_user_def_var, name_s) >= 0)
                echo name_s . ":: is already user defined"
            else 
                let name_s = printf('%-5s %-20s %-40s ;',v_type, width_str, name_s)
                call add(name_list,name_s)
            endif
        elseif(line_str =~ '^\s*\w\+.*=.*{ur\d\+}.*')
            let line_comp = matchlist(line_str, '^\s*\(\w\+\)\W*.*\s*\(=\|<=\).*.*\/\/.*{ur\(\d\+\)}.*')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,3)
            let v_type = "reg"

            let width_nr = str2nr(width)
            if(width_nr ==1)
                let width_str = ""
            else 
                let width_out = width_nr -1
                let width_str = printf("[%3s:0]",width_out)
            endif

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_user_def_var, name_s) >= 0)
                echo name_s . ":: is already user defined"
            else 
                let name_s = printf('%-5s %-20s %-40s ;',v_type, width_str, name_s)
                call add(name_list,name_s)
            endif
        ""always express 2: parameter ==============================
        elseif(line_str =~ '^.*[:]\s*\w\+\s*[<]*=.*{ur<.*>}.*')
            let line_comp = matchlist(line_str, '^.*[:]\s*\(\w\+\)\s*\(=\|<=\).*.*\/\/.*{ur<\(.*\)>}.*')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,3)
            let v_type = "reg"

            let width_str = printf("[%5s -1:0]",width)

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_user_def_var, name_s) >= 0)
                echo name_s . ":: is already user defined"
            else 
                let name_s = printf('%-5s %-20s %-40s ;',v_type, width_str, name_s)
                call add(name_list,name_s)
            endif
        elseif(line_str =~ '^\s*\w\+.*=.*{ur<.*>}.*')
            let line_comp = matchlist(line_str, '^\s*\(\w\+\)\W*.*\s*\(=\|<=\).*.*\/\/.*{ur<\(.*\)>}.*')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,3)
            let v_type = "reg"

            let width_str = printf("[%5s -1:0]",width)

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_user_def_var, name_s) >= 0)
                echo name_s . ":: is already user defined"
            else 
                let name_s = printf('%-5s %-20s %-40s ;',v_type, width_str, name_s)
                call add(name_list,name_s)
            endif
        ""always express 3: output =================================
        elseif(line_str =~ '^.*[:]\s*\w\+\s*[<]*=.*{uro\d\+}.*')
            let line_comp = matchlist(line_str, '^.*[:]\s*\(\w\+\)\s*\(=\|<=\).*\/\/.*{uro\(\d\+\)}.*')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,3)
            let v_type = "reg"

            let width_nr = str2nr(width)
            if(width_nr ==1)
                let width_str = ""
            else 
                let width_out = width_nr -1
                let width_str = printf("[%3s:0]",width_out)
            endif

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_output_port_list, name_s) >= 0)
                echo name_s . ":: is already output port"
            else 
                let name_s = printf('output %-5s %-20s %-40s ,',v_type, width_str, name_s)
                call add(name_list_output_port,name_s)
            endif
        elseif(line_str =~ '^\s*\w\+.*=.*{uro\d\+}.*')
            let line_comp = matchlist(line_str, '^\s*\(\w\+\)\W*.*\s*\(=\|<=\).*\/\/.*{uro\(\d\+\)}.*')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,3)
            let v_type = "reg"

            let width_nr = str2nr(width)
            if(width_nr ==1)
                let width_str = ""
            else 
                let width_out = width_nr -1
                let width_str = printf("[%3s:0]",width_out)
            endif

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_output_port_list, name_s) >= 0)
                echo name_s . ":: is already output port"
            else 
                let name_s = printf('output %-5s %-20s %-40s ,',v_type, width_str, name_s)
                call add(name_list_output_port,name_s)
            endif


        ""always express 4: output with parameter ==================
        elseif(line_str =~ '^.*[:]\s*\w\+\s*[<]*=.*{uro<.*>}.*')
            let line_comp = matchlist(line_str, '^.*[:]\s*\(\w\+\)\s*\(=\|<=\).*\/\/.*{uro<\(.*\)>}.*')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,3)
            let v_type = "reg"

            let width_str = printf("[%5s -1:0]",width)

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_output_port_list, name_s) >= 0)
                echo name_s . ":: is already output port"
            else 
                let name_s = printf('output %-5s %-20s %-40s ,',v_type, width_str, name_s)
                call add(name_list_output_port,name_s)
            endif
        elseif(line_str =~ '^\s*\w\+.*=.*{uro<.*>}.*')
            let line_comp = matchlist(line_str, '^\s*\(\w\+\)\W*.*\s*\(=\|<=\).*\/\/.*{uro<\(.*\)>}.*')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,3)
            let v_type = "reg"

            let width_str = printf("[%5s -1:0]",width)

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_output_port_list, name_s) >= 0)
                echo name_s . ":: is already output port"
            else 
                let name_s = printf('output %-5s %-20s %-40s ,',v_type, width_str, name_s)
                call add(name_list_output_port,name_s)
            endif
        ""module instance for connect: from input port ================
        ""if not from input, must be define from always or assign
        elseif(line_str =~ '^\s*\..*(.*).*\/\/.*{uwi\d\+}.*')
            let line_comp = matchlist(line_str, '^\s*\.\s*\w\+\s*(\s*\(\w\+\)\W*.*).*\/\/.*{uwi\(\d\+\)}.*$')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,2)
            let v_type = ""

            let width_nr = str2nr(width)
            if(width_nr ==1)
                let width_str = ""
            else 
                let width_out = width_nr -1
                let width_str = printf("[%3s:0]",width_out)
            endif

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_input_port_list, name_s) >= 0)
                echo name_s . ":: is already input port"
            else 
                let name_s = printf('input  %-5s %-20s %-40s ,',v_type, width_str, name_s)
                call add(name_list_input_port,name_s)
            endif

        ""module instance for connect: from input port, with parameter =======
        ""if not from input, must be define from always or assign
        elseif(line_str =~ '^\s*\..*(.*).*\/\/.*{uwi<.*>}.*')
            let line_comp = matchlist(line_str, '^\s*\.\s*\w\+\s*(\s*\(\w\+\)\W*.*).*\/\/.*{uwi<\(.*\)>}.*$')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,2)
            let v_type = ""

            let width_str = printf("[%5s -1:0]",width)

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_input_port_list, name_s) >= 0)
                echo name_s . ":: is already input port"
            else 
                let name_s = printf('input  %-5s %-20s %-40s ,',v_type, width_str, name_s)
                call add(name_list_input_port,name_s)
            endif

        ""module instance for connect 1: variable define =====================
        elseif(line_str =~ '^\s*\..*(.*).*\/\/.*{uw\d\+}.*')
            let line_comp = matchlist(line_str, '^\s*\.\s*\w\+\s*(\s*\(\w\+\)\W*.*).*\/\/.*{uw\(\d\+\)}.*$')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,2)
            let v_type = "wire"

            let width_nr = str2nr(width)
            if(width_nr ==1)
                let width_str = ""
            else 
                let width_out = width_nr -1
                let width_str = printf("[%3s:0]",width_out)
            endif

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_user_def_var, name_s) >= 0)
                echo name_s . ":: is already user defined"
            else 
                let name_s = printf('%-5s %-20s %-40s ;',v_type, width_str, name_s)
                call add(name_list,name_s)
            endif

        ""module instance for connect 2: variable define with parameter ======
        elseif(line_str =~ '^\s*\..*(.*).*\/\/.*{uw<.*>}.*')
            let line_comp = matchlist(line_str, '^\s*\.\s*\w\+\s*(\s*\(\w\+\)\W*.*).*\/\/.*{uw<\(.*\)>}.*$')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,2)
            let v_type = "wire"

            let width_str = printf("[%5s -1:0]",width)

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_user_def_var, name_s) >= 0)
                echo name_s . ":: is already user defined"
            else 
                let name_s = printf('%-5s %-20s %-40s ;',v_type, width_str, name_s)
                call add(name_list,name_s)
            endif
        ""module instance for connect 3: variable define =====================
        ""if not from input, must be define from always or assign
        elseif(line_str =~ '^\s*\..*(.*).*\/\/.*{uwo\d\+}.*')
            let line_comp = matchlist(line_str, '^\s*\.\s*\w\+\s*(\s*\(\w\+\)\W*.*).*\/\/.*{uwo\(\d\+\)}.*$')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,2)
            let v_type = ""

            let width_nr = str2nr(width)
            if(width_nr ==1)
                let width_str = ""
            else 
                let width_out = width_nr -1
                let width_str = printf("[%3s:0]",width_out)
            endif

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_output_port_list, name_s) >= 0)
                echo name_s . ":: is already output port"
            else 
                let name_s = printf('output %-5s %-20s %-40s ,',v_type, width_str, name_s)
                call add(name_list_output_port,name_s)
            endif

        ""module instance for connect 4: variable define with parameter ======
        elseif(line_str =~ '^\s*\..*(.*).*\/\/.*{uwo<.*>}.*')
            let line_comp = matchlist(line_str, '^\s*\.\s*\w\+\s*(\s*\(\w\+\)\W*.*).*\/\/.*{uwo<\(.*\)>}.*$')
            let name_s = get(line_comp,1)
            let width  = get(line_comp,2)
            let v_type = ""

            let width_str = printf("[%5s -1:0]",width)

            " check if variable is output or not 
            " if index(xxx) = -1, mean not in list, if >=0 in list
            if (index(module_output_port_list, name_s) >= 0)
                echo name_s . ":: is already output port "
            else 
                let name_s = printf('output %-5s %-20s %-40s ,',v_type, width_str, name_s)
                call add(name_list_output_port,name_s)
            endif
        endif 
    endfor

    "echo name_list
    "echo name_list_input_port
    "echo name_list_output_port
    "generate or refresh variable define
    /^\s*\/\/\/{.*auto.*port.*define.*begin
    let line_def_begin = line(".")
    call append(line_def_begin, name_list_output_port)
    call append(line_def_begin, name_list_input_port)

    /^\s*\/\/\/{.*auto.*variable.*define.*begin
    let line_def_begin = line(".")
    call append(line_def_begin, name_list)
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" Veriolg chk module instance used signal bit match with defined or not
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function V_chk_bit_mat()
    let module_var_list=[]
    let var_width_unmatch_list=[]
    let module_var_list=V_get_all_var_with_wid()

    for S_VAR in module_var_list
        let s_var_re = matchlist(S_VAR, '\(\w\+\)\(\[.*\]\|\)')
        let S_VAR_RAW = s_var_re[1]
        "search match S_VAR_RAW word line only
        let S_VAR_RAW_RE = "^\\s*.\\w\\+.*(.*\\<" . S_VAR_RAW . "\\>"

        exec "normal gg"

        while search(S_VAR_RAW_RE, "W") > 0
            "search until the end of file
            let line_inst = getline(line("."))
            if(line_inst =~ '^\s*.\w\+\s*(')   "only inst line checkd
                let s_inst_re = "^\\s*.\\w\\+\\s*(\\s*.*\\(" . S_VAR_RAW . "\\)\\s*\\(\\[[^\\[\\]]*\\]\\|\\).*)"
                let s_inst_str_match = matchlist(line_inst, s_inst_re)
                let inst_var_name = s_inst_str_match[1]
                let inst_var_width = s_inst_str_match[2]

                let inst_var_name_wid = inst_var_name . inst_var_width
                "remove string space
                let inst_var_name_wid = substitute(inst_var_name_wid, " ", "", "g")

                if(S_VAR != inst_var_name_wid)
                    let line_num = line(".")
                    let inst_var_unmatch_info = printf("line: %7d,  variable inst used: %s, variable defined as: %s", line_num, inst_var_name_wid, S_VAR)
                    let var_width_unmatch_list = add(var_width_unmatch_list, inst_var_unmatch_info)
                endif
            endif
        endwhile
    endfor

    :new chk_unmatch.log
    :b chk_unmatch.log
    call append(0, var_width_unmatch_list)
endfunction



