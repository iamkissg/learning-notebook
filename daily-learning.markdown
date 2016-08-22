#### Before 2016-08-01
- 求余数: (-len(s)) % 4 => 4 - (len(s))%4
- Linux下, 以非root用户身份, 用nvm安装Node.JS, Node.JS将被安装在当前用户家目录下. 其他用户, 甚至root用户并不知道系统中已经安装了Node.JS, 之后用户通过npm安装的工具程序, 也只能被当前用户使用, 即, 此时`sudo　cmd`会提示`cmd`不存在. 解决方法是：软链接

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
E: Encountered a section with no Package: header
E: Problem with MergeList /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_natty_main_binary-i386_Packages
E: The package lists or status file could not be parsed or opened.
```

- 上述问题解决: `sudo rm -vf /var/lib/apt/lists/*` - 删除Merge List

- `System program problem detected`问题的解决: `sudo rm /var/crash/*` - 删除旧的crash. 虽然之前的问题已经解决了, 但旧的crash文件被保存了下来, 所以会持续报错.

```js
document.getElementById('container').addEventListener('click', function(event) {
	     console.log(event.target.innerHTML);
	}
})
```

- 在一个<div>上注册事件(click)监听, 对div内所有元素的点击都会在控制台打印. (不需要为每个元素单独注册事件)
- `docker exec -it <container id> /bin/bash` -  connect to a bash prompt on the running container.
- `find . -name "filename"` - 在当前目录递归地查找指定文件名的文件
- Linux process states:

```txt
D Uninterruptible sleep (usually IO)
R Running or runnable (on run queue)
S Interruptible sleep (waiting for an event to complete)
T Stopped, either by a job control signal or because it is being traced.
W paging (not valid since the 2.6.xx kernel)
X dead (should never be seen)
Z Defunct ("zombie") process, terminated but not reaped by its parent.

# additional characters
< high-priority (not nice to other users)
N low-priority (nice to other users)
L has pages locked into memory (for real-time and custom IO)
s is a session leader
l is multi-threaded (using CLONE_THREAD, like NPTL pthreads do)
+ is in the foreground process group
```

- `ps -ef` - 查看所有进程的父进程
- `trap -l` - Linux查看信号及其编号
- 交互式Bash获取进程PID:

```shell
ps -ef | grep "name" | grep -v grep | awk '{print $2}'
ps -ef | awk '/[n]ame/{print $2}'
ps x | awk '/[n]ame/{print $1}'
pgrep -f name  # 最简单的方法
pkill -f name  # 通过名称找到进程并杀死
pidof name     # ?
```

- shell 脚本获得进程 pid:

```shell
#! /bin/bash
# process-monitor.sh
process=$1
pid=$(ps -ef | grep $process | grep 'name' | grep -v grep | awk '{print $2}')
echo $pid
```

- `$$` - 当前 Shell 进程的 pid; `$!` - 上一个后台进程的 pid
- 查看指定进程是否存在:

```shell
if ps -p $PID > /dev/null
then
    echo "$PID is running"
    # Do something knowing the pid exists, i.e. the process with $PID is running
fi
```

#### 2016-08-02

- Python str 2 time/datetime - datetime.datetime.strptime(str, time\_format).date() | time.time.strptime(str, time\_format)
- Python get pid of the running program, or you can apply this to check if the program is running

```
# check_output - Run command with arguments and return its output.
# If the exit code was non-zero it raises a CalledProcessError.
from subprocess import check_output
def get_pid(name):
    return check_output(["pidof",name])

    # or handle multiple entries and cast into ints
    # using set for quick search
    # return set(map(int,check_output(["pidof",name]).split()))

    # or with -s flag to get a single pid
    # return int(check_output(["pidof","-s",name]))
```

- jQuery 显隐元素: `$(selector).hide();`, ` $(selector).show();`
- JavaScript 使用 document.createElement() 动态创建 DOM 节点:

```JavaScript
var childNode = document.createElement('p');
childNode.innerHTML = '<span>这里是提示信息〜〜</span>';
childNode.setAttribute('class', 'alerts');
childNode.setAttribute('onclick', 'this.style.display = "none"');
/*or
childNode.className = 'alerts';
childNode.onclick = function () {
    this.style.display = 'none';
}
*/
document.getElementsByTagName('body')[0].appendChild(childNode);
```

- CSS, `inline-block` 替代 `float:left` 实现横向列表. 默认情况下, inline 元素之间会有空隙, 通过设置 padding, margin 等属性可消除空隙
- jQuery 绑定事件与 not 函数, button 反 click 应用举例:

```JavaScript
$(".trade-filter button").on("click", function(){
    $(".trade-filter button").not(this).removeClass('active');
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

- 不同于 C/C++ 的 `switch`, ECMAScript 的 `switch` 可用于字符串, 即 `case "kissg": do_something`
- jQuery, `$(selector)` 选择器从**从父级标签一路定位到子级标签, 不是把子级标签写在父级标签之前**

#### 2016-08-03
- 新学 2 个前端日期选择器: jqueryui datepicker 和 bootstrap datetimepicker. 前者的使用见[这里](http://api.jqueryui.com/datepicker/), 后者使用见[这里](http://www.bootcss.com/p/bootstrap-datetimepicker/)
- JavaScript 获取当前日期时间: `var dt = new Date()`, `Data` 对象提供了多种日期时间操作
- JavaScript 切片操作: `stringObject.slice(start,end)`

#### 2016-08-06

- Chrome -> editor：`data:text/html, <html contenteditable>`
- Ubuntu install the latest version of git, add ppa: `sudo apt-add-repository ppa:git-core/ppa`
- Python 运行时, 查看版本: `import sys; sys.version_info`

#### 2016-08-08

- CentOS, 查看系统版本: `cat /etc/*elease`, 其中 `*elease` 包括 centos-release, os-release, redhat-release, system-release, 每一个都带有版本信息, 其中 `os-release` 最详细, 并且在其他发行版也通用 (Ubuntu 可用)
- 局域网内, 切记要修改 IP 地址绑定! 比如使用多个容器来运行主从 redis 数据库应用, redis.conf 默认是 `bind 127.0.0.1`, 这就造成了主从数据库之间无法同步, 必须同时修改为 `bind 0.0.0.0` 才能使已经通过 `--link` 连接的多个容器的数据库同步, 从数据库才能查询到主数据写入的值.
- `$$` 表示 shell 中当前运行的进程 pid
- 查看进程 namespace: `ls -l /proc/[pid]/ns`
- UTS - Unix Timesharing System

#### 2016-08-10

- 查看进程的能力: `cat /proc/$pid/status` (功能不止如此)

#### 2016-08-11

- 查看 IP 路由表, 指令 `route`
- `lo` - 回环网卡 (lookback adaptor), 本地进程与另一本地进程通信时可用
- `eth0` - 与外网通信的网卡
- `pscap` - 查看进程的能力, 需要安装工具: `sudo apt-get install libcap-ng-utils`
- `brctl` - 查看和管理网桥, 需要安装工具包: `sudo apt-get install bridge-utils`
- `exec $SHELL -l` - reload shell
- `pip -r <file>` - Install from the given requirements file, can be used multiple times

#### 2016-08-16

- `netifaces` - Python, portable network interface information
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

- Unix 系统测试程序运行时间: `time cmd`, 比如: `time python3 hw.py`
- 有一些嵌套的 if 语句其实不能用逻辑运算符取消嵌套：


```python
if "." in package:
    if package[:package.find(".")] not in  LT:
        print("2")
elif "as" in package:
    if package[:package.find("as") - 1] not in  LT:
        print("3")
elif package not in LT:
    print("4")

# wrong way (也许只是还没找到合适的方式)
# 以第一条为例，写成以下形式，就不能判断带 "." 的但属于 LT 的包了
# 会直接跳到第 3 个逻辑, 然后判断出错
if "." in package and package[:package.find(".")] not in  LT:
    print("2")
elif "as" in package and package[:package.find("as") -LT:
    print("3")
elif package not in LT:
    print("4")
```

- utc: 协调世界时，世界上调节时钟和时间的主要时间标准

#### 2016-08-19

- regex `\w` (word) matches any letter, number or underscore, 即[a-zA-Z\_]
- svg (Scalable Vector Graphics) - 是**基于 XML**, 用于描述二维矢量图形的一种图形格式, 所以需要浏览器或其他可查看 svg 的图片查看器来打开
- git 回溯到打了某个 tag 的版本: `git reset --hard tag_name`
- Python 的 Counter, 可用于统计序列中元素出现的次数, 以元素为 key, 出现次数为 value.
- `Counter.values()` 和 `Counter.keys()` 会按 keys 从小到大的顺序返回 values/keys 的序列, 类型分别是 dict\_values 和 dict\_keys
- `not` 与 `is None`, 大多数情况下可以混用, 但 `not 0` 和 `0 is None` 不能混用, 前者返回`True`, 后者返回 `False`
- `strptime(str, format)` -> new datetime parsed from a string\\
`strftime(format, ttime)` or `time.strftime(format)` -> convert time to formatting str
- Python, 有些操作, 将文件内容加载到对象, 之后关闭文件也能操作; 另一些, 需要文件一直打开, 相当于创建了一个文件指针对象, 比如:

```python
with open(filename, 'r') as f:
    reader = csv.reader(f)  # 就我所理解, reader 应该是一个文件指针对象
    next(reader)  # ok
next(reader)  # I/O operation closed file

with open(filename, 'r') as f:
    pop_data = json.load(f)
# ok,
# json.load - deserialize file-like object to Python object
for pop_dict in pop_data:
    some_operations
```

- Python, Pygal 移除了 i18n module, 不过可以安装pyga\_maps\_world 插件

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

- 使用列表推导式读取 JSON-line 的技巧: records = [json.loads(line) for line in open(path)]

#### 2016-08-22
