## Chapter 1

- `tmux`: open a new session, 听说以上方法不被建议使用
- `exit`: close the current session and return to standard terminal
- `tmux new-session -s session_name` or `tmux new -s session_name`创建命名会话
- tmux的一个最大优势是启动tmux环境并执行各种程序或进程时,可通过会话分离让tmux在后台运行.
- 从tmux会话分离时,tmux会话运行的程序仍然在运行.
- `PREFIX d`从一个会话分离
- `tmux list-sessions` or `tmux ls`列出当前存在的会话
- `tmux attach` or `tmux a` 连接到当前仅有的一个会话
- `tmux a -t session_name`连接到指定名称的会话
- `tmux kill-session -t session_name`杀死指定会话
- tmux窗口的功能就像web浏览器的标签页
- `tmux new -s windows -n shell`创建一个名为windows的会话,并将第一个窗口命名为shell
- `PREFIX c`在当前会话创建一个新窗口
- 如果不对窗口命名,窗口的名称会随着当前运行的程序变化而变化
- `PREFIX ,`重命名窗口
- `PREFIX n`切换至下一个窗口
- `PREFIX p`切换至上一个窗口
- 每个窗口都有一个序号,可以通过`PREFIX No.`切换窗口
- `PREFIX f`通过窗口名来查找窗口,将直接跳转到相应的窗口
- `PREFIX w`显示一个可视化的窗口列表,选中即跳转
- `exit`还可以用于关闭窗口
- `PREFIX &`会在状态栏给出确认信息询问是否关闭当前窗口(&=et=exit)
- 如果要完全退出一个tmux会话,必须关闭所有窗口
- `PREFIX %`水平切分窗口,将当前窗口(或面板)切分为左右两个面板
- `PREFIX "`垂直切分窗口,将当前窗口(或面板)切分为上下两个面板
- `PREFIX o`循环(逆时针)切换面板
- tmux默认面板布局:
 1. `even-horizontal`: 将所有面板均匀地水平排列
 2. `even-vertical`: 将所有面板均匀地垂直排列
 3. `main-horizontal`: 在顶部创建一个主面板,其余面板在底部水平排列
 4. `main-vertical`: 在左侧创建一个主面板,其余面板在右侧垂直排列
 5. `tiled`: 将所有面板大小均等地在屏幕上显示

- `PREFIX <space>`依次轮流切换面板布局
- `exit`还可以关闭面板
- `PREFIX x`杀死一个面板.如果当前窗口只有一个面板,关闭面板将关闭窗口
- `PREFIX :`进入tmux命令模式
- `: new-window -n window_name`创建一个命名的窗口
- `: new-window -n window_name "cmd"`创建一个命名窗口,并在其内执行命令运行进程.当进程被关闭时,窗口也将被关闭
- `PREFIX ?`查看tmux预定义的快捷键列表

## Chapter 2

- 当我们向tmux发送命令时,tmux增加了一个小小的延时(即松开`PREFIX`到按下命令键的时间),可修改延时而让tmux响应更快
- `set`其实是`set-option`的缩写,如果要配置与窗口进行交互的选项,需要使用`set-window-option`
- 通过在多条命令之间添加`\;`,使一个键能绑定多条命令
- 通过在`bind`命令后添加`-n`参数,就可以通知tmux这个快捷键不需要按下前缀.但会禁用tmux会话里任何程序或命令的组合键
- `-r`参数表示repeatable,即只要按下前缀一次,就可以持续地使用定义的命令键

```shell
$ wget http://www.vim.org/scripts/download_script.php?src_id=4568 -O colortest
$ perl colortest -w
```

- 以上命令可用于测试终端的色彩模式
- linux系统,在`~/.bashrc`文件中添加`[ -z "$TMUX" ] && exportTERM=xterm-256color`条件语句,可确保`TERM`变量在tmux外运行,因为tmux会自己设置所在的终端
- `~/.tmux.conf` is set up for self, and `/etc/tmux.conf` is set up for all users.

