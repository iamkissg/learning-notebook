# Note on IPython

## Introducing IPython

- 四大最优用的命令
 - `?` - IPython 介绍与 IPython 功能一览
 - `%quickref` - 速查
 - `help` - Python 的帮助系统
 - `object?` - object 的详情, `object??` 更多的详情
- 强大的 tab 自动补全功能, 除了 Python 对象和关键字以外, 还可以补全文件和目录名
- `object_name?` - 按序打印有关 object 的所有细节, 包括 docstrings, 函数定义, 类构造器细节. 使用 `%pdoc`, `%pdef`, `%psource`, `%pfile` 获取指定信息, 使用方法是 `cmd obj`

#### Magic functions

- IPython 预定义了一些 magic function, 用普通命令行语法就能调用
- 有 2 类 magic, 面向行的(line-oriented), 面向单元的(cell-oriented)
- Line Magic 用 `%` 做前缀, 是一条命令, 像操作系统命令行一样工作: 将命令之后的, 全部视为参数, 并且参数不需要括号或引号
- Line Magic 可以返回结果, 并且可以用于赋值
- Cell Magic 以 `%%` 为前缀, 是函数, 当前单元内的一切作为参数
- 内建的 magics 包括:
 - work with code: `%run`, `%edit`, `%save`, `%macro`, `%recall`, etc
 - affect the shell: `%colors`, `%xmode`, `%autoindent`, `%automagic`, etc
 - others: `%reset`, `%timeit`, `%%writefile`, `%laod`, `%paste`
- 在 Line Magic 行内调用 Line Magic, 只要标识符在命名空间没有被定义, 可省略前缀 `%`. 执行 `%automagic` 切换省略的行为
- Cell Magic 必须带 `%%` 前缀
- `%magic` 查看 magic 系统更多的信息, 可用 `%somemagic?` 查看 somemagic 的描述, `%lsmagic` 查看可用的 magic
- `%run` 命令可用于运行任何 Python 脚本, 并直接加载所有的数据到交互式命名空间. 每次运行, 文件都会从磁盘重读, 因此对文件的修改会立即生效. IPython 还包含了 `dreload` (deepreload) 函数, 可递归的重载
- `%run` 提供了多个 flags, `-t` 检测脚本的执行时间, `-d` 以 Python pdb 的调试(debugger)功能运行, `-p` 检查(profiler)
- `%edit` 通过调用编辑器, 提供多行编辑功能. (尼玛嗨, 直接启动了编辑器) 编辑结束之后, IPython 会立即执行代码, 就好像是在交互式环境中一样. 要让 `%edit` 工作, 启动编辑器的调用必须是阻塞的调用.
- 当有异常时, 调用 `%debug` 启动 pdb(Python debugger) 以查找问题所在. 替代的方案是, 调用 `%pdb`, IPython 会在任意未捕获的异常抛出点, 自动启动调试器. 用户可以打印变量, 查看代码, 执行语句, 检查调用栈以跟踪问题.

#### History

- IPython 保存了命令以及结果, 用上下键可查看之前的命令
- 输入输出历史分别保存在 `In` 和 `Out` 变量中, 以提示数字为 key, 比如 `In[7]`.
- 最近三次输出的对象还保存在 `_`, `__`, `___` 变量中
- 使用 `%history` 查看输入输出历史(我怎么只看到输入信息), 输入历史被保存到数据库, IPython 可通过配置来保存输出历史
- 可以使用输入历史的 magic 函数, 包括 `%edit`, `%rerun`, `%recall`, `%macro`, `%save`, `%pastebin` 的输入

#### System shell commands

- To run any command at the system shell, simply prefix it with `!`
- 使用 `!` 前缀来执行 shell 命令
- 可用 String List 来保存输出: `files = !ls -l`
- 将 Python 变量传递给系统命令, 使用前缀 `$`
- 自定义在 IPython 中使用的 shell 命令, IPython 已经预定义了一些
- 使用 `ipython profile create` 命令来创建默认的配置文件, 将被保存到 `~/.ipython/profile_default`
- 为不同的任务设置不同的配置文件, 是个好主意
- 若需要在 IPython 会话启动时执行代码, 最简单的方式是添加 Python 或 IPython 脚本到 `profile_default/startup/` 目录即可. 该目录下的文件, 在 IPython shell 构造时就会被执行, 按文件名顺序执行, 因此可以前缀来控制执行顺序

---

## Plotting

- IPython kernel 的主要功能之一就是绘图, 设计的初衷就是与 matplotlib 的无缝连接, 以提供绘图的能力
- 在任何绘图或导入 matplotlib 生效之前, 必须执行 `%matplotlib`, 这使 IPython 能正确地处理 `matplotlib`. 若不执行 `%matplotlib`, 执行 `import` 命令, no names are added to the namespace
- 无参调用 `%matplotlib` 时, 绘图命令使用默认的 `matplotlib`. 另外, 可显式地指明后端分离窗口, 例如 `%matplotlib gtk`
- IPython 提供了一个 `inline` 后端, 只在 Jupyter Notebook 和 Jupyter QtConsole 中可用. 调用方法同上: `%matplotlib inline`
- 使用 `inline` 后端, 将不会在弹出窗口中绘图, 而是像一般的 notebook 输出一样, 显示在 cell 中, 结果图也将保存在 notebook 文档中

---

## IPython Tips & Tricks

#### Embed IPython in your programs

#### Run doctests

- `%doctest_mode` - 启动后, IPython 的提示符, 输出, 异常显示将类似于默认的 Python 解释器. 该模式允许直接粘贴 `>>>` 前导的代码 (忽略前导空格). 和 `%history -t` 合用, 查看 doctest 工作流的翻译历史

#### Use IPython to present interactive demos

- 使用 `IPython.lib.demo.Demo` 类, 加载 Python 脚本作为交互式 demo. 用少量的简单标记, 用户可以控制脚本的执行, 必要时可暂停

#### Suppress output

- 在行末加 `;`, 以 suppress 输出的打印. 当计算会生成大量输出时, 可以隐藏(?)感兴趣的部分. 该做法, 还不会将对象保存在输出 cache 中, 因此, 有大量临时对象时, 会很快地被释放

#### Lightweight 'version control'

- 当无参调用 `%edit` 时, IPython 用编辑器打开一个临时文件, 并将编辑内容保存为一个字符串变量. 因为 IPython 的输出缓存机制, 该变量会被自动保存.
- 当调用 `%edit -p` 时, IPython 会试着打开前一次 `%edit` 编辑的数据. 若同一时间没有使用 `%edit`, 相同的内容会被重新打开, 但是在一个全新的文件中. 这意味着, 如果做了修改, 又想找回旧版本, 可用 输出编号`%edit _NN`.


---

## IPython as a system shell

- 设置 sh 配置:
 - 通过命令参数
 - 启动 ipython 之后执行指令 `%rehashx`, 就可以 make system commands directly available
 - `%autofull` - full mode
- 环境变量
 - `%env` - 打印全部的环境变量
 - `%env key` - 返回特定环境变量的值
 - `%env key val` or `%env key=val` 设置环境变量, 环境变量值默认就是字符串, 因此不必使用引号
 - `%env key=$var` - 用 Python 变量设置环境变量
- 别名
 - 执行 `%rehashx` 命令时, `$PATH` 所有的命令都会被加载为 IPython 别名. 由此, 可以执行任何常规的系统命令
 - `%alias?` 查看别名详情
 - `%rehashx` 也可以查看 `rehashx` 命令的详情
- 目录管理
 - 每一条 IPython 传递给底层系统的命令, 都由一个子 shell 执行, 并马上退出. 因此不能使用 `!cd` 在文件系统进行导航
 - IPython 提供了内建的 `%cd` 命令 (magic command), 以提供在文件系统的移动, 当 `automagic` 的值为 1 时, 不用加 %.
 - `%dhist` - 查看历史浏览过的目录
 - `%pushd`, `%popd`, `%dirs` 提供了目录栈操作
- 字符串列表
 - String lists 是一种处理系统命令输出的便利方式, 通过 `var = !cmd` 语法实现. 必须将 `!`, 否则 ls 将被认为是变量
 - 还能对返回的 String lists 进行过滤, 使用 `str.grep(pattern, prune = False, field=None)`, `prune` 用于反选, `field` 关键字用于指定 `pattern` 出现的位置
 - 用 `fileds(pos, ..)` 获取指定字段的值, 选出的所有字段拼接成一条字符串作为列表的一项. `.s` 属性可将列表中的所有字符串拼接成一个由空格分隔的大字符串
 若不适用任何参数, 则各字符串组成一个列表作为更大的列表的一项.\\
 - String Lists 继承自 Python 的列表, 任何列表方法能可用
- .s, .n, .p 属性
 - `.s` 属性, 返回由单个空格分隔的一条字符串
 - `.n` 属性, 返回由新行分隔的单个字符串
 - 若 String List 中的项是文件名, 则 `.p` 可用于返回一个 path 对象的列表

---

## IPython as a system shell

- 设置 sh 配置:
 - 通过命令参数
 - 启动 ipython 之后执行指令 `%rehashx`, 就可以 make system commands directly available
 - `%autofull` - full mode
- 环境变量
 - `%env` - 打印全部的环境变量
 - `%env key` - 返回特定环境变量的值
 - `%env key val` or `%env key=val` 设置环境变量, 环境变量值默认就是字符串, 因此不必使用引号
 - `%env key=$var` - 用 Python 变量设置环境变量
- 别名
 - 执行 `%rehashx` 命令时, `$PATH` 所有的命令都会被加载为 IPython 别名. 由此, 可以执行任何常规的系统命令
 - `%alias?` 查看别名详情
 - `%rehashx` 也可以查看 `rehashx` 命令的详情
- 目录管理
 - 每一条 IPython 传递给底层系统的命令, 都由一个子 shell 执行, 并马上退出. 因此不能使用 `!cd` 在文件系统进行导航
 - IPython 提供了内建的 `%cd` 命令 (magic command), 以提供在文件系统的移动, 当 `automagic` 的值为 1 时, 不用加 %.
 - `%dhist` - 查看历史浏览过的目录
 - `%pushd`, `%popd`, `%dirs` 提供了目录栈操作
- 字符串列表
 - String lists 是一种处理系统命令输出的便利方式, 通过 `var = !cmd` 语法实现. 必须将 `!`, 否则 ls 将被认为是变量
 - 还能对返回的 String lists 进行过滤, 使用 `str.grep(pattern, prune = False, field=None)`, `prune` 用于反选, `field` 关键字用于指定 `pattern` 出现的位置
 - 用 `fileds(pos, ..)` 获取指定字段的值, 选出的所有字段拼接成一条字符串作为列表的一项. `.s` 属性可将列表中的所有字符串拼接成一个由空格分隔的大字符串
 若不适用任何参数, 则各字符串组成一个列表作为更大的列表的一项.\\
 - String Lists 继承自 Python 的列表, 任何列表方法能可用
- .s, .n, .p 属性
 - `.s` 属性, 返回由单个空格分隔的一条字符串
 - `.n` 属性, 返回由新行分隔的单个字符串
 - 若 String List 中的项是文件名, 则 `.p` 可用于返回一个 path 对象的列表
