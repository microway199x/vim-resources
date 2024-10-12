"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"���а�Ȩ����������
"��ӻ����ͷ
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

"��������޸�ʱ����ļ���
function UpdateTitle()
     "��ǵ�ǰ��λ�ã�normal��ʾ��normal״̬�µ�����
    normal m' 
    execute '/modify date/s@:.*@\=": ". strftime("%y-%m-%d  %H:%M")@'
    "���ر��λ��
    normal '' 
    normal mk
    execute '/filename/s@:.*@\=": " .expand("%:t")@'
    normal 'k
    echohl WarningMsg | echo "Successful in updating the copy right." | echohl None
endfunction
"�ж�ǰ10�д������棬�Ƿ���Last modified������ʣ�
"���û�еĻ�������û����ӹ�������Ϣ����Ҫ����ӣ�
"����еĻ�����ôֻ��Ҫ���¼���

function TitleDetc()
    let n=0
    "Ĭ��Ϊ���
    while n < 11
        let line = getline(n)
        "let line = getline(.)  " . ��ʾ��������У���ǰ��
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




