gvim:
	rm -rf /home/micro/.vimrc
	rm -rf /home/micro/.vim/colors
	rm -rf /home/micro/.vim
	mkdir /home/micro/.vim
	ln -s /home/micro/git/vim-resources/micro-config-files/_vimrc /home/micro/.vimrc
	cp /home/micro/git/vim-resources/micro-config-files/vimfiles/* /home/micro/.vim/ -rf
neovim:
	rm -rf /home/micro/.config/nvim/init.vim
	rm -rf /home/micro/.config/nvim/colors
	rm -rf /home/micro/.config/nvim
	mkdir /home/micro/.config/nvim
	ln -s /home/micro/git/vim-resources/micro-config-files/init.vim  /home/micro/.config/nvim/init.vim
	cp /home/micro/git/vim-resources/micro-config-files/vimfiles/colors /home/micro/.config/nvim/colors -rf
	cp /home/micro/git/vim-resources/micro-config-files/vimfiles/* /home/micro/.config/nvim/ -rf
all:gvim neovim
