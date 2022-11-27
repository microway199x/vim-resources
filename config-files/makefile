gvim:
	rm -rf ~/.vimrc
	rm -rf ~/.vim/colors
	rm -rf ~/.vim
	mkdir ~/.vim
	ln -s ~/git/vim-resources/_vimrc ~/.vimrc
	cp ~/git/vim-resources/vimfiles/* ~/.vim/ -rf
neovim:
	rm -rf ~/.config/nvim/init.vim
	rm -rf ~/.config/nvim/colors
	rm -rf ~/.config/nvim
	mkdir ~/.config/nvim
	ln -s ~/git/vim-resources/_vimrc ~/.config/nvim/init.vim
	#ln -s ~/git/vim-resources/vimfiles/colors ~/.config/nvim/colors
	cp ~/git/vim-resources/vimfiles/* ~/.config/nvim/ -rf
all:gvim neovim
