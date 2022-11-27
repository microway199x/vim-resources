"==================================================================
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"基本设定
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""set nu " 行号 
"set relativenumber "相对行号
set mouse=a  "双击选中bar或者tags等，双击有效
set noerrorbells  " 不让vim发出讨厌的滴滴声
set gcr=a:blinkon0 "取消光标闪烁
set guicursor=n-v-c:block,i-ci-ve:ver25,r-cr:hor20,o:hor50
		  \,a:blinkwait700-blinkoff400-blinkon250-Cursor/lCursor
		  \,sm:block-blinkwait175-blinkoff150-blinkon175
" 我的状态行显示的内容（包括文件类型和解码）
set statusline=[%F]%y%r%m%*%=[Line:%l/%L,Column:%c][%p%%]    "显示文件名: 总行数, 总的字符数
set ruler
set magic
"colorscheme night"设置主题 
"colorscheme biogoo"设置主题 
set background=light
colorscheme gruvbox "设置主题 
"colorscheme molokai"设置主题 
set cc=80 "hight 80th column  cc means colorcolumn also set corlorcolumn=80 work
set cursorline "高亮显示当前行
set cursorcolumn  "高亮显示当前列
""can set several options operately
"hi CursorLine cterm=NONE ctermbg=darkred ctermfg=white guibg=darkred guifg=white
"hi CursorColumn cterm=NONE ctermbg=darkred ctermfg=white guibg=darkred guifg=white
"" s使用autocmd来解决和colorshceme设定之间的冲突
"autocmd BufRead,BufNew * hi CursorLine guibg=black 
"autocmd BufRead,BufNew * hi CursorColumn guibg=black 
set nobackup                 " 设置无备份文件
"printf函数返回格式化字符串
"set backupdir=printf("%s,%s",getcmd()，"/vi_backup/")
set noswapfile 
set noundofile 
let autosave = 300 "每300s自动保存一次" "let as = 300  "as  就是autosave的意思
set showmatch               "代码匹配
set laststatus=2            "总是显示状态行
set autoread                "文件在Vim之外修改过，自动重新读入
syntax enable
syntax on
set ai                      "自动缩进
set autoindent              " 自动缩进对齐
set smartindent
set autochdir               "自动设置当前目录为正在编辑的目录
set backspace=2             "设置退格键可用
set clipboard+=unnamed      " 与windows共享剪贴板
if(g:iswindows)
    set guifont=Consolas:h12    " windows设置方式，字体与字体大小之间为:
else
    set guifont=Monospace\ 12   " unix设置方式,字体与字体大小之间为空格，\用来转义空格字符
   "set guifont=Courier\ New:h11   "\ 为转义字符  转义空格
endif
"autocmd GUIEnter * simalt ~x   "windows下启动之后默认最大化
set guioptions=+m               "显示菜单栏，如果不设置则都显示
"set guioptions=+T              "显示工具栏,guioptions如果设置了则只能赋一个值，

set scrolloff=7                 "设置光标所在位置最高和最低到边界行数为3
set incsearch
set autoindent                  " 自动对齐
set softtabstop=4               "set tab = insertspace "缩进宽度为4个字符"  
set shiftwidth=4                "tab宽度为4个字符"  
"set tabstop=4  
""编辑时将所有tab替换为空格"  
set et  
set expandtab                   " 将Tab自动转化成空格[需要输入真正的Tab键时，使用 Ctrl+V + Tab]
"set ft = c                     "filetype设定
"
syntax enable                " 打开语法高亮
syntax on                    " 开启文件类型侦测
filetype indent on           " 针对不同的文件类型采用不同的缩进格式
filetype plugin on           " 针对不同的文件类型加载对应的插件
filetype plugin indent on    " 启用自动补全


