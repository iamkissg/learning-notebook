# Linux Commands

标签（空格分隔）： 学校 Linux

---
##day1
> Unix是严格区分大小写的

- Cancel an operation：Ctrl+c

>  参数的多种写法: -r -f = -rf

> 命令行的一般形式：command_name [options] [arguments]

- echo - display a line of text

> - 检查前一条命令的错误代码：echo $?

- cat - concatenate(把...联系起来) files and print on the standard output
1. -l,

- man - man+“指令”，查看“指令”的help

- who - show who is logged on

- cal, ncal — displays a calendar and the date of Easter

- clear - clear the terminal screen

- date - print or set the system date and time

- passwd - change user password

- date --set=string(时间)

- adduser, addgroup - add a user or group to the system

- userdel - delete a user account and related files

- groupdel - delete a group

- su - change user ID or become superuser

> 用户密码经加密后存储在/etc/shadow文件内，只要知道其中一个用户的密码，就可修改所有用户的密码(复制粘贴即可)

> Linux treats everything as files.

> components of files:inode onwer data ..

> file types: regular directory device link

##day2

- grep [OPTIONS] PATTERN [FILE...]，for lines containing  a  match to the given PATTERN.
1. -v，取反，输出匹配之外的所有行
2. -i
3. -A NUM，输出匹配行以及之后
4. -B
5. -C
6. -E
7. -F
8. []: 搜索集合字符，
9. ^表示行的开头，也可用在[]中，匹配正则表达式的开头
10. $表示行尾，同^，用于匹配正则表达式的结尾
PS:MS文件，行尾有一个‘^M’字符，只是不
- sort - sort lines of text files。默认按字典序进行排序。
1. -n
2. -b ignore the leading blanks
3. -f
- touch - change file timestamps
- uniq  - report or omit repeated lines
- comm - compare two sorted files line by line.
- cp - copy files and directories
- rm - remove files or directories
1. -i:prompt before every removal
2. -f, --force: ignore nonexistent files and arguments, never prompt
4. -I:prompt once beforing removing more than 3 files.
5. -r, -R: remove directories and their contents recursively.
- mv - move (rename) files
- wc - print newline, word, and byte counts for each file
 1. -l: print the newline counts
 2. -c: print the byte counts
 3. -m: prints the newline
 4. -w: print the word counts
- tail - output the last part of files
- head - output the first part of files

##day3
> 树状结构
绝对路径:以根目录为起点,`/xxx/xxx/xxx...`
相对路径:以当前位置为起点

- mkdir - make directory
 1. -p make parent directories as needed
- rmdir - remove empty directories
- cd - change directory
- pwd - print working directory
- ls - list directory contents
 1. -a all
 2. -c list contents in order of timeof last modification,
 3. -l using a long listing format

> `.`,表示当前目录
`..`,表示父目录
`-rw-rw-r-- 1 kissg kissg   57 Mar 24 16:13 a.txt`
依次:file_type permission  link_numbers owner group size modification_time file_name
file_type: `-`:regular file;`d`:directory;`b`:device;`c`:character;`l`:link file
permissions: ugo `r`:readable;`w`:writable;`x`:excutable。也可以用数字表示,3个一组,`r`:4;`w`:2;`x`:1;`-`:0
在命令后 + `&`

- chmod - change mode
1. `+x` - 为所有用户添加可执行属性
2. `u+x` - 仅为所有者添加可执行属性
3. `744` - update permissions(rwxr--r--)

- `./` - excucate
- ps -
- kill -
- top - display Linux processes
 1. -u|U user_name - 查看指定用户的使用情况
 2. -p  PID        - 查看指定进程号的进程的使用情况
 - kill PID -  终止进程
 - gcc xxx.c - 编译c语言源程序
 - sleep - delay for a specific time for a command
  1. sleep sec() ; command
- gzip - compress or uncompress files
 1.
- tar -
 1. -c - create a new archive
 2. -x - extract files from an archive
 3. -f - use archive file or device ARCHIVE
 4. -z - gzip
- sed
-
##day4

- shell type: bash, csh, ksh, tcsh, zsh
- 一般在shell脚本首行输入"#!/bin/bash"用于指示
- 3钟执行shell脚本的方式:(首先得确保脚本有执行的权限)
 1. ./file_name.sh
 2. bash shell_script parameers
 3. bash < shell_script (老师说不建议,不能处理带参数的形式)
- `history`, 查看历史操作
- `alias`: 别名,比如`alias dir=/home/kissg/Downloads/`
- `ll` is short for `ls -l`
- `*`,表示任意的
- `?`,表示一个
- `[a-zA-Z0-9]`表示范围
- `!`表示非
- `*(pattern)`,0次以上
- `@(pattern)`
- `+(pattern)`,出现一次以上
- `?(pattern)`,出现0次或1次
- `!(pattern)`,不出现
- 双引号 - 不将`$`,'`',`\`当作普通字符
- 单引号 - 当所了有的字符都当作普通字符
- 倒引号 - 将字符串当作shell命令
- `<` - 表示流,右边的文件流到左边的命令
- `>` - 左边的命令输出到右边的文件,会覆盖原文件的内容
- `>>` - 表示追加
- `|` - pipeline, 左边命令的输出作为右边的输入
- `;` - 将多个命令写在一行,先后执行
- `&&` - 只有cmd1被执行了,cmd2才会被执行
- `||` - 执行两条命令中的一条, cmd1被执行了,cmd2就不被执行
- `{}` - 与()不同,并没有创建一个子shell, 标准使用是{<space> cmd...;}
- `()` - 相当于在()内部创建了一个子shell,内部变量的作用域限于()内部
- 使用变量(非定义)时,变量名前必须加`$`,否则将被视为字符
- 数组的定义: `a=(n1 n2 n3 ...)`
- 通过下标数组的值时,要用{}包裹,以指示a[0]是一个整体
- `read 变量名`表示将键盘输入的值赋给变量.指定了多个变量,最好输入相应数量的值,否则错误将超乎想象
- 位置参数,`$1`,`$2`, `$0`表示命令本身或文件本身
- 特殊参数 `$#`表示输入参数的个数
- `$$`:当前进程的id
- `$?`:前一个命令是否正确执行
- shell的算术运算 `$(( exp ))`
- `let var="exp"`
- `expr expression`
- 浮点运算: $(echo "" |bc)
- 使用`|`, `>`, `<`, `>>`等重定向操作, 是匿名的
- `var=$(echo "expression" | bc l)
- 分支语句:`if-then-[elif-then-]else-fi`:
 - 条件结构:
  1. test condition
  2. [ condition ]
  3. [[ condition ]]

>    -r filename - 存在且可读
   -w filename - 存在
   -x filename - 存在
   -f filename -
   -d filename - 存在且是目录

>   -z str -
   -n str -

>   n1 -eq n2 - equal
   n1 -ne n2 - not equal
   n1 -lt n2 - less than
   n1 -le n2 - less or equal
   n1 -gt n2 - great than
   n1 -ge n2 - great or equal

>  ! - not
   -o - or
   -a - and

>    case var
   patter 1) cmd1;;
   patter 2) cmd2;;

- 循环语句:

```shell
  while [ condition ]
  do cmds
  done
```


```shell
  until [ condition ] "条件不满足才执行
  do cmds
  done
```

```shell
  for var in list
  do cmds
  done
```

```shell
  for ((init;condition;operation))
  do cmds
  done
```

- break, continue
- 函数:

```shell
function_name()
{   " 花括号一定要这样用
    cmds
}
```
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-


