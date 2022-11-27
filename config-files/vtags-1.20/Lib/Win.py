"""
https://my.oschina.net/u/2520885
"""
#===============================================================================
# Copyright (C) 2016 by Jun Cao

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#===============================================================================

try:
    import vim
except: 
    pass
import sys
import re
import os
import GLB
G = GLB.G
from Base import *

def Reset_Win_Size():
    cur_act_wins = Cur_Act_Win()
    if G['Report_Inf']['Report_Path'] in cur_act_wins:
        Jump_To_Win(G['Report_Inf']['Report_Path'])
        vim.command('wincmd J')
        vim.current.window.height = G['Report_Inf']['Report_Win_y']
    if G['Frame_Inf']['Frame_Path'] in cur_act_wins:
        Jump_To_Win(G['Frame_Inf']['Frame_Path'])
        vim.command('wincmd H')
        vim.current.window.width = G['Frame_Inf']['Frame_Win_x']
    return

def Refresh_OpenWinTrace():
    cur_act_win_path      = Cur_Act_Win()
    cur_act_work_win_path = cur_act_win_path - set([ G["Report_Inf"]["Report_Path"], G["Frame_Inf"]["Frame_Path"] ])
    i = 0
    while i < len(G['WorkWin_Inf']['OpenWinTrace']) :
        c_path = G['WorkWin_Inf']['OpenWinTrace'][i]
        if c_path not in cur_act_work_win_path:
            del G['WorkWin_Inf']['OpenWinTrace'][i]
        else:
            i += 1
    return

def Cur_Act_Win():
    Act_Win = set()
    for w in vim.windows:
        Act_Win.add(w.buffer.name)
    return Act_Win

def Open(name):
    path = get_path_for_name(name)
    Act_Win = Cur_Act_Win()
    if path in Act_Win: # win has open and just jump to than window
        Jump_To_Win(path)
    elif path == G['Frame_Inf']["Frame_Path"]:
        Open_Frame_Win()
    elif path == G['Report_Inf']["Report_Path"]:
        Open_Report_Win()
    else:
        Open_Work_Win(path)
    Reset_Win_Size()
    Jump_To_Win(path)
    assert(vim.current.buffer.name == path)

def Jump_To_Win(path):
    cur_act_wins = Cur_Act_Win()
    assert(path in cur_act_wins)
    start_path = vim.current.buffer.name
    if start_path == path:
        return
    vim.command('wincmd w')
    cur_path = vim.current.buffer.name
    while cur_path != start_path:
        if cur_path == path:
            break
        vim.command("wincmd w")
        cur_path = vim.current.buffer.name
    assert(vim.current.buffer.name == path),'vim.current.buffer.name: %s, path: %s'%(vim.current.buffer.name, path)

def Open_Frame_Win():
    G['VimBufferLineFileLink'].setdefault(G["Frame_Inf"]["Frame_Path"],[{}])
    vim.command("vertical topleft sp " + G["Frame_Inf"]["Frame_Path"])

def Open_Report_Win():
    G['VimBufferLineFileLink'].setdefault(G["Report_Inf"]["Report_Path"],[{}])
    vim.command("bot sp " + G["Report_Inf"]["Report_Path"])
    if G["Frame_Inf"]["Frame_Path"] in Cur_Act_Win():
        Jump_To_Win(G["Frame_Inf"]["Frame_Path"])
    vim.command('wincmd H')
    Jump_To_Win(G["Report_Inf"]["Report_Path"])

def Open_Work_Win(path):
    # path must valid
    assert(os.path.isfile(path))
    # refresh open work win trace
    Refresh_OpenWinTrace()
    # leave at most G['WorkWin_Inf']['MaxNum'] work win
    win_num_need_to_close = len(G['WorkWin_Inf']['OpenWinTrace']) - G['WorkWin_Inf']['MaxNum']
    for i in range(win_num_need_to_close):
        win_path_need_close = G['WorkWin_Inf']['OpenWinTrace'][i]
        Jump_To_Win(win_path_need_close)
        vim.command('q')
        del G['WorkWin_Inf']['OpenWinTrace'][i]
    # if has work win
    cur_work_win_num = len(G['WorkWin_Inf']['OpenWinTrace'])
    if cur_work_win_num > 0:
        # case 0: has work win, and num less than max
        #         just go last work win, and vsp a new win
        if cur_work_win_num < G['WorkWin_Inf']['MaxNum']:
            Jump_To_Win(G['WorkWin_Inf']['OpenWinTrace'][-1])
            vim.command('vsp '+path)
        else: # case 1: opened all work win, just replace the oldest open work win
            Jump_To_Win(G['WorkWin_Inf']['OpenWinTrace'][0])
            vim.command('e '+path)
            del G['WorkWin_Inf']['OpenWinTrace'][0] # replace [0], just del old
    else: # cur no work win
        cur_act_win_paths = Cur_Act_Win()
        cur_act_hold_wins = cur_act_win_paths - set([G["Report_Inf"]["Report_Path"], G["Frame_Inf"]["Frame_Path"]])
        # if has hold win, go hold win, vsp
        if cur_act_hold_wins:
            Jump_To_Win(list(cur_act_hold_wins)[0])
            vim.command('vsp '+path)
        elif G["Report_Inf"]["Report_Path"] in cur_act_win_paths:
            # if no hold win, has report , go report sp new
            Jump_To_Win(G["Report_Inf"]["Report_Path"])
            vim.command('sp '+path)
        else:
            vim.command('vsp '+path)
    # finial add path to trace
    assert(vim.current.buffer.name == path)
    G['WorkWin_Inf']['OpenWinTrace'].append(path)

def get_file_vim_buffer(path):
    for i,b in enumerate(vim.buffers):
        if b.name == path:
            return b
    # path buffer not open
    vim.command("bad "+path)
    assert(vim.buffers[ len(vim.buffers) - 1].name == path)
    return vim.buffers[ len(vim.buffers) - 1]

# edit the vim buffer, with put data at some position
# mode : a --after     : append data after current buffer data
#        b --before    : append data before current buffer data
#        w --write     : clear old buffer data, and write data
#        i --insert    : inster list to n
#        del -- delete : delete del_range lines
#        del_range     : (start,end) del range, include end 
def edit_vim_buffer(path_or_name = '', data = [], file_links = [], mode = 'a', n = 0, del_range = ()):
    # weather to edit link buffer
    need_edit_buffer_file_link = False
    if data == [] and mode != 'del':
        PrintDebug('Warning: edit_vim_buffer: edit file with empty data= [], file:%s !'%(path_or_name))
        return
    if type(data) is str:
        data = [data]
    path = get_path_for_name(path_or_name)
    # some time edit other buffer, may change cur window cursor or add empty line to cur buffer file,
    # so must edit current buffer
    assert(vim.current.buffer.name == path),'%s,%s'%(vim.current.buffer.name, path)
    if path in [G['Report_Inf']['Report_Path'], G['Frame_Inf']['Frame_Path']]:
        need_edit_buffer_file_link = True
        if file_links:
            assert(len(data) == len(file_links))
        else:
            file_links = [ {} for i in range(len(data))]
    # PrintDebug('edit_vim_buffer path_or_name:'+path_or_name)
    # PrintDebug('edit_vim_buffer data:'+data.__str__())
    # PrintDebug('edit_vim_buffer file_links:'+file_links.__str__())
    # PrintDebug('edit_vim_buffer mode:'+mode.__str__())
    # PrintDebug('edit_vim_buffer n:'+n.__str__())
    # PrintDebug('edit_vim_buffer del_range:'+del_range.__str__())
    t_buffer = get_file_vim_buffer(path)
    assert(t_buffer)
    if mode is 'w':
        del t_buffer[:]
        t_buffer.append(data)
        del t_buffer[:1]
        if need_edit_buffer_file_link:
            G["VimBufferLineFileLink"][path] = file_links
    elif mode is 'a':
        t_buffer.append(data)
        if need_edit_buffer_file_link:
            G["VimBufferLineFileLink"].setdefault(path,[])
            G["VimBufferLineFileLink"][path] = G["VimBufferLineFileLink"][path] + file_links 
    elif mode is 'b':
        t_buffer.append(data, 0)
        if need_edit_buffer_file_link:
            G["VimBufferLineFileLink"].setdefault(path,[])
            G["VimBufferLineFileLink"][path] = file_links + G["VimBufferLineFileLink"][path]  
    elif mode is 'i':
        while len(t_buffer) <= n+1:
            t_buffer.append('')
            if need_edit_buffer_file_link:
                G["VimBufferLineFileLink"][path].append({})
        t_buffer.append(data, n)
        if need_edit_buffer_file_link:
            G["VimBufferLineFileLink"].setdefault(path,[])
            G["VimBufferLineFileLink"][path] = G["VimBufferLineFileLink"][path][:n] + file_links + G["VimBufferLineFileLink"][path][n:]
    elif mode is 'del':
        assert(del_range != () )
        if type(del_range) is int:
            del t_buffer[del_range]
            del G["VimBufferLineFileLink"][path][del_range]
        elif type(del_range) in [ tuple, list ]:
            del t_buffer[del_range[0]:del_range[1]+1]
            del G["VimBufferLineFileLink"][path][del_range[0]:del_range[1]+1]
        else:
            assert(0)

def go_win( path_or_name = '', pos = (), search_word = ''):
    if not path_or_name:
        return
        # path_or_name = vim.current.buffer.name
    Open(path_or_name)
    if re.search('\w+',search_word):
        vim.current.window.cursor = (1,0) # search from top in case match to left vim warning
        vim.command('/\c\<'+search_word+'\>')
    if pos:
        cursor = (pos[0]+1, pos[1])
        vim.current.window.cursor = cursor

############################################################################