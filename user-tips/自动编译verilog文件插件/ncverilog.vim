" Compiler:Ncverilog

" Only do this when not done yet for this buffer
if exists("current_compiler")
    finish
endif

" Don't load another plugin for this buffer
let current_compiler = 'ncverilog'

if exists(":CompilerSet") !=2
  command -nargs=* CompilerSet setlocal <args>
endif


" Save the compatibility options and temporarily switch to vim defaults
let s:cpo_save = &cpoptions
set cpoptions -=C

set makeprg=irun\ -nohistory\ -nolog\ -clean\ -ntcnotchks\ -q\ -nocopyright\ -c
"error level format
CompilerSet erroformat = %.%#:\ *%t\\,%.%#\ %#\(%f\\,%l\|%c\):\ %m
CompilerSet erroformat += %.%#:\ *%t\\,%.%#\ %#\(%f\\,%l\):\ %m
"multi line format
CompilerSer erroformat += %A%.%#\ *%t\\,%.%#:\ %m,%ZFile:\ %f\\,\ line\ =\ %l\\,\ pos\ =\ %c 

"ignore warning
if (exists("g:verilog_err_level")&&(g:verilog_err_level == "error"))
    CompilerSet erroformat ^= %-G%.%#\ *W\\,%.%#:\ %m
endif

" Restore saved compatibility options
let &cpoptions = s:cpo_save
unlet s:cpo_save
