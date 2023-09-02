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

import os
import sys
# import vim, when gen vtags it will no vim,so use try 
try:
    import vim
except: 
    pass
# import normal lib
import re
import Lib.Code as Code
import Lib.View as View
PrintReport = View.PrintReport
import Lib.GLB as GLB
G = GLB.G
from Lib.Base import *

# init gen module_inf, and glb define
if G['HDLTagsActive']:
    G['ModuleInf'], G['CodeDefineInf'] = gen_modules_and_defines_inf(G['FileInf'])

# open snapshort wins
if G['HDLTagsActive'] and G['EnvSnapshortWinsInf']:
    OldOpenWinTrace = [p for p in G['WorkWin_Inf']['OpenWinTrace']]
    G['WorkWin_Inf']['OpenWinTrace'].insert(0,vim.current.buffer.name)
    for w_inf in G['EnvSnapshortWinsInf']:
        c_path   = w_inf['path']
        c_cursor = w_inf['cursor']
        if os.path.isfile(c_path):
            View.Open(c_path)
            if c_path not in OldOpenWinTrace:
                if G['WorkWin_Inf']['OpenWinTrace'] and G['WorkWin_Inf']['OpenWinTrace'][-1] == c_path:
                    del G['WorkWin_Inf']['OpenWinTrace'][-1]
        else:
            PrintDebug('Warning: reload file not exit ! file: %s'%(c_path))
    for w_inf in G['EnvSnapshortWinsInf']:
        c_size  = w_inf['size']
        c_path   = w_inf['path']
        if os.path.isfile(c_path):
            View.Open(c_path)
            vim.current.window.width   = c_size[0]
            vim.current.window.height  = c_size[1]
    # because base module may be changed so refresh topo and show base
    if G['Frame_Inf']['Frame_Path'] in [ w.buffer.name for w in vim.windows]:
        View.refresh_topo()
        View.show_base_module()
    PrintReport('reload snapshort finish !')
elif G['HDLTagsActive']:
    # treat the first win as work win , if cur win is hdl code, and add first trace point
    first_cursor_inf = View.get_cur_cursor_inf()
    if first_cursor_inf['hdl_type'] == 'verilog':
        G['WorkWin_Inf']['OpenWinTrace'].append(first_cursor_inf['file_path'])
        View.add_trace_point()
    PrintDebug('Point: initial new env finish !')


# shortcut key: gi
def go_into_submodule(): 
    cursor_inf       = View.get_cur_cursor_inf()
    cur_module_inf   = cursor_inf['cur_module_inf']
    if not cur_module_inf:
        PrintReport('Warning: cur cursor not in a valid module, no submodule call !')
        return
    call_module_name = cur_module_inf['module_name']
    sub_call_inf     = Code.get_module_call_sub_module_io_inf(cursor_inf['line'], cursor_inf['pos'], cursor_inf['file_path'])
    if not sub_call_inf:
        PrintReport('Warning: cur cursor not on recgnized subcall !')
        return
    sub_module_name  = sub_call_inf['sub_module_name'] 
    sub_module_inf   = get_module_inf(sub_module_name)
    if not sub_module_inf:
        PrintReport('Warning: sub module %s no module inf in database !'%(sub_module_name))
        return
    sub_signal_name  = sub_call_inf['sub_io_name']
    sub_match_pos    = []
    if sub_signal_name:
        sub_match_pos    = sub_call_inf['sub_match_pos']
    else:
        sub_signal_name = sub_module_name
        sub_match_pos   = sub_module_inf['module_pos']
    call_sub_inf     = sub_call_inf['call_sub_inf']      # GLB call sub inf(atom)
    sub_module_path  = sub_module_inf['file_path']
    set_module_last_call_inf(sub_module_name, call_module_name, call_sub_inf['inst_name'])
    View.add_trace_point()
    View.go_win( sub_module_path, sub_match_pos, sub_signal_name)

def try_go_into_submodule():
    if not G['HDLTagsActive']: return
    if G['Debug']:
        go_into_submodule()
    else:
        try: go_into_submodule()
        except: pass

# shortcut key: gu
def go_upper_module(): 
    cursor_inf        = View.get_cur_cursor_inf()
    cur_module_inf    = cursor_inf['cur_module_inf']
    if not cur_module_inf:
        PrintReport('Warning: cur line not in a valid verilog module, or current module not in database !')
        return
    cur_last_call_inf = get_module_last_call_inf(cur_module_inf['module_name'])
    if not cur_last_call_inf:
        PrintReport('Warning: cur module %s not called by upper module before !'%(cur_module_inf['module_name']))
        return
    upper_module_name  = cur_last_call_inf['upper_module_name']
    upper_call_sub_inf = cur_last_call_inf['upper_call_inf']
    upper_match_pos    = upper_call_sub_inf['match_pos']
    upper_inst_name    = upper_call_sub_inf['inst_name']
    View.add_trace_point()
    View.go_win( upper_module_name, upper_match_pos, upper_inst_name)

def try_go_upper_module():
    if not G['HDLTagsActive']: return
    if G['Debug']:
        go_upper_module()
    else:
        try: go_upper_module()
        except: pass


# shortcut key: <Space><Left>
def trace_signal_sources():
    if G['IgnoreNextSpaceOp']:
        G['IgnoreNextSpaceOp'] = False
        PrintDebug('Care: not do this trace source op ,bucause <space> is come from unknow reason !')
        return
    cursor_inf = View.get_cur_cursor_inf()
    trace_signal_name = cursor_inf['word']
    if not trace_signal_name:
        PrintReport("Warning: Current cursor not on signal name, can not trace source !")
        return
    # case0: if cur cursor on a macro, go macro define
    if Code.trace_glb_define_signal('source', cursor_inf): return
    # case1: if cur cursor on io signal, need cross to upper module
    if Code.trace_io_signal('source', cursor_inf): return
    # case2: if cur cursor on module call io line go to submodule io
    if Code.trace_module_call_io_signal('source', cursor_inf): return
    # case3: trace signal same as pre trace signal, just show next result
    if (G['TraceInf']['LastTraceSource']['Path'] == cursor_inf['file_path']) and (G['TraceInf']['LastTraceSource']['SignalName'] == trace_signal_name) :
        View.show_next_trace_result('source')
        return
    # case4: trace a new normal(not io, sub call io) signal
    if Code.trace_normal_signal('source', cursor_inf): return

def try_trace_signal_sources():
    if not G['HDLTagsActive']: return
    if G['Debug']:
        trace_signal_sources()
    else:
        try: trace_signal_sources()
        except: pass


# shortcut key: <Space><Right>
def trace_signal_destinations():
    if G['IgnoreNextSpaceOp']:
        G['IgnoreNextSpaceOp'] = False
        PrintDebug('Care: not do this trace source op ,bucause <space> is come from unknow reason !')
        return
    cursor_inf = View.get_cur_cursor_inf()
    trace_signal_name = cursor_inf['word']
    if not trace_signal_name:
        PrintReport("Warning: Current cursor not on signal name, can not trace dest!")
        return
    # case0: if cur cursor on io signal, need cross to upper module
    if Code.trace_io_signal('dest', cursor_inf): return
    # case1: if cur cursor on module call io line go to submodule io
    if Code.trace_module_call_io_signal('dest', cursor_inf): return
    # case2: trace signal same as pre trace signal, just show next result
    if (G['TraceInf']['LastTraceDest']['Path'] == cursor_inf['file_path']) and (G['TraceInf']['LastTraceDest']['SignalName'] == trace_signal_name) :
        View.show_next_trace_result('dest')
        return
    # case3: if cur cursor on a macro, go macro define
    if Code.trace_glb_define_signal('dest', cursor_inf): return
    # case4: trace a new normal(not io, sub call io) signal
    Code.trace_normal_signal('dest', cursor_inf)

def try_trace_signal_destinations():
    if not G['HDLTagsActive']: return
    if G['Debug']:
        trace_signal_destinations()
    else:
        try: trace_signal_destinations()
        except: pass


# shortcut key: <Space><Down> 
def roll_back():
    if G['IgnoreNextSpaceOp']:
        G['IgnoreNextSpaceOp'] = False
        PrintDebug('Care: not do this trace source op ,bucause <space> is come from unknow reason !')
        return
    cur_nonius        = G['OpTraceInf']['Nonius'] - 1
    TracePoints       = G['OpTraceInf']['TracePoints']
    # if reach to the oldest trace point just return
    if cur_nonius < 0:
        PrintReport("Warning: roll backed to the oldest trace point now !")
        return
    # go to the trace point
    cur_point = TracePoints[cur_nonius]
    G['OpTraceInf']['Nonius'] = cur_nonius
    View.go_win( cur_point['path'], cur_point['pos'], cur_point['key'])
    return

def try_roll_back():
    if not G['HDLTagsActive']: return
    if G['Debug']:
        roll_back()
    else:
        try: roll_back()
        except: pass


# shortcut key: <Space><Up> 
def go_forward():
    if G['IgnoreNextSpaceOp']:
        G['IgnoreNextSpaceOp'] = False
        PrintDebug('Care: not do this trace source op ,bucause <space> is come from unknow reason !')
        return
    cur_nonius        = G['OpTraceInf']['Nonius'] + 1
    TracePoints       = G['OpTraceInf']['TracePoints']
    if cur_nonius >= len(TracePoints):
        PrintReport("Warning: go forward to the newest trace point now !")
        return
    cur_point = TracePoints[cur_nonius]
    G['OpTraceInf']['Nonius'] = cur_nonius
    View.go_win( cur_point['path'], cur_point['pos'], cur_point['key'])
    return

def try_go_forward():
    if not G['HDLTagsActive']: return
    if G['Debug']:
        go_forward()
    else:
        try: go_forward()
        except: pass


# shortcut key: <space>
def space_operation():
    if G['IgnoreNextSpaceOp']:
        G['IgnoreNextSpaceOp'] = False
        PrintDebug('Care: not do this trace source op ,bucause <space> is come from unknow reason !')
        return
    cursor_inf = View.get_cur_cursor_inf()
    # if cur in Frame or Report, show file link files
    if cursor_inf['file_path'] in [ G['Frame_Inf']['Frame_Path'], G['Report_Inf']['Report_Path'] ]:
        cur_frame_link = G['VimBufferLineFileLink'][cursor_inf['file_path']][cursor_inf['line_num']]
        View.add_trace_point()
        if cur_frame_link and cur_frame_link['path']:
            View.go_win( cur_frame_link['path'], cur_frame_link['pos'], cur_frame_link['key'])
            View.add_trace_point()
        else:
            PrintReport('Warning: No file link in current line ! ')
    else:
        PrintReport('Warning: No space operation in current file ! ')

def try_space_operation():
    if not G['HDLTagsActive']: return
    if G['Debug']:
        space_operation()
    else:
        try: space_operation()
        except: pass

# shortcut key: <s-t>
def show_frame():
    G["IgnoreNextSpaceOp"] = G['FixExtraSpace']
    if cur_in_frame():
        cursor_line = vim.current.window.cursor[0] - 1 
        View.frame_line_fold_operation(cursor_line)
    else:
        View.show_topo()
        View.show_check_point(False)
        View.show_base_module(False)
    return

def try_show_frame():
    if not G['HDLTagsActive']: return
    if G['Debug']:
        show_frame()
    else:
        try: show_frame()
        except: pass
    return

# shortcut key: <Space>h
def hold_current_win():
    cur_path = vim.current.buffer.name
    # just del current win frome work win, then will not auto close current win
    for i,path in enumerate(G['WorkWin_Inf']['OpenWinTrace']):
        if cur_path == path:
            del G['WorkWin_Inf']['OpenWinTrace'][i]
            break

def try_hold_current_win():
    if not G['HDLTagsActive']: return
    if G['Debug']:
        hold_current_win()
    else:
        try: hold_current_win()
        except: pass


# shortcut key: <Space>c
def add_check_point():
    G["IgnoreNextSpaceOp"] = G['FixExtraSpace']
    cursor_inf   = View.get_cur_cursor_inf()
    level        = G['CheckPointInf']['TopFoldLevel'] + 1 
    key          = G['Frame_Inf']['FoldLevelSpace']*level + cursor_inf['word']
    link         = {
         'type'     : 'check_point'
        ,'key'      : cursor_inf['word']
        ,'pos'      : cursor_inf['pos']
        ,'path'     : cursor_inf['file_path']
        ,'fold_inf' : { 'fold_status': 'fix', 'level': level }
    }
    G['CheckPointInf']['CheckPoints'].insert(0, {'key': key, 'link': link })
    if len(G['CheckPointInf']['CheckPoints']) > G['CheckPointInf']['MaxNum']:
        del G['CheckPointInf']['CheckPoints'][-1]
    View.show_check_point()

def try_add_check_point():
    if not G['HDLTagsActive']: return
    if G['Debug']:
        add_check_point()
    else:
        try: add_check_point()
        except: pass

# shortcut key: <Space>b
def add_base_module():
    G["IgnoreNextSpaceOp"] = G['FixExtraSpace']
    cursor_inf    = View.get_cur_cursor_inf()
    cursor_module = cursor_inf['word']
    if not cursor_module:
        PrintReport('Warning: cursor not on a valid word ! ')
        return
    if not get_module_inf(cursor_module):
        PrintReport('Warning: cursor words: %s not a recgnized module name ! will no file link ! '%(cursor_module))
    if cursor_module in G['BaseModuleInf']['BaseModules']:
        PrintReport('Care: module %s is already base module ! '%(cursor_module))
        return
    G['BaseModuleInf']['BaseModules'].add(cursor_module)
    update_base_module_pickle()
    View.show_base_module()
    View.refresh_topo()


def try_add_base_module():
    if not G['HDLTagsActive']: return
    if G['Debug']:
        add_base_module()
    else:
        try: add_base_module()
        except: pass

#------------------------------
# shortcut key: <Space>d
def del_operation():
    if not cur_in_frame():
        PrintReport('Warning: Cur file no del function ! ')
        return
    cur_path      = vim.current.buffer.name
    cur_line_num  = vim.current.window.cursor[0] - 1
    cur_file_link = G['VimBufferLineFileLink'][cur_path][cur_line_num]
    if not cur_file_link:
        PrintReport('Warning: Cur line no del function ! ')
        return
    # delete a check point, if link has path means a valid link
    if (cur_file_link['type'] == 'check_point') and (cur_file_link['fold_inf']['level'] > G['CheckPointInf']['TopFoldLevel']):
        G["IgnoreNextSpaceOp"] = G['FixExtraSpace']
        check_point_begin_line_num = get_frame_range_inf()['check_point_range'][0]
        del_index = cur_line_num - check_point_begin_line_num - 1
        del G['CheckPointInf']['CheckPoints'][ del_index ]
        View.show_check_point()
        return
    # del a base module
    if (cur_file_link['type'] == 'base_module') and (cur_file_link['fold_inf']['level'] > G['BaseModuleInf']['TopFoldLevel']): 
        G["IgnoreNextSpaceOp"] = G['FixExtraSpace']
        G['BaseModuleInf']['BaseModules'].remove(cur_file_link['key'])
        update_base_module_pickle()
        View.show_base_module()
        View.refresh_topo()
        return
    PrintReport('Warning: Cur line no del function ! ')

def try_del_operation():
    if not G['HDLTagsActive']: return
    if G['Debug']:
        del_operation()
    else:
        try: del_operation()
        except: pass

#----------------------------------------
# shortcut key: <Space>s
def try_save_env_snapshort():
    if not G['HDLTagsActive']: return
    if G['Debug']:
        if G['SaveEnvSnapshort_F']():
            PrintReport('save env snapshort success !')
    else:
        try: 
            if G['SaveEnvSnapshort_F']():
                PrintReport('save env snapshort success !')
        except: pass
