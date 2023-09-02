"""
" https://my.oschina.net/u/2520885
"""
"===============================================================================
" Copyright (C) 2016 by Jun Cao

" Permission is hereby granted, free of charge, to any person obtaining a copy
" of this software and associated documentation files (the "Software"), to deal
" in the Software without restriction, including without limitation the rights
" to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
" copies of the Software, and to permit persons to whom the Software is
" furnished to do so, subject to the following conditions:

" The above copyright notice and this permission notice shall be included in
" all copies or substantial portions of the Software.

" THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
" IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
" FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
" AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
" LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
" OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
" THE SOFTWARE.
"===============================================================================

function! VimPythonExtend() 
python << EOF
import os
import sys
vtags_install_path = ""
if os.path.isdir(vtags_install_path):
    sys.path.insert(0,vtags_install_path)
    from Lib.API import *
EOF
endfunction

let is_vtags_installed = 1

if is_vtags_installed == 1
    "vi_HDLTags_begin-----------------------------------
    call VimPythonExtend()
    map gi                   :py try_go_into_submodule()           <CR>
    map gu                   :py try_go_upper_module()             <CR>
    map <Space><Left>        :py try_trace_signal_sources()        <CR>
    map <Space><Right>       :py try_trace_signal_destinations()   <CR>
    map <Space><Down>        :py try_roll_back()                   <CR>
    map <Space><Up>          :py try_go_forward()                  <CR>
    map <Space>v             :py try_show_frame()                  <CR> 
    map <Space>c             :py try_add_check_point()             <CR> 
    map <Space>b             :py try_add_base_module()             <CR> 
    map <Space>              :py try_space_operation()             <CR>
    map <Space>h             :py try_hold_current_win()            <CR>
    map <Space>d             :py try_del_operation()               <CR>
    map <Space>s             :py try_save_env_snapshort()          <CR>
    "vi_HDLTags_end-------------------------------------
endif
