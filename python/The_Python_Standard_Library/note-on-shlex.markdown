# shlex — Simple lexical (词法) analysis

[shlex](https://docs.python.org/3/library/shlex.html#shlex.shlex) 类使写一个词法分析器更容易. 这对于写一个迷你语言很有帮助 (比如, 写一个 Python 应用的运行时控制文件), 或解析引用的字符串

## shlex 定义的顶层函数:

- `shlex.split(s, comments=False, posix=True)` - 使用 shell-like 的语法分割 str. 后两个参数如其名描述的, 一个是忽略注释, 一个是确定平台, 是否符合 POSIX 标准. 该函数会创建一个 shlex 实例
- `shlex.quote(s)` - 返回 str 的 shell-escaped 版. 如果不想用 list, 返回值可以作为 shell 命令行的 token

非正确示范:

```python
>>> filename = 'somefile; rm -rf ~'
>>> command = 'ls -l {}'.format(filename)
>>> print(command)  # executed by a shell: boom!
ls -l somefile; rm -rf ~
```

`shlex.quote(s)` 的使用, 与 UNIX shell 兼容:

```python
>>> command = 'ls -l {}'.format(quote(filename))
>>> print(command)
ls -l 'somefile; rm -rf ~'
>>> remote_command = 'ssh home {}'.format(quote(command))
>>> print(remote_command)
ssh home 'ls -l '"'"'somefile; rm -rf ~'"'"''
>>> remote_command = split(remote_command)
>>> remote_command
['ssh', 'home', "ls -l 'somefile; rm -rf ~'"]
>>> command = split(remote_command[-1])
>>> command
['ls', '-l', 'somefile; rm -rf ~']
```

- `class shlex.shlex(instream=None, infile=None, posix=False)` - shlex 实例或其子类实例是一个词法分析器对象.
    - instream - 指定从何处读取字符, 必须是带 `read()` 和 `readline()` 方法的类文件或流对象, 或者可以是 str. 省略时, 默认从 `sys.stdin` 读取输入
    - infile - 表示文件名的字符串, 设置 `infile` 初始值. `instream` 省略时或等价于 `sys.stdin` 时, `infile` 默认被置为 `stdin`.

## shlex 对象

#### 方法

- `shlex.get_token()` - 返回 token. 若用 `push_token()` 对 token 进行过压栈 (stacked) 处理, 从栈中 pop 得到 token; 否则从输入流中读取. 读到 eof 时, 返回之.
- `shlex.push_token(str)` - 将 str 压入 token stack
- `shlex.read_token()` - 读取原始的 token (a word or other atomic parse element), 忽略压回栈 (pullbac stack), 不解析源请求 (source request)
- `shlex.sourcehook(filename)` - 当 shlex 检测到一个 source request 时, 以 token 为参数调用该方法, 并预期着返回一个文件名和 open file-like 对象组成的 tuple
    - 通常, 该方法会去除参数两边的任何引号. 若结果是绝对路径名, 或者没有有效的 previous source, 或者 previous source 是流 (比如 `sys.stdin`) 的情况下, 返回单一值. 否则, 若结果是相对路径名, the directory part of the name of the file immediately before it on the source inclusion stack is prepended (this behavior is like the way the C preprocessor handles #include "file.h").
    - 该操作的结果将被视为文件名, 并作为 tuple 的第一个元素返回, 并调用内置函数 `open()` 打开该文件, 作为 tuple 的第二个参数.
    - 这个钩子是裸露的, 因此用户可利用其实现 directory search path, addition of file extensions, and other namespace hacks.
    - 没有相应的 `close` 钩子, shlex 实例会遇到 EOF 时, 调用 `close()` 方法
- `shlex.push_source(newstream, newfile=None)` - 将输入源流压入输入栈. 若指定了文件名, 其之后在错误消息中可用. 被 `sourcehook()` 使用
- `shlex.pop_source()` - 出栈. 当词法分析器读到 EOF 时, 调用该方法
- `shlex.error_leader(infile=None, lineno=None)` - 产生 UNIX C 编译器错误标签的格式的错误消息 leader (?). 格式: `'"%s", line %d: '`, `%s` 由当前源文件填充, `%d` 由当前输入的行号填充 (可选参数用于覆盖这些值)
    - 这为 shlex 的使用者提供了便利, 以生成标准的, Emacs 或其他 Unix 工具可解析的错误消息

#### 属性

- `shlex.commenters` - 注释, 默认以 `#` 为开始
- `shlex.wordchars` - token 字符. 默认包括所有的 ASCII 字母和 `_`
- `shlex.whitespace` - 空白字符. 默认包括空格, tab, 回车与换行
- `shlex.escape` - 转义字符. 只在 POSIX 模式下有效, 默认是 `\`
- `shlex.quotes` - 引号. 匹配到相同的引号, 才算一个 token. 默认是 ASCII 单双引号
- `shlex.escapedquotes` - 根据 escape 定义的转义字符, 引号中的字符会被转义. 只在 POSIX 模式下有效, 默认为 `'"'`
- `shlex.whitespace_split` - 为真时, tokens 只会以空格分割
- `shlex.infile` -  当前输入文件名. 实例化对象时指定, 或在之后的 source request 中入栈. 构造错误消息时, 测试该属性, 可能会有所帮助
- `shlex.instream` - 输入流
- `shlex.source` - 默认是 `None`. 若为其赋一个 str, 将被哦\

