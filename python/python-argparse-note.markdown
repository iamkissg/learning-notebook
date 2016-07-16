##python3 argparse note

(以下`参数`与`选项`是一个概念, 使用场景不同, 使用不同的名称而已)

####[Argparse Tutorial](https://docs.python.org/3/howto/argparse.html)

- `--help`选项是唯一不用指定的选项, 在创建`ArgumentParser`对象时默认绑定了该选项, 是一个可选选项(optional)
- `add_argument`方法用于添加命令行选项 - `parser.add_argument("echo")`
- `parse_args`方法返回选项的值 - `args = parser.parse_args(); print(args.echo)`
- `add_argument`方法指定选项的名称时, 还可以通过`help`关键字参数来设置提示信息 - `parser.add_argument("echo", help="echo the string you use here")`
- `add_argument`方法还可以指定选项的值类型, 使用`type`关键字(默认将视作字符串), 此时当输入的值与指定不相符时, 还会有错误信息提示 - `parser.add_argument("square", help="display a square of a given number", type=int)`
- 在程序运行时, 不指定可选选项是不会报错的, 但没有位置选项将会报错, 以上方法定义的选项是位置选项. `mkdir dirname`中的`dirname`就是一个位置选项
- 默认的, 当一个可选的参数未被使用时, 其对应的变量值是`None`
- `add_argument`方法中使用`action`为选项指定行为,如`action="store_true"`, 使得指定的选项变成一个标志, 即当指定了该参数, 其对应的变量值就为`True`, 为其指派值将报错. `ls -l`就是一个很好的例子
- 可选参数以`--`为前缀, 指定参数时, `--`开头的参数将被视为可选参数, 其简写形式为以`-`开头. - `add_argument("-v", "--verbose", ...)`
- `add_argument`方法中使用`choices=list`来为选项设定一个取值范围, 输入值超出范围的, 将报错
- 令`action="count"`, 将统计出现的次数, 统计值将赋给选项对应的变量值
- `add_argument`方法中使用`default`关键字参数, 为选项设置默认值
- 在创建解析器时, 通过`description`来使帮助信息更可读

####[moduel argparse](https://docs.python.org/3/library/argparse.html)

- `nargs`关键字参数可以为一个选项指定多个值.
 - 定义时指定`nargs=N`, 则命令行中的N个参数将被作为一个list, 即使当`nargs=1`也将返回list, 而不是默认的字符串
 - `?` - 命令行中的一个参数将被作为选项的值, 或者未使用选项, 则将使用默认值
 - `*` - 命令行中所有参数都以list的形式作为选项值
 - `+` - 与`*`类似, 除此之外, 若一个参数都没有, 因抛出异常
 - `argparse.REMAINDER` - 剩余的命令行参数全部以list的形式作为选项的值
