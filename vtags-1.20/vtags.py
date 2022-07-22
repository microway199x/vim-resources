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
__version__ = "1.20"
__project_url__ = "https://my.oschina.net/u/2520885"

import os
import sys
import re
import pickle


#print help
help = ''
try:
    help = sys.argv[1]
except:
    pass
if help in ['-h','-help']:
    print("(1) generate vtags at code dir, use command \"vtags\" ;"                                    )
    print("(2) config vtags vim at vtags gen dir \"/vtags.db/vim_local_config.py\","                   )
    print("    config items and detail look vim_local_config.py notes;"                                )
    print("(3) support action in vim window:"                                                          )
    print("        1) gi             : if cursor on module call, go in submodule;"                     )
    print("        2) gu             : if cur module called before, go upper module;"                  )
    print("        3) <Space><Left>  : trace cursor word signal source;"                               )
    print("        4) <Space><Right> : trace cursor word signal dest;"                                 )
    print("        5) <Space><Down>  : roll back;"                                                     )
    print("        6) <Space><Up>    : go forward;"                                                    )
    print("        7) <Space>v       : show current module topo "                                      )
    print("                            or fold/unfold sidebar items;"                                  )
    print("        8) <Space>c       : add current cursor as checkpoint, can go back directly;"        )
    print("        9) <Space>b       : add current cursor module as basemodule, not show in topo;"     )
    print("        10) <Space>       : in sidebar or report win, just go cursor line link;"            )
    print("        11) <Space>h      : hold cursor win, will not auto close it;"                       )
    print("        12) <Space>d      : in sidebar, delete valid items(base_module, checkpoint...);"    )
    print("        13) <Space>s      : save current vim snapshort,"                                    )
    print("                            use \"gvim/vim\" without input file to reload snapshort;"       )
    exit()


def cur_file_dir():
     path = sys.path[0]
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

vtags_install_path = cur_file_dir()
sys.path.insert(0,vtags_install_path)

sed_vtags_install_path = re.sub('/','\/',vtags_install_path)
os.system('sed -ig \'s/vtags_install_path =.*/vtags_install_path = "%s"/g\' %s/vtags_vim_api.vim' %(sed_vtags_install_path, vtags_install_path) )
os.system('sed -ig \'s/let is_vtags_installed =.*/let is_vtags_installed = 1/g\' %s/vtags_vim_api.vim' %(vtags_install_path) )

vtags_folder_path = os.getcwd() + '/vtags.db'
os.system('mkdir -p %s'%(vtags_folder_path))
if os.path.isfile(vtags_folder_path + '/vtag_gen_log.txt'):
    os.system('rm -rf '+vtags_folder_path+'/vtag_gen_log.txt')

import Lib.GLB as GLB
G = GLB.G
GLB.vtags_run_log_path[0] = vtags_folder_path + '/vtags_run.log'
import Lib.Code as Code
import Lib.View as View
from Lib.Base import *

# filelist:
#     use "//" as note sign
#     support dir_path and file path mix 
def get_all_verilog_files_from_filelist(filelist_path):
    verilog_file_paths = []
    # get ~ path
    home_path = os.popen('echo ~').readlines()[0].rstrip('\n').rstrip('/')
    for l in open(filelist_path,'r').readlines():
        l = l.strip('\n')
        l = re.sub('//.*','',l)
        l = re.sub('^~', home_path, l)
        if re.match('\s*$',l):
            continue
        path = l
        if os.path.isdir(path):
            c_files_path     = os.popen('find ' + dir_path + ' -type f 2>/dev/null').readlines()
            c_files_path     = [ d_l.rstrip('\n') for d_l in c_files_path ]
            for c_f in c_files_path:
                if get_file_path_postfix(c_f) not in G['SupportVerilogPostfix']:
                    continue
                verilog_file_paths.append(c_f)
        if os.path.isfile(path):
            if get_file_path_postfix(path) not in G['SupportVerilogPostfix']:
                continue
            verilog_file_paths.append(path)
    return verilog_file_paths

# get all verilog files inf and merge
#   modules_inf  = { module_name: module_inf }
#   defines_inf  = { macro_name : [ define_inf ] }
#   files_inf    = { file_name  : file_inf }
#       module_inf    = {  'module_name'        : module_name
#                         ,'file_path'          : f
#                         ,'line_range_in_file' : (module_start_line_num, module_end_line_num)
#                         ,'sub_modules'        : sub_modules }
#       define_inf    = {  "name" : xxx
#                         ,"path" : f 
#                         ,"pos"  : (line_num, colum_num)  # name first char pos
#                         ,'code_line' : `define xxx .... }
#       file_inf      = {  'glb_defines'   : [ define_inf ] 
#                         ,'module_infs'   : [ module_inf ]
#                         ,'module_calls'  : [ call_sub_inf ]
#                         ,'file_edit_inf' : { 'create_time': ..., 'last_modify_time': ...}
#                       call_sub_inf  =  { 'inst_name'     : inst_name
#                                         ,'module_name'   : modu_name
#                                         ,'match_range'   : match_range }
def get_verilog_files_code_inf(paths):
    # step 1/2 get all module/define inf
    all_file_module_inf = {}
    all_file_define_inf = {}
    all_module_name     = set()
    print('step 1/2:')
    for i,f in enumerate(paths):
        show_progress_bar( i, len(paths))
        PrintDebug(f)
        # gen cur module and define inf
        cur_file_module_inf = get_single_verilog_file_module_inf(f)
        cur_file_define_inf = get_single_verilog_file_define_inf(f)
        # add to result
        all_file_module_inf[f] = cur_file_module_inf
        all_file_define_inf[f] = cur_file_define_inf
        all_module_name        = all_module_name | set([ mi['module_name'] for mi in cur_file_module_inf])
    print('')
    # step 2/2 get all file sub call inf
    all_file_subcall_inf = {}
    patten = get_submodule_match_patten(all_module_name)
    print('step 2/2:')
    for i,f in enumerate(paths):
        PrintDebug(f)
        show_progress_bar( i, len(paths))
        all_file_subcall_inf[f] = get_single_verilog_file_subcall_inf(f, patten, all_module_name)
    print('')
    # merge to all_file_inf
    all_file_inf = {}
    for i,f in enumerate(paths):
        add_single_verilog_file_submodule_inf_to_module_inf( all_file_module_inf[f], all_file_subcall_inf[f] )
        all_file_inf[f] = {
             'glb_defines'   : all_file_define_inf[f]
            ,'module_infs'   : all_file_module_inf[f]
            ,'module_calls'  : all_file_subcall_inf[f]
            ,'file_edit_inf' : { 'create_time': os.path.getctime(f), 'last_modify_time': os.path.getmtime(f)}
        }
    modules_inf , global_defines_inf = gen_modules_and_defines_inf(all_file_inf)
    return {
         'files_inf'   : all_file_inf
        ,'modules_inf' : modules_inf
        ,'defines_inf' : global_defines_inf
    }

#------------------------function for get module inf--------------------
filelist_path = ''
verilog_file_paths = []
if filelist_path:
    verilog_file_paths = get_all_verilog_files_from_filelist(filelist_path)
else:
    c_dir_path           = os.getcwd()
    c_dir_files_path     = os.popen('find ' + c_dir_path + ' -type f 2>/dev/null').readlines()
    c_dir_files_path     = [ d_l.rstrip('\n') for d_l in c_dir_files_path ]
    for c_f in c_dir_files_path:
        if get_file_path_postfix(c_f) not in G['SupportVerilogPostfix']:
            continue
        verilog_file_paths.append(c_f)

# get all code inf
verilog_code_inf = get_verilog_files_code_inf(verilog_file_paths)
modules_inf  = verilog_code_inf['modules_inf']
files_inf    = verilog_code_inf['files_inf'  ]
defines_inf  = verilog_code_inf['defines_inf']

# set base module
base_modules     = set()
base_threshold  = G['BaseModuleInf']['BaseModuleThreshold']
module_inst_num = {}
for m in modules_inf:
    for sm in modules_inf[m]['sub_modules']:
        module_name = sm['module_name']
        module_inst_num.setdefault(module_name,0)
        module_inst_num[module_name] += 1
for m in module_inst_num:
    if module_inst_num[m] >= base_threshold:
        base_modules.add(m)

# change vim HDLTags path

fp = open(vtags_folder_path + '/files_inf.py','w')
fp.write('FileInf = %s \n'%(files_inf.__str__()))
fp.write('HDLTagsActive = True \n')
fp.close()
if not os.path.isfile(vtags_folder_path + '/vim_local_config.py'):
    os.system('cp %s/vim_glb_config.py %s/vim_local_config.py'%(vtags_install_path, vtags_folder_path))
if not os.path.isfile(vtags_folder_path+'/base_modules.pkl'):
    output = open(vtags_folder_path+'/base_modules.pkl','wb')
    pickle.dump(base_modules, output)
    output.close()