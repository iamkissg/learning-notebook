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
