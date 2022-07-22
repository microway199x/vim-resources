"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"进行版权声明的设置
"添加或更新头
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
map <F4> :call TitleDet()<cr>'s
function AddTitle()
    call append(0,"/*========================================================= ")
    call append(1,"author : Micro")
    call append(2,"version :  #0.01 as first version ")
    call append(3,"modify engineer &　date : " .strftime("%y-%m-%d  %H:%M"))
    call append(4,"filename : " .expand("%:t"))
    call append(5,"function describe : " )
    call append(6,"==========================================================*/")
    echohl WarningMsg | echo "Successful in adding the copyright." | echohl None
endf
"更新最近修改时间和文件名
function UpdateTitle()
     "标记当前按位置，normal表示是normal状态下的命令
    normal m' 
    execute '/# *Last modified:/s@:.*$@\=strftime(":\t%Y-%m-%d %H:%M")@'
    "跳回标记位置
    normal '' 
    normal mk
    execute '/# *Filename:/s@:.*$@\=":\t\t".expand("%:t")@'
    execute "noh"
    normal 'k
    echohl WarningMsg | echo "Successful in updating the copy right." | echohl None
endfunction
"判断前10行代码里面，是否有Last modified这个单词，
"如果没有的话，代表没有添加过作者信息，需要新添加；
"如果有的话，那么只需要更新即可
function TitleDet()
    let n=1
    "默认为添加
    while n < 7
        let line = getline(n)
        "let line = getline(.)  " . 表示光标所在行，当前行
        if line =~ '^\#\s*\S*Last\smodified:\S*.*$'
            call UpdateTitle()
            return
        endif
        let n = n + 1
    endwhile
    call AddTitle()
endfunction

