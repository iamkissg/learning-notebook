#### before 2016-08-01
- 求余数: (-len(s)) % 4 => 4 - (len(s))%4
- linux下, 以非root用户身份, 用nvm安装node.js, node.js将被安装在当前用户家目录下. 其他用户, 甚至root用户并不知道系统中已经安装了node.js, 之后用户通过npm安装的工具程序, 也只能被当前用户使用, 即, 此时`sudo　cmd`会提示`cmd`不存在. 解决方法是：软链接

```shell
sudo ln -s /home/kissg/.nvm/versions/node/v4.4.4/bin/npm /usr/bin/npm
sudo ln -s /home/kissg/.nvm/versions/node/v4.4.4/bin/node /usr/bin/node
sudo ln -s /home/kissg/.nvm/versions/node/v4.4.4/lib/node /usr/lib/node
sudo ln -s /home/kissg/.nvm/versions/node/v4.4.4/bin/node-waf /usr/bin/node-waf
sudo npm install -g configurable-http-proxy #　此时sudo命令就不报错了
```

- 假设存在**软链接**`file1　->　file2`, 程序对`file1`的操作都会反应在`file2`, 即使之后改变`file1`的指向, 在更改原程序的行为之前原程序不会对`file1`新指向的文件作修改, 而是继续对`file2`进行修改.
- 我想到的硬链接也不能解决上述问题--原程序先向`file1`进行写入, 再创建`file2`到`file1`的硬链接, 相当于给文件取一个别名, 之后删除并新建`file1`. 我原来的想法是原程序一直向`file1`进行写入, 并创建一个硬链接, 当`file1`的大小达到预设的上限时, 重建`file1`, 重建硬链接. 但是原程序已经锁定`file1`了, 即使是瞬间的删除新建, 也会导致原程序出错.

```txt
e: encountered a section with no package: header
e: problem with mergelist /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_natty_main_binary-i386_packages
e: the package lists or status file could not be parsed or opened.
```

- 上述问题解决: `sudo rm -vf /var/lib/apt/lists/*` - 删除merge list

- `system program problem detected`问题的解决: `sudo rm /var/crash/*` - 删除旧的crash. 虽然之前的问题已经解决了, 但旧的crash文件被保存了下来, 所以会持续报错.

```js
document.getelementbyid('container').addeventlistener('click', function(event) {
	     console.log(event.target.innerhtml);
	}
})
```

- 在一个`<div>`上注册事件(click)监听, 对div内所有元素的点击都会在控制台打印. (不需要为每个元素单独注册事件)
- `docker exec -it <container id> /bin/bash` -  connect to a bash prompt on the running container.
- `find . -name "filename"` - 在当前目录递归地查找指定文件名的文件
- linux process states:

```txt
d uninterruptible sleep (usually io)
r running or runnable (on run queue)
s interruptible sleep (waiting for an event to complete)
t stopped, either by a job control signal or because it is being traced.
w paging (not valid since the 2.6.xx kernel)
x dead (should never be seen)
z defunct ("zombie") process, terminated but not reaped by its parent.

# additional characters
< high-priority (not nice to other users)
n low-priority (nice to other users)
l has pages locked into memory (for real-time and custom io)
s is a session leader
l is multi-threaded (using clone_thread, like nptl pthreads do)
+ is in the foreground process group
```

- `ps -ef` - 查看所有进程的父进程
- `trap -l` - linux查看信号及其编号 (ubuntu 14.04 没找到这个命令诶)
- 交互式bash获取进程pid:

```shell
ps -ef | grep "name" | grep -v grep | awk '{print $2}'
ps -ef | awk '/[n]ame/{print $2}'
ps x | awk '/[n]ame/{print $1}'
pgrep -f name  # 最简单的方法
pkill -f name  # 通过名称找到进程并杀死
pidof name     # 包含 name 的所有命令的 pid
```

- shell 脚本获得进程 pid:

```shell
#! /bin/bash
# process-monitor.sh
process=$1
pid=$(ps -ef | grep $process | grep 'name' | grep -v grep | awk '{print $2}')
echo $pid
```

- `$$` - 当前 shell 进程的 pid; `$!` - 上一个后台进程的 pid
- 查看指定进程是否存在:

```shell
if ps -p $pid > /dev/null
then
    echo "$pid is running"
    # do something knowing the pid exists, i.e. the process with $pid is running
fi
```

#### 2016-08-02

- python, str to time/datetime - datetime.datetime.strptime(str, time\_format).date() | time.time.strptime(str, time\_format)
- python, get pid of the running program, or you can apply this to check if the program is running

```
# check_output - run command with arguments and return its output.
# if the exit code was non-zero it raises a calledprocesserror.
from subprocess import check_output
def get_pid(name):
    return check_output(["pidof",name])

    # or handle multiple entries and cast into ints
    # using set for quick search
    # return set(map(int,check_output(["pidof",name]).split()))

    # or with -s flag to get a single pid
    # return int(check_output(["pidof","-s",name]))
```

- jquery 显隐元素: `$(selector).hide();`, ` $(selector).show();`
- javascript 使用 document.createelement() 动态创建 dom 节点:

```javascript
var childnode = document.createelement('p');
childnode.innerhtml = '<span>这里是提示信息〜〜</span>';
childnode.setattribute('class', 'alerts');
childnode.setattribute('onclick', 'this.style.display = "none"');
/*or
childnode.classname = 'alerts';
childnode.onclick = function () {
    this.style.display = 'none';
}
*/
document.getelementsbytagname('body')[0].appendchild(childnode);
```

- css, `inline-block` 替代 `float:left` 实现横向列表. 默认情况下, inline 元素之间会有空隙, 通过设置 padding, margin 等属性可消除空隙
- jquery 绑定事件与 not 函数, button 反 click 应用举例:

```javascript
$(".trade-filter button").on("click", function(){
    $(".trade-filter button").not(this).removeclass('active');
    switch($(this).attr("id")){
        case "trade-all":
            $("tr").show();
            break;
        case "trade-running":
            $("tr").not($(".running")).hide();
            $(".running").show();
            break;
        case "trade-stopped":
            $(".running").hide();
            $("tr").not($(".stopped")).hide();
            $(".stopped").show();
            break;
    };
});
```

- 不同于 c/c++ 的 `switch`, ecmascript 的 `switch` 可用于字符串, 即 `case "kissg": do_something`
- jquery, `$(selector)` 选择器从**从父级标签一路定位到子级标签, 不是把子级标签写在父级标签之前**

#### 2016-08-03
- 新学 2 个前端日期选择器: jqueryui datepicker 和 bootstrap datetimepicker. 前者的使用见[这里](http://api.jqueryui.com/datepicker/), 后者使用见[这里](http://www.bootcss.com/p/bootstrap-datetimepicker/)
- javascript 获取当前日期时间: `var dt = new date()`, `data` 对象提供了多种日期时间操作
- javascript 切片操作: `stringobject.slice(start,end)`

#### 2016-08-06

- chrome -> editor：`data:text/html, <html contenteditable>`
- ubuntu install the latest version of git, add ppa: `sudo apt-add-repository ppa:git-core/ppa`
- python 运行时, 查看版本: `import sys; sys.version_info`

#### 2016-08-08

- centos, 查看系统版本: `cat /etc/*elease`, 其中 `*elease` 包括 centos-release, os-release, redhat-release, system-release, 每一个都带有版本信息, 其中 `os-release` 最详细, 并且在其他发行版也通用 (ubuntu 可用)
- docker, 局域网内, 切记要修改 ip 地址绑定! 比如使用多个容器来运行主从 redis 数据库应用, redis.conf 默认是 `bind 127.0.0.1`, 这就造成了主从数据库之间无法同步, 必须同时修改为 `bind 0.0.0.0` 才能使已经通过 `--link` 连接的多个容器的数据库同步, 从数据库才能查询到主数据写入的值.
- 查看进程 namespace: `ls -l /proc/[pid]/ns`
- uts - unix timesharing system

#### 2016-08-10

- 查看进程的能力: `cat /proc/$pid/status` (功能不止如此)

#### 2016-08-11

- 查看 ip 路由表, 指令 `route`
    - `lo` - 回环网卡 (lookback adaptor), 本地进程与另一本地进程通信时可用
    - `eth0` - 与外网通信的网卡
- `pscap` - 查看进程的能力, 需要安装工具: `sudo apt-get install libcap-ng-utils`
- `brctl` - 查看和管理网桥, 需要安装工具包: `sudo apt-get install bridge-utils`
- `exec $shell -l` - reload shell
- `python 批量安装包, pip -r <file>` - install from the given requirements file, can be used multiple times

#### 2016-08-16

- `netifaces` - python, portable network interface information
- 逻辑运算符是简化嵌套条件语句的常用方法, 对非嵌套条件同样适用:

```python
s = some_function_that_returns_a_string()
if s:
    first_char = s[0]
else:
    first_char = ""

# 更好的写法应该是
first_char = s and s[0]
```

#### 2016-08-17

- unix 系统测试程序运行时间: `time cmd`, 比如: `time python3 hw.py`
- 有一些嵌套的 if 语句其实不能用逻辑运算符取消嵌套：


```python
if "." in package:
    if package[:package.find(".")] not in  lt:
        print("2")
elif "as" in package:
    if package[:package.find("as") - 1] not in  lt:
        print("3")
elif package not in lt:
    print("4")

# wrong way (也许只是还没找到合适的方式)
# 以第一条为例，写成以下形式，就不能判断带 "." 的但属于 lt 的包了
# 会直接跳到第 3 个逻辑, 然后判断出错
if "." in package and package[:package.find(".")] not in  lt:
    print("2")
elif "as" in package and package[:package.find("as") -lt:
    print("3")
elif package not in lt:
    print("4")
```

- utc: 协调世界时，世界上调节时钟和时间的主要时间标准

#### 2016-08-19

- regex `\w` (word) matches any letter, number or underscore, 即[a-za-z\_]
- svg (scalable vector graphics) - 是**基于 xml**, 用于描述二维矢量图形的一种图形格式, 所以需要浏览器或其他可查看 svg 的图片查看器来打开
- git 回溯到打了某个 tag 的版本: `git reset --hard tag_name`
- python 的 counter, 可用于统计序列中元素出现的次数, 以元素为 key, 出现次数为 value.
- `counter.values()` 和 `counter.keys()` 会按 keys 从小到大的顺序返回 values/keys 的序列, 类型分别是 dict\_values 和 dict\_keys
- `not` 与 `is none`, 大多数情况下可以混用, 但 `not 0` 和 `0 is none` 不能混用, 前者返回`true`, 后者返回 `false`
- `strptime(str, format)` -> new datetime parsed from a string
- `strftime(format, ttime)` or `time.strftime(format)` -> convert time to formatting str
- python, 有些操作, 将文件内容加载到对象, 之后关闭文件也能操作; 另一些, 需要文件一直打开, 相当于创建了一个文件指针对象, 比如:

```python
with open(filename, 'r') as f:
    reader = csv.reader(f)  # 就我所理解, reader 应该是一个文件指针对象
    next(reader)  # ok
next(reader)  # i/o operation closed file

with open(filename, 'r') as f:
    pop_data = json.load(f)
# ok,
# json.load - deserialize file-like object to python object
for pop_dict in pop_data:
    some_operations
```

- python, pygal 移除了 i18n module, 不过可以安装pyga\_maps\_world 插件

#### 2016-08-21

- 作为程序猿, 需要学习的最重要的技能之一是如何高效地摆脱困境. 陷入困境之后, 首先要判断形势. 必须明确地问自己 3 个问题, 才能从他人哪里获得帮助:
 1. 你想要做什么?
 2. 你已尝试哪些方式?
 3. 结果如何?
- 通过回答这三个问题, 你会发现遗漏了什么, 从而无需再做其他事情就能摆脱困境. (橡皮鸭子调试法)
- `git checkout` - 放弃工作区的修改, 恢复到之前的任何提交.
 - `git checkout .` - 放弃最后一次提交之后所做的所有修改, 将项目恢复到最后一次提交的状态.
 - `git checkout hash_val` - 切换到某一节点
 - `git checkout -b` - 创建分支, 并切换
- `in` 操作对于 dict, 是在 keys 范围内进行检查
- 对 list of multi-elements tuple 进行排序, 会按元素在 tuple 中的顺序依次排序, 即先按 0 号元素排序, 若 0 号元素相同, 再按 1 号元素进行排序, 依次类推. 因此, 对于字典的一个处理技巧是, 用列表推导式生成 list of multi-elements tuple, 再对 list 进行排序, 如下:

```python
value_key_pairs = [(v, k) for k, v in some_dict.items()]
value_key_pairs.sort()
# return value_key_pairs[-len(some_dict):]  # 逆序
```

- 使用列表推导式读取 json-line 的技巧: records = [json.loads(line) for line in open(path)]

#### 2016-08-22

- ipython 加载扩展命令: `%load_ext xx`, 比如 `%load_ext zipline`

#### 2016-08-25

- vim 窗口移动: `ctrl-w` + `h/j/k/l`
- shell, `find /path -type f -print | wc -l` - 查看某目录下文件总数 (递归地), `-type f` 只查找 regular file, `-print` - print the full file name on the standard output, followed by a newline
- shell, `find .` - 递归地查看当前目录下所有文件, 最简单的方式, 没有之一

#### 2016-08-26 (tar & zip)

- tar 命令, 最后一个 flag 必须是 `f`, 以指出 tar包
 - `-t` - 列出 tar 包中的文件
 - `-c` - 创建 tar 包
 - `-r` - 追加文件到 tar 包
 - `-x` - 解压 tar 包
 - `-u` - 更新 tar 包中的指定文件
 - `-z` - 调用 gzip, `.gz` 结尾
 - `-j` - 调用 bzip2, `.bz2` 结尾
 - `-z` - 调用 compress, `.z` 结尾, 实际上 `.z` 结尾的文件就是 bzip2 压缩的结果
 - `-v` - verbose, 显示处理过程
 - `-o` - 将文件解压到标准输出
- zip 与 unzip, 使用与 tar 命令类似, 先指定压缩包名, 再指定文件 (如果存在的话). 血与泪的教训, 如果是压缩一个目录, 需要递归!

#### 2016-08-28 (自制 shell)

- shell - 启动时, 会立即显示提示符并等待输入, 在接收到命令并执行完毕后, shell 会再次回到等待循环, 以接收下一条命令
- python 提供了 `shlex` 的标准库, 做 shell 命令的切分
- python, `os` 提供了多种系统调用 `exec` 的变种, 比如 `execvp`, 其中 `v` 表示第二个参数是程序参数列表(或元组), `p` 表示搜索 `$path` 查找给定程序. 其他的还有 `execvpe`, `execl`, `execlp`, `execlpe` 等
- `exec` 会将当前进程的内存替换为一个即将执行的进程. 这意味着原进程将被终止, 新进程成为主进程
- `fork` 则会分配新的内存, 在新内存中拷贝当前进程, 称为子进程. 子进程与父进程完全一样. 子进程中再执行 `exec`, 则会将子进程替换为新的进程, 不影响父进程.
- 在 linux 中，创造新进程的方法只有一个，就是 `fork`
- python, 当父进程调用 `os.fork` 时, 可以认为所有的源码都被拷贝进子进程, 这时父子进程的代码相同, 且并行执行
- 调用一次 `fork`, 会得到 2 次返回值, 分别返回给父进程和子进程, 向子进程返回 `pid=0`, 向父进程返回 `pid` 为子进程的 id
- 当 `fork` 了一个子进程, 并执行命令, 命令并不会在父进程中执行, 比如 `cd` 仅仅会改变子进程的目录, 而不是改变父进程的目录. 之后子进程终止, 父进程保持原先的目录
- 因此, 如 `cd`, `exit` 的命令必须为 shell 本身内置, 并在 shell 进程中执行, 而不是通过 `fork`

#### 2016-08-29

- shell, `groups` - 查看当前用户所在组
- shell, `cut -d: -f1 /etc/passwd` - 查看系统中所有的用户
- shell, `cut -d: -f1 /etc/group` - 查看系统中所有的组
- python 判断字符串是否有效/合法日期, 如下. 因为会直接以格式化字符串读取, 若读入的日期非法, 直接抛出异常, 因此通过是否抛出异常判断日期是否有效.

```python
def is_valid_date(str):
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(str, "%y%m%d")
        return true
    except:
        return false
```

#### 2016-08-30

- cr(carriage return), lf(line feed). dos 和 windows 采用回车+换行 cr / lf 换行
- 而 unix / linux 采用换行符 lf 换行
- 苹果系统则采用回车符 cr 换行
- cr 用符号 `\r`表示, 十进制 ascii 代码是 13, 十六进制代码为 0x0d
- lf 使用 `\n`符号表示, ascii 代码是 10, 十六制为 0x0a
- 所以 windows 平台上换行在文本文件中是使用 0d 0a 两个字节表示，而 unix 和苹果平台上换行则是使用 0a 或 0d 一个字节表示
- 在不同平台间使用 ftp 软件传送文件时，在 ascii 文本模式传输模式下，一些 ftp 客户端程序会自动对换行格式进行转换。经过这种传输的文件字节数可能会发生变化。`如果不想ftp修改原文件，可以使用 bin 模式(二进制模式)传输文本`
- python 的三元操作符(类 `a?b:c`): `res =  exp1 if condition else exp2`
- 列表推导式可以用 `[x*y for x in [1,2,3] for y in  [1,2,3]]` 两个 for 的形式, 同时对两个iterable进行迭代, 返回 [1, 2, 3, 2, 4, 6, 3, 6, 9]
- python, 正常的 for 语句, 可用 `for x, y in zip([1, 2, 3], [1, 2, 3])`, 采用 `zip` 函数对多个序列进行迭代, 但元素是对应的, 即 numpy 所谓的 broadcast. 若需要 n * m 的迭代, 另外写一个生成器函数吧, 比如:

```python
def unique_pairs(n):
    """在 range(n) 范围内生成索引对"""
    for i in range(n):
        for j in range(i+1, n):
            yield i, j
```

- python, 查看 str 是否另一个 str 的子串:
 1. `in` 操作符, 最简单最 pythonic 的方法
 2. `str.find` 方法, 找不到时返回 `-1`

#### 2016-08-31

- ubuntu 更新软件时提示, `the following packages have been kept back:`, 而无法更新, 原因:
- `if the dependencies have changed on one of the packages you have installed so that a new package must be installed to perform the upgrade then that will be listed as "kept-back".`
- 解决办法: `apt-get install <list of packages kept back>`

#### 2016-09-01

- shell, `id -z` - 查看当前用户的上下文
- shell, `ls -z` - 查看文件的上下文
- shell, `ps -efz` - 查看进程的上下文
- centos 上的 docker 容器内, 挂载的数据卷, root permission denied. 原因是宿主机开启了 `selinux`. 此时, 即使容器内没有开启 selinux, 挂载的数据卷由于是容器与宿主机共享的, 文件自带 seliunx 限制, 因此无法访问:

```shell
the host：
[root@centos-minion share]# id -z
unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023

[root@centos-minion share]# ls -ldz /home/share
drwxr-xr-x. root root unconfined_u:object_r:home_root_t:s0 /home/share

the container：
[root@4ccce73bed9d share]# id -z
id: --context (-z) works only on an selinux-enabled kernel

[root@4ccce73bed9d share]# ls -ldz /home/share
drwxr-xr-x. root root unconfined_u:object_r:home_root_t:s0 /home/share
```

- 取消 selinux 的方法:
    1. 永久方法: 修改 `/etc/sysconfig/selinux` 文件, `selinux=permissive|enforcing|disabled`, 需重启生效
    2. 临时方法: 设置系统参数 `setenforce 0|1`. 0 - permissive 模式; 1 - enforcing 模式
- 因此, 要实现容器内的文件安全, 限制访问权限, 可以使用 selinux

#### 2016-09-02

###### crontab

- shell, `crontab` 命令的使用如下:

```python
# 五个时间点, 从左到右依次是: 分, 小时, 日, 月, 周
# 五个域用空格分隔, 域内可用`,`分隔, 指定多个时间点

# *     *   *   *    *  command to be executed
# -     -    -    -    -
# |     |     |     |     |
# |     |     |     |     +----- day of week (0 - 6) (sunday=0)
# |     |     |     +------- month (1 - 12)
# |     |     +--------- day of month (1 - 31)
# |     +----------- hour (0 - 23)
# +------------- min (0 - 59)
```

- crontab 命令格式: `crontab [-u user] file` 或 `crontab [-u user] [ -e | -l | -r ]`
    - -u user：用来设定某个用户的crontab服务；
    file：file是命令文件的名字,表示将file做为crontab的任务列表文件并载入crontab。如果在命令行中没有指定这个文件，crontab命令将接受标准输入（键盘）上键入的命令，并将它们载入crontab。
    - -e(dit)：编辑某个用户的crontab文件内容。如果不指定用户，则表示编辑当前用户的crontab文件。
    - -l(ist)：显示某个用户的crontab文件内容，如果不指定用户，则表示显示当前用户的crontab文件内容。
    - -r(emove)：从/var/spool/cron目录中删除某个用户的crontab文件，如果不指定用户，则默认删除当前用户的crontab文件。
    - -i(nteractive)：在删除用户的crontab文件时给确认提示
- `crontab -e` 将在 `/tmp` 目录下创建临时文件并打开, 这样做是为了确保编写的 crontab 命令没有错误 (完整性检查), 起保护作用. 若直接打开真正的 crontab 文件进行编辑, 在编写 crontab 文件出错的时候, 会有问题.
    - 真正的 crontab 保存在 `/var/spool/cron/crontabs` 目录下
- 手动执行某个任务时，是在当前shell环境下进行的，程序能找到环境变量, 而系统自动执行任务调度时，是不会加载任何环境变量的，因此，就需要在crontab文件中指定任务运行所需的所有环境变量. 要注意以下几点:
    - 脚本中涉及文件路径时写全局路径
    - 脚本执行要用到 java 或其他环境变量时, 通过 source 命令引入环境变量:  `source /etc/profile`
    - 当手动执行脚本ok，但是crontab死活不执行时,很可能是环境变量惹的祸，可尝试在crontab中直接引入环境变量解决问
- 系统级任务调度主要完成系统的一些维护操作，用户级任务调度主要完成用户自定义的一些任务，可以将用户级任务调度放到系统级任务调度来完成（不建议这么做），但是`反过来却不行` ，root用户的任务调度操作可以通过”crontab –u root –e”来设置，也可以将调度任务直接写入 `/etc/crontab` 文件
- `crontab -r` - 将从 crontab 目录 (/var/spool/cron) 中删除用户的 crontab 文件, 用户所有的 crontab
- 在 crontab 中, `%` 表示换行的意思

---

- shell, `sed` is a `stream editor`. a stream editor is used to perform `basic text transformations on an input stream` (a file or input from a pipeline).  while in some ways similar to an editor which permits scripted edits (such as ed), sed works by making only one pass over the input(s), and is consequently more efficient. but it is sed's ability to `filter text in a pipeline` which particularly distinguishes it from other types of editors.
- shell, 九九乘法表! `seq 9 | sed 'h;g' | awk -v rs='' '{for(i=1;i<=nf;i++)printf("%dx%d=%d%s", i, nr, i*nr, i==nr?"\n":"\t")}'`
- `vi` 的替换应该是借鉴了 `sed`, 用 `s/to_be_replaced/replacing_character/g` 表示全局替换
- `-i` 是 `--in-place` 的缩写, 将直接对文本进行修改. 若不适用 `-i`, 会将修改后的副本输出到标准输出, 而不修改文件本身

---

#### 2016-09-04

- python2.7, `print repr(s)` 输出原生字符串
- python2.7, 在线编程网站的多行读入写法:

```python
import sys

for line in sys.stdin:
    pass
```

- python, `str.strip()` remove leading & tailing `whitespace characters`
- code, 三角形数(1, 3, 4, 10, 15, 21, ... 这样的数列), 公式 `n * (n + 1) / 2`
- python2.7, `print` 是一条语句, `print exp1,` 在表达式后加 `,` 就取消了换行, 但多了空格
- python3.x, `print` 函数带 `end`参数, 可用于指定结束字符, 默认是 `\n`. 另有 `sep` 参数, 用于指定分隔符, 默认时空格. `print` 函数可在一次打印中打印不同类型的变量
- python, `sys.stdout.write()` 对输出到标准输出的更灵活的控制
- `pyenv virtualenv 3.3.0 env`    #创建一个 python 版本为 3.3.0 的环境, 环境叫做 env
- `pyenv activate env_name`       #激活 env 这个环境, 此时 python 版本自动变为 3.3.0, 且是独立环境
- `pyenv deactivate`              #离开已经激活的环境
- shell 配置文件:
    1. `/etc/profile`
    2. `$shell/.bashrc`
    3. `$shell/.profile`

---

###### ps

- ps 命令列出的是当前进程的快照，就是执行 ps 命令的那个时刻的进程，如果想要动态的显示进程信息，可以使用`top`命令。
- linux 上进程有 5 种状态:
    1. 运行 `r` (正在运行或在运行队列中等待)
    2. 中断 `s` (休眠中, 受阻, 在等待某个条件的形成或接受到信号)
    3. 不可中断 `d` (收到信号不唤醒和不可运行, 进程必须等待直到有中断发生)
    4. 僵死 `z` (进程已终止, 但进程描述符存在, 直到父进程调用wait4(系统调用后释放)
    5. 停止 `t` (进程收到sigstop, sigstp, sigtin, sigtou信号后停止运行运行))
- 常用参数:
    - a 显示所有进程
    - -a 显示同一终端下的所有程序
    - -a 显示所有进程
    - c 显示进程的真实名称
    - -n 反向选择
    - -e 等于“-a”
    - e 显示环境变量
    - f 显示程序间的关系
    - -h 显示树状结构
    - r 显示当前终端的进程
    - t 显示当前终端的所有程序
    - u 指定用户的所有进程
    - -au 显示较详细的资讯
    - -aux 显示所有包含其他使用者的行程
    - -c<命令> 列出指定命令的状况
    - --width<字符数> 每页显示的字符数
    - lines<行数> 每页显示的行数
    - --help 显示帮助信息
    - --version 显示版本显示
- 输出列含义:
    - f 代表这个程序的旗标 (flag)， 4 代表使用者为 super user
    - s 代表这个程序的状态 (stat)，关于各 stat 的意义将在内文介绍
    - uid 程序被该 uid 所拥有
    - pid 进程的id
    - ppid 则是其上级父程序的id
    - c cpu 使用的资源百分比
    - pri 这个是 priority (优先执行序) 的缩写，详细后面介绍
    - ni 这个是 nice 值，在下一小节我们会持续介绍
    - addr 这个是 kernel function，指出该程序在内存的那个部分。如果是个 running的程序，一般就是 “-“
    - sz 使用掉的内存大小
    - wchan 目前这个程序是否正在运作当中，若为 - 表示正在运作
    - tty 登入者的终端机位置
    - time 使用掉的 cpu 时间。
    - cmd 所下达的指令为何

```shell
# to list every process on the system:
ps aux

# to list a process tree
ps axjf

# to list every process owned by foouser:
ps -aufoouser

# to list every process with a user-defined format:
ps -eo pid,user,command
```
---

- `-u user` - `-u` 通常用于指定用户

#### 2016-09-05

```python
from math import factorial as f
def ncr(n,r):
    return f(n) / f(r) / f(n-r)
```

- 排列公式: `nam = n! / (n - m)!`
- 组合公式: `ncm = n! / m! / (n - m)!`

```python
from math import factorial as f

def ncr(n, r):
    return f(n) / f(r) / f(n - r)

def nar(n, r):
    return f(n) / f(n - r)
```

- python 组合: [itertools.combinations](https://docs.python.org/3/library/itertools.html#itertools.combinations):

```python
>>> import itertools
>>> itertools.combinations('abcd',2)
<itertools.combinations object at 0x01348f30>
>>> list(itertools.combinations('abcd',2))
[('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd'), ('c', 'd')]
>>> [''.join(x) for x in itertools.combinations('abcd',2)]
['ab', 'ac', 'ad', 'bc', 'bd', 'cd']
```

---

- [关于索引](http://blog.csdn.net/pang040328/article/details/4164874). 以下是一些重要的:
    - 创建索引可以大大提高系统的性能
        - 通过创建唯一性索引，可以保证数据库表中每一行数据的唯一性
        - 加快数据的检索速度
        - 加速表和表之间的连接
    - 索引的代价:
        - 创建索引和`维护索引`要耗费时间，这种时间随着数据量的增加而增加
        - 索引需要占物理空间
        - 当对表中的数据进行增加、删除和修改的时候，索引也要`动态的维护`，这样就降低了数据的维护速度。
    - 一般应该建立索引的列特征:
        - 在经常需要搜索的列上，可以加快搜索的速度；
        - 在作为主键的列上，强制该列的唯一性和组织表中数据的排列结构；
        - 在经常用在连接的列上，这些列主要是一些外键，可以加快连接的速度;
        - 在经常需要根据范围进行搜索的列上创建索引，因为索引已经排序，其指定的范围是连续的；
        - 在经常需要排序的列上创 建索引，因为索引已经排序，这样查询可以利用索引的排序，加快排序查询时间；
        - 在经常使用在where子句中的列上面创建索引，加快条件的判断速度。
    - 索引的特征:
        - 唯一性索引: 唯一性索引保证在索引列中的全部数据是唯一的，不会包含冗余数据
        - 复合索引就是一个索引创建在两个列或者多个列上。在搜索时，当两个或者多个列作为一个关键值时，最好在这些列上创建复合索引

---

- 子网掩码的作用就是用来区分网络上主机是否在同一网段内, 不能单独存在, 必须结合 ip 地址一起使用。子网掩码只有一个作用，就是将某个 ip 地址划分成网络地址和主机地址两部分。是一种 `ip 网络地址复用方式`
- 网间网规模的迅速扩展对ip地址模式的威胁:
    - 巨大的网络地址管理开销
    - 网关寻径急剧膨胀, 寻径表的膨胀不仅会降低网关寻径效率, 更重要的是将增加内外部路径刷新时的开销，从而加重网络负担。
- 在实际应用中通常各网点采用连续方式的子网掩码 (不连续的子网掩码给分配主机地址和理解寻径表都带来一定困难)
- 子网划分的步骤:
    1. 将子网数目转为 $2^m$ 形式, 如果恰好是 2  的指数, 取多一位
    2. 将第 1 步确定的 m, 按高序占用主机地址 m 位, 转为十进制. 若 c 类子网, m = 3, 则 `11100000`, 最终的子网掩码是 `255.255.255.224`
- 利用主机数划分子网:
    1. 将子网中需要容纳的主机数转为二进制
    2. 如果主机数小于或等于 254(`0`, 和 `255` 是保留 ip 地址), 则取该主机数的二进制位数 n
    3. 将 `255.255.255.255` 的掩码, 从低位开始, 将低 n 位置为 0

---

###### coolshell 上的 sed 简明教程

- `sed` 是流编辑器, 用程序的方式编辑文本, 其基本上是`正则模式匹配`, (`regex`)
- `/^` 匹配行首, 因此 `sed 's/^/#/g' pets.txt`, 可以在每行首添加 `#`. `/$` 匹配行尾
- `sed` 使用反斜杆转义, 但是没办法用 `\'`, 在双引号内, 用 `\"` 转义可以
- 不带任何参数的 `sed` 不会对文件本身进行修改, 可通过 `重定向` 写回文件, 或者 `-i` (--in-place)
- 再谈 regex
    - `^` 表示一行的开头。如：/^#/ 以#开头的匹配。
    - `$` 表示一行的结尾。如：/}$/ 以}结尾的匹配。
    - `\<` 表示词首。 如 \\<abc 表示以 abc 为首的詞。
    - `\>` 表示词尾。 如 abc\\> 表示以 abc 結尾的詞。
    - `.` 表示任何单个字符。
    - `*` 表示某个字符出现了0次或多次。
    - `[ ]` 字符集合。 如：[abc]表示匹配a或b或c，还有[a-za-z]表示匹配所有的26个字符。如果其中有^表示反，如[^a]表示非a的字符
- `s 命令` 替换:
    - `sed "3s/my/your/g" pets.txt` - 指定替换第 3 行的内容, 文件的行号从 1 开始
    - `sed "3,6s/my/your/g" pets.txt` - 替换第 3 到 6 行文本
    - `sed 's/s/s/1' my.txt` - 替换每行的第一个 s
    - `sed 's/s/s/3g' my.txt` - 替换第一行的第 3 个 以后的所有 s
    - 多匹配模式: `sed '1,3s/my/your/g; 3,$s/this/that/g' my.txt`, 替换 1 到 3 行的 my 为 your, 替换第 3 行以后的所有 this 为 that
    - 上面的多匹配等价于 `sed -e '1,3s/my/your/g' -e '3,$s/this/that/g' my.txt`, 参数解释: `-e script, --expression=script`
    - 使用 `&` 当作被匹配的变量, 比如 `sed 's/my/[&]/g' my.txt`, 此处 `&` 匹配 my
    - 使用圆括号匹配的示例：（圆括号括起来的正则表达式所匹配的字符串会可以当成变量来使用，sed中使用的是\1,\2…）:
    - `sed 's/this is my \([^,]*\),.*is \(.*\)/\1:\2/g' my.txt`
- `n 命令` - 把下一行的内容纳入当成缓冲区做匹配, 比如 `sed 'n;s/my/your/' pets.txt` 会将原文本的偶数行纳入奇数行匹配, 且只匹配替换一次
- `a 命令` - (append) `sed "$ a this is my monkey, my monkey's name is wukong" my.txt` - 在最后一行之后追加 (默认每行之后都会追加, 按行修改嘛~)
- `i 命令` - (insert) `sed "1 i this is my monkey, my monkey's name is wukong" my.txt` - 在第 1 行插入 (默认每行之前都会插入)
- `c 命令` - 替换匹配行 - `sed "2 c this is my monkey, my monkey's name is wukong" my.txt` - 替换第 2 行
- `d 命令` - 删除匹配行 - `sed '2,$d' my.txt` - 删除第 2 行到尾行的所有行
- `p 命令` - 打印命令, 可以看作 `grep` 式的命令 - `sed '2 p' my.txt` - 匹配第 2 行并打印, 这时会打印匹配的行 2 次, 其他行则打印一次
    - `-n` 参数, 解决以上问题, 只打印匹配的行
    - `/mode1/,/mode2/p` - 与 `2,$` 类似的用法
- `sed "/fish/a this is my monkey, my monkey's name is wukong" my.txt` - 匹配到 fish 之后就追加, 对 `i`, `c`, `d`, `p` 都同样适用
- sed 的四个基本点:
    - `-n 参数
    - 几乎所有的命令都是 `[address[,address]][!]{cmd}`, `!` 表示匹配成功后是否执行命令. `address` 可以是数字也可以是一个模式
        - `adddress` 可以使用相对位置, `sed '/dog/,+3s/^/# /g' pets.txt` - `+3` 表示向后 3 行
    - cmd 可以是多个, 可以用 `;` 分隔, 可以用大括号括起来作为嵌套命令
        - `sed '3,6 {/this/d}' pets.txt` - 对 3 到 6 行执行命令 `/this/d`
        - `sed '3,6 {/this/{/fish/d}}' pets.txt` - 对3行到第6行，匹配/this/成功后，再匹配/fish/，成功后执行d命令
        - `sed '1,${/this/d;s/^ *//g}' pets.txt` - 从第一行到最后一行，如果匹配到this，则删除之；如果前面有空格，则去除空格
    - `hold space`:
        - g： 将hold space中的内容拷贝到pattern space中，原来pattern space里的内容清除
        - g： 将hold space中的内容append到pattern space\n后
        - h： 将pattern space中的内容拷贝到hold space中，原来的hold space里的内容被清除
        - h： 将pattern space中的内容append到hold space\n后
        - x： 交换pattern space和hold space的内容

---

###### 二叉树的遍历

- 前、中、后是指`根结点的访问时机`，在左、右子树之前、中间、或之后。层序就是从根结点开始从上至下、从左到右地依次访问。

```python
# 递归方式实现前, 中, 后序遍历
def visittree_recursive(root, order):
  if root:
    if order == 'nlr': print(root.data)
    visittree_recursive(root.left, order)
    if order == 'lnr': print(root.data)
    visittree_recursive(root.right, order)
    if order == 'lrn': print(root.data)
```

---

- ipv6 二进制下为 `128` 位长度, 16 位为一组, 用 `:` 分隔, 分为 8 组, 每组以 4 位十六进制方式表示. 举例: `2001:0db8:85a3:08d3:1319:8a2e:0370:7344`
- python, 排序, str 默认按字典序排序, 数值型默认按数值大小排序, 升序

#### 2016-09-12

> python 的索引为什么从 0 开始? (为了与半开区间搭配~)
一个原因是`切片语法(slice notation)`
使用 0-based 的索引方式, 半开区间切片和缺省匹配区间, 可以使取前 n 位和从第 i 位开始取 n 位的表示变得非常优雅: `a[: n]` 和 `a[i: i+n]`
使用 1-based 的索引方式, "取前 n 个元素", 要么使用闭合区间切片语法, 要么在切片语法中使用起始位置和切片长度作为参数. 半开区间切片语法加上 1-based 索引方式, 会变得不够优雅; 而闭区间切片语法, 为了从第 i 位索引开始取 n 个元素, 需要将表达式写成 `a[i: i+n-1]`, 也不优雅
使用半开区间与 `index: length` 的方式, 会使得切片的语法很优雅. 完整的序列, 就可以用 i, j 两个位置切成三部分: `a[:i]`, `a[i: j]`, `a[j:]`

> c 语言的索引为什么从 0 开始?
数组名实际是一个指针, 表示内存的起始位置. 因此表达式 `a[n]` 表示距离起始元素 n 个元素的内存位置. 可以说, 索引就是被当作`偏移量`来用的. 数组的第一个元素, 就包含在数组名表示那块内存中, 因此偏移量是 0, 用 `a[0]` 表示.
另外, 根据 dijkstra 的说法: this is a problem on how to denote a subsequence of natural numbers (自然数). 1 到 10 的自然数序列, 有四种表示方式:
    1. 0 < i < 11
    2. 1 <= i < 11
    3. 0 < i <= 10
    4. 1 <= i <= 10
dijkstra 表示, 真正合理的表示方式应该能适应以下两种情况:
    1. 子序列包含最小的自然数 0
    2. 子序列是空的
因此, 可以首先排除 1 和 3, 因为它们将使用到 `-1<i` 的形式, 而 -1 不是自然数 (dijkstra 说这太丑了). 其次, 可以排除 4, 因为需要表示一个空集时, 4 需要使用 `0 <= i <= -1` 来表示, 会显得混乱. 此外, 2 的范围一减, 就得到了序列的长度, 这算是一项加分吧.

###### python 排序数据的多种方法(部分学习自编程派 codingpy)

- `list.sort()` - 对 list 进行排序, 会改变 list 本身
- `sorted()` - 对一个 iterable 进行排序, 返回一个新的有序 `list`. 返回排序后的副本, 不会对原 iterable 作修改
- 当不需要保留原始列表时, `list.sort()` 方式会略高效一些. 但是 `sorted()` 更通用, 它支持任意的 iterable, 而 `list.sort` 是 method of list
- `list.sort()` 和 `sorted()` 都带 `key` 关键字参数, `用于指定比较之前, 调用何种函数对元素进行处理`. `key` 参数的值应该是一个函数, 该函数接收一个参数, 并返回一个 key 为排序时所用. `可以用 lambda 的匿名函数作为 key 的参数`
- python 提供了一些简单快速地访问属性的函数, 如 `operator` 模块的 `itemgetter()`、`attrgetter()` 和 `methodcaller()`, 这些方法还允许多级排序, 按序指定排序的列即可.
- `reverse` 关键字参数用于指定是否反序.
- `list.sort()` 和 `sorted()` 的排序是`稳定`的, 这就允许通过一系列排序进行复杂排序
- python 使用的 `timsort` 算法由于可以有效利用数据集中已有的顺序, 因而可以高效地进行多级排序
- decorate-sort-undecorate(旧方法, 已经被 key 的方式取代):
    1. 初始的列表进行转换, 获得用于排序的新值
    2. 将转换为新值的列表进行排序
    3. 还原数据并得到一个排序后仅包含原始值的列表

```python
>> decorated = [(student.grade, i, student) for i, student in enumerate(student_objects)]
>> decorated.sort()
>>> [student for grade, i, student in decorated]  # undecorate
```

- python 的 tuple 按字典序比较, 且先比较第一项, 再比较第二项, 依此类推
- 在排序过程中, 包含原始下标的好处:
    - 排序是稳定的, 如果有两项有相同的 key，排序后的列表会保留他们的顺序
    - 原始项不需要是可比较的
- python2.x 提供了 cmp 关键字参数, 接收一个函数, 函数接收 2 个参数, 返回比较的结果, 作为排序的依据
- python3.x 不再提供 cmp, 可能需要将用户提供的排序函数转换为 key 函数, 可使用下述的包装器:

```python
def cmp_to_key(mycmp):
    'convert a cmp= function into a key= function'
    class k:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return k

sorted([5, 2, 4, 1, 3], key=cmp_to_key(reverse_numeric))
```

- python3.2 `functools.cmp_to_key()` 函数已经添加到标准库的 functools 模块中
- 针对时区的相关排序, 使用 `locale.strxfrm()` 作为 key 函数, 或使用 `locale.strcoll()` 作为比较函数
- 在两个对象进行比较时，sort 使用的是 lt() 方法。所以，只需要为类添加 lt() 方法，就可以为类加入排序顺序

```python
>>> student.__lt__ = lambda self, other: self.age < other.age
>>> sorted(student_objects)
[('dave', 'b', 10), ('jane', 'b', 12), ('john', 'a', 15)]
```

- key 函数不需要直接依赖于排序的对象, 可以访问外部资源. 例如:

```python
>>> students = ['dave', 'john', 'jane']
>>> newgrades = {'john': 'f', 'jane':'a', 'dave': 'c'}
>>> sorted(students, key=newgrades.__getitem__)
['jane', 'dave', 'john']
```

#### 2016-09-13

###### python 爬虫经验

- 通过代理访问, 可以从 header 的 x-forwarded-for 字段查看真实 ip. (真的吗?)
- 多线程并发抓取
- 增加 gzip/deflate 支持, 通过压缩网页, 减小传输时间. python 2.x 和 3.x 默认都不提供压缩, 以下是 python 2.x 的做法, python 3.x 类似:

```python
import urllib2
from gzip import gzipfile
from stringio import stringio

class contentencodingprocessor(urllib2.basehandler):
  """a handler to add gzip capabilities to urllib2 requests """

  # add headers to requests
  def http_request(self, req):
    req.add_header("accept-encoding", "gzip, deflate")
      return req

  # decode
  def http_response(self, req, resp):
    old_resp = resp
    # gzip
    if resp.headers.get("content-encoding") == "gzip":
        gz = gzipfile(
                    fileobj=stringio(resp.read()),
                    mode="r"
                  )
        resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
        resp.msg = old_resp.msg
    # deflate
    if resp.headers.get("content-encoding") == "deflate":
        gz = stringio( deflate(resp.read()))
        resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
        # class to add info() and
        resp.msg = old_resp.msg
        return resp
        # deflate support

import zlib
def deflate(data):

   # zlib only provides the zlib compress format, not the deflate format;
  try:
# so on top of all there's this workaround:
    return zlib.decompress(data, -zlib.max_wbits)
  except zlib.error:
    return zlib.decompress(data)

encoding_support = contentencodingprocessor
opener = urllib2.build_opener( encoding_support, urllib2.httphandler )
#直接用opener打开网页，如果服务器支持gzip/defalte则自动解压缩

content = opener.open(url).read()
```

- 简单的爬虫 - requests
- 讲究效率的 - scrapy
- 页面复杂的 - mechanize + bs4

#### 2016-09-17

- python 设置布尔变量的一种方式: `is_busy = (amount > 0)`

> 你不知道的 c♯
真正的名字是"c♯", 而不是"c#". 前一个是乐谱里常用的代表升半音的符号, 后一个是表示数字的符号
"c♯"这一名字的由来并不只是大多数人认识到的是对"c++++"的简写，读作 sharp 表示一种编程利器的含义。sharp 在音乐中原本就有提升的意思。恰巧的是 sharp 的符号 ♯ 拆开又可以看做是++++的简写。于是就有了c sharp 的井号标记和 sharp 读音的由来，取其对 c 的提升之意。

###### python 部署方法 (源自伯乐在线)

- 通过 `pip` 是从 python 包索引 (pypi, python package index) 下载和安装. the python package index is a repository of software for the python programming language.
- pip 没有提供“部署回滚”策略. pip unistall 并不是每次都能正常工作，也没有办法“回滚”到上一个状态
- pip 安装依赖会让部署变得缓慢, 尤其是安装一个由 c 编写的模块,经常需要从源码进行编译. `部署应用应该是一个以秒计算的快速而轻量的过程`
- 在每台主机上分别构建代码会有一致性问题
- `pip install` 和 `git pull` 通常依赖于外部服务器, 可靠性不太强
- python 部署应当这样:
    - 能够构建代码成单一, 有版本控制的工件
    - 受版本控制的工件可以进行单元测试和系统测试
    - 一种简单的机制可以从远程主机完全地安装或卸载工件
- 更快的迁移代码并不应该重新执行整个基础架构自动化和编排层. 因此, 利用 docker 来部署也存在问题:
    - 内核版本可能不能完美支持 docker
    - 在专用网络里分发 docker 镜像要有一个独立服务, 这时需要对服务进行配置, 测试和维护
    - 将 ansible 自动化安装转换为 dockerfile 的过程是痛苦的, 需要对日志配置, 用户权限和密钥管理进行大量繁琐的编辑
- `pex` 是 twitter 开发的智能工具, 允许 python 代码以可执行压缩文件进行传送
- 使用 docker 会增加运行时的复杂度, pex 会增加构建时的复杂度
- 包 (package) 是原始的容器. `dh-virtualenv`, 用于构建内含 virtualenv 的 debian 包. 这个包将包含 virtualenv 和罗列在 requirement.txt 文件里的所有依赖
- 利用持续集成服务器 (jenkins) 运行 dh-virtualenv 来构建包, 用 python 的 wheel 缓存来避免对依赖重新构建. 然后对其进行大量的单元测试和系统测试

#### 2016-09-18

- 获取当前时间的时间戳: `import time; time.time()`
- 获得结构化的时间对象: `time.localtime([timestamp])` - convert seconds since the epoch to a time tuple expressing local time. when 'seconds' is not passed in, convert the current time instead.
- `time.strftime('%y-%m-%d',time.localtime(time.time()))` - 也许是你想要的

#### 2016-09-20

- numpy, `np.any()` 类似于 python 内置的 `any()` 函数, 当数组中有一个元素为 true, 返回 `true`. 同理, `np.all()` 在数组中所有元素都为 true 的情况下, 才返回 `true`
- numpy, 数组的逻辑操作符不同于 python 的逻辑操作符, 非用 `-`, 与用 `&`, 或用 `|`
- 服务器端针对用户的定时任务需要定到用户所在时区的时。
- `pd.panel.drop()` 指定 `axis` 参数, 可丢弃某一维度的 xx (好吧, 我不知道怎么称呼)
- python, 双向字典: `bidict` (第三方库, bidict), 简单用法:

```python
>>> from bidict import bidict
>>> d=bidict({'a':'b'})
>>> d['a']
'b'
>>> d[:'b']  # 修改该切片语法
'a'
>>> ~d  #反转字典
bidict({'b': 'a'})
>>> dict(d)  # 转为普通字典
{'a': 'b'}
>>> d['c']='c'  # 添加元素，普通字典的方法都可以用
>>> d
bidict({'a': 'b', 'c': 'c'})
```

- 可以使用 namedbidict 类给双向字典取两个两个别名, 对外提供正向和逆向的 2 个子字典, 实际仍是一个双向字典

```python
# namedbidict(typename, keyname, valname, base_type=<class 'bidict._bidict.bidict'>)
>>> htmlentities = namedbidict('htmlentities', 'names', 'codepoints')
>>> entities = htmlentities({'lt': 60, 'gt': 62, 'amp': 38}) # etc
>>> entities.names['lt']
60
>>> entities.codepoints[38]
'amp'
```

###### python 时区问题

- datetime 模块定义了如下类:
    - datetime.date - 理想化的日期对象
    - datetime.time - 理想化的时间对象，不考虑闰秒（即认为一天总是24*60*60秒），有hour, minute, second, microsecond, tzinfo五个属性
    - datetime.datetime - datetime.date和datetime.time的组合
    - datetime.timedelta - 后面我们会用到的类，表示两个datetime.date, datetime.time或者datetime.datetime之间的差。
    - datetime.tzinfo - 时区信息
- time 模块提供了各种时间操作转换的方法
- calendar 模块提供日历相关的方法
- pyt 模块, 使用 [olson tz database](https://en.wikipedia.org/wiki/list_of_tz_database_time_zones) 解决了跨平台的时区计算一致性问题, 解决了夏令时带来的计算问题
- `datetime.fromtimestamp()`, 从时间戳创建 datetime 对象
- 未完待续

#### 2016-09-26

- python, 浅拷贝, 它复制了对象，但对于对象中的元素，依然使用原始的引用. (新瓶旧酒)
- python, 赋值, 进行对象引用 (内存地址) 的传递 (旧瓶旧酒)
- python, 深拷贝, 复制了容器对象, 以及其中的所有元素 (新瓶新酒)
- 对于非容器类型 (如数字、字符串、和其他'原子'类型的对象) 没有被拷贝一说
- 如果元祖变量只包含原子类型对象, 则不能深拷贝
- pandas, `df.isnull` 用于判断 dataframe 的 cell, 是否缺失值. 而不能用于判断 dataframe 是否为空!
- pnadas, `df.empty` 才是用于判断 dataframe 是否为空的方法!
- pandas, `cannot cast datetimeindex to dtype <u0`, 错误可能是版本引起的, 更新可解决
- numpy, dtype (data type objects) 描述了数组元素对应的的字节在固定大小的内存块中如何解释. 其包含几个部分:
    1. 数据类型 (整型, 浮点型, python 对象等)
    2. 数据大小 (描述数据占多少字节的整型)
    3. 数据的字节顺序 (小端还是大端)
    4. 如果数据类型是结构化的, 即是其他数据类型的聚合:
        1. 结构化数据的字段名, 即通过此可访问数据
        2. 每个字段的数据类型
        3. 每个字段占内存块数
    5. 如果数据类型是子数组, 它的形状 (shape) 和数据类型
- 常见 dtype 数据类型:
    - 'b' boolean
    - 'i' (signed) integer
    - 'u' unsigned integer
    - 'f' floating-point
    - 'c' complex-floating point
    - 'm' timedelta
    - 'm' datetime
    - 'o' (python) objects
    - 's', 'a'    (byte-)string
    - 'u' unicode
    - 'v' raw data (void)
- numpy, 数组是同质的 (homogeneous)

#### 2016-09-27

- python, 使用豆瓣的 pypi 源, 用 `-i` 指定: `sudo pip3 install -i https://pypi.doubanio.com/simple/ package`
- 添加豆瓣源为默认源的几种方法:
    1. alias
    2. 修改 `~/.config/pip/pip.conf`, 添加 `index-url = http://pypi.douban.com/simple`

#### 2016-09-28

- shell, `grep` normally the exit status is 0 if a line is selected, 1 if no lines were selected, and 2 if an error occurred
- python, subprocess 使用 pipe 的正确姿势:

```python
docker_ps = popen("docker ps -a".split(), stdout=pipe)
query_result = check_output(('grep', user_id), stdin=docker_ps.stdout)
# query_result 实际上是 docker_ps 的子进程, 因此, 父进程等待子进程终止
docker_ps.wait()
```

> if `shell` is `true`, the specified command will be executed through the shell. this can be useful if you are using python primarily for the enhanced control flow it offers over most system shells and still want convenient access to other shell features such as shell `pipes`, `filename wildcards`, `environment variable expansion`, and expansion of `~` to a user’s home directory. however, note that python itself offers implementations of many shell-like features (in particular, glob, fnmatch, os.walk(), os.path.expandvars(), os.path.expanduser(), and shutil).

- python, shlex -  a lexical analyzer class for simple shell-like syntaxes.
    - `shlex.split(cmd_str)` - 将命令更科学地进行切分
    - kenneth 的 envoy 就用到了 shelx 来科学地解析 shell cmd

#### 2016-10-07

- xterm, 对应的文件是: `.xresources`, 命令: `.xrdb -merge .xresources`

###### kill vs. terminate:

> sigterm 信号是可中途阻止的 (intercepted), 程序收到终止信号之后, 将启动一个关闭进程来终止自身, 以 clean exit.
sigkill 是暴力不可终止的, 收到该信号的程序将立即被终止
当关闭或重启计算机时, 通常会先发一个 sigterm, 优雅地退出进程 (如果进程支持的话), 几秒钟后, 向仍在运行的程序发送 sigkill, 强制退出进程.

- python, `__enter__` 和 `__exit__` (magic functions), 用于实现 `with` 语句的关键

#### 2016-10-08

- after you have imported a module in python, it's always good to see what functions ,classes and methods that the module provides. 导入模块之后, 使用 `dir(module)` 查看其提供了哪些函数, 类与方法是个好习惯

#### 2016-10-14

- 2016-10-14

###### tuple/list of 2 elements vs. dict

- `(x, y)` - 其中 x, y 不一定意味着"此二者有关联"
- `{"x": "y"}` - 意味着, x 与 y 之间有内在的联系
- tuple 易于比较, 先比较首位元素, 再次位, 依此类推 

###### python 代码中直接插入断点

```python
import pdb
pdb.set_trace()

###### ubuntu 解压缩工具大全

`sudo apt-get install p7zip-rar p7zip-full unace unrar zip unzip sharutils rar uudeview mpack arj cabextract file-roller`

###### linux 开机自动运行脚本 (未试)

1. 在 /etc/init 目录下写脚本
2. 在 /etc/rc.local 文件的 exit 0 语句前编写执行语句 (python xxxx)

###### 你不知道的 print

- `print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=false)`, 因为 `file` 默认值是 `sys.stdout`, 所以将打印到屏幕, 若修改为打开的 file obj, 亲测可写入

###### 取得当前文件同目录下某个文件的绝对路径 & 目录操作

```python
def from_this_dir(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
```

获取当前目录: `os.getcwd()`
修改工作目录: `os.chdir()`

###### 简单粗暴的设置缩进 (可用于 code_gen)

`pad = " " * indent`

###### dict.items() 方法返回的其实是 `(key, value)`

```python
in [14]: a = {"kissg": "echo", "echo": "kissg"}

in [15]: a.items()
out[15]: [('kissg', 'echo'), ('echo', 'kissg')]
```


#### 2016-10-21

###### 为服务器设置 ssh 登录

0. 在本机生成公密钥: `ssh-keygen -t rsa -b 4096 -c "enginechen07@gmail.com"`
    - `-t` 指定算法
    - `-b` 指定密钥对的长度
    - `-c` comments
1. 将本机的公钥添加到服务器 `$home/.ssh/authorized_keys` 文件
2. 设置 `$home/.ssh/authorized_keys` 权限为 `600`
3. 设置 `$home/.ssh` 的权限为 `700`

#### 2016-10-24

- `xlrd`: 自动根据 cell 值判断其 type, 与 excel 单元格属性无关.

#### 2016-10-25

###### curl (updating)

- -h - "headers"
- -x - (http) request method
- -d, --data - (http) sends the specified data in a post request to the http server
- -k, --insecure - (ssl)  this  option explicitly allows curl to perform "insecure" ssl connections and transfers.

###### ubuntu 添加删除 ppa

- 添加 ppa: `sudo apt-add-repository ppa:andrei-pozolotin/maven3`
- 移除 ppa 1: `sudo add-apt-repository --remove ppa:whatever/ppa`
- 移除 ppa 2: `sudo apt-get install ppa-purge && sudo ppa-purge ppa_name  # ppa_name 带 `ppa:``

###### mime 管窥

- mime (multipurpose internet mail extensions, 多用途互联网邮件扩展).通过标准化电子邮件报文的头部的附加域 (fields) 而实现的; 这些头部的附加域, 描述新的报文类型的内容和组织形式.
- 版本: `mime-version: 1.0` (目前是 1.0)
- 内容类型: `content-type: [type]/[subtype]; parameter`

###### others

- [ubuntu install mysql](http://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/)
- [ubuntu install docker](https://docs.docker.com/engine/installation/linux/ubuntulinux/)
- 当前用户重新登录: `su yourself` (temp)
- shell 重新登录: `exec zsh`
- gnome 自带 pdfviewer: evince, 命令也是 `evince pdf_file`
- linux, 查看端口占用情况: `netstat –apn` or `netstat –apn | portno`
- linux 安装 maven
    1. 下载二进制包并解压到指定目录
    2. 设置环境变量:
        - `export m2_home=/home/kissg/tools/apache-maven-3.3.9`
        - `export path=$m2_home/bin:$path`

###### shadowsokcs server 配置

(以 centos 6 为例)

1. 安装工具
    - yum install epel-release
    - yum update
    - yum install python-setuptools m2crypto supervisor
    - easy_install pip
    - pip install shadowsocks
2. `vi /etc/shadowsocks.json`

```json
{
  "server":"0.0.0.0",
  "server_port":8388,
  "local_port":1080,
  "password":"yourpassword",
  "timeout":600,
  "method":"aes-256-cfb"
}
```

3. `vi /etc/supervisord.conf`

```shell
[program:shadowsocks]
command=ssserver -c /etc/shadowsocks.json -d start
autostart=true
autorestart=true
user=root
log_stderr=true
logfile=/var/log/shadowsocks.log
```

4. `vi /etc/rc.local`
    - `service supervisord start`

5. `reboot`

#### 2016-10-27

###### python tips

- `\` 可以用来表示行的连续, 但最好不好用. python 能智能地识别 open bracket, 逗号分隔的列表, 回车
- `str` 是不可变的, 当你以为修改了一个字符串, 实际是新建了一个
- `for item in alist` - `alist` 是一个序列, `dict.items()` 其实是返回了 tuple.

#### 2016-11-01

- git, 先 commit 再 pull, 避免多余的提交.

#### 2016-11-04

- python, 奇葩组合：

```python
from operator import is_not
from functools import partial
filter(partial(is_not, none), l)
```

#### 2016-11-07

- python, `codecs` 模块的 `open`, 加强版的 `open`, 可以指定 `coding` 等等
- python, `tuple` is hashable，`list` is not hashable
- python，`{exp for statement}` 可以是字典推导式也可以是集合推导式, 使用请注意
- python, `vim` 执行当前编辑的 python 脚本：`:!python`, or 选中代码片段也可执行

#### 2016-11-08

- json, key 只能是字符串
    - 将以 tuple 为 key 的 dict 序列化为 json，可以将 tuple 转为 str 先。事实上，ultrajson 就是这么做的： `json.dumps({str(k): v for k, v in data.iteritems()})`
- python，`pickle.dump` 的 key 可以是任何对象。通常以 `.p` 文件保存 `pickle.dump()` 的结果
- python, popular json parsers: `ultrajson`, `json`, `simplejson`, `yajl`
- python, `frozenset` - 不可变的 `set`， 具有与 `set` 相同的接口，区别是不可变。

###### how to check if a directory exists and create it if necessary?

[stackoverflow](http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary/14364249#14364249)

```python
# python2.7
try: 
    os.makedirs(path)
except oserror:
    if not os.path.isdir(path):
        raise

# python 3.2+
os.makedirs(path, exist_ok=true)
```

#### 2016-11-09

- python, 路径相关的 `os.path` 函数：
    - `os.path.dirname()`
    - `os.path.split()`
    - `os.path.isdir()`
    - `os.path.isfile()`

- pandas, `to_*` 函数，当向 `dir/file` 写入时，若 `dir` 不存在，会报文件/路径不存在错。因此需先创建目录
- pandas, `df.sort_index()` 对索引进行排序，`['q1.3','q6.1','q1.2','q1.1',......]` ==> `['q1.1','q1.2','q1.3',.....'q6.1',......]`
- pandas，`pd.read_excel()` 将会把第一列读为索引，好违和啊- -
- pandas，`df.dropna()` - 默认（"any"）将在某行存在空值时，就丢弃该行。`how="all"`，在某行全为空值才丢弃行
- pandas.dataframe，`axis` 表示轴向，`0` - 行，`1` - 列。`level` 用于多层索引的层级

#### 2016-11-14

- 神奇的正则表达式，可匹配 `dd/mm/yyyy`, `dd.mm.yyyy`, `dd-mm-yyyy`, `mm` 可以是月份缩写

```python
^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:jan|mar|may|jul|aug|oct|dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:jan|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:jan|feb|mar|apr|may|jun|jul|aug|sep))|(?:1[0-2]|(?:oct|nov|dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$
```

- python, `dateutil` - powerful extensions to datetime， 可自动完成以上解析，而不必指定多种格式，但有时候需要人为地干预判断，否则将出错。如下所示的例子，需要人为干预 `day first` or `month first`

```python
# 11/12/2016 -> nov. 12, 2016
# 13/12/2016 -> dec. 13, 2016
```

#### 2016-11-15

- python 监控文件更新
    1. 查看文件修改时间 [stackoverflow 的回答](http://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python)
        1. `os.path.getmtime(file)` (os.path.getctime(file) - 获得修改时间）
        2. `os.stat(file)` - 返回 `(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)`
    2. 计算文件的校验值 [stackoverflow 的回答](http://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file/3431835#3431835)

###### python 虚拟环境

- `virtualenv` - 用于创建隔绝的 python 环境, 包括一个所有必要的可执行文件的目录
- 创建虚拟环境: `virtualenv [options] dst_dir`
- `-p python_exe` - 指定 python 解释器
- `source bin/activate` - 激活虚拟环境
- `deactivate` - 退出虚拟环境
- `pip freeze > requirements.txt` - `pip` 的命令, 将所有安装的包导出到 `requirements.txt`
- `pip install -r requirements.txt` - `-r` 选项, 指定从 `requirements.txt` 安装依赖包

#### 2016-11-16

- ubuntu, 启动系统设置: `unity-control-center`
- python, `python -m script` 可用于检查代码是否有语法错误
- linux，`nmcli` - network manager 命令行接口
    - `nmcli dev wifi list` - 列举可用 wifi
    - `nmcli dev wifi connect ssid password xxxx` - 连接到 wifi
- python，用 `os.path.join()` 函数来组装 path，字符串拼接容易出错
- `fnmatch.filter(names, pattern)` - same as [n for n in names if fnmatch(n, pattern)], but more efficiently.
- `os.path.normcase` - normalize case of pathname.  has no effect under posix
- `os.path.lexists(path)` - test whether a path exists.  returns true for broken symbolic links. l for link.
- `os.path.exists(path)` - test whether a path exists.  returns false for broken symbolic links

#### 2016-11-21

- `os.listdir` - `ls` in python, 包括 `.*`, 但不包括 `..` 和 `.`

#### 2016-11-22

- celery, `received unregistered task`, 一定是指派任务时有误。构造函数的 `include` 属性是模块的列表。
- celery，多任务，简单的做法就是 `include` 指定多个任务
- celerybeat，任务调度，可配置 `celerybeat_schedule`
- python 之 json 格式化：`python -m josn.tool jsonfile` [stackoverflow](http://stackoverflow.com/questions/352098/how-can-i-pretty-print-json/1920585#1920585)
- json, json 文本的 mime 媒体类型是 `application/json`， 默认以 utf-8 编码。[stackoverflow](http://stackoverflow.com/questions/477816/what-is-the-correct-json-content-type/477819#477819), [mime types](https://github.com/h5bp/server-configs-nginx/blob/master/mime.types)

#### 2016-11-24

- vim - `%` 跳转到匹配的另一端， 比如括号， if 与 endif， /\* 与 \*/ 等
- python `from __future__ import absolute_import` - 自定义模块名与第三方或标准库同名时， 解决冲突.

> bla

- scala, list
    - head, last - 返回头尾元素
    - tail, init - 返回除头尾元素以外的元素的列表
    - drop (dropright) - 移除到 n 指定的索引. selects all elements except first n ones.
    - dropwhile - 从 list 头开始, 删除满足条件的元素, 直到条件不成立
    - :: - 将一个元素追加到 list 头
    - ::: - 作为方法调用时, 将参数 list 加到调用者 list 之前:
    - span - 根据条件将 list 拆分成前后两部分. 等价于 (c takewhile c, c dropwhile p), 但更高效

```scala
scala> list(1) ::: list(2)
res18: list[int] = list(1, 2)

scala> list(1).:::(list(2))
res19: list[int] = list(2, 1)
```

- vim, `highlight matchparen xxx term=reverse cterm=bold ctermfg=13 gui=bold guifg=#b2b2a0 guibg=#2e2e2e` - 自定义匹配的风格

#### 2016-11-30

- scala for statement
    - `for (i <- collections) func` (用 `;` 分隔, 对多个集合进行多重循环遍历, n\*m\*..)
    - 带守卫的语法 `for (i <- collections conditions)`
    - `for yield`
- scala - `yield` 是推导式的一部分. scala 的 `for 推导式` 是组合了 `foreach`, `map`, `flatmap`, `filter` 或 `withfilter` 的语法糖, 实际上 `for 表达式` 会转译成依次调用以上方法.
    - `for(x <- c1; y <- c2; z <-c3) {...}` -> `c1.foreach(x => c2.foreach(y => c3.foreach(z => {...})))`
    - `for(x <- c1; y <- c2; z <- c3) yield {...}` -> `c1.flatmap(x => c2.flatmap(y => c3.map(z => {...})))`
    - `for(x <- c; if cond) yield {...}` -> `c.withfilter(x => cond).map(x => {...})`
    - `for (i <- n to m)` - [n, m]

#### 2016-12-01

> f5 or control + r = reload the current page
control + shift + r or control + f5 or shift + f5 = reload your current page, ignoring cached content

#### 2016-12-02

- `reverse proxy` - 反向代理, 是一种代理服务器, 根据客户端的请求, 从后端的服务器上获取资源, 再返回给客户端. 前向代理作为一个媒介将资源返回给相关联的客户端, 而反向代理是在服务器端作为代理使用. web 服务器通常都会使用反向代理, acting as shields (防护) for application frameworks with weaker http capabilities.
- in the broadest sense a gateway is a filter somewhere in your web stack which filters your api traffic in someway.
- implement an api gateway that is the single entry point for all clients. the api gateway handles requests in one of two ways. some requests are simply proxied/routed to the appropriate service. it handles other requests by fanning out to multiple services.
- typically the types of functions the gateway may provide may include:
    - `access control` (filtering traffic so only authenticated/authorized traffic gets through)
    - `rate limiting` (restricting how much traffic can be sent by each client of the api)
    - `analytics/metrics capture and logging` (tracking what's going on on the api)
    - `security filtering` (checking the content on incoming messages for attacks)
    - `redirection/traffic routing` (sending traffic to different endpoints in your own infrastructure depending on the sender or the request)
- an event-driven/reactive approach is best if it must scale to scale to handle high loads. on the jvm, nio-based libraries such as netty, spring reactor, etc. make sense.

#### 2016-12-05

- scala, `->`, 不是特殊语法, 返回元组的方法. `"a" -> 2` 只是 `"a".->(2)` 的语法糖
- actor is a synchronous object which processes all received messages successively. the multithreading model come out from the concept that everything that is outside an actor is asynchronous and processed in different threads. it is much better to use an actor as an object with a state, since there is no concurrency within an actor. all communication with an actor must be done by sending messages to it.
- if there is no state in an `actor`, then it is much better to use a simple `future` or something related which is focused on a stateless behavior.
- a web crawler is usually a part of a web search engine.
- scala, 格式化字符串, `s"$name balabala"`

#### 2016-12-06

- scala style guide
    - never use `isinstanceof` or `asinstanceof`
    - the standard is to indent using 2 spaces
    - use local values to simplify complex expressions
    - choose meaningful names for methods and values. no, `temp` is never a good name :-)
    - 避免不必要的计算密集型操作
    - don’t copy-paste code! you should factor out common parts into separate methods instead of copying code around.
    - 分号是不必需的, 避免写不必要的分号
    - avoid using `return`
    - avoid mutable local variable
    - Eliminate (消除) redundant (多余的) “If” Expressions
- Scala, CBV (call-by-value) vs. CBN (call-by-name):
    - CBV, 在执行函数/方法之前, 先计算出参数值, 再进入函数体执行. 优点是只计算一次.
    - CBN, 先进入函数体, 用到参数值时, 再计算. 优点是相应的参数没有被用到时, 不会计算参数值
    - test(2, 3), test(3 + 4, 8), test(7, 2 \*4), test(3 + 4, 2 \*4)
- Scala, `def and(x: Boolean, y: => Boolean) = if (x) y else false`  == x && y (其实还是有点差别)
- Scala, `def or(x: Boolean, y: => Boolean) = if (x) true else y`    == x || y
- DSL - Domain-specific language, in contrast to a general-purpose language (GPL)
- Microservice - It's usually responsible for processing only one type of data. They rarely use high level of abstraction over databases, networking, and other components. It all makes them easier to understand and easier to reuse in multiple projects.
- Akka - One of the great features of akka-http is response marshalling.

#### 2016-12-07

- CentOS, 添加用户, 并加入 sudo group:
    - useradd kissg
    - passwd kissg
    - yum install sudo && visudo
- 反向路由, 重定向会反映在 URL 上.

#### 2016-12-08

- Scala - 不同范畴的容器总是不相等的; 在同一范畴下的容器是相等的，当且仅当它们具有相同的元素 (对于序列, 元素和顺序都要相同)

#### 2016-12-09

- NoSQL means different things in different contexts, and interestingly it's not really about SQL.

#### 2016-12-15

- `git mv` - Move or rename a file, a directory, or a symlink
- `git log --graph` - 可查看分支情况
- 偏应用函数与默认值的不能共存 - When you use partial application to generate a function, you lose the ability to call the default. A method is a static thing, so the compiler knows where to look up the default value; a function can be passed around into different contexts, so the compiler will not in general have the information it needs to be able to apply the default parameter.

##### [Scala apply 解读](http://stackoverflow.com/questions/9737352/what-is-the-apply-function-in-scala/9738862#9738862)

> 程序员说: 调用 f 函数, 传入 x 作为参数.
数学家说: 将函数 f 应用于 x.
`apply` 是 Scala 融合 OO 特性和函数式编程特性的手段.
函数是对象, a function that takes an Int parameter and returns an Int will have OO type of `Function1[Int,Int]`.
every object can be treated as a function, provided it has the apply method
将对象视为函数有许多用例, 最常见的就是工厂模式.

#### 2016-12-16

- Slick, A Database object usually manages a thread pool and a connection pool. You should always shut it down properly when it is no longer needed (unless the JVM process terminates anyway).
- Sick, use of `===` instead of `==` for comparing two values for equality and `=!=` instead of `!=` for inequality.
- Scala, 常量存到 `object` 中.
- Slick, Note that map and all other combinators which run user code (e.g. flatMap, cleanup, filter) take an implicit `ExecutionContext` on which to run this code. Slick uses its own ExecutionContext internally for running blocking database I/O but it always maintains a clean separation and prevents you from running non-I/O code on it.

#### 2016-12-18

- EPEL - Extra Packages for Enterprise Linux
- `useradd kissg` - Linux 添加新用户; `usermode -a -G sudo kissg` - 将用户添加到对应的用户组;

###### Google 搜索技巧 (感谢[小土刀](http://wdxtub.com/2016/03/26/google-tip/))

- `+` - 强制搜索, Google 会忽略和过滤一些词
- `-` - 减去, 与关键词搭配时, 中间无空格
- `~` - 同义词
- `*` - 通配符
- `**`, `^` - 指数, 感觉没什么卵用
- `" "` - 不拆分
- `|`, `OR` - 或
- `..` 数字范围, `1994..2016`
- `define:` - 查找解释
- `ext:`, `filetype:` - 文件类型. 目前限定于:
    - Adobe Acrobat PDF (.pdf)
    - Adobe Postscript (.ps)
    - Autodesk DWF (.dwf)
    - Google地球 KML (.kml)
    - Google地球 KMZ (.kmz)
    - Lotus 1-2-3（wk1、wk2、wk3、wk4、wk5、wki、wks、wku）
    - Lotus WordPro (.lwp)
    - MacWrite (.mw)
    - Microsoft Excel (.xls)
    - Microsoft Powerpoint (.ppt)
    - Microsoft Word (.doc)
    - Microsoft Works（wks、wps、wdb）
    - Microsoft Write (.wri)
    - Rich Text Format富文本格式 (.rtf)
    - Shockwave Flash (.swf)
    - 纯文本（ans、txt）
- `intitle:` - 限定网页标题包含关键字 (多个关键字: `allintitle`)
- `inurl:` - 限定 URL 包含关键字 (`allinurl`)
- `inanchor:` - 限定搜索页面链接锚包含关键字 (`allinanchor`)
- `intext:` - 限定搜索正文文本包含关键字
- `site:` - 指定网页内搜索
- `link:` - 搜索链接向某网站的页面
- `related:` - 搜索类似网页
- `cache:` - 搜索某网页在 Google 缓存中的版本
- `info:` - 综合查询某网页的信息. 显示上述四个命令
- `图片搜索`
    - 文件类型支持: `jpg`, `gif`, `png`, `bmp`
    - `imagesize:` - 限定搜索尺寸
    - URL 参数:
        - `&imgtype=news` - 资讯
        - `&imgtype=face` - 脸部特写
        - `&imgtype=clipart` - 剪贴画
        - `&imgtype=lineart` - 素描
        - `&imgtype=photo` - 照片
        - `&imgc=gray` - 黑白照片
        - `&imgc=mono` - 灰阶照片
        - `&imgc=color` - 全彩照片

#### 2016-12-19

- Scalatra, `ScalatraBootstrap.scala` is the Scalatra bootstrap config file, and it's where you should do most of your app configuration work. (`配置`) `ScalatraBootstrap` the class which gets executed when the web application is started
- Integrating a persistence library, 持久化集成基本套路:
    - Start a connection pool at application start
        - (Scala)
            - make `PersistenceInit` trait
            - run init code when app starts up: add `PersistenceInit` trait to `ScalatraBootStrap` and call initialization code in `init` method.
    - Clean up the connection pool when your application stops
    - Provide a way for your controllers to access the connection pool
        - (Scala)
            - details are specific to each libraries.
            - make a `PersistenceSupport` trait which can be mixed into controllers, the trait provides a handle to connection for datastore.
            - a common pattern - open a database connection on each request, close it after the request finishes.
    - Write your application!
- Unix, get timestamp: `date +%s` or `date -d "datetime" +%s`
- Unix, md5 hash of a string in shell - `echo -n "seKUMdXuytClsQWYG1tcQa1x1482139190" | md5sum`, `-n` 是必须的, 去掉换行

#### 2016-12-20

- Scala, 定义
    - val x = loop // 马上执行
    - def x = loop // 别名
- 线性表: 数组, 链表, 栈, 队列
    - 数组 - 连续区域, 访问开销极低, 插入与删除需要移动元素
    - 链表 - 头节点的特殊性
    - 栈 - 数组实现与链表实现
- 贪婪算法 - 局部最优.
- 分治法 - 子问题与原始问题相同, 只是规模更小. 分解 - 解决 - 合并
- 动态规划 - 多阶段决策过程转化为一系列单阶段决策问题, 利用各接段之间的递推关系, 逐个确定每个阶段的最优决策
- Python, 检查包的位置: `python -c 'import os; import inspect; import tensorflow; print(os.path.dirname(inspect.getfile(tensorflow)))'`
- 安装多模块包 - python setup.py install
- Web API 的作用: 让应用程序访问后端系统和数据
- RNNs are particularly useful for learning sequential data like music.
- [How do API gateways work](http://stackoverflow.com/questions/11331386/how-do-api-gateways-work/11335822#11335822)
- 尾递归
- [Hook](http://whatis.techtarget.com/definition/hook): In programming, a hook is a place and usually an interface provided in packaged code that allows a programmer to insert customized programming. For example, a programmer might want to provide code that analyzed how often a particular logic path was taken within a program. Or a progammer might want to insert an additional capability. Typically, hooks are provided for a stated purpose and are documented for the programmer. Some writers use hook to also mean the program that gets inserted.
- DDD vs OOD:
    - DDD 的意义是明确业务领域。而通过 Akka 实现 Actor 模型是描述某个领域模型的最佳方式之一，它不仅能够表现出明确性，并且也可以避免不必要的架构上的困难，以及无意间（或有意识地！）造成的复杂性
    - OOD, 与对象内部如何实现相比，对象之间的消息传递是一种更重要得多的关注点
- Scala/Java, String2Hexdigest simplest method: `import org.apache.commons.codec.digest.DigestUtils.md5Hex; md5Hex("String")`

#### 2016-12-22

- Git 冲突时, 用 `git mergetool` 启动手动混合. ("both modified")

#### 2016-12-27

- Scala, `in seq` 操作: `Seq.contains()`
- Mysql, 创建 utf-8 支持数据库: `create database linkTestDB  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

#### 2016-12-28

- Scala, `try .. catch .. ` 也是一个作用域
- Scala, `Option` 的正确打开方式:

```optionInstance match {
    case Some(name) => ..
    case None =>
}
```

- Scala, 慎用 null(Using the Scala Option, Some, and None idiom (instead of Java null)), Option.get
- Scala, `Try, Success, Failure` 使用
