
* 安装
 1. 将hdl.vim copy到vim plugin文件夹中，或者直接在.vimrc中source；
 2. 将ncverilog.vim copy到compiler文件夹中；

* 使用
1. 简单使用，
   命令行输入 :IRUN 命令即可
2. 当当前编译需要依赖其他文件时：
   命令行输入 ：IRUN -v xxx_define.v -f xxx.lst
   后面的文件指定方式ncverilog能够识别即可
