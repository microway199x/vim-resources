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

# left sidebar window width
frame_window_width          = 20

# right bottom report window height
report_window_height        = 8

# max work window vtags auto opened, not include use self opened window and holded window
max_open_work_window_number = 1

# when use <Space><left>/<Space><right> the max number of history trace valid
max_roll_trace_depth        = 1000

# when <Space>c add check point, the max number of check point valid
max_his_check_point_num     = 10

# when gen the vtags database, in all verilog modules when some module called more then threshold times,
# set this module to be base module, then show topo will not list it's inst one by one  
base_module_threshold       = 200

# supported verilog postfix, we only add postfix in below to data base
support_verilog_postfix     = ['v']

# open debug module or not, open debug module will print a lot debug log at vtags.db
debug_mode                  = False

# when trace source, match bigger than TraceSourceOptimizingThreshold, open opt func, mainly for signal like clk,rst ...
trace_source_optimizing_threshold   = 20 

# frame fold level space, use to set pre space num, if current level is 3 ,
# and fold level space is ' ', then current line pre space is ' '*3 = '   ' 
frame_fold_level_space          = '    '

# weather show report or not
show_report                 = True

# weather show sidebar or not
show_sidebar                = True