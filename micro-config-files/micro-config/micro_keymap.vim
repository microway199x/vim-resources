"==================================================================
"""""" map keys  use :h map for more information
"==================================================================
let mapleader="\<space>"
nnoremap [b :bp<CR>
nnoremap ]b :bn<CR>
map Q gq  "重新映射格式化快捷键，现在默认Q gq都可以
"tab bar 相关设置
map <tab> :tabn<CR>
map <s-tab> :tabp<CR>
map n<tab> :tabnew

nmap <Leader>f v%zf

"previous line and center current line to middle of window
nnoremap <Up> kzz     
"next line and center current line to middle of window
nnoremap <Down> jzz  
nnoremap <esc><esc>  :nohl<cr>   " remove serach hightlight
"" use "cc" command, clear current line and indent line then insert

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" Veriolg quick and efficent tips
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"检查例化模块信号名是否一致
"map <F2> /^\s*\.\(\w\+\)\s*(\1<CR>
map <F2> /\.\(\w\+\)\s*(\1<CR>
map <F3> %s/\d\+/\=submatch(0)+1/g  "所有数字加1


"==================================================================
"""""" Abbreviate use for quick typing
""help different between: iab , inorea
"==================================================================

inorea begin begin<cr><cr>end<up>
inorea alws always @(posedge clk or negedge rst_n) begin<cr><cr>end<up>    if(rst_n == 1'b0) begin<cr><cr>end<up>
inorea alwc always @(*) begin<cr><cr>end<up>
iab casec case()<cr>    default:<cr>endcase<up><up>


