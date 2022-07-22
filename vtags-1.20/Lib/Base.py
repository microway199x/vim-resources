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
try:
    import vim
except: 
    pass
import os
import re
import pickle
import GLB
G = GLB.G
# function to print debug
PrintDebug  = G['PrintDebug_F']

def get_valid_code( str ):
    str = re.sub('(^\s*)|(\s*$)', '' ,str)
    str = re.sub('//.*', '' ,str)
    str = re.sub('^`.*', '' ,str)  # bug ^\s*`.*
    return str

def get_valid_code_leave_head_space( str ):
    str = re.sub('\s*$', '' ,str)
    str = re.sub('//.*', '' ,str)
    str = re.sub('^`.*', '' ,str)
    return str

def cur_in_frame():
    return vim.current.buffer.name == G['Frame_Inf']['Frame_Path']

def cur_in_report():
    return vim.current.buffer.name == G['Report_Inf']['Report_Path']

def get_path_for_name(path_or_name):
    if path_or_name == 'Frame':
        return G["Frame_Inf"]["Frame_Path"]
    if path_or_name == 'Report':
        return G["Report_Inf"]["Report_Path"]
    may_module_inf = get_module_inf(path_or_name)
    if may_module_inf:
        return may_module_inf['file_path']
    return path_or_name

def get_file_name_from_path(path):
    return re.sub('.*/','',path)

def get_full_word(line, y):
    pre_part  = ( re.match('^(?P<pre>\w*)',(line[:y])[::-1]).group('pre') )[::-1]
    post_part = re.match('^(?P<post>\w*)', line[y:]).group('post')
    return pre_part + post_part

def get_file_path_postfix(file_path):
    if type(file_path) != str:
        return
    split_by_dot = file_path.split('.')
    if len(split_by_dot) < 2 : # which means file_path has no postfix
        return ''
    # post_fix = split_by_dot[-1].lower() # postfix don't care case
    post_fix = split_by_dot[-1]           # postfix care case
    return post_fix

def get_file_hdl_type(file_path):
    postfix = get_file_path_postfix(file_path)
    if postfix in G['SupportVHDLPostfix']:
        return 'vhdl'
    elif postfix in G['SupportVerilogPostfix']:
        return 'verilog'
    else:
        return ''

#------------------------------------------------------------
def get_vhdl_full_line(codes, start_pos, direction):
    pass

def get_verilog_pre_full_line(codes, start_pos):
    pre_full_line = ''
    start_x, start_y = start_pos
    start_line = codes[start_x][:start_y+1]
    start_line = start_line.strip('\n')
    start_line = re.sub('//.*','',start_line)
    colon_y    = start_line.rfind(';')
    if colon_y != -1:
        pre_full_line = start_line[colon_y+1:]
    else:
        pre_full_line = start_line
        for i in range(start_x-1,-1,-1):
            t_line = codes[i].strip('\n')
            t_line = re.sub('//.*', '', t_line)
            t_colon_y = t_line.rfind(';')
            if t_colon_y != -1:
                pre_full_line = t_line[t_colon_y+1:] + ' ' + pre_full_line
                break
            else:
                pre_full_line = t_line + ' ' +pre_full_line
    return pre_full_line

def get_verilog_post_full_line(codes, start_pos):
    post_full_line = ''
    start_x, start_y = start_pos
    start_line = codes[start_x][start_y:]
    start_line = start_line.strip('\n')
    start_line = re.sub('//.*','',start_line)
    colon_y    = start_line.find(';')
    if colon_y != -1:
        pre_full_line = start_line[:colon_y+1]
    else:
        pre_full_line = start_line
        for i in range(start_x+1,len(codes)):
            t_line = codes[i].strip('\n')
            t_line = re.sub('//.*', '', t_line)
            t_colon_y = t_line.find(';')
            if t_colon_y != -1:
                pre_full_line = pre_full_line + ' ' + t_line[: t_colon_y+1]
                break
            else:
                pre_full_line = pre_full_line + ' ' + t_line
    return pre_full_line

def get_verilog_full_line(codes, start_pos, direction):
    if direction == -1:  # 0 <- x
        return get_verilog_pre_full_line(codes, start_pos)
    elif direction == 1: #      x -> n
        return get_verilog_post_full_line(codes, start_pos)
    elif direction == 0: # 0 <- x -> n
        return get_verilog_pre_full_line(codes, start_pos) + get_verilog_post_full_line(codes, start_pos)[1:] # [1:] because start char at both part
    else:
        return ''

def get_full_line( codes, hdl_type, start_pos, direction = 0):
    if hdl_type == 'vhdl': 
        return get_vhdl_full_line(codes, start_pos, direction)
    elif hdl_type == 'verilog':
        return get_verilog_full_line(codes, start_pos, direction)
    else:
        return ''

# --------------------------------------------------------
# ok
def recgnize_io_signal_line(line, line_num):
    # pre check if is not io
    if line.find('input') == -1 and line.find('output') == -1:
        return False
    line = line.strip('\n')
    line = re.sub('//.*','',line) # del notes
    # raw re match
    re_match = re.match('\s*(input|output)\W',line)
    if not re_match:
        re_match = re.match('(?P<prefix>.*\(\s*)(?P<real_io>(input|output)\W.*)',line)
        if re_match:
            prefix       = re_match.group('prefix')
            real_io_line = re_match.group('real_io')
            line         = ' '*(len(prefix)) + real_io_line
        else:
            return False
    # match used egrep io line decode function
    egrep_io_line = str(line_num)+':'+line
    io_inf = decode_egreped_verilog_io_line(egrep_io_line)['io_infs']
    return io_inf
    #      "name"        : name
    #    , "io_type"     : io_type
    #    , "left"        : left_index
    #    , "right"       : right_index
    #    , "size"        : size
    #    , 'line_num'    : line_num
    #    , 'name_pos'    : (line_num, colm_num)
    #    , 'code_line'   : code_line
    #    , 'signal_type' : signal_type }

#-----------------------------------------------------------
# ok
def search_verilog_code_use_grep(key, path, row_range = ()):
    search_result = []
    if not path:
        path = vim.current.buffer.name
    match_lines    = os.popen('egrep -n -h \'(^|\W)%s(\W|$)\' %s'%(key, path)).readlines()
    for l in match_lines:
        l = l.strip('\n')
        split0 = l.split(':')
        line_num   = int(split0[0]) - 1
        code_line  = ':'.join(split0[1:])
        if row_range and ( line_num not in range(row_range[0], row_range[1]+1 ) ):
            continue
        # del note see if has key
        s0 = re.search('(?P<pre>^|\W)%s(\W|$)'%(key), re.sub('//.*','',code_line) )
        if s0:
            colum_num  = s0.span()[0] + len(s0.group('pre'))
            match_pos  = (line_num, colum_num)
            line       = code_line
            search_result.append( (match_pos, line) )
    return search_result


#----------------------------------------------------------
def get_fram_topo_sub_inf(topo_module, cur_level):
    sub_level   = cur_level + 1
    topo_prefix = G['Frame_Inf']['FoldLevelSpace'] * sub_level
    topo_datas   = []
    topo_links   = []
    sub_func_modules, sub_base_modules = get_sub_func_base_module(topo_module)
    # first deal sub func module, show "inst(module)"
    sub_func_modules_inst_names = list(sub_func_modules)
    sub_func_modules_inst_names.sort()
    for c_sub_inst_name in sub_func_modules_inst_names:
        c_call_sub_inf    = sub_func_modules[c_sub_inst_name]
        c_sub_module_name = c_call_sub_inf['module_name']
        # gen show data
        c_str      = '%s%s(%s)'%(topo_prefix, c_sub_inst_name, c_sub_module_name)
        topo_datas.append(c_str)
        # gen link
        c_topo_link = {
                 'type'           : 'topo'
                ,'topo_inst_name' : ''
                ,'key'            : ''
                ,'pos'            : ''
                ,'path'           : ''
                ,'fold_inf'       : {'fold_status':'off', 'level': sub_level}
        }
        c_sub_module_inf = get_module_inf(c_sub_module_name)
        if c_sub_module_inf:
            c_topo_link['topo_inst_name'] = c_sub_inst_name
            c_topo_link['key'           ] = c_sub_module_name
            c_topo_link['pos'           ] = c_sub_module_inf['module_pos']
            c_topo_link['path'          ] = c_sub_module_inf['file_path']
            # show cur module, then all submodule, last call set to cur module
            set_module_last_call_inf(c_sub_module_name, topo_module, c_call_sub_inf['inst_name'])
        topo_links.append(c_topo_link)
    sub_base_modules_names = list(sub_base_modules)
    sub_base_modules_names.sort()
    if len(sub_base_modules_names) > 0:
        # deal base , show "module(n)"
        # add one to sep func and base
        topo_datas.append(topo_prefix+'------')
        c_topo_link = {
             'type'           : 'topo'
            ,'topo_inst_name' : ''
            ,'key'            : ''
            ,'pos'            : ()
            ,'path'           : ''
            ,'fold_inf'       : {'fold_status':'on', 'level': sub_level}
        }
        topo_links.append(c_topo_link)
        for c_sub_module_name in sub_base_modules_names:
            # deal data
            c_sub_inst_n = len(sub_base_modules[c_sub_module_name])
            c_str = '%s%s(%d)'%(topo_prefix,c_sub_module_name,c_sub_inst_n)
            topo_datas.append(c_str)
            # deal link
            c_topo_link = {
                     'type'           : 'topo'
                    ,'topo_inst_name' : ''
                    ,'key'            : ''
                    ,'pos'            : ''
                    ,'path'           : ''
                    ,'fold_inf'       : {'fold_status':'off', 'level': sub_level}
            }
            c_sub_module_inf = get_module_inf(c_sub_module_name)
            if c_sub_module_inf:
                c_topo_link['key' ] = c_sub_module_name
                c_topo_link['pos' ] = c_sub_module_inf['module_pos']
                c_topo_link['path'] = c_sub_module_inf['file_path']
            topo_links.append(c_topo_link)
    return topo_datas, topo_links

def get_fram_check_point_inf():
    datas = []
    links = []
    for cp in G['CheckPointInf']['CheckPoints']:
        datas.append(cp['key'])    
        links.append(cp['link'])
    return datas, links   

def get_fram_base_module_inf():
    datas = []
    links = []
    base_module_level = G['BaseModuleInf']['TopFoldLevel'] + 1
    base_module_space = G['Frame_Inf']['FoldLevelSpace'] * base_module_level
    base_modules      = list(G['BaseModuleInf']['BaseModules'])
    base_modules.sort()
    for bm in base_modules:
        key  = base_module_space + bm
        link = {
             'type'     : 'base_module'
            ,'key'      : bm
            ,'pos'      : ''
            ,'path'     : ''
            ,'fold_inf' : { 'fold_status': 'fix', 'level': base_module_level }
        }
        bm_module_inf = get_module_inf(bm)
        if bm_module_inf:
            link['pos']  = bm_module_inf['module_pos']
            link['path'] = bm_module_inf['file_path']
        datas.append(key)
        links.append(link)
    return datas, links

###########################################################
#----------------------------------------------------------
def decode_egreped_verilog_io_line(o_io_line):
    # exp: 
    #   365:output alu_frf_part_p0_w;
    #   366:output [127:0] alu_frf_data_p0_w;
    #   357:output [THR_WIDTH-1:0] alu_dst_cond_tid_w
    #   368:output reg  alu_frf_part_p0_w;
    #   369:output wire [127:0] alu_frf_data_p0_w;
    #   370:output reg  [THR_WIDTH-1:0] alu_dst_cond_tid_w
    #   388:input [width-1 : 0]  A,B;
    # split by ":" |  388:input [width-1 : 0]  A,B;
    # split0       |   0 ^      1        ^  2
    split0    = o_io_line.split(':')
    line_num  = int(split0[0]) - 1   # -1 because egrep form 1, our line from 0
    code_line = ':'.join(split0[1:])
    # valid code line is code_line del note, and change all \s+ to ' '
    valid_code_line = re.sub('(//.*)|(^\s+)|(\s+$)','',code_line)
    valid_code_line = re.sub('\s+',' ',valid_code_line)
    valid_code_line = re.sub('\W*$', '',valid_code_line)# del end ";" or ","
    # io type is the first word in valid_code_line
    match_io_type   = re.match('(?P<io_type>\w+)\s*(?P<other>.*)',valid_code_line)
    assert(match_io_type)
    io_type         = match_io_type.group('io_type')
    other           = match_io_type.group('other').strip(' ')
    # other: [width-1 : 0]  A,B | wire [127:0] alu_frf_data_p0_w | alu_frf_part_p0_w
    # get name, name is the last word or words sep by ',' ; reverse it and reverse back
    # exp: A | A,B | A,B,C
    match_name = re.match('\s*(?P<r_names_str>\w+(\s*,\s*\w+)*)\s*(?P<r_other>.*)',other[::-1])
    assert(match_name),'%s | %s'%(other,code_line)
    other      = (match_name.group('r_other')[::-1]).strip(' ')
    names_str  = match_name.group('r_names_str')[::-1]
    names      = re.sub('\s+','',names_str).split(',')
    names_pos  = []
    if len(names) == 1:
        colum = re.search('\W%s(\W|$)'%(names[0]),code_line).span()[0] + 1
        names_pos = [ ( line_num, colum ) ]
    else:
        for n in names:
            colum = re.search('\W%s(\W|$)'%(n),code_line).span()[0] + 1
            names_pos.append( (line_num, colum) )
    # signal_type is the first word of other, maybe empty
    # case0 : empty
    # case1 : reg
    # case2 : reg  [THR_WIDTH-1:0]
    # case3 : [127:0]
    signal_type  =  'wire'
    if other:
        match_signal_type = re.match('\s*(?P<signal_type>\w*)\s*(?P<other>.*)',other)
        assert(match_signal_type)
        m_signal_type = match_signal_type.group('signal_type')
        if m_signal_type:
            signal_type = m_signal_type
        other = match_signal_type.group('other').strip(' ')
    # other is empty or [a : b]
    left_index   =  ''
    right_index  =  ''
    size         =  1
    if other:
        assert(other[0] == '[' and other[-1] == ']'),'%s'%(other)
        indexs = other[1:-1].split(':')
        if len(indexs) == 2:
            left_index  = indexs[0].strip(' ')
            right_index = indexs[1].strip(' ')
        try:
            left_index  = int(left_index)
            right_index = int(left_index)
            size        = right_index - left_index + 1
        except:
            size        = other
    # may a line has mulity names
    io_infs = {}
    for i, name in enumerate(names):
        io_infs[name] = {
              "name"        : name
            , "io_type"     : io_type
            , "left"        : left_index
            , "right"       : right_index
            , "size"        : size
            , 'line_num'    : line_num
            , 'name_pos'    : names_pos[i]
            , 'code_line'   : code_line
            , 'signal_type' : signal_type 
        }
    return {'io_infs':io_infs, 'name_list':names}

#------------------------------------------------
# for code in verilog modules, from pos to find next pair ")"
# case 0:
# if pos is "(" | ( A...B )                              
# pos           | ^                                       
# rest          |  parm_line= A...B,  end_pos  = B 's pos 
# case 1:
# if pos not "("| ( A...B )                              
# pos           |   ^                                       
# rest          |   parm_line= A...B,  end_pos  = B 's pos
def get_str_to_next_right_bracket(module_lines, pos):
    assert(0),'not used not realized '

















































def get_str_to_pre_left_bracket(module_lines, pos):
    assert(0),'not used not realized '

















































#-------------------------------------------
# for situation: 
# case0  : module_name inst_name (.a(A), .b(B), .c(C)) |
#        |                        ^                    | input pos
#        | ^0          ^1                              | module_range[0]
# case1  : module_name #( .a(A), .b(B), .c(C) ) inst_name ( ... )
#        |                ^                            | input pos
#        | ^                                           | module_range[0]  
# case2  : module_name #( A, B, C ) inst_name ( .x(X), .y(Y) )
#        |                                      ^      | input pos
#        | ^                                           | module_range[0]  
# case3  : module_name ... inst_name[a:b] ...
# case4  : module_name ... inst_name[a:b] (A,B,C)
def get_verilog_sub_module_inf_from_dot_line( pos, module_lines, module_start_line_num):
    dot_line = get_valid_code(module_lines[pos[0]])
    assert(dot_line[pos[1]] == '.')
    module_name =  ''
    inst_name   =  ''
    match_range =  []
    match_pos   =  ()
    # first deal pre dot line
    pre_line_end       = False
    dot_pre_line       = dot_line[:pos[1]+1] # module_name inst_name (.
    pre_next_line_num  = pos[0] - 1
    search_case0       = '' 
    search_case12      = ''
    while not pre_line_end:
        semicolon_y    = dot_pre_line.find(';')
        if semicolon_y != -1:
            pre_line_end = True
            dot_pre_line = dot_pre_line[semicolon_y + 1:]
        search_case0 = re.search('(^|\W)(?P<m_name>\w+)\s+(?P<i_name>\w+(\s*\[[^\[\]]*\])?)\s*\(\s*\.$',dot_pre_line)
        if search_case0:
            module_name    = search_case0.group('m_name')
            inst_name      = search_case0.group('i_name')
            break
        search_case12 = re.search('(^|\W)(?P<m_name>\w+)\s*#\s*\(', dot_pre_line)
        if search_case12:
            module_name    = search_case12.group('m_name')
            match_case2_inst_name   = re.match('\.\s*\(\s*(?P<r_i_name>(\s*\][^\[\]]*\[\s*)?\w+)',dot_pre_line[::-1]) # inst_name ( .
            if match_case2_inst_name:
                inst_name      = match_case2_inst_name.group('r_i_name')[::-1]
            break
        if pre_next_line_num >= 0:
            dot_pre_line = get_valid_code(module_lines[pre_next_line_num]) + ' ' + dot_pre_line
            pre_next_line_num -= 1
        else:
            pre_line_end = True
    # if not match anyone then unrecgize
    if not (search_case0 or search_case12):
        PrintDebug('Error: 0 cur dot match cannot recgnize ! line: %s , pos: %s'%(dot_line, pos.__str__()))
        return False
    # if no inst name need decode dot back line
    if not inst_name:  # case1: module_name #( .a(A), .b(B), .c(C) ) inst_name ( ... )
        back_line_end       = False
        dot_back_line       = dot_line[pos[1]:] # .a(A), .b(B), .c(C))
        back_next_line_num  = pos[0] + 1
        search_case1_inst_name = '' 
        while not back_line_end:
            semicolon_y    = dot_back_line.find(';')
            if semicolon_y != -1:
                back_line_end = True
                dot_back_line = dot_back_line[:semicolon_y]
            # inst_name ( .x
            search_case1_inst_name = re.search('\)\s*(?P<i_name>\w+(\s*\[[^\[\]]*\])?)\s*\(',dot_back_line)
            if search_case1_inst_name:
                inst_name = search_case1_inst_name.group('i_name')
                break
            if back_next_line_num < len(module_lines):
                dot_back_line = dot_back_line + ' ' +get_valid_code(module_lines[back_next_line_num])
                back_next_line_num += 1
            else:
                back_line_end = True
    if not inst_name:
        PrintDebug('Error: 1 cur dot match cannot recgnize inst name ! line: %s , pos: %s'%(dot_line, pos.__str__()))
        return False
    match_range    = [ pre_next_line_num + 1 + module_start_line_num, -1 ]
    module_y       = module_lines[pre_next_line_num + 1].find(module_name)
    assert(module_y != -1)
    match_pos      = ( pre_next_line_num + 1 + module_start_line_num, module_y )
    return {
         'inst_name'     : inst_name
        ,'module_name'   : module_name
        ,'match_range'   : match_range
        ,'match_pos'     : match_pos
    }

# case 0: dff # (...) my_dff(a, b, c);  in only one line
def get_verilog_sub_module_inf_from_pound_line( pos, module_lines, module_start_line_num):
    pound_line = get_valid_code(module_lines[pos[0]])
    match_sub  = re.match('\s*(?P<module_name>\w+)\s+#\s*\(.*\)\s*(?P<inst_name>\w+)\s*\(.*\)\s*;\s*', pound_line)
    if match_sub:
        return {
             'inst_name'   : match_sub.group('inst_name')
            ,'module_name' : match_sub.group('module_name')
            ,'match_range' : [ pos[0] + module_start_line_num, pos[0] + module_start_line_num ]
            ,'match_pos'   : ( pos[0] + module_start_line_num, module_lines[pos[0]].find(match_sub.group('module_name')) )
        }
    return False

# for current valid module lines
# find each pair           : (".xxx(...)"  ";")
# get the each pair result :{  'inst_name'     : inst_name
                            # ,'module_name'   : modu_name
                            # ,'match_range'   : match_range
                            # ,'match_pos'     : match_pos}
# finial result is         : [ pair_result0, pair_result1, ... ]
def get_verilog_sub_module_inf(module_lines, module_start_line_num, gen_vtags_log_path = ''):
    sub_module_inf        = []
    has_call_sub_not_end  = False
    find_next = True
    for i ,l in enumerate(module_lines):
        if find_next:
            assert(not has_call_sub_not_end),'already start new search, should not has unfinish subcall'
            cur_sub_module_inf   = {}
            cur_match_right_part = ''
            if l.find('.') != -1:
                l  = get_valid_code(l)
                s0 = re.search('(^|\W)\.\w+\s*\(', l)
                if not s0:
                    continue
                # no matter recgnize or not , must wait next ";", continue search
                find_next = False
                # get dot pos
                dot_colm = ''
                if l[0] is '.':
                    dot_colm = 0
                else:
                    dot_colm = s0.span()[0] + 1
                assert(dot_colm != '')
                cur_match_right_part = l[s0.span()[1]:]
                # get cur sub module inf
                cur_sub_module_inf = get_verilog_sub_module_inf_from_dot_line( (i, dot_colm), module_lines, module_start_line_num)
            elif l.find('#') != -1:
                l  = get_valid_code(l)
                s1 = re.search('#\s*\(', l)
                if not s1:
                    continue
                # no matter recgnize or not , must wait next ";", continue search
                find_next = False
                # get dot pos
                pound_colm = ''
                dot_colm = s1.span()[0]
                cur_match_right_part  = l[s1.span()[1]:]
                # get cur sub module inf
                cur_sub_module_inf = get_verilog_sub_module_inf_from_pound_line( (i, pound_colm), module_lines, module_start_line_num)
            else:
                continue
            # find result in two way
            if cur_sub_module_inf:
                assert(not has_call_sub_not_end)
                sub_module_inf.append(cur_sub_module_inf)
                has_call_sub_not_end = True
            else:
                PrintDebug( 'Error : not recgnize %d: %s '%(i+module_start_line_num, l ), gen_vtags_log_path )
            # no matter find or not , current back line has valid ";", continue find new match
            if cur_match_right_part.find(';') != -1:
                find_next = True
            # if end at current line, set the call range [1]
            if has_call_sub_not_end and cur_match_right_part.find(';') != -1:
                sub_module_inf[-1]['match_range'][1] = i + module_start_line_num # start line and end line the same
                has_call_sub_not_end = False
            continue
        if (not find_next) and l.find(';') != -1:
            if get_valid_code(l).find(';') != -1:
                # if current not find next, and match a valid ";", need continue search
                find_next = True
                # if has unended sub call, and find a valid ";", set last call sub range[1]
                if has_call_sub_not_end:
                    sub_module_inf[-1]['match_range'][1] = i + module_start_line_num # end line is the first ; line
                    has_call_sub_not_end = False
        # if has_call_sub_not_end and (not find_next) and l.find(';') != -1:
        if has_call_sub_not_end and l.find(';') != -1:
            if get_valid_code(l).find(';') != -1:
                sub_module_inf[-1]['match_range'][1] = i + module_start_line_num # end line is the first ; line
                has_call_sub_not_end = False
    if has_call_sub_not_end:
        PrintDebug('Error : call sub not end at end module , try module end as callsub end ! : %s'%(sub_module_inf[-1].__str__()), gen_vtags_log_path)
        sub_module_inf[-1]['match_range'][1] = len(module_lines) - 1 + module_start_line_num # end line is the first ; line
    return sub_module_inf


#-------------------------------------------
#   modules_inf  = { module_name: module_inf }
#   defines_inf  = { macro_name : [ define_inf ] }
#   files_inf    = { file_name  : file_inf }
#       module_inf    = {  'module_name'        : module_name
#                         ,'file_path'          : f
#                         ,'line_range_in_file' : (module_start_line_num, module_end_line_num)
#                         ,'module_pos'         : module_pos
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
#                                         ,'module_name'   : module_name
#                                         ,'match_range'   : match_range
#                                         ,'match_pos'     : match_pos }
def gen_modules_and_defines_inf(files_inf):
    modules_inf                   = {}
    global_defines_inf            = {}
    for c_file_path in files_inf:
        c_file_inf               = files_inf[c_file_path]
        # merge defines
        c_file_glb_defines       = c_file_inf['glb_defines']
        for d in c_file_glb_defines:
            d_name = d['name'] 
            global_defines_inf.setdefault(d_name,[])
            global_defines_inf[d_name].append(d)
        # merge modules_inf
        c_file_module_infs       = c_file_inf['module_infs']
        for m in c_file_module_infs:
            mn = m['module_name']
            if mn in modules_inf:
                PrintDebug('Error: module %s has multip defines ! in %s '%(mn, [ modules_inf[mn]['file_path'], m['file_path'] ].__str__() ))
            else:
                modules_inf.setdefault(mn, None)
            modules_inf[mn] = m
    return modules_inf, global_defines_inf

def updata_file_pickle_inf(path):
    PrintDebug('Care: updata database, file: %s'%(path))
    if get_file_path_postfix(path) not in G['SupportVerilogPostfix']:
        PrintDebug('Warning: updata_file_pickle_inf: file not verilog file ! file: %s'%(path))
        return False
    if not os.path.isfile(path):
        PrintDebug('Error: updata_file_pickle_inf: file not exit ! file: %s'%(path))
        return
    new_file_modules_inf = get_single_verilog_file_code_inf(path)
    glb_defines          = new_file_modules_inf['glb_defines']    #[ define_inf ] 
    module_infs          = new_file_modules_inf['module_infs']    #[ module_inf ]
    # updata files_inf
    if path not in G['FileInf']:
        # if add new inf just add
        G['FileInf'][path] = new_file_modules_inf
        # add glb_defines
        for gd in glb_defines:
            gd_name = gd['name']
            G['CodeDefineInf'].setdefault(gd_name,[])
            G['CodeDefineInf'][gd_name].append( gd )
        # add module infs
        for m_inf in module_infs:
            m_name = m_inf['module_name']
            if m_name in G['ModuleInf']:
                PrintDebug('Error: module %s define twice ! used last at %s, %s'%(m_name, G['ModuleInf'][m_name]['file_path'], path))
            G['ModuleInf'][m_name] = m_inf
    else:
        # need refresh old and add new, so just gen new inf
        G['FileInf'][path] = new_file_modules_inf
        G['ModuleInf'], G['CodeDefineInf'] = gen_modules_and_defines_inf(G['FileInf'])
    # update pickles
    if not os.path.isdir(G['VTagsPath']):
        os.system('mkdir -p '+G['VTagsPath'])
    fp = open(G['VTagsPath'] + '/files_inf.py','w')
    fp.write('FileInf = %s \n'%(G['FileInf'].__str__()))
    fp.write('HDLTagsActive = True \n')
    fp.close()

def get_module_inf(module_name):
    if module_name not in G['ModuleInf']:
        PrintDebug('Warning:get_module_inf: "%s" not konwn module !'%(module_name) )
        return False
    module_inf       = G['ModuleInf'][module_name]
    module_path      = module_inf['file_path']
    cur_inf_time     = G['FileInf'][module_path]['file_edit_inf']['last_modify_time']
    last_modify_time = os.path.getmtime(module_path)
    # cur module file not modify, then inf valid and return
    if cur_inf_time == last_modify_time:
        return module_inf
    # if cur module file modify , update Module_inf and return new
    updata_file_pickle_inf(module_path)
    return get_module_inf(module_name)

#----------------------------------------------------
def get_line_inf_from_cur_file_inf(line_num, file_inf):
    line_module_inf   = {}
    line_call_sub_inf = {}
    module_infs  = file_inf['module_infs' ] #[ module_inf ]
    module_calls = file_inf['module_calls'] #[ call_sub_inf ]
    # first get current line module inf
    for m_inf in module_infs:
        c_module_range = m_inf['line_range_in_file']
        if c_module_range[1] < line_num:
            continue
        if line_num < c_module_range[0]:
            break
        line_module_inf = m_inf
    # second get current line call sub inf
    for c_inf in module_calls:
        c_call_range = c_inf['match_range']
        if c_call_range[1] < line_num:
            continue
        if line_num < c_call_range[0]:
            break
        line_call_sub_inf = c_inf
    return  {
         'line_module_inf'   : line_module_inf
        ,'line_call_sub_inf' : line_call_sub_inf
    }

def get_file_line_inf(line_num, path = ''):
    if not path:
        path = vim.current.buffer.name
    if get_file_path_postfix(path) not in G['SupportVerilogPostfix']:
        PrintDebug('Warning: get_file_line_inf: file not verilog file ! file: %s'%(path))
        return False
    if path not in G['FileInf']:
        updata_file_pickle_inf(path)
        if path not in G['FileInf']:
            PrintDebug('Warning: get_file_line_inf: %s has no file database !'%(path) )
            return False
    cur_inf_time     = G['FileInf'][path]['file_edit_inf']['last_modify_time']
    last_modify_time = os.path.getmtime(path)
    # cur module file not modify, then inf valid and return
    if cur_inf_time == last_modify_time:
        return get_line_inf_from_cur_file_inf( line_num, G['FileInf'][path] )
    # if cur module file modify , update Module_inf and return new
    updata_file_pickle_inf(path)
    return get_file_line_inf(line_num, path)

#----------------------------------------------
# { module_name:'', 'call_inf':atom}

def get_module_last_call_inf(module_name):
    if module_name not in G['ModuleLastCallInf']:
        return False
    upper_module_name = G['ModuleLastCallInf'][module_name]['upper_module_name']
    upper_inst_name   = G['ModuleLastCallInf'][module_name]['upper_inst_name']
    if upper_module_name not in G['ModuleInf']:
        return False
    if upper_inst_name not in G['ModuleInf'][upper_module_name]['sub_calls']:
        return False
    upper_call_inf = G['ModuleInf'][upper_module_name]['sub_calls'][upper_inst_name]
    return {'upper_module_name': upper_module_name, 'upper_call_inf': upper_call_inf}

def set_module_last_call_inf(sub_module_name, upper_module_name, upper_inst_name):
    G['ModuleLastCallInf'][sub_module_name] = { 'upper_module_name': upper_module_name, 'upper_inst_name': upper_inst_name }


#----------------------------------------------
# for a module's submodule, sep function module and base module
def get_sub_func_base_module(module_name):
    func_modules   = {} # inst:module
    base_modules   = {} # module : [inst0,inst1...]
    sub_modules    = []
    if module_name in G['ModuleInf']:
        sub_modules = G['ModuleInf'][module_name]['sub_modules']
    for sm in sub_modules:
        inst_name   =  sm['inst_name']
        module_name =  sm['module_name']
        if module_name in G['BaseModuleInf']['BaseModules']:
            base_modules.setdefault(module_name,[])
            base_modules[module_name].append(inst_name)
        else:
            if inst_name in func_modules: # has to same inst name, may be use `ifdefine sep
                new_inst_name = inst_name+'_'+str(sm['match_range'][0])
                func_modules[new_inst_name] = sm
                continue
            func_modules[inst_name] = sm
    return func_modules, base_modules

#----------------------------------------------
# update function base information, no need added each times
def update_base_module_pickle():
    pkl_output = open(G['VTagsPath'] + '/base_modules.pkl','wb')
    pickle.dump(G['BaseModuleInf']['BaseModules'], pkl_output)
    pkl_output.close()

#----------------------------------------------
# topo/checkpoint/basemodule line range ,in frame file
def get_frame_range_inf():
    fram_file_link = G["VimBufferLineFileLink"][G['Frame_Inf']['Frame_Path']]
    # get topo range , default 0,0
    has_topo          = False
    has_check_point   = False
    has_base_module   = False
    topo_range        = [0, 0]
    check_point_range = [0, 0]
    base_module_range = [0, 0]
    for i,link in enumerate(fram_file_link):
        if link and (link['type'] == 'topo'):
            if not has_topo:
                topo_range[0] = i
                has_topo      = True
            topo_range[1] = i
        if link and (link['type'] == 'check_point'):
            if not has_check_point:
                check_point_range[0] = i
                has_check_point      = True
            check_point_range[1] = i
        if link and (link['type'] == 'base_module'):
            if not has_base_module:
                base_module_range[0] = i
                has_base_module      = True
            base_module_range[1] = i
    # if no topo ,next topo start at [0,0]
    if not has_topo:
        topo_range = [0, 0]
    # check point initial start at topo end + 2 
    if not has_check_point:
        check_point_range[0] = topo_range[1] + 2
        check_point_range[1] = topo_range[1] + 2
    # base module initial at check point end + 2
    if not has_base_module:
        base_module_range[0] = check_point_range[1] + 2
        base_module_range[1] = check_point_range[1] + 2
    return { 'topo_range'        : tuple(topo_range)
            ,'check_point_range' : tuple(check_point_range)
            ,'base_module_range' : tuple(base_module_range) 
            ,'has_topo'          : has_topo
            ,'has_check_point'   : has_check_point
            ,'has_base_module'   : has_base_module }


#----------------------------------------------------
def get_submodule_match_patten(all_module_name):
    patten_char_set_list = []
    len_2_modules = {}
    for m_n in all_module_name:
        l = len(m_n)
        len_2_modules.setdefault(l,[])
        len_2_modules[l].append(m_n)
    l_pattens = []
    for l in len_2_modules:
        l_m = len_2_modules[l]
        l_patten = '(['+ (']['.join(map(''.join, map(set,zip(*l_m))))) + '])'
        l_pattens.append(l_patten)
    patten = '(' + '|'.join(l_pattens) + ')'
    return patten

#----------------------------------------------------
def get_single_verilog_file_module_inf(f):
    all_module_start_end_lines = os.popen('egrep -n -h \'^\s*(module|endmodule)\>\' %s'%(f)).readlines()
    cur_file_module_inf = []
    has_module_not_end  = False
    i = 0
    while i < len(all_module_start_end_lines):
        cur_start_end_line      = all_module_start_end_lines[i]
        cur_start_end_line_num  = int(cur_start_end_line.split(':')[0]) - 1
        cur_start_end_line_code = ':'.join( cur_start_end_line.split(':')[1:] )
        match_module_start = re.match('\s*module\s+(?P<name>(|`)\w+)', cur_start_end_line_code) # some module use macro as name so (|`)
        if match_module_start:
            module_name           = match_module_start.group('name')
            module_start_line_num = cur_start_end_line_num
            module_pos            = ( module_start_line_num, cur_start_end_line_code.find(module_name) )
            # if pre module not end, set new module start pre line as pre module end line
            if has_module_not_end:
                PrintDebug('Error: module:"%s" in file:"%s", no "endmodule" !'%(cur_file_module_inf[-1]['module_name'],f) )
                cur_file_module_inf[-1]['line_range_in_file'][1] = module_start_line_num - 1
            cur_file_module_inf.append(
                {  'module_name'        : module_name
                  ,'file_path'          : f
                  ,'line_range_in_file' : [module_start_line_num, -1]
                  ,'sub_modules'        : None  # []
                  ,'module_pos'         : module_pos
                }
            )
            has_module_not_end = True
            i += 1
            continue
        match_module_end  = re.match('\s*endmodule(\W|$)', cur_start_end_line_code)
        if match_module_end:
            if not has_module_not_end:
                PrintDebug( 'Error: line: %s "endmodule" has no correlation module define ! file: %s '%(match_module_end,f) )
                continue
            module_end_line_num = cur_start_end_line_num
            cur_file_module_inf[-1]['line_range_in_file'][1] = module_end_line_num
            has_module_not_end  = False
            i += 1
            continue
        i += 1
    if has_module_not_end:
        PrintDebug( 'Error: module:"%s" in file:"%s", no "endmodule" !'%(cur_file_module_inf[-1]['module_name'],f) )
    return cur_file_module_inf


# for current file line match all patten: `define xxx ....
# patten_result = {
#     "name" : xxx
#    ,"path" : f
#    ,"pos"  : (line_num, colum_num)  # name first char pos
#    ,'code_line' : `define xxx ....
# }
# finial return [ patten_result0, patten_result1 ]
def get_single_verilog_file_define_inf(f):
    global_define_inf = []
    global_define_lines = os.popen('egrep -n -h \'^\s*`define\W\' %s'%(f)).readlines()
    for l in global_define_lines:
        split0      = l.split(':')
        line_num    = int(split0[0]) - 1
        code_line   = ':'.join(split0[1:])
        match_name  = re.match('\s*`define\s*(?P<name>\w+)',code_line)
        name        = ''
        colum_num   = -1
        if match_name:
            name        = match_name.group('name')
            colum_num   = code_line.find(name)
        if colum_num != -1:
            global_define_inf.append(
                { "name" : name
                 ,"path" : f
                 ,"pos"  : (line_num, colum_num)
                 ,'code_line' : code_line }
            )
    return global_define_inf

def get_single_line_sub_call_inf(egrep_line, all_module_names):
    sp     = egrep_line.split(':')
    l_num  = int(sp[0]) - 1
    l_code = re.sub('//.*', '', ':'.join(sp[1:]))
    if l_code.find(';') == -1:
        return False
    # match_name = re.match('\s*(?P<m_n>(|`)\w+)\s*(?P<other>.*;)\s*$',l_code)
    match_name = re.match('\s*(?P<m_n>(|`)\w+)\s*(?P<other>.*;)',l_code)
    assert(match_name),'%s,%s'%(egrep_line, l_code)
    module_name = match_name.group('m_n')
    if module_name not in all_module_names:
        return False
    other  =  match_name.group('other')
    inst_name_patten = '\w+((\s*\[[^\[\]]*\])|)'
    search_i_n = re.search('(^(?P<i_n0>%s))|(#.*\)\s*(?P<i_n1>%s)\s*\()'%(inst_name_patten,inst_name_patten),other)
    if not search_i_n:
        PrintDebug( 'Warning: match module name %s, but no inst name !' )
        return False
    inst_name = search_i_n.group('i_n0')
    if not inst_name:
        inst_name = search_i_n.group('i_n1')
    assert(inst_name)
    return {
         'module_name': module_name
        ,'inst_name'  : inst_name
        ,'match_range': [l_num, l_num]
        ,'match_pos'  : [l_num, l_code.find(module_name)]
    }

def get_mult_line_sub_call_inf(egrep_line, f_lines, all_module_names):
    sp        = egrep_line.split(':')
    l_num     = int(sp[0]) - 1
    code_line = re.sub('//.*', '', ':'.join(sp[1:]))
    # get module name
    module_name = ''
    module_pos  = (-1,-1)
    match_name  = re.match('^\s*(?P<m_n>(|`)\w+)\s*(?P<other>.*)',code_line)
    assert(match_name)
    module_name = match_name.group('m_n')
    if module_name not in all_module_names:
        return False
    module_pos = (l_num, code_line.find(module_name))
    # get inst name
    inst_name = ''
    inst_name_patten = '\w+((\s*\[[^\[\]]*\])|)'
    other  =  match_name.group('other')
    i = l_num + 1
    max_i = len(f_lines)
    line_end = False
    while not other and i < max_i and not line_end:
        next_code_line_with_semi = re.sub('((^\s+)|(^\s*`.*)|(//.*))','',f_lines[i].strip('\n'))
        next_code_line_no_semi   = re.sub(';.*','',next_code_line_with_semi)
        other = next_code_line_no_semi
        if len(next_code_line_no_semi) != len(next_code_line_with_semi):
            line_end = True
        i += 1
    match_inst_name_no_parm = re.match('^(?P<i_n>%s)'%(inst_name_patten),other)
    if match_inst_name_no_parm:
        inst_name = match_inst_name_no_parm.group('i_n')
    elif other[0] != '#':
        PrintDebug('Warning: un recgnize 0 module match ! %s ||| %s'%(egrep_line, other))
        return False
    # del has parm inst_name
    search_inst_name_has_parm = re.search('#\s*\(.*\)\s*(?P<i_n>%s)\s*\('%(inst_name_patten),other)
    if search_inst_name_has_parm:
        inst_name = search_inst_name_has_parm.group('i_n')
    while i < max_i and not line_end:
        next_code_line_with_semi = re.sub('((^\s+)|(^\s*`.*)|(//.*))','',f_lines[i].strip('\n'))
        next_code_line_no_semi   = re.sub(';.*','',next_code_line_with_semi)
        other = other +' '+next_code_line_no_semi
        if len(next_code_line_no_semi) != len(next_code_line_with_semi):
            line_end = True
        i += 1
        search_inst_name_has_parm = re.search('#\s*\(.*\)\s*(?P<i_n>%s)\s*\('%(inst_name_patten),other)
        if search_inst_name_has_parm:
            inst_name = search_inst_name_has_parm.group('i_n')
            break
    if not inst_name:
        PrintDebug('Warning: un recgnize 1 module match ! %s ||| %d ||| %s '%(egrep_line, i, str(line_end) ) )
        return False
    # get cur call end line
    end_line_num = max_i
    while i < max_i and not line_end:
        next_code_line = re.sub('(^`.*)|(//.*)','',f_lines[i])
        if next_code_line.find(';') != -1:
            line_end = True
            break
        i += 1
    if not line_end:
        PrintDebug('Warning: cur sub call no end ";" ! %s'%(egrep_line))
    else:
        end_line_num = i
    # return result
    return {
         'module_name': module_name
        ,'inst_name'  : inst_name
        ,'match_range': [l_num, end_line_num]
        ,'match_pos'  : module_pos
    }

def get_single_verilog_file_subcall_inf(f, patten, all_module_names):
    egrep_match_lines  = os.popen('egrep -n -h \'^\s*(%s)\>\' %s'%(patten,f)).readlines()
    # start get sub call inf
    if not egrep_match_lines:
        return []
    file_sub_call_infs = []
    c0_cnt = 0
    c1_cnt = 0
    f_lines = open(f,'r').readlines()
    for egrep_l in egrep_match_lines:
        # case0: signal line call
        c0_rst = get_single_line_sub_call_inf(egrep_l, all_module_names)
        if c0_rst:
            c0_cnt += 1
            file_sub_call_infs.append(c0_rst)
            continue
        # case1: mult line call
        c1_rst = get_mult_line_sub_call_inf(egrep_l, f_lines, all_module_names)
        if c1_rst:
            c1_cnt += 1
            file_sub_call_infs.append(c1_rst)
            continue
    PrintDebug('subcall: one_line/mult_line = %d/%d'%( c0_cnt,c1_cnt) )
    return file_sub_call_infs


def add_single_verilog_file_submodule_inf_to_module_inf( file_module_inf, file_subcall_inf ):
    s_inf_i = 0
    for m_inf in file_module_inf:
        m_inf['sub_modules'] = []
        m_inf['sub_calls'] = {}
        m_range = m_inf['line_range_in_file']
        while s_inf_i < len(file_subcall_inf):
            s_range = file_subcall_inf[s_inf_i]['match_range']
            # cur subcall in cur module
            if m_range[0] <= s_range[0] and s_range[1] <= m_range[1]:
                m_inf['sub_modules'].append(file_subcall_inf[s_inf_i])
                m_inf['sub_calls'][file_subcall_inf[s_inf_i]['inst_name']] = file_subcall_inf[s_inf_i]
                s_inf_i += 1
                continue
            elif s_range[0] < m_range[0]:
                PrintDebug('Error: subcall %s not in valid module !'%(file_subcall_inf[s_inf_i].__str__()))
                s_inf_i += 1
            elif s_range[1] > m_range[1]:
                if s_range[0] < m_range[0]:
                    PrintDebug('Error: subcall %s cross two module !'%(file_subcall_inf[s_inf_i].__str__()))
                break
            else:
                assert(0)
    return

def get_single_verilog_file_code_inf(f):
    # gen cur module and define inf
    new_file_module_inf = get_single_verilog_file_module_inf(f)
    new_file_define_inf = get_single_verilog_file_define_inf(f)
    # gen new all_module_names, del old current file add new
    new_module_names    = set([ mi['module_name'] for mi in new_file_module_inf ])
    old_file_module_inf = G['FileInf'][f]['module_infs']
    old_module_names    = set([ mi['module_name'] for mi in old_file_module_inf ])
    all_module_name     = ( set(G['ModuleInf']) - old_module_names ) | new_module_names
    # get file sub call inf
    patten = get_submodule_match_patten(all_module_name)
    new_file_subcall_inf = get_single_verilog_file_subcall_inf(f, patten, all_module_name)
    # merge to file_inf
    add_single_verilog_file_submodule_inf_to_module_inf( new_file_module_inf, new_file_subcall_inf )
    new_file_inf = {
         'glb_defines'   : new_file_define_inf
        ,'module_infs'   : new_file_module_inf
        ,'module_calls'  : new_file_subcall_inf
        ,'file_edit_inf' : { 'create_time': os.path.getctime(f), 'last_modify_time': os.path.getmtime(f)}
    }
    return new_file_inf

def show_progress_bar( i, i_max, show_char = '#', show_width = 20):
    i += 1 # count from 1
    i_max_len = len(str(i_max))
    i_len     = len(str(i))
    i_str     = ' '*(i_max_len-i_len)+str(i)
    i_max_str = str(i_max)
    prefix    = '%s/%s: '%(i_str,i_max_str)
    pass_str  = show_char*((i*show_width)/i_max)
    empty_str = ' '*(show_width - len(pass_str))
    progress_bar = '[%s%s]'%(pass_str,empty_str)
    tool_len  = len(prefix) + show_width
    sys.stdout.write(' '*tool_len + '\r')
    sys.stdout.flush()
    sys.stdout.write(prefix + progress_bar)