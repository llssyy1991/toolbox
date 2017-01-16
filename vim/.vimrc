set nocompatible              " required
filetype off                  " required
set background=dark
colorscheme molokai
syntax enable
syntax on
set backspace=indent,eol,start
" setup for python

au BufNewFile,BufRead *.test
\ set tabstop=10

au BufNewFile,BufRead *.py
\ set tabstop=15

au BufNewFile,BufRead *.php
			\set tags=tags;

			\set guifont=Monaco:h10       " 字体 && 字号
			\ set expandtab                " 设置tab键换空格
			\ set tabstop=4                " 设置tab键的宽度
			\ set shiftwidth=4             " 换行时行间交错使用4个空格
			\ set autoindent               " 自动对齐
			\ set backspace=2              " 设置退格键可用
			\ set cindent shiftwidth=4     " 自动缩进4空格
			\ set smartindent              " 智能自动缩进
			\ set ai!                      " 设置自动缩进
			\ set nu!                      " 显示行号
			\ set showmatch               " 显示括号配对情况
			\ set mouse=a                  " 启用鼠标
			\ set ruler                    " 右下角显示光标位置的状态行
			\ set incsearch                " 查找book时，当输入/b时会自动找到
			\ set hlsearch                 " 开启高亮显示结果
			\ set incsearch                " 开启实时搜索功能
			\ set nowrapscan               " 搜索到文件两端时不重新搜索
			\ set nocompatible             " 关闭兼容模式
			\ set vb t_vb                 " 关闭提示音
			\ set cursorline              " 突出显示当前行
			\ set hidden                   " 允许在有未保存的修改时切换缓冲区  


" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" Add all your plugins here (note older versions of Vundle used Bundle instead of Plugin)

Plugin 'tomasr/molokai'
Plugin 'octol/vim-cpp-enhanced-highlight'
Plugin 'rkulla/pydiction'
Plugin 'scrooloose/nerdtree'


" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
let g:pydiction_location='/home/lsy/.vim/bundle/pydiction/complete-dict'
