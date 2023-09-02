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
import os
try:
    import vim
except: 
    pass
import GLB
G = GLB.G
from Base import*
import View
PrintReport = View.PrintReport

########################################################
def get_sub_io_signal_name_from_sub_call_line(call_line, y):
    word = get_full_word(call_line, y)
    # if | .xxx(xxxx)
    #  y |   ^
    #    |     ^    ^ // call_sub_assign_signal_str
    # cur_word is sub_io_signal_name
    if re.match('\w+\.', call_line[:y+1][::-1]):
        call_sub_assign_signal_str = re.sub('(^\w*)|(\.\w+\(.*)', '', call_line[y:])
        call_sub_signals = set( re.findall('\w+',call_sub_assign_signal_str) )
        sub_call_io      = word
        return { 'call_sub_signals': call_sub_signals
                ,'sub_call_io'     : word
                ,'sub_call_io_num' : None }
    # if | .xxx(xxxx)
    #  y |        ^
    #    |     ^    ^ // call_sub_assign_signal_str
    s0 = re.search('\(\s*(?P<sub_call_io>\w+)\.',call_line[:y+1][::-1])
    if s0:
        sub_call_io = s0.group('sub_call_io')[::-1]
        call_sub_assign_and_right = call_line[y-s0.span()[0]:]
        assert(call_sub_assign_and_right[0] == '(')
        call_sub_assign_signal_str = re.sub('\.\w+\s*\(.*', '', call_line[y:])
        call_sub_signals = set( re.findall('\w+',call_sub_assign_signal_str) )
        return { 'call_sub_signals': call_sub_signals
                ,'sub_call_io'     : sub_call_io
                ,'sub_call_io_num' : None }
    # if module_name #(parm) inst_name( a, b,     c)
    # if module_name         inst_name( a, b,     c)
    #                                      y
    # call_sub_signals                     set(b)
    # sub_call_io_num                      1
    # sub_call_io                          ''
    if word:
        s1 = re.search('\)\s*\w+\s*\(',call_line[:y+1])
        if not s1:
            s1 = re.match('\s*\w+\s*\w+\s*\(',call_line[:y+1])
        full_match_s1 = True
        if s1:
            pre_sub_call_signal_str = call_line[s1.span()[1]:y+1]
            pre_sub_call_signals    = pre_sub_call_signal_str.split(',')
            assert(pre_sub_call_signals)
            for sc in pre_sub_call_signals:
                if not re.match('\s*(\w+)|(\w+\s*\[[^\[\]]+\])\s*$',sc):
                    full_match_s1 = False
            if full_match_s1:
                return { 'call_sub_signals': set([word])
                        ,'sub_call_io'     : ''
                        ,'sub_call_io_num' : len(pre_sub_call_signals) - 1 }
    return None

# if has io_name return cur io inf
# else return all io inf of current module
#io_inf = 
    #      "name"        : name
    #    , "io_type"     : io_type
    #    , "left"        : left_index
    #    , "right"       : right_index
    #    , "size"        : size
    #    , 'line_num'    : line_num
    #    , 'name_pos'    : (line_num, colm_num)
    #    , 'code_line'   : code_line
    #    , 'signal_type' : signal_type }
def get_io_inf(module_name, io_name = ''):
    module_inf   = get_module_inf(module_name)
    if not module_inf:
        return False
    module_path  = module_inf['file_path']
    module_range = module_inf['line_range_in_file']
    if io_name: # get cur io inf
        io_inf       = {}
        io_lines     =  os.popen('sed -n \'%d,%dp\' %s | egrep -n -h \'^\s*(input|output)\>.*\<%s\>\''%(module_range[0]+1, module_range[1]+1, module_path, io_name)).readlines()
        if len(io_lines) == 0:
            PrintDebug('Error: module: %s \'s io: %s define not found !'%(module_name,io_name))
            return False
        if len(io_lines) > 1:
            PrintDebug('Error: module: %s \'s io: %s define multiple times !'%(module_name,io_name))
        line = io_lines[0]
        assert(line.find(io_name) != -1)
        io_inf = decode_egreped_verilog_io_line(line)['io_infs']
        if io_name in io_inf:
            # because use "sed ... | grep ..." so the line number is not the real number need add sed started line num
            io_inf[io_name]['line_num'] = io_inf[io_name]['line_num'] + module_range[0]
            io_inf[io_name]['name_pos'] = ( io_inf[io_name]['line_num'], io_inf[io_name]['name_pos'][1] )
            return io_inf[io_name]
        else:
            PrintDebug('Warning: get_io_inf, io_name is parm name ,not a io !')
            return False
    else: # get module all io inf
        all_io_inf    = []
        cur_module_code_range = module_inf['line_range_in_file']
        all_io_lines  =  os.popen('sed -n \'%d,%dp\' %s | egrep -n -h \'^\s*(input|output)\>\''%(cur_module_code_range[0]+1, cur_module_code_range[1]+1, module_path)).readlines()
        for line in all_io_lines:
            line      = line.rstrip('\n')
            egrep_io_infs = decode_egreped_verilog_io_line(line)
            io_inf        = egrep_io_infs['io_infs']
            name_list     = egrep_io_infs['name_list']
            if not io_inf:
                PrintDebug('Error: module: %s, line: %s, can not decode by decode_egreped_verilog_io_line() ! file: %s'(module_name, line, module_path))
                continue
            for io_name in name_list:
                assert(io_name in io_inf)
                c_io_inf = io_inf[io_name]
                c_io_inf['line_num'] = c_io_inf['line_num'] + cur_module_code_range[0]
                c_io_inf['name_pos'] = (c_io_inf['line_num'], c_io_inf['name_pos'][1])
                all_io_inf.append( c_io_inf )
        return all_io_inf

def get_module_call_sub_module_io_inf(call_line, io_pos, call_file_path):
    call_line_num  = io_pos[0]
    # if database has no this file return
    if call_file_path not in G['FileInf']:
        PrintDebug("Warning: get_module_call_sub_module_io_inf : cur file has not in hdltags database, file: %s !"%(call_file_path))
        return False
    file_line_inf     = get_file_line_inf(call_line_num, call_file_path)
    line_call_sub_inf = {}
    line_module_inf   = {}
    if file_line_inf:
        line_call_sub_inf = file_line_inf['line_call_sub_inf']
        line_module_inf   = file_line_inf['line_module_inf']
    # if cursor line not no sub call , return
    if not line_call_sub_inf:
        PrintDebug("Warning: get_module_call_sub_module_io_inf: cur line %d not on sub call ! "%(call_line_num))
        return False
    sub_call_signal_inf    = get_sub_io_signal_name_from_sub_call_line(call_line, io_pos[1]) # may be parm
    # call module name
    assert(line_module_inf),'is in sub call, must be valid mudule'
    call_module_name  = line_module_inf['module_name']
    # valid cursor on sub call
    sub_module_name   = line_call_sub_inf['module_name']
    sub_module_path   = ''
    sub_module_inf    = get_module_inf(sub_module_name)
    if sub_module_inf:
        sub_module_path  = sub_module_inf['file_path']
    # sub_match_pos means cursor call io signal in sub module io pos
    sub_io_inf        = {} 
    call_sub_signals  = set()
    if sub_call_signal_inf:
        call_sub_signals = sub_call_signal_inf['call_sub_signals']
        sub_call_io      = sub_call_signal_inf['sub_call_io']
        sub_call_io_num  = sub_call_signal_inf['sub_call_io_num']
        if sub_call_io:
            sub_io_inf    = get_io_inf(sub_module_name, sub_call_io)
        elif sub_call_io_num != None:
            all_io_inf    = get_io_inf(sub_module_name)
            assert(sub_call_io_num < len(all_io_inf))
            sub_io_inf    = all_io_inf[sub_call_io_num]
    sub_match_pos     = ()
    sub_io_type       = ''
    sub_io_line       = ''
    sub_io_name       = ''
    if sub_io_inf:
        sub_io_name   = sub_io_inf['name']
        sub_match_pos = sub_io_inf['name_pos']
        sub_io_type   = sub_io_inf['io_type']
        sub_io_line   = sub_io_inf['code_line']
    return {
         'sub_io_name'      : sub_io_name    
        ,'sub_module_name'  : sub_module_name
        ,'sub_module_path'  : sub_module_path
        ,'sub_match_pos'    : sub_match_pos  
        ,'sub_io_type'      : sub_io_type
        ,'sub_io_line'      : sub_io_line
        ,'sub_io_inf'       : sub_io_inf    
        ,'call_sub_signals' : call_sub_signals
        ,'call_sub_inf'     : line_call_sub_inf  
        ,'call_module_name' : call_module_name }

#########################function for trace##############################

# ok
def get_upper_module_call_io_inf(cur_module_name , cur_io_name):
    cur_module_last_call_inf = get_module_last_call_inf(cur_module_name)
    if not cur_module_last_call_inf:
        PrintDebug("Warning: get_upper_module_call_io_inf: module %s, not called before, no upper module !"%(cur_module_name))
        return False
    upper_module_name  = cur_module_last_call_inf['upper_module_name']
    upper_call_inf     = cur_module_last_call_inf['upper_call_inf']
    upper_module_inf   = get_module_inf(upper_module_name)
    assert(upper_module_inf),'upper module %s call %s before, upper should has inf in database !'%(upper_module_name, cur_module_name)
    upper_module_path  = upper_module_inf['file_path']
    # get upper call, match this signal pos
    upper_call_lines   = open(upper_module_path,'r').readlines()
    upper_call_pos     = upper_call_inf['match_pos'] # initial to call inst line
    upper_matched      = False
    for i in range( upper_call_inf['match_range'][0] , upper_call_inf['match_range'][1] + 1 ):
        f0 = upper_call_lines[i].find(cur_io_name)
        if f0 == -1:
            continue
        s0 = re.search('(?P<pre>^|\W)%s(\W|$)'%(cur_io_name) , re.sub('//.*','',upper_call_lines[i]))
        if s0:
            colum_num = s0.span()[0] + len(s0.group('pre'))
            upper_call_pos = (i, colum_num)
            upper_matched  = True 
            break
    assert(upper_matched),'upper called so should be match, cur_io_name:%s, %s '%(upper_call_inf['match_range'].__str__(), cur_io_name)
    upper_call_line   = upper_call_lines[upper_call_pos[0]]
    return {
         'module_name' : upper_module_name
        ,'call_pos'    : upper_call_pos
        ,'call_line'   : upper_call_line
        ,'module_path' : upper_module_path 
    }


def get_cur_appear_is_source_or_dest(key, code_lines, appear_pos):
    a_x, a_y = appear_pos
    appear_code_line = re.sub('(//.*)|(^\s*`.*)', '', code_lines[a_x] )
    # case 0 cur pos in note return not source and dest
    if len(appear_code_line) - 1 < a_y:
        return 'None'
    # case 1 is io
    if (appear_code_line.find('input') != -1) or (appear_code_line.find('output') != -1):
        match_io_type = re.match('\s*(?P<io_type>(input|output))\W',appear_code_line) # may input a,b,c
        match_io_name = re.match('\s*[;,]?\s*(?P<r_names>\w+(\s*,\s*\w+)*)',appear_code_line[::-1]) # may input a,b,c
        if match_io_type and match_io_name:
            io_type  = match_io_type.group('io_type')
            io_names = match_io_name.group('r_names')[::-1]
            io_names = set(re.split('\s*,\s*',io_names))
            if (io_type == 'input') and (key in io_names):
                return 'Source'
            if (io_type == 'output') and (key in io_names):
                return 'Dest'
        elif match_io_type:
            PrintDebug('Error: recgnize_signal_assign_line: unrecgnize io line: '+appear_code_line)
            return 'None'
    # case 2 cur pos in case/casez/for/if (...key...) then it's dest
    match_case2 = False
    c2 = re.search( '(^|\W)(case|casez|for|if|while)\s*\(' , appear_code_line)
    if c2:
        appear_code_right_line = appear_code_line[c2.span()[1]:]
        unmatch_bracket_count = 1
        end_match_patten      = '^'
        end_y                 = len(appear_code_right_line) - 1
        all_brackets = re.findall('\(|\)', appear_code_right_line)
        for b in all_brackets:
            if b == '(':
                unmatch_bracket_count += 1
            else:
                unmatch_bracket_count -= 1
            end_match_patten = end_match_patten + '[^()]*\\'+b
            if unmatch_bracket_count == 0:
                end_y = re.search(end_match_patten, appear_code_right_line).span()[1] - 1
                break
        end_y = c2.span()[1] + end_y
        if end_y >= a_y:
            return 'Dest'
        else:
            # if key not in (...), then use ) right str as real appear_code_line
            match_case2 = True
            appear_code_line = appear_code_line[end_y + 1:]
    # case 3 cur line has = at left or right
    assign_patten = '([^=>!]=[^=<>])'
    # ... =|<= ... key : is dest
    if re.search(assign_patten, appear_code_line[:a_y + 1]):
        return 'Dest'
    # key ... =|<= ... : is source
    if re.search(assign_patten, appear_code_line[a_y:]):
        return 'Source'
    # case 4 if not match case2(if match no pre line) post full line sep by ";" has =|<=, it's dest
    if not match_case2:
        pre_full_line = get_verilog_pre_full_line(code_lines, appear_pos)
        if re.search(assign_patten, pre_full_line):
            return 'Dest'
    # case 5 post full line sep by ";" has =|<=, it's source
    post_full_line = get_verilog_post_full_line(code_lines, appear_pos)
    if re.search(assign_patten, post_full_line[:a_y + 1]):
        return 'Source'
    # case 6 unrecgnize treat as maybe dest/source
    return 'Maybe'


# ok
def clear_last_trace_inf( trace_type ):
    if trace_type in ['source','both']:
        G['TraceInf']['LastTraceSource']['Maybe']      = []
        G['TraceInf']['LastTraceSource']['Sure']       = []
        G['TraceInf']['LastTraceSource']['ShowIndex']  = 0
        G['TraceInf']['LastTraceSource']['SignalName'] = ''
        G['TraceInf']['LastTraceSource']['Path']       = ''
    if trace_type in ['dest','both']:
        G['TraceInf']['LastTraceDest']['Maybe']        = []
        G['TraceInf']['LastTraceDest']['Sure']         = []
        G['TraceInf']['LastTraceDest']['ShowIndex']    = 0
        G['TraceInf']['LastTraceDest']['SignalName']   = ''
        G['TraceInf']['LastTraceDest']['Path']         = ''

# #-------------------trace_io_signal---------------------------
# del get_cur_module_inf
def real_trace_io_signal(trace_type, cursor_inf, io_signal_inf):
    assert(trace_type in ['dest', 'source']),'only trace dest/source'
    # verilog
    if (trace_type is 'dest') and (io_signal_inf['io_type'] != 'output'):
        PrintDebug('Warning: real_trace_io_signal: not output signal, not dest')
        return False # not output signal, not dest
    if (trace_type is 'source') and (io_signal_inf['io_type'] != 'input'):
        PrintDebug('Warning: real_trace_io_signal: not input signal, not source')
        return False # not input signal, not source
    # trace a input signal
    clear_last_trace_inf( trace_type )  # clear pre trace dest/source result
    cur_module_inf   = cursor_inf['cur_module_inf']
    if not cur_module_inf:
        PrintDebug('Warning: cur file not in database, will not go upper ! file: %s'(cursor_inf['file_path']))
        return True
    cur_module_name  = cur_module_inf['module_name']
    upper_module_call_inf = get_upper_module_call_io_inf(cur_module_name , io_signal_inf['name'])
    if not upper_module_call_inf:
        PrintReport('Warning: no upper module call this module before !')
        return True # this dest/source but not found upper module
    # has upper module go to upper module call location
    upper_module_name = upper_module_call_inf['module_name']
    upper_call_pos    = upper_module_call_inf['call_pos']
    upper_call_line   = upper_module_call_inf['call_line']
    upper_module_path = upper_module_call_inf['module_path']
    show_str          = '%s %d : %s'%(upper_module_name, upper_call_pos[0]+1, upper_call_line)
    file_link         = {'key':io_signal_inf['name'], 'pos': upper_call_pos, 'path': upper_module_path}
    trace_result      = {'show': show_str, 'file_link': file_link}
    if trace_type is 'dest':
        G['TraceInf']['LastTraceDest']['Sure'].append(trace_result)
        G['TraceInf']['LastTraceDest']['SignalName'] = cursor_inf['word']
        G['TraceInf']['LastTraceDest']['Path']       = cursor_inf['file_path']
    else :
        G['TraceInf']['LastTraceSource']['Sure'].append(trace_result)
        G['TraceInf']['LastTraceSource']['SignalName'] = cursor_inf['word']
        G['TraceInf']['LastTraceSource']['Path']       = cursor_inf['file_path']
    # show dest/source to report win, and go first trace
    PrintReport(spec_case = trace_type)
    View.show_next_trace_result(trace_type)
    return True

# ok
def trace_io_signal(trace_type, cursor_inf):
    trace_signal_name  = cursor_inf['word']
    io_signal_infs     = recgnize_io_signal_line(cursor_inf['line'], cursor_inf['line_num'])
    if not io_signal_infs:
        PrintDebug('Warning: trace_io_signal: not io signal')
        return False # not io signal
    # if trace_signal_name != io_signal_inf['name']:
    if trace_signal_name not in io_signal_infs:
        PrintDebug('Warning: trace_io_signal: is io signal but not traced signal')
        return False # is io signal but not traced signal
    if trace_type in ['source','dest']:
        return real_trace_io_signal(trace_type, cursor_inf, io_signal_infs[trace_signal_name])
    assert(0),'unkonw tarce type %s' %(trace_type)

#-------------------------------------------------------------
# ok
def real_trace_module_call_io_signal(trace_type, sub_call_inf, cursor_inf):
    assert(trace_type in ['source', 'dest'])
    if trace_type == 'source' and sub_call_inf['sub_io_type'] != 'output':
        return False # submodule not source, just pass
    elif trace_type == 'dest' and sub_call_inf['sub_io_type'] != 'input':
        return False # submodule not source, just pass
    # has sub module and in submodule signal is out, then it's source
    sub_module_name         = sub_call_inf['sub_module_name']
    sub_module_path         = sub_call_inf['sub_module_path']
    sub_module_match_pos    = sub_call_inf['sub_match_pos']
    sub_module_match_line   = sub_call_inf['sub_io_line']
    sub_module_signal_name  = sub_call_inf['sub_io_name']
    show_str     = '%s %d : %s'%(sub_module_name, sub_module_match_pos[0]+1, sub_module_match_line)
    file_link    = {'key':sub_module_signal_name, 'pos': sub_module_match_pos, 'path': sub_module_path}
    trace_result = {'show': show_str, 'file_link': file_link}
    if trace_type == 'source':
        G['TraceInf']['LastTraceSource']['Sure'].append(trace_result)
        G['TraceInf']['LastTraceSource']['SignalName'] = cursor_inf['word']
        G['TraceInf']['LastTraceSource']['Path']       = cursor_inf['file_path']
    else: # dest
        G['TraceInf']['LastTraceDest']['Sure'].append(trace_result)
        G['TraceInf']['LastTraceDest']['SignalName'] = cursor_inf['word']
        G['TraceInf']['LastTraceDest']['Path']       = cursor_inf['file_path']
    # go to sub module code now, so cur module is the sub module last call
    cur_module_name  = sub_call_inf['call_module_name']
    call_sub_inf     = sub_call_inf['call_sub_inf']
    set_module_last_call_inf(sub_module_name, cur_module_name, call_sub_inf['inst_name'])
    # show source to report win, and go first trace
    PrintReport(spec_case = trace_type)
    View.show_next_trace_result(trace_type)
    return True

# ok
# del is_module_call_range
def trace_module_call_io_signal(trace_type, cursor_inf):
    sub_call_inf = get_module_call_sub_module_io_inf(cursor_inf['line'], cursor_inf['pos'], cursor_inf['file_path'])
    if not sub_call_inf:
        PrintDebug('Warning: trace_module_call_io_signal: not in module call io')
        return False # not in module call io
    if sub_call_inf['sub_module_name'] == cursor_inf['word']:
        PrintReport('Warning: trace key is a submodule call, module name , no source !')
        return True
    if not sub_call_inf['sub_io_name']:
        PrintDebug('Warning: trace_module_call_io_signal: is module call ,but unrecgnize io name !')
        return False
    clear_last_trace_inf( trace_type )
    return real_trace_module_call_io_signal(trace_type, sub_call_inf, cursor_inf)


# #---------------------------------------------------------------------
def real_trace_normal_signal(trace_type, signal_appear_pos_line, cursor_inf):
    assert(trace_type in ['source', 'dest'])
    clear_last_trace_inf(trace_type)
    if trace_type == 'source':
        G['TraceInf']['LastTraceSource']['SignalName'] = cursor_inf['word']
        G['TraceInf']['LastTraceSource']['Path']       = cursor_inf['file_path']
    else: 
        G['TraceInf']['LastTraceDest']['SignalName'] = cursor_inf['word']
        G['TraceInf']['LastTraceDest']['Path']       = cursor_inf['file_path']
    trace_signal_name = cursor_inf['word']
    cur_module_inf    = cursor_inf['cur_module_inf'] # already qualify
    cur_module_name   = cur_module_inf['module_name']
    cur_module_path   = cur_module_inf['file_path']
    # add optimizing for signal such like clk, used by many times, but only io, or sub call is source
    input_is_only_source = False
    if trace_type == 'source' and len(signal_appear_pos_line) > G['TraceInf']['TraceSourceOptimizingThreshold']:
        for appear_pos, appear_line in signal_appear_pos_line:
            signal_appear_line = cursor_inf['codes'][appear_pos[0]]
            if signal_appear_line.find('input') == -1:
                continue
            dest_or_source = get_cur_appear_is_source_or_dest(trace_signal_name, [signal_appear_line], (0,appear_pos[1]) )
            if dest_or_source != source:
                continue
            input_is_only_source = True
            show_str = '%s %d : %s'%(cur_module_name, appear_pos[0]+1, appear_line)
            file_link = {'key':trace_signal_name, 'pos': appear_pos, 'path': cur_module_path}
            trace_result = {'show': show_str, 'file_link': file_link}
            G['TraceInf']['LastTraceSource']['Sure'].append(trace_result)
            break
    # if found a input as source, should be the only source, clear appear pos to jump, normal search
    if input_is_only_source:
        signal_appear_pos_line = []
    # appear_pos (line number, column), deal each match to find source
    for appear_pos, appear_line in signal_appear_pos_line:
        appear_dest_or_source     = False
        appear_is_dest            = False
        appear_is_source          = False
        # module call assign range
        sub_call_inf = get_module_call_sub_module_io_inf(appear_line, appear_pos, cur_module_path)
        if sub_call_inf:
            if trace_signal_name in sub_call_inf['call_sub_signals']:
                # cur is subcall but not io name not match trace name go next
                if not sub_call_inf['sub_io_type']:
                    appear_dest_or_source = True
                elif sub_call_inf['sub_io_type'] == 'output':
                    appear_is_source      = True
                elif sub_call_inf['sub_io_type'] == 'input':
                    appear_is_dest        = True
            else:
                PrintDebug('Warning: subcall match on sub io name, not on assign name ! %s,%s'%(appear_pos.__str__(), appear_line))
                continue
        else:
            # not module call then check if a assign signal
            dest_or_source = get_cur_appear_is_source_or_dest(trace_signal_name, cursor_inf['codes'], appear_pos)
            if dest_or_source == 'Dest':
                appear_is_dest = True
            elif dest_or_source == 'Source':
                appear_is_source = True
            elif dest_or_source == 'Maybe':
                appear_dest_or_source = True
            else:
                PrintDebug('Warning: match not source or dest ! %s : %s'%(appear_pos.__str__(), appear_line))
        # finial add to source/dest
        show_str = '%s %d : %s'%(cur_module_name, appear_pos[0]+1, appear_line)
        file_link = {'key':trace_signal_name, 'pos': appear_pos, 'path': cur_module_path}
        trace_result = {'show': show_str, 'file_link': file_link}
        if trace_type == 'source':
            if appear_dest_or_source:
                G['TraceInf']['LastTraceSource']['Maybe'].append(trace_result)
            elif appear_is_source:
                G['TraceInf']['LastTraceSource']['Sure'].append(trace_result)
        else: # trace dest
            if appear_dest_or_source:
                G['TraceInf']['LastTraceDest']['Maybe'].append(trace_result)
            elif appear_is_dest:
                G['TraceInf']['LastTraceDest']['Sure'].append(trace_result)
        continue
    # finish get all dest/source
    if trace_type == 'source':
        finded_source_num       = len(G['TraceInf']['LastTraceSource']['Sure'])
        finded_maybe_source_num = len(G['TraceInf']['LastTraceSource']['Maybe'])
        # not find signal source
        if not (finded_source_num + finded_maybe_source_num):
            PrintReport("Warning: Not find signal source !")
            return True
    else: # dest
        finded_dest_num       = len(G['TraceInf']['LastTraceDest']['Sure'])
        finded_maybe_dest_num = len(G['TraceInf']['LastTraceDest']['Maybe'])
        # not find signal dest
        if not (finded_dest_num + finded_maybe_dest_num):
            PrintReport("Warning: Not find signal dest !")
            return True
    # show source to report win, and go first trace
    PrintReport(spec_case = trace_type)
    View.show_next_trace_result(trace_type)
    return True

def trace_normal_signal(trace_type, cursor_inf):
    cur_module_inf    = cursor_inf['cur_module_inf']
    if not cur_module_inf:
        PrintDebug('Warning: cur file has no module inf, may be no database or cur line not in module, file: %s '%(cursor_inf['file_path']))
        return False
    # just use grep get all signal appear in current file to speed up signal search
    signal_appear_pos_line = search_verilog_code_use_grep( cursor_inf['word'], cursor_inf['file_path'], cur_module_inf['line_range_in_file'] )
    return real_trace_normal_signal(trace_type, signal_appear_pos_line, cursor_inf)

#----------------------------------------------------
def trace_glb_define_signal(trace_type, cursor_inf):
    assert(trace_type in ['dest', 'source'])
    cur_line  = cursor_inf['line']
    cur_word  = cursor_inf['word']
    if cur_line.find('`') == -1:
        return False
    s0        = re.search('(?P<prefix>^|\W)%s(\W|$)'%(cur_word),cur_line)
    if not s0:
        return False
    if s0.group('prefix') != '`':
        return False
    if cur_word not in G['CodeDefineInf']:
        PrintReport('Warning: cur macro: \"%s\", not has find in database !'%(cur_word))
        return True
    cur_define_infs = G['CodeDefineInf'][cur_word]
    clear_last_trace_inf(trace_type)
    for inf in cur_define_infs: # {name path pos code_line}
        file_name = re.sub('.*/','',inf['path'])
        show_str = '%s %d : %s'%(file_name, inf['pos'][0]+1, inf['code_line'])
        file_link = {'key':cur_word, 'pos': inf['pos'], 'path': inf['path']}
        trace_result = {'show': show_str, 'file_link': file_link}
        if trace_type == 'source':
            G['TraceInf']['LastTraceSource']['SignalName'] = cursor_inf['word']
            G['TraceInf']['LastTraceSource']['Path']       = cursor_inf['file_path']
            G['TraceInf']['LastTraceSource']['Sure'].append(trace_result)
        else: # dest
            PrintReport('Warning: cur not support trace macro dest !')
            return True
    # show source to report win, and go first trace
    PrintReport(spec_case = trace_type)
    View.show_next_trace_result(trace_type)
    return True



