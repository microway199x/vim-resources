"comment for perl plugin must use the fixed version
""function! Align_inst() 
""    let line_start=line("'<")
""    let line_end=line("'>")
""    perl Align(line_start, line_end)
""endfunction
"""///"EOF"必须在行首(前面不能有前导空格)
""perl << EOF
""sub align_inst{
""\\  ($success_1,$line_begin) = VIM::Eval('line("'<")');
""\\  ($success_2,$line_end)   = VIM::Eval('line("'>")');
""    $line_begin = $_[0];
""    $line_end   = $_[1];
""    @lines = $curbuf->Get($line_begin .. $line_end); 
""    @lines_out=[];
""    $len_inst_max = 0;
""    $len_con_max  = 0;
""    foreach $line in @lines{
""        if($line =~ m/\s*\.(?<inst_wire>\w+)\(?<con_wire>\w+\).*/){
""            $len_inst = len($inst_wire)    
""            if($len_inst > $len_inst_max){
""                $len_inst_max = $len_inst;
""            }
""            
""            if($len_con > $len_con_max){
""                $len_con_max = $len_con;
""            }
""        }   
""    }
""    
""    $len_inst_out = $len_inst_max + 1;
""    $len_con_out = $len_con_max + 1;
""    foreach $line in @lines{
""        if($line =~ m/\s*\.(?<inst_wire>\w+)\(?<con_wire>\w+\),(?<other>.*)/){
""            $line_out_inst = sprintf("%*s",$len_inst_out,$inst_wire);
""            $line_out_con  = sprintf("%*s",$len_con_out,$con_wire);
""        }   
""        $line_out = "    ." .. $line_out_inst .. "(" .. $line_out_con .. ")," .. $other;
""        push @lines_out, $line_out;
""    }
""    
""    $curbuf->Delete($line_begin, $line_end); 
""    $curbuf->Set($line_begin, @lines_out); 
""}
""EOF

