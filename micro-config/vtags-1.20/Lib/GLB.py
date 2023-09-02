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
sys.path.append('../')
import vim_glb_config as glb_config

import os
import re
import pickle

vim_start_open_file = ''
try:
    import vim
    vim_start_open_file = vim.current.buffer.name
except:
    vim_start_open_file = '|vim_not_open|'
    pass


# cur call path
cur_path = os.getcwd()

# find most resent vtags path
hdl_tags_path = ''
while cur_path and cur_path[0] == '/':
    if os.path.isdir(cur_path + '/vtags.db'):
        hdl_tags_path = cur_path + '/vtags.db'
        break
    cur_path = re.sub('/[^/]*$','',cur_path)

# get local config
config        = glb_config
try:
    if hdl_tags_path:
        sys.path.append(hdl_tags_path)
        import vim_local_config as local_config
        config = local_config
except:
    pass


# get next empty frame, report,log report index, first try del Frame, Report
def del_old_logs():
    ls_a_f = [ f.strip('\n') for f in os.popen('ls -a ' + hdl_tags_path).readlines() ]
    used_log_index = set()
    for f in ls_a_f:
        match_swp = re.match('\.(Frame\.HF|Report\.HF|run\.log)(?P<idx>\d+)\.swp',f)
        if match_swp:
            used_log_index.add(int(match_swp.group('idx')))
    ls_f   = [ f.strip('\n') for f in os.popen('ls ' + hdl_tags_path).readlines() ]
    for f in ls_f:
        match_idx = re.match('(Frame\.HF|Report\.HF|run\.log)(?P<idx>\d+)', f)
        if not match_idx:
            continue
        cur_index = int(match_idx.group('idx'))
        if cur_index in used_log_index:
            continue
        os.system('rm %s/%s'%(hdl_tags_path,f) )
    return

empty_log_index = 0
if hdl_tags_path:
    del_old_logs()
    while os.path.isfile(hdl_tags_path + '/run.log'   + str(empty_log_index)) or \
          os.path.isfile(hdl_tags_path + '/Frame.HF'  + str(empty_log_index)) or \
          os.path.isfile(hdl_tags_path + '/Report.HF' + str(empty_log_index)):
        empty_log_index += 1

# if in generate vtags situation, print log to vtags.db/vtags_run.log
vtags_run_log_path = ['']
# run log path
run_log_path = hdl_tags_path + '/run.log'+str(empty_log_index)
def PrintDebug( str, out_path = ''):
    if vtags_run_log_path[0]:
        output = open( vtags_run_log_path[0], 'a')
        output.write(str+'\n')
        output.close()
        return
    if not config.debug_mode:
        return
    if out_path:
        output = open( out_path, 'a')
        output.write(str+'\n')
        output.close()
        return
    if hdl_tags_path:
        output = open( run_log_path ,'a')
        output.write(str+'\n')
        output.close()

def get_file_path_postfix(file_path):
    split_by_dot = file_path.split('.')
    if len(split_by_dot) < 2: # which means file_path has no postfix
        return ''
    post_fix = split_by_dot[-1]          # postfix care case
    return post_fix

HDLTagsActive = True
# if cur open a valid file, and file not verilog file not act vtags
if vim_start_open_file \
   and (get_file_path_postfix(vim_start_open_file) not in config.support_verilog_postfix):
    HDLTagsActive = False

# get file inf
FileInf       = {}
try:
    if hdl_tags_path and HDLTagsActive:
        import files_inf
        HDLTagsActive = files_inf.HDLTagsActive
        FileInf       = files_inf.FileInf
    else:
        HDLTagsActive = False
except:
    HDLTagsActive = False

BaseModules   = set()
if HDLTagsActive:
    # get base module inf
    try:
        pkl_input     = open(hdl_tags_path + '/base_modules.pkl','rb')
        BaseModules   = pickle.load(pkl_input)
        pkl_input.close()
    except:
        pass

# function -------------------------------------------------
def save_env_snapshort():
    snapshort = {}
    # 0: save cur dir path, used to quality opne snapshort
    snapshort['snapshort_dir_path'] = os.getcwd()
    # 1: save Frame
    snapshort['frame_file_lines'] = []
    if os.path.isfile(G['Frame_Inf']['Frame_Path']):
        snapshort['frame_file_lines'] = open(G['Frame_Inf']['Frame_Path'],'r').readlines()
    # 2: save Report
    snapshort['report_file_lines'] = []
    if os.path.isfile(G['Report_Inf']['Report_Path']):
        snapshort['report_file_lines'] = open(G['Report_Inf']['Report_Path'],'r').readlines()
    # 3: save G
    snapshort['G'] = {}
    snapshort['G']['OpTraceInf']                   = {}
    snapshort['G']['OpTraceInf']['TracePoints']    = G['OpTraceInf']['TracePoints'] 
    snapshort['G']['OpTraceInf']['Nonius'     ]    = G['OpTraceInf']['Nonius'     ]
    snapshort['G']['WorkWin_Inf']                  = {}
    snapshort['G']['WorkWin_Inf']['OpenWinTrace']  = G['WorkWin_Inf']['OpenWinTrace']
    snapshort['G']['VimBufferLineFileLink' ]       = G["VimBufferLineFileLink" ]
    snapshort['G']["TraceInf"              ]       = G['TraceInf']
    snapshort['G']['CheckPointInf']                = {}
    snapshort['G']['CheckPointInf']['CheckPoints'] = G['CheckPointInf']['CheckPoints']
    snapshort['G']['TopoInf']                      = {}
    snapshort['G']['TopoInf']['CurModule']         = G['TopoInf']['CurModule']
    snapshort['G']['ModuleLastCallInf']            = G['ModuleLastCallInf']
    snapshort['G']['Frame_Inf']                    = {}
    snapshort['G']['Frame_Inf']['Frame_Path']      = G['Frame_Inf']['Frame_Path']
    snapshort['G']['Report_Inf']                   = {}
    snapshort['G']['Report_Inf']['Report_Path']    = G['Report_Inf']['Report_Path']
    # 4: save act windows inf
    act_win_inf = []
    for w in vim.windows:
        c_file_path = w.buffer.name
        if c_file_path == vim.current.buffer.name:
            continue
        c_cursor    = w.cursor
        c_size      = (w.width, w.height)
        act_win_inf.append({'path': c_file_path, 'cursor': c_cursor, 'size': c_size })
    # last is current window
    cur_file_path  = vim.current.buffer.name
    cur_cursor     = vim.current.window.cursor   
    cur_size       = (vim.current.window.width, vim.current.window.height)
    act_win_inf.append({'path': cur_file_path, 'cursor': cur_cursor, 'size': cur_size })
    snapshort['act_win_inf'] = act_win_inf
    pkl_output = open(hdl_tags_path + '/env_snapshort.pkl','wb')
    pickle.dump(snapshort, pkl_output)
    pkl_output.close()
    return True

def reload_env_snapshort(snapshort):
    # 1: reload G
    snapshort_G = snapshort['G']
    G['OpTraceInf']['TracePoints']    = snapshort_G['OpTraceInf']['TracePoints'] 
    G['OpTraceInf']['Nonius'     ]    = snapshort_G['OpTraceInf']['Nonius'     ]
    G['WorkWin_Inf']['OpenWinTrace']  = snapshort_G['WorkWin_Inf']['OpenWinTrace']
    G['VimBufferLineFileLink' ]       = snapshort_G["VimBufferLineFileLink" ]
    G["TraceInf"              ]       = snapshort_G['TraceInf']
    G['CheckPointInf']['CheckPoints'] = snapshort_G['CheckPointInf']['CheckPoints']
    G['TopoInf']['CurModule']         = snapshort_G['TopoInf']['CurModule']
    G['ModuleLastCallInf']            = snapshort_G['ModuleLastCallInf']
    G['Frame_Inf']['Frame_Path']      = snapshort_G['Frame_Inf']['Frame_Path']
    G['Report_Inf']['Report_Path']    = snapshort_G['Report_Inf']['Report_Path']
    # 2: reload Frame
    os.system('touch ' + G['Frame_Inf']['Frame_Path'])
    assert(os.path.isfile(G['Frame_Inf']['Frame_Path']))
    frame_fp = open(G['Frame_Inf']['Frame_Path'],'w')
    for l in snapshort['frame_file_lines']:
        frame_fp.write(l)
    frame_fp.close()
    # 3: reload Report
    os.system('touch ' + G['Report_Inf']['Report_Path'])
    assert(os.path.isfile(G['Report_Inf']['Report_Path']))
    report_fp = open(G['Report_Inf']['Report_Path'],'w')
    for l in snapshort['report_file_lines']:
        report_fp.write(l)
    report_fp.close()
    # 4: reload act windows inf need re open at API.py
    G['EnvSnapshortWinsInf'] = snapshort['act_win_inf']
    return

# structure -----------------------------------------------------

# frame file_link = { 
#                      'type'     : '', topo                      | check_point          | base_module
#                     'key'      : '', topo module name          | add check point word | base module name
#                     'pos'      : '', module def pos            | add pos              | module pos
#                     'path'     : '', module def file path      | add file path        | module def file path
#                     'fold_inf' :                              {}, 'fold_status': on/off/fix     
#                                                                 , 'level'     : n           
#                                    
#                   }
Frame_Inf = {
     "Frame_Win_x"        : config.frame_window_width      # frame window width
    ,"Frame_Path"         : ''
    ,"FoldLevelSpace"     : config.frame_fold_level_space
}
Frame_Inf['Frame_Path'] = hdl_tags_path + '/' + "Frame.HF" + str(empty_log_index)


# report file_link = {
#                      'key'   :  '' ,  signal_name
#                     'pos'   :  '' ,  match_pos
#                     'path'  :  '' ,  match_path
# }
Report_Inf = {
     "Report_Win_y"       : config.report_window_height        # report window height
    ,"Report_Path"        : hdl_tags_path + '/' + "Report.HF"
}
Report_Inf['Report_Path'] = hdl_tags_path + '/' + "Report.HF" + str(empty_log_index)


WorkWin_Inf ={
     "MaxNum"       : config.max_open_work_window_number
    ,"OpenWinTrace" : []
}

# all vim buffer line file link { path:[...]}
VimBufferLineFileLink = {}

TraceInf = {
     'LastTraceSource' : {'Maybe':[], 'Sure':[], 'ShowIndex': 0, 'SignalName':'', 'Path':'' } # Maybe[{'show':'', 'file_link':{ 'key':'','pos':(l,c),'path':'' } }] 
    ,'LastTraceDest'   : {'Maybe':[], 'Sure':[], 'ShowIndex': 0, 'SignalName':'', 'Path':'' }
    ,'TraceSourceOptimizingThreshold' : config.trace_source_optimizing_threshold
}

# operation trace
OpTraceInf = {
     'TracePoints' : [] # {'path':'', "pos":(line, colum), 'key':''}
    ,'TraceDepth'  : config.max_roll_trace_depth
    ,'Nonius'      : -1  # roll nonius 
}

TopoInf       = {
     'CurModule'    : ''
    ,'TopFoldLevel' : 0
}

CheckPointInf = {
     "MaxNum"         : config.max_his_check_point_num
    ,"CheckPoints"    : []  #{}--- key: '', link: {}
    ,"TopFoldLevel"   : 0
}

BaseModuleInf = {
     "BaseModuleThreshold"  : config.base_module_threshold  # when module inst BaseModuleThreshold times, then default set it to base module
    ,"BaseModules"          : BaseModules # module name set()
    ,"TopFoldLevel"         : 0
}

G = {
     'HDLTagsActive'         : HDLTagsActive
    ,'SupportVHDLPostfix'    : set([])
    ,'SupportVerilogPostfix' : set(config.support_verilog_postfix)
    ,'ModuleInf'             : {}
    ,'ModuleLastCallInf'     : {}           # {module_name:{ upper_module_name:'', 'upper_inst_name':inst_name} }
    ,'FileInf'               : FileInf
    ,'CodeDefineInf'         : {}           # {name: [ {name path pos code_line} ]}
    ,'OpTraceInf'            : OpTraceInf
    ,"Debug"                 : config.debug_mode    # debug mode
    ,"ShowReport"            : config.show_report
    ,"ShowFrame"             : config.show_sidebar
    ,"PrintDebug_F"          : PrintDebug   # function to print debug
    ,"Frame_Inf"             : Frame_Inf    # Frame window inf
    ,"Report_Inf"            : Report_Inf   # report window inf
    ,"WorkWin_Inf"           : WorkWin_Inf  # win config
    ,"VimBufferLineFileLink" : VimBufferLineFileLink
    ,"TraceInf"              : TraceInf
    ,"CheckPointInf"         : CheckPointInf
    ,"BaseModuleInf"         : BaseModuleInf
    ,'TopoInf'               : TopoInf
    ,"FixExtraSpace"         : True         # some situation come extra space, need do nonthing
    ,"IgnoreNextSpaceOp"     : False        # just flod has a else space, not do space op
    ,"EnvSnapshortWinsInf"   : []
    ,"SaveEnvSnapshort_F"    : save_env_snapshort
    ,"VTagsPath"             : hdl_tags_path
}



# has save history sence then just repaly it
start_with_empty_file = False
if not vim_start_open_file :
    start_with_empty_file = True

EnvSnapshort  = {}
if HDLTagsActive and start_with_empty_file and os.path.isfile(hdl_tags_path + '/env_snapshort.pkl'):
    pkl_input       = open(hdl_tags_path + '/env_snapshort.pkl','rb')
    c_snapshort     = pickle.load(pkl_input)
    if c_snapshort['snapshort_dir_path'] == os.getcwd():
        os.system('echo \'do you want reload vim snapshort ? (y/n): \'')
        yes_or_no = raw_input()
        if yes_or_no.lower() in ['y','yes']:
            EnvSnapshort  = c_snapshort
    pkl_input.close()

if EnvSnapshort:
    reload_env_snapshort(EnvSnapshort)

