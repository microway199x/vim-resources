"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"进行版权声明的设置
"添加或更新头
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
map <F4> :call TitleDet()<cr>'s
function AddTitle()
    call append(0,"/////////////////////////////////////////////////////////// ")
    call append(1,"///author : Micro")
    call append(2,"///initial version :  #0.01 as first version ")
    call append(3,"///initial date :  " . strftime("%y-%m-%d  %H:%M"))
    call append(4,"///modify engineer : " )
    call append(5,"///modify date : " . strftime("%y-%m-%d  %H:%M"))
    call append(6,"///modify version : " )
    call append(7,"///filename : " .expand("%:t"))
    call append(8,"///function describe : " )
    call append(9,"/// " )
    call append(10,"////////////////////////////////////////////////////////////")
    echohl WarningMsg | echo "Successful in adding the copyright." | echohl None
endf

"更新最近修改时间和文件名
function UpdateTitle()
     "标记当前按位置，normal表示是normal状态下的命令
    normal m' 
    execute '/modify date/s@:.*@\=": ". strftime("%y-%m-%d  %H:%M")@'
    "跳回标记位置
    normal '' 
    normal mk
    execute '/filename/s@:.*@\=": " .expand("%:t")@'
    normal 'k
    echohl WarningMsg | echo "Successful in updating the copy right." | echohl None
endfunction
"判断前10行代码里面，是否有Last modified这个单词，
"如果没有的话，代表没有添加过作者信息，需要新添加；
"如果有的话，那么只需要更新即可

function TitleDetc()
    let n=0
    "默认为添加
    while n < 11
        let line = getline(n)
        "let line = getline(.)  " . 表示光标所在行，当前行
        if line =~ 'modify date'
            call UpdateTitle()
            return
        endif
        let n = n + 1
    endwhile
    call AddTitle()
endfunction




"if path has space, use path/aaa\ bbb/xxx
"use read command: help read, to learn more
"NUMread: insert file content after NUM line
"read: insert file content after current cursor line
function AddVerilogTpl()
    :0read  $VIM/micro-config/file_tpl/verilog.tpl
    call AddTitle()
endfunction

" autocmd Bufxxx *.v,*.sv,*.c command   " more than one file type must not has
" space, shall only use  "," split
autocmd BufNewFile *.v,*.sv  call AddVerilogTpl()
autocmd BufNewFile *.lua  :0r $VIM/micro-config/file_tpl/lua.tpl
autocmd BufNewFile *.py  :0r $VIM/micro-config/file_tpl/python.tpl




