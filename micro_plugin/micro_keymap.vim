"==================================================================
"""""" map keys  use :h map for more information
"==================================================================
let mapleader="\<space>"
nnoremap [b :bp<CR>
nnoremap ]b :bn<CR>
map Q gq  "����ӳ���ʽ����ݼ�������Ĭ��Q gq������
"tab bar �������
map <tab> :tabn<CR>
map <s-tab> :tabp<CR>
map n<tab> :tabnew

nmap <Leader>f v%zf


"==================================================================
"""""" Abbreviate use for quick typing
""help different between: iab , inorea
"==================================================================

inorea begin begin<cr><cr>end<up>
inorea alws always @(posedge clk or negedge rst_n) begin<cr><cr>end<up>if(rst_n == 1'b0) begin<cr><cr>end<up>
inorea alwc always @(*) begin<cr><cr>end<up>
iab casec case()<cr>default:<cr>endcase<up><up>
