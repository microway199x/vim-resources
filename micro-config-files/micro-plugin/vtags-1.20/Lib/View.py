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

import sys
import re
try:
    import vim
except: 
    pass
import os
import re
from Base import *
from Win import *
import GLB
G = GLB.G

#--------------------------------------
SnapshotStack = []

def snapshort_push():
    cur_cursor        = vim.current.window.cursor
    cur_pos           = (cur_cursor[0]-1, cur_cursor[1]) # minus 1 because cursor start from 1, and lines start from 0
    cur_line_num      = cur_pos[0] 
    cur_line          = vim.current.buffer[cur_line_num]
    cur_word          = get_full_word(cur_line, cur_pos[1])
    cur_file_path     = vim.current.buffer.name
    cur_snapshort     = {"path": cur_file_path, "pos":cur_pos, "key":cur_word}
    SnapshotStack.append(cur_snapshort)

def snapshort_pop():
    pop_snapshort = SnapshotStack[-1]
    del SnapshotStack[-1]
    go_win( pop_snapshort['path'], pop_snapshort['pos'], pop_snapshort['key'])
#--------------------------------------

def Show(path): # just show frame win , and not go to that window
    path    = get_path_for_name(path)
    Act_Win = Cur_Act_Win()
    if path not in Act_Win:
        snapshort_push()
        Open(path)
        snapshort_pop()
    return

#--------------------------------------

def add_trace_point():
    cur_cursor        = vim.current.window.cursor
    cur_file_path     = vim.current.buffer.name
    if cur_file_path in [ G['Frame_Inf']['Frame_Path'], G['Report_Inf']['Report_Path'] ]:
        PrintDebug('Warning: Frame and Report not add trace point !')
        return
    cur_pos           = (cur_cursor[0]-1, cur_cursor[1]) # minus 1 because cursor start from 1, and lines start from 0
    cur_line_num      = cur_pos[0] 
    cur_line          = vim.current.buffer[cur_line_num]
    cur_word          = get_full_word(cur_line, cur_pos[1])
    cur_trace_point   = {"path": cur_file_path, "pos":cur_pos, "key":cur_word}
    cur_nonius        = G['OpTraceInf']['Nonius']
    TracePoints       = G['OpTraceInf']['TracePoints']
    # when roll back, and add from middle of queue, just clear old trace point after cur insert index
    # |  0  |  1  |  2  |  3  |  4  |
    #                      ^           if len 5, nonius <= 3 then del 4 
    if cur_nonius <= (len(TracePoints) - 2):
        del TracePoints[cur_nonius + 1 : ]
    # add a new point to TracePoints
    # if cur add is equ to pre not add
    if not TracePoints:
        TracePoints.append(cur_trace_point)
    else:
        pre_point = TracePoints[-1]
        if cur_trace_point != pre_point:
            TracePoints.append(cur_trace_point)
    # if length bigger than TraceDepth del 
    TraceDepth        = G['OpTraceInf']['TraceDepth']
    while (len(TracePoints) > TraceDepth):
        del TracePoints[0]
    # if add new point ,nonius assign to len(TracePoints)
    # |  0  |  1  |  2  |  3  |  4  |
    #                                 ^  because roll back will first sub 1
    G['OpTraceInf']['Nonius'] = len(TracePoints)


def get_cur_cursor_inf():
    cur_cursor       = vim.current.window.cursor
    cur_line_num     = cur_cursor[0] - 1 # minus 1 because cursor start from 1, and lines start from 0
    cur_colm_num     = cur_cursor[1]
    cur_line         = vim.current.buffer[cur_line_num]
    cur_word         = get_full_word(cur_line, cur_cursor[1])
    cur_codes        = vim.current.buffer
    cur_file_path    = vim.current.buffer.name
    cur_hdl_type     = get_file_hdl_type(cur_file_path)
    cur_call_sub_inf = {}
    cur_module_inf   = {}
    cur_line_inf     = get_file_line_inf(cur_line_num, cur_file_path)
    if cur_line_inf:
        cur_call_sub_inf = cur_line_inf['line_call_sub_inf']
        cur_module_inf   = cur_line_inf['line_module_inf']
    cur_module_name  = ''
    if cur_module_inf: 
        cur_module_name = cur_module_inf['module_name']
    else:
        PrintDebug('Warning: get_cur_cursor_inf: current cursor %s not in module, file: %s ! '%(cur_cursor.__str__(), cur_file_path ))
    return {  'cursor'           : cur_cursor
             ,'pos'              : (cur_line_num, cur_colm_num)
             ,'line_num'         : cur_line_num
             ,'colm_num'         : cur_colm_num
             ,'line'             : cur_line
             ,'word'             : cur_word
             ,'file_path'        : cur_file_path
             ,'hdl_type'         : cur_hdl_type
             ,'cur_call_sub_inf' : cur_call_sub_inf
             ,'cur_module_inf'   : cur_module_inf
             ,'codes'            : cur_codes }

# ok
# report file_link = {
#                      'key'   :  '' ,  signal_name
#                     'pos'   :  '' ,  match_pos
#                     'path'  :  '' ,  match_path
# }
#----for python edition 2.7 + 
# def PrintReport(*show, file_link = {}, spec_case = '', mode = 'a'):
#     # normal show a string 
#     show_str = ' '.join([ i.__str__() for i in show ])
#----for python edition 2.6
def PrintReport(show = '', file_link = {}, spec_case = '', mode = 'a'):
    if not G['ShowReport']:
        return
    has_self_snap_short = False
    if not cur_in_report():
        snapshort_push()
        Open('Report')
        has_self_snap_short = True
    show_str = show
    if show_str: 
        edit_vim_buffer('Report', [show_str], file_links = [file_link], mode = mode)
    # show trace source result
    if spec_case == 'source':
        edit_vim_buffer('Report', "---------------------------source--------------------------------")
        t_data      = []
        t_file_link = []
        for Sure in G['TraceInf']['LastTraceSource']['Sure']:
            t_data.append( Sure['show'] )
            t_file_link.append( Sure['file_link'] )
        edit_vim_buffer('Report', t_data, t_file_link)
        edit_vim_buffer('Report', "------------------------maybe source-----------------------------")
        t_data      = []
        t_file_link = []
        for Maybe in G['TraceInf']['LastTraceSource']['Maybe']:
            t_data.append( Maybe['show'] )
            t_file_link.append( Maybe['file_link'] )
        edit_vim_buffer('Report', t_data, t_file_link)
        edit_vim_buffer('Report', "----------------------------END----------------------------------")
        edit_vim_buffer('Report', "")
    # show trace dest result
    if spec_case == 'dest':
        edit_vim_buffer('Report', "---------------------------dest--------------------------------")
        t_data      = []
        t_file_link = []
        for Sure in G['TraceInf']['LastTraceDest']['Sure']:
            t_data.append( Sure['show'] )
            t_file_link.append( Sure['file_link'] )
        edit_vim_buffer('Report', t_data, t_file_link)
        edit_vim_buffer('Report', "------------------------maybe dest-----------------------------")
        t_data      = []
        t_file_link = []
        for Maybe in G['TraceInf']['LastTraceDest']['Maybe']:
            t_data.append( Maybe['show'] )
            t_file_link.append( Maybe['file_link'] )
        edit_vim_buffer('Report', t_data, t_file_link)
        edit_vim_buffer('Report', "----------------------------END----------------------------------")
        edit_vim_buffer('Report', "")
    # go report to the last line, and return
    assert(cur_in_report())
    # if mode == 'a':
    vim.current.window.cursor = (len(vim.current.buffer) - 1 , 0)
    vim.command('w!')
    if has_self_snap_short:
        snapshort_pop()

# ok
def show_next_trace_result( trace_type ):
    if trace_type == 'source':
        cur_show_index   = G['TraceInf']['LastTraceSource']["ShowIndex"]
        sure_source_len  = len(G['TraceInf']['LastTraceSource']['Sure'])
        maybe_source_len = len(G['TraceInf']['LastTraceSource']['Maybe'])
        if (sure_source_len + maybe_source_len) == 0:
            PrintReport('not find source !')
            return
        cur_file_link = {}
        if cur_show_index < sure_source_len:
            cur_file_link = G['TraceInf']['LastTraceSource']['Sure'][cur_show_index]['file_link']
        else:
            cur_file_link = G['TraceInf']['LastTraceSource']['Maybe'][cur_show_index - sure_source_len]['file_link']
        G['TraceInf']['LastTraceSource']["ShowIndex"] = (cur_show_index + 1) % (sure_source_len + maybe_source_len)
        add_trace_point()
        go_win( cur_file_link['path'], cur_file_link['pos'], cur_file_link['key'] )
    elif trace_type == 'dest':
        cur_show_index   = G['TraceInf']['LastTraceDest']["ShowIndex"]
        sure_dest_len  = len(G['TraceInf']['LastTraceDest']['Sure'])
        maybe_dest_len = len(G['TraceInf']['LastTraceDest']['Maybe'])
        if (sure_dest_len + maybe_dest_len) == 0:
            PrintReport('not find dest !')
            return
        cur_file_link = {}
        if cur_show_index < sure_dest_len:
            cur_file_link = G['TraceInf']['LastTraceDest']['Sure'][cur_show_index]['file_link']
        else:
            cur_file_link = G['TraceInf']['LastTraceDest']['Maybe'][cur_show_index - sure_dest_len]['file_link']
        G['TraceInf']['LastTraceDest']["ShowIndex"] = (cur_show_index + 1) % (sure_dest_len + maybe_dest_len)
        add_trace_point()
        go_win( cur_file_link['path'], cur_file_link['pos'], cur_file_link['key'])
    else:
        assert(0)

#--------------------------------------------------------------------------
def gen_top_topo_data_link(topo_module):
    topo_datas   = []
    topo_links   = []
    topo_module_inf = get_module_inf(topo_module)
    if not topo_module_inf:
        PrintDebug('Error: get topo module name %s, should has module inf !'%(topo_module))
        return topo_datas, topo_links
    TopTopoLevel    = G['TopoInf']['TopFoldLevel']
    TopTopoPrefix   = G['Frame_Inf']['FoldLevelSpace'] * TopTopoLevel
    # add first topo line 
    topo_datas.append(TopTopoPrefix + 'ModuleTopo:')
    topo_link = {
         'type'           : 'topo'
        ,'topo_inst_name' : ''
        ,'key'            : ''
        ,'pos'            : ''
        ,'path'           : ''
        ,'fold_inf'       : {'fold_status':'on', 'level': TopTopoLevel - 1 }
    }
    topo_links.append(topo_link)
    # add cur module name
    topo_datas.append(TopTopoPrefix + topo_module + ':')
    topo_link = {
         'type'           : 'topo'
        ,'topo_inst_name' : ''
        ,'key'            : topo_module
        ,'pos'            : topo_module_inf['module_pos']
        ,'path'           : topo_module_inf['file_path']
        ,'fold_inf'       : {'fold_status':'on', 'level': TopTopoLevel}
    }
    topo_links.append(topo_link)
    # gen current module sub function module, and base module topo inf
    sub_module_data, sub_module_link = get_fram_topo_sub_inf(topo_module, 0)
    topo_datas = topo_datas + sub_module_data
    topo_links = topo_links + sub_module_link
    return topo_datas, topo_links


def edit_frame(data = [], file_links = [], mode = 'a', n = 0, del_range = ()):
    has_self_snap_short = False
    if not cur_in_frame():
        snapshort_push()
        Open('Frame')
        has_self_snap_short = True
    edit_vim_buffer( path_or_name = 'Frame', data = data, file_links = file_links, mode = mode, n = n, del_range = del_range)
    # go frame w! and go back
    assert(cur_in_frame())
    vim.command('w!')
    if has_self_snap_short:
        snapshort_pop()

#---------------------------------------
def show_base_module(fold = True):
    frame_data   = []
    frame_link   = []
    # if frame not show ,show it
    Show("Frame")
    # add initial line
    level        = G['BaseModuleInf']['TopFoldLevel']
    key          = G['Frame_Inf']['FoldLevelSpace']*level + 'BaseModules:'
    link         = {
         'type'     : 'base_module'
        ,'key'      : ''
        ,'pos'      : ''
        ,'path'     : ''
        ,'fold_inf' : { 'fold_status': 'on', 'level': level }
    }
    frame_data.append(key)
    frame_link.append(link)
    # add check points
    range_inf         = get_frame_range_inf()
    has_base_module   = range_inf['has_base_module']
    base_module_range = range_inf['base_module_range']
    cp_data = []
    cp_link = []
    if fold:
        cp_data, cp_link  = get_fram_base_module_inf()
    else:
        frame_link[-1]['fold_inf']['fold_status'] = 'off'
    frame_data = frame_data + cp_data
    frame_link = frame_link + cp_link
    # del old cp, add new cp
    if has_base_module: # del
        edit_frame(mode = 'del', del_range = base_module_range)
    edit_frame(data = frame_data, file_links = frame_link, mode = 'i', n = base_module_range[0])
    return True

#-------------------------------------
def show_check_point(fold = True):
    frame_data   = []
    frame_link   = []
    # if frame not show ,show it
    Show("Frame")
    # add initial line
    level        = G['CheckPointInf']['TopFoldLevel']
    key          = G['Frame_Inf']['FoldLevelSpace']*level + 'CheckPoints:'
    link         = {
         'type'     : 'check_point'
        ,'key'      : ''
        ,'pos'      : ''
        ,'path'     : ''
        ,'fold_inf' : { 'fold_status': 'on', 'level': level }
    }
    frame_data.append(key)
    frame_link.append(link)
    # add check points
    range_inf         = get_frame_range_inf()
    has_check_point   = range_inf['has_check_point']
    check_point_range = range_inf['check_point_range']
    cp_data = []
    cp_link = []
    if fold:
        cp_data, cp_link  = get_fram_check_point_inf()
    else:
        frame_link[-1]['fold_inf']['fold_status'] = 'off'
    frame_data = frame_data + cp_data
    frame_link = frame_link + cp_link
    # del old cp, add new cp
    if has_check_point: # del
        edit_frame(mode = 'del', del_range = check_point_range)
    edit_frame(data = frame_data, file_links = frame_link, mode = 'i', n = check_point_range[0])
    return True

#---------------------------------------
def show_topo(topo_module_name = ''):
    if not topo_module_name:
        cursor_inf      = get_cur_cursor_inf()
        if cursor_inf['hdl_type'] != 'verilog':
            # if not in support file type(verilog,vhdl) just return
            PrintReport("Warning: Current only support verilog !")
            return False
        # get current module inf
        cur_module_inf  = cursor_inf['cur_module_inf']
        # current not at module lines, just return
        if not cur_module_inf:
            PrintReport("Warning: Current cursor not in valid module !")
            return False
        topo_module_name = cur_module_inf['module_name']
    else:
        if topo_module_name not in G['ModuleInf']:
            PrintReport("Warning: show topo module %s not have database !"%(topo_module_name))
            return False
    # if frame not show ,show it
    Show("Frame")
    # current module must has module inf
    G['TopoInf']['CurModule']  = topo_module_name  # note cur topo name for refresh
    range_inf                  = get_frame_range_inf()
    has_topo                   = range_inf['has_topo']
    topo_range                 = range_inf['topo_range']
    topo_data, topo_link       = gen_top_topo_data_link(topo_module_name)
    # del old topo, add new topo
    if has_topo: # del
        edit_frame(mode = 'del', del_range = topo_range)
    edit_frame(data = topo_data, file_links = topo_link, mode = 'i', n = topo_range[0])
    return True

def iteration_fold_no_module(inst_module_pairs, base_modules):
    c_frame_range_inf = get_frame_range_inf()
    if not c_frame_range_inf['has_topo']:
        return
    frame_path   = G['Frame_Inf']['Frame_Path']
    c_topo_range = c_frame_range_inf['topo_range']
    c_topo_links = G['VimBufferLineFileLink'][frame_path][c_topo_range[0] : c_topo_range[1]]
    for i,lk in enumerate(c_topo_links):
        if not( lk and (lk['fold_inf']['fold_status'] == 'off') and lk['key'] ):
            continue
        if lk['topo_inst_name']:
            c_inst_module_pair = (lk['topo_inst_name'], lk['key'])
            if c_inst_module_pair in inst_module_pairs:
                fold_frame_line(lk, i+c_topo_range[0], lk['fold_inf']['level'], 'topo')
                iteration_fold_no_module(inst_module_pairs, base_modules)
                return
        else:
            if lk['key'] in base_modules:
                fold_frame_line(lk, i+c_topo_range[0], lk['fold_inf']['level'], 'topo')
                iteration_fold_no_module(inst_module_pairs, base_modules)
                return
    return

def refresh_topo():
    # get all folded module or inst pair
    old_frame_range_inf = get_frame_range_inf()
    if not old_frame_range_inf['has_topo']:
        return
    frame_path     = G['Frame_Inf']['Frame_Path']
    old_topo_range = old_frame_range_inf['topo_range']
    old_topo_links = G['VimBufferLineFileLink'][frame_path][old_topo_range[0] + 2 : old_topo_range[1] + 1]
    old_fold_inst_module_pairs = set()
    old_fold_base_modules      = set()
    for lk in old_topo_links:
        if not( lk and (lk['fold_inf']['fold_status'] == 'on') and lk['key'] ):
            continue
        if lk['topo_inst_name']:
            old_fold_inst_module_pairs.add( (lk['topo_inst_name'], lk['key']) )
        else:
            if lk['key'] in G['BaseModuleInf']['BaseModules']:
                old_fold_base_modules.add(lk['key'])
    # start new topo
    new_topo_module_name = G['TopoInf']['CurModule']
    show_topo(new_topo_module_name)
    # iteration opened old folded topo
    iteration_fold_no_module(old_fold_inst_module_pairs, old_fold_base_modules)

#---------------------------------------
def unfold_frame_line(frame_links, frame_line, cur_frame_level, cur_frame_type):
    assert(frame_links[frame_line]['fold_inf']['fold_status'] == 'on')
    G['VimBufferLineFileLink'][ G['Frame_Inf']['Frame_Path'] ][frame_line]['fold_inf']['fold_status'] = 'off'
    unfold_end_line_num =  frame_line
    for i in range(frame_line+1, len(frame_links)):
        # if cur not have file link, then cur is unflod end
        if not frame_links[i]:
            unfold_end_line_num = i - 1
            break
        # if has file link ,but not topo inf then unflod end
        if frame_links[i]['type'] != cur_frame_type:
            unfold_end_line_num = i - 1
            break
        # if is topo , but level <= cur level then unflod end
        if frame_links[i]['fold_inf']['level'] <= cur_frame_level:
            unfold_end_line_num = i - 1
            break
    # if cur module has no sub module then just return
    if unfold_end_line_num == frame_line:
        return True
    # else edit the frame buffer and file link, del the unflod lines
    if unfold_end_line_num > frame_line:
        edit_frame(mode = 'del', del_range = (frame_line + 1, unfold_end_line_num))
        return True
    # else some trouble
    assert(0),'shold not happen !'

def fold_frame_line(cur_line_link, frame_line, cur_frame_level, cur_frame_type):
    assert(cur_line_link['fold_inf']['fold_status'] == 'off')
    G['VimBufferLineFileLink'][ G['Frame_Inf']['Frame_Path'] ][frame_line]['fold_inf']['fold_status'] = 'on'
    if cur_frame_type == 'topo':
        # if cur is ModuleTopo: line, show refresh topo
        if cur_frame_level == G['TopoInf']['TopFoldLevel'] - 1:
            topo_module_name = G['TopoInf']['CurModule']
            show_topo(topo_module_name)
            return
        # cur_line_link['key'] is the cur topo line module name
        cur_module_name = cur_line_link['key']
        if  not cur_module_name:
            PrintReport('Warning: cur topo line has no module name !')
            return 
        if cur_module_name not in G['ModuleInf']:
            PrintReport('Warning: cur module: \"%s\" has no database !'%(cur_module_name))
            return
        # get cur module sub module inf
        sub_topo_data, sub_topo_link = get_fram_topo_sub_inf(cur_module_name, cur_frame_level)
        # add cur module topo inf to frame
        edit_frame(data = sub_topo_data, file_links = sub_topo_link, mode = 'i', n = frame_line + 1)
    elif cur_frame_type == 'check_point':
        show_check_point()
    elif cur_frame_type == 'base_module':
        show_base_module()
    else:
        PrintReport('Warning: no operation in this line !')
    return

def frame_line_fold_operation(frame_line):
    frame_path     = G['Frame_Inf']['Frame_Path']
    frame_links    = G['VimBufferLineFileLink'][frame_path]
    cur_line_link  = frame_links[frame_line]
    if not cur_line_link :
        PrintReport('Warning: cur frame line no fold operation !')
        return
    cur_frame_type  = cur_line_link['type']
    cur_frame_level = cur_line_link['fold_inf']['level']
    cur_fold_state  = cur_line_link['fold_inf']['fold_status']
    if cur_fold_state == 'off':
        fold_frame_line(cur_line_link, frame_line, cur_frame_level, cur_frame_type)
    elif cur_fold_state == 'on':
        unfold_frame_line(frame_links, frame_line, cur_frame_level, cur_frame_type)
    else:
        PrintReport('Warning: cur frame line no fold operation !')
        return






