# Vim学习册手

标签（空格分隔）： vim

---
[TOC]

##知识
- 指令字母大小写区分,且不需在指令后加按`Enter`键
- 一部分指令在输入时不会显示在屏幕上,如`i`,另一部分指令在输入时将显示在屏幕底部,如`/`,`?`,`:`
- 使用vi(其他任何文本编辑器),都是将要编辑的文件复制到内存缓冲区,显示缓冲区,并且用户能自由地增加、删除、更改文本。直到存储编辑的结果,vi才将缓冲区中的内容写回硬盘。可以说, 使用文本编辑器,我们都是在缓冲区里的文件副本上进行操作
- 使用vi时,最左边的`~`表示当前行没有文本,连空格都没有;底下的提示行显示了文件的名称与状态
- 命令模式:所有的按键都代表命令;插入模式:输入将成为文件内容
- `!xxx`在感叹号之后,可以使用shell命令
- `:`提示符表示处在`ex`行编辑模式中
- 依照终端类型的不同,<backspace>键可能是消除原来输入的文字,也可能只是后退。无论如何,退格键经过的内容都将被删除
- 

 
##命令:

0. vi/vim [filename]
1. i        (insert)
2. cw       (change word)
3. :q       (quit)
4. `esc`    返回命令模式 
5. ZZ       保存并离开
6. :wq      (write & quit, ex形式)
7. :e!      撤销此次编辑的所有结果,但不离开
8. :q!      撤销本次编辑的所有结果,并离开 
9. :w pathname/file 将文件保存到指令位置
10. :sh     创建一个shell。输入Crtl-D或exit,结束shell,并回到vi
11. Ctrl-Z  暂停vi(挂到后台),回到shell。输入fg命令,回到vi
12. :pre    :preserve的简写,强迫系统保存当前缓冲区
13. h       左移一个字符
14. l       右移一个字符
15. j       下移一个字符
16. k       上移一个字符
17. o       在当前行后插入一行
18. O       在当前行前插入一行
19. e       end word
20. E       end WORD(英语里将“word+紧跟着word的标点”算作一个WORD)
21. w       next word(一个标点也算一个word)
22. W       next WORD(直到遇到<space>都算一个WORD)
23. :split/:vsplit file<cr>     在新的纵向/横向分屏编辑指定文件
24. source $MYVIMRC             重读.vimrc文件,使新的修改生效
25. viw     高亮显示单词
26. dw      删除到下一个单词   delete word
27. ci(     替换括号里的内容   change inside (
28. yt,     复制到", "         yank till comma
29. :normal 命令后的跟着一串字符,无论字符表示什么含义,`:normal`命令都会执行他们,就像在常规模式下敲击这些字符意义
30. >>      缩进当前行
31. :execute 命令后面跟着一个VIm脚本字符串,然后把这个字符串当作一个命令执行,`:normal!`不能识别特殊字符,这是`execute`命令存在一个原因.当`execute`碰到字符串时,会先替换这个字符串中的所有特殊字符
32. ?^==\+$  执行效果是,向后(文章头)搜索任何两个及以上等号组成的行,由于用^和$加以了限定,该行不会包含任何等号以外的字符
33. :nohlsearch 清楚之前的搜索结果的高亮显示
34. g_      移动都当前行的最后一个非空字符上,使用.与`$`的不同之处在于,`$`会选中换行符号
35. Ctrl-W + h/j/k/l 切换分屏
36. qa      开始录制宏,并将宏储存到寄存器a,因此,可以通过qb,qc录制其他的宏
37. n@a     从寄存器a中取出宏,并重复n次
38. :ls     查看所有缓冲区
39. :b <name or number> 查看缓冲区(即一个打开的文件),此时会直接将指定缓冲区的内容拉到当前窗口.配合`:ls`更好用




##Learn Vim script The Hard Way
- 当写Vimscript时,使用`:echo`打印输出,但脚本运行结束后,输出信息将丢失(一次性打印);使用`:echom`打印信息,会保存下来,执行`:messages`可以查看这些信息
> `:echo` - echoes each {exp1}, with a space in betwee.`"\n"`to start a new line, `"\r"`move the cursor to the first column
`:echom` - Echo the expression(s) as a true message, saving the message in the |message-history|.
`:messages` - This message is given when there is something on the screen for you to read, and the screen is about to be redrawn

- Vimscript使用`"`添加注释
- Vim有多种选项可以设置来改变其展现方式。其中主要的2种是:`布尔选项`(on or off)和`键值选项` 
- 所有的`布尔选项`都可用`:set <name>`打开选项,`:set no<name>`关闭
- 使用`:set <name>!`的方式,切换布尔选项的值(on -> off, off -> on)
- 使用`:set <name>?`的方式,来查看选项的当前值
- 键值选项,可通过`:set <name>=<value>`来改变值,如`:set numberwidth=10`将行号的列宽改为10
- 可一次性设置多个选项值,中间用` `隔开
> `number` - precede(加上前言) each line with its line number.
`relativenumber` - Show the line number relative to the line with the cursor in front of each line.(计算每一行与当前行的距离,默认是 off)
`wrap` - When on, lines longer than the width of the window will wrap and displaying continues on the next line.  When off lines will not wrap and only part of long lines will be displayed.(默认是 on,“自动换行”)
`shiftround` - round 在这里应该是取整的意思。当缩进不成倍时，开启这个选项将会让 Vim 自动把周围的缩进化零为整，就不需要手动去填/删空格了
`showmatch` - When a bracket is inserted, briefly jump to the matching one.  The jump is only done if the match can be seen on the screen. The time to show the match can be set with `matchtime`(当输入成对括号时,Vim将自动跳转到与之匹配的括号,并高亮一下,随后自动回到正在输入的位置,默认是 off)
`matchtime`:功能如上所述

- `键盘映射`:类似于赋值,将某功能赋给某指定键(`:map - x` 将`x`键的功能赋给`-`)
- `特殊字符`:自定义特殊字符/组合键(`:map <space> viw` 将依次按下`v`,`i`,`w`的键组合绑定到空格键上。功能是,移动光标到一个单词上,按<space>可高亮选中真个单词)
- 还可以映射组合键,如`:map <c-d> dd`将`dd`的功能绑定到`Ctrl+d`上
- 不能在同一行为`键盘映射`添加注释,因为`"...`都将被当作键盘映射的内容
- `模式映射`:Vim存在三种模式(normla,visual,insert),故可使用`nmap`,`vmap`,`imap`分别指定映射仅在对应的模式下生效
- Vim只按我们说的做。`:imap <c-d> dd`,实际效果并不是删除一行,而是输入两个字符`d`。因为是在insert模式下,而insert模式下的`dd`不就是输入两个`d`嘛。为了实现删除当前行的期望,需要修改指令为`:imap <c-d> <esc>dd`,更符合预期的指令还应该是`:imap <c-d> <esc>ddi`
- 如`:nmap dd O<esc>jddk`的功能是无限插入空行,`*map`映射存在“递归”的危险,以及传递性
- 当多个行为映射到同一个键上,将发生冲突,结果仅有一个映射有效
- 每个`*map`系列的命令都有对应的`*noremap`命令,包括：noremap/nnoremap、vnoremap和inoremap。这些命令将不递归解释映射的内容。这些命令不递归地解释映射的内容(也不在具有传递性)。
- ***任何时候,都应该定义非递归映射`noremap`/`nnoremap`、 `vnoremap`和`inoremap`,而不是递归映射***
- `~/.vimrc`文件添加一个映射并不立即生效,而是在重启vim后读取生效。
- 为了不覆盖功能键,可定义一个自己的`leader`键,用于做自定义功能键的前缀。`:let mapleader = "-"`
- `:let maplocalleader = "\\"`设置local leader,使之仅对某类文件有效
- 自定义纠错机制,如insert模式下,如`:iabbrev adn and`,就可将输入的`adn`自动更正为`and`,注意`adn...`不会被更改
- Vim定义的`keyword`包括:`_` `[0-9]` `[a-z]` `[A-Z]` `ascii码192-255`的字符。只要输入`non-keyword character`就会引发abbreviations替换
- abbreviations除了纠错,还可以用于缩写,如`:iabbrev @@ enginechen07@gmail.com`
> abbreviations vs mappings
- abbreviations是上下文相关的,但只在需要的时候替换
- mappings只要检测到匹配的键组合,不管被映射字符的前后字符是什么,一律替换

- 输入组合键时,若中间停顿过久,Vim将判定用户不想生效那个映射,而执行之前输入的键的行为(若存在)
- 正确使用Vim的关键就是使得自己能够快速的离开插入模式，然后在常用模式下进行移动。
- 在映射命令中,使用`<buffer>`告诉Vim这个映射只定义在它的缓冲区(即定义该映射的文件)有效
- 更正确的定义本地缓冲区映射的方式是使用`<localleader>`
- `<leader>`和`<localleader>`就好像设置了一种命名空间,保证了不同映射的清晰
- 使用`<localleader>`来设置本地映射可以防止插件覆盖`<leader>`设置的全局映射
- `:setlocal xxx`可以设置本地选项。默认情况下,使用`:set xxx`设置的选项将在同一窗口内共享
- 本地设置(映射)将覆盖全局的设置(映射)
- `自动命令`:让Vim自动地执行某些指定的命令,这些命令会在某些事件发生时执行
- `Vim xxx` then immediately `:q`,由于并没有保存,文件xxx实际并不存在,Vim并没有真正创建它
- `autocmd event pattern cmd`,自动命令的第一部分是事件的类型,包括:
 - 开始编辑一个当前并不存在的文件。
 - 读取一个文件，不管这个文件是否存在。
 - 改变一个缓冲区的filetype设置。
 - 在某段时间内不按下键盘上面的某个按键。
 - 进入插入模式。
 - 退出插入模式。
 - ...
- 自动命令的第二部分是模式,用于限定要执行的命令的执行范围
- 自动命令的第三部分是事件发生时执行的命令。
- 可以创建一个绑定多个事件的自动命令,用`,`分隔
- 在Vim脚本编程中,有一个不成文的规定,应该同时使用`BufRead`和`BufNewFile`来运行命令,这样当打开某个类型的文件时,不论文件是否存在,命令都会执行
- 自动命令+本地选项(映射)能根据不同的文件类型进行不同的处理,省心省力,比如:
```
:autocmd FileType javascript nnoremap <buffer> <localleader>c I//<esc>
:autocmd FileType python     nnoremap <buffer> <localleader>c I#<esc>
```
- 本地缓冲缩写+自动命令,可以实现对不同类型文件的`snippet`,
- 每次加载`~/.vimrc`文件时,vim会重新读取整个文件.多次重载`~/.vimrc`文件,也将导致自动命令的重复,这将导致vim运行速度的减慢.
- 解决的办法是,将创建自动命令组,每组以`autocmd!`开头,该命令将清空该组自动命令,之后再加载就不会重复命令
- `autocmd filetype html nnoremap <buffer> <localleader>f Vatzf`将关闭一个html匹配的html标签
- 一个操作是这样的命令,当你键入该操作之后,它并不先执行,而是等待一个移动命令,然后对你选中的文本(当前所在位置,以及移动命令终止处)进行操作
- 常见的操作包括`d`,`c`和`y`.
- 因此可以对移动命令进行映射,可方便的执行`d`,`c`,`y`操作
```s
:onoremap in( :<c-u>normail! f(vi(<cr>  # find next (, and select the inner contennt
```
- `:normal`命令表示,像是在normal模式下敲击这些字符一样.`:normal gg`即相当于在normal模式下键入2个gg.
- `:execute`命令后跟一个Vim脚本字符串,然后将这个字符串当作命令执行
- 使用状态栏之前,需要`:set laststatus=2`将状态栏永久显示在编辑器底部.状态栏的设置与python的格式化字符串有点相似
- 在选项名称前面加`&`符号,表示引用,可以获得值,也可以修改之.前缀`&l:`表示本地选项,而不是全局
- 通过`@x`的方式,可以设置与读取寄存器.`@x`其中x被指定为寄存器名,`"`表示一个未命名的寄存器,在复制的时候没有指定寄存器的文本都会放在这里. 
- 寄存器的定义: `"{a-zA-Z0-9.%#:-"} Use register {a-zA-Z0-9.%#:-"} for next delete, yank or put`
- @: Execute the contents of register {0-9a-z".=*+} [count] times
- vim有多种不同的作用域,在变量名中使用`b:`,相当于告诉vim`b:`修饰的变量是当前缓冲区的本地变量.除了`b`以外,还有`w`,`t`,`g`等等
- 用管道(`|`)可将多行命令写在一行,而它们将被视为分离的命令.并且实际上,只需要在最前面使用`:`即可
- 如有必要,vim将强制转换变量的类型.以数字开头的字符串被转换成数字(仅将前面的数字部分进行转换), 而非数字开头的字符串将被转换成0
- vim支持if-elseif-...else的条件分句
- vim可设置大小写忽略项,因此"foo"可能等于"Foo".因此,`==`的行为完全取决于用户设置.`==?`则自带忽略大小写功能,`==#`自带大小写敏感功能.比较整数时,`==?`,`==#`都可一样使用
- 没有作用域限制的Vimscript函数必须与大小字母开头,`function Xxxx() ... endfunction`用于定义函数,`call Xxxx()`用于调用函数,或者`Xxxx()`也能直接调用函数
- 如果函数没有返回值,将隐式返回`0`
- 在写需要参数的函数时,总是需要给参数加上`a:`前缀,告诉vim去参数作用域查找.定义函数时,是用`...`相当于python的`*args`即可变参数,当定义了一个可变参数的函数,`a:0`将被设置为传入的可变参数的数量.可变参数从`a:1`的索引开始.`a:000`被设置为一个包括所有传递过来的可变参数的list,而不能对list使用`echom`
- 不能对参数变量重新复制,相当于总是使用c++的`const`
- vimscript有2种数值类型:Number和Float.Number是32位带符号整数(4字节).十六进制数的表示与其他语言相同,即使用前缀`0x`,使用前缀`0`表示八进制数,但最好不要使用八进制数,因为`019`这样的数将被识别为十进制数(八进制数19本身就是个错误)
- 表示浮点数时,小数点和小数点后的数字必须要有,否则将出错
- 
 
