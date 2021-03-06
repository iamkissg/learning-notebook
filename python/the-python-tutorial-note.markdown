# The Python Tutorial

## Chapter 2 Using Python Interpreter

- 交互模式下,Python解释器自动将上一个表达式的值赋给变量`_`.如果对其进行赋值,就成了一个普通变量

## Chapter 3 An Informal Introduction ot Pyton

- python支持复数,可用`j`或`J`表示虚部
- 在字符串前使用`r`,得到`raw strings`,特殊字符不需要转义
- 三重引号包裹的字符串,自动包括了行结束符,可通过在行尾添加`\`,取消当前行的自动换行,实现"续行"
- 操作符`+`和`*`可分别用于字符串的拼接与重复
- 形如`"Py" "thon"`,将被视为1个字符串.
- python没有字符类型,一个字符仅仅是一个大小为1的字符串
- 负数索引从`-1`开始,因为`-0=0`啊
- 对字符串使用切片时,第一个索引省略,则默认其是0;第二个索引省略,则默认是字符串的大小
- 取单个字符时,下标越界将出错;但切片能处理下标越界
- `list`是同质的,`tuple`是异质的
- list的切片,功能很强大,可以将任意list赋给选中的切片\\
切片的强大又岂止于list
- `print`会自动换行,使用`end`关键字参数可取消自动换行,而以指定的值结束

## Chapter 4 More Control Flow Tools

- python没有`switch .. case...`语句,只有`if...elif...else...`
- python的`for`语句,实现对`序列`的迭代,仅此而已.
- 当要在`for`语句的迭代过程中实现对序列的修改,建议的做法是先创建一份副本.迭代的过程不会隐式地创建副本.可以通过切片方便的实现拷贝:

```python
for w in words[:]:
    if len(w) > 6:
        words.insert(0, w)
```

- `range()`函数可生成算术级数.有两种调用方式:
 1. range(stop)                -> range object   默认从0开始
 2. range(start, stop[, step]) -> range object
- 通过下标对序列进行迭代的常用方法是,使用`enumerate()`函数\\
`enumerate()`函数接受第二个参数, 作为开始序号
- `range object`是一个可迭代对象.
- 循环语句可以带一个`else`子句.当循环自然结束(while语句的条件不再成立,或for语句的迭代完成), 被执行; 若循环是被`break`终止的,`else`子句不会被执行
- `try`语句的`else`子句, 在没有异常抛出时被执行
- 参数传递, 传递是**引用**,而非值.因此若函数的参数是可变类型的对象,是可以对其进行修改的
- 函数是一个对象
- 没有`return`语句的函数, 将自动返回`None`;不带表达式的`return`语句也返回`None`
- 几种定义函数参数的方式:
 1. 位置参数: 必须是按顺序传入参数
 2. 默认值参数: 给参数设置默认值,当调用函数未传入参数时,使用默认值.
  - 默认值在定义函数时被计算出来
  - 若默认值参数是可变类型对象,那么默认值也是可以被修改的! 因此,最好是不要使用可变类型对象作为默认值
 3. 关键字参数: 函数调用时,必须指明函数名与函数值.关键字参数必须在位置参数之后,关键字参数名必须与函数定义时的参数名相匹配,其位置不重要.
 4. 可选参数: 将参数包装称一个tuple使用.必须出现在普通参数之后,因为它会将剩余的参数全部打包进tuple.唯一可以出现在可选参数之后的,是关键字参数
 5. `**name`: 接受一个字典作为关键字参数
 6. `*name`: 接受一个位置参数的元组.`*name`必须在`**name`之前
 7. `*`操作符,可用于将`list`或`tuple`解压,作为可变参数传入`*args`
 8. `**`操作符,用于将`dict`解压,作为关键字参数传入`**kw`
- `lambda`表达式,用于创建一个匿名函数.`lambda`函数可被用于任何函数能应用的场合. `lambda`表达式实际是一种语法糖
- 编程风格简章:
 1. 使用4个空格的缩进, 而非`tab`键
 2. 折叠行, 使其不要超过79个字符
 3. 函数与类定义之间插入空行
 4. 尽量当行注释
 5. 使用`docstrings`
 6. 操作符两侧加空格, 逗号之后加空格
 7. 统一命名风格. 推荐是, 类使用`CamelCase`风格, 方法或函数使用`lower_case_with_underscores`
 8. 不用迷之编码格式. `utf-8`是最好的选择

## Chapter 5 Data Structures

### List

`list` 对象的所有方法:

- list.append(x)
- list.extend(L)
- list.insert(i, x)
- list.remove(x)
- list.pop([i])
- list.clear()
- list.index(x)
- list.count(x)
- list.sort()
- list.reverse()
- list.copy()

PS: Python 2 没有 `list.clear()` 和 `list.copy()`

`attend()` + `pop()`, 实现 stack. 可以用 `insert()` 和 `pop()` 实现 queue. 但是 `append()` 和从 list 尾 `pop()` 很快, 但 `insert()` 和 `pop()` 到 list 头很慢. 使用 `collections.deque`

列表推导式提供了简洁的创建列表的方式. 

Common applications are to make new lists where each element is the result of some operations applied to each member of another sequence or iterable (操作), or to create a subsequence of those elements that satisfy a certain condition (条件).

```python
>>> squares = []
>>> for x in range(10):
...     squares.append(x**2)
...
>>> squares
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

上述循环结束后, `x` 变量仍存在! 简化方法: `squares = list(map(lambda x: x**2, range(10)))` 或简洁可读的列表推导式: `squares = [x**2 for x in range(10)]`

列表推导式至少包含一个 `for`, 之后可以有 0 或多个 `for` 或 `if`. 像是拉平的循环语句

嵌套的列表推导式, 列表推导式的初始化表达式可以是任意表达式, 嵌套函数或另一个列表推导式都可以.

```python
# 按列组合
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

# list comprehension
[[row[i] for row in matrix] for i in range(4)]

# 更简洁高效的写法:
list(zip(*matrix))
```

`del` 按索引删除元素: `del a[i]`; 还可以删除切片; 或删除整个变量: `del a`

### tuple & sequences

`tuple` 是不可变的, 但其元素可以是可变的, 比如 `list`

`tuple`  通常包含异质的 (heterogeneous) 元素序列, 可通过索引以及解压 (unpack) 进行访问; `list` 通常是同质的, 通过迭代进行访问

`t = a, b, c` - tuple packing; `x, y, z = t` - sequence unpacking, 此时等号左边的变量数量要和 sequence 包含的一样多. 多重赋值就是 tuple packing 和 sequence unpacking 的组合

### set

`set` - 无序, 互异. 基本的用途包括: 成员检测, 消除重复值, 并支持数学操作 (交, 并, 差, 对称差等)

`{exp for statement}` 实现集合推导式

### dict

序列通过下标访问, 字典通过 `key` 索引, `key` 可以是任意不可变类型 (str, num, 只包含不可变对象的 tuple)

`del` 可删除 key:value 对

`dict()` 构造器可直接用 key-value 对的序列创建字典, 当 `key` 是简单的字符串时, 可以关键字参数的方式创建字典

`{k: v for statement}` - 字典推导式

### Looping Tech

1. dict.items()
2. enumerate()
3. zip()
4. reversed()
5. sorted()
6. 对序列的迭代, 不会隐式地创建拷贝. 但要在迭代过程中改变序列, 建议是先创建一份拷贝, 可用切片 `[:]` (否则一边迭代一边修改, 会造成混乱)

### More on Conditions

`while` 和 `if` 语句的条件可以包含任何操作符, 不只是比较.

- `in`, `not in` - 是否成员
- `is`, `is not` - 是否同一对象
- 比较操作符优先级相同, 但低于所有数字操作符
- 链式比较: `a < b == c`, a 小于 b, 并且 b 等于 c 才为真
- and, or, not 优先级低于比较操作符. 这里, not 高于 and 高于 or. `短路`
- 比较或布尔表达式的结果可以赋给变量

```python
string1, string2, string3 = '', 'Trondheim', 'Hammer Dance'
non_null = string1 or string2 or string3
# "Trondheim"
```

- 序列的比较按下标, 按字典序比较. 不同类型的 `<`, `>` 比较是合法的, 会使用恰当的比较方法, 因此 `0` 与 `0.0` 是相等的

## Chapter 6 Modules

模块是包含 Python 定义和语句的文件. 在模块内部, 模块名可通过 `__name__` 全局变量获得.

`import module` 只是将模块名导入了当前符号表 (current symbol table), 并没有直接导入模块内定义的函数或类

模块可包含函数定义, 也可包含可执行的语句. 这些语句用于初始化模块, 并只在导入时执行 1 次 (如果文件是可执行的)

每个模块都有 private symbol table, 作为该模块内定义的所有函数的 global symbol table

`import imp; imp.reload(modulename)` - 重新加载模块

`if __name__ == "__main__":` - 提供了方便的模块接口或直接测试

导入时, 解释器首先在内建模块中搜索, 然后在 `sys.path` 变量描述的 list of directories 中查找. `sys.path` 包括:

- 输入脚本所在的目录 (或当前目录)
- `PYTHONPATH` 环境变量给定的目录
- 默认的安装依赖目录

> 包含软链接的目录不会被加入模块搜索路径

被执行脚本所在的目录位于搜索路径的顶层, 在标准库之前.

为了加快导入模块的速度, Python 会将每个模块的编译后的版本缓存到 `__pycache__` 目录, 以 `module.version.pyc` 命名

Python 会检查源的修改日期, 以确认是否需要重新编译. 这是一个完全自动的过程.

`编译后的模块是平台独立的, 因此可以在不同架构下共享.

两种情况下, Python 不会检查缓存:

1. 直接从命令行导入的模块, 总是重新编译, 而不会保存编译结果
2. 没有模块的源文件. 为了支持无源文件的发布, 编译好的模块必须保存在源目录内, 但必须不能包含源模块文件

Tips:

- 从 `.pyc` 或 `.pyo` 读取的程序不会运行得更快, 只是加载更快
- 使用 `-O` 或 `-OO` 切换 Python 命令的模式, 减少编译模块的大小. `-O` 移除了断言语句 (assert), `-OO` 移除了断言语句和 `__doc__` 字符串. 慎用!
- `compileall`  模块将目录下所有模块编译成 `.pyc`. 使用 `-O` 选项, 则编译成 `.pyo`

### Standard Modules

一些模块已经内建到解释器, 它们提供了非核心的, 但同样的重要的功能: 效率或操纵系统原子访问 (调用)

`sys.ps1`, `sys.ps2` 定义了解释器使用的提示符, 只在交互模式下有用

`sys.path` 包含了模块搜索路径的字符串, 是一个 list

### dir()

`dir()` 函数查看模块定义的 name, 返回 a sorted list of strings. 无参调用时, 返回当前定义的 names (包括变量, 函数, 模块等等). 不会返回内建函数或变量名, 要查看这些:

```python
dir(__builtin__)
```

### 包

- 包是结构化 Python 模块的命名空间的一种方式, 以 `点标记法` 表示. `A.B` 表示包 A 下名为 B 的模块.
- `__init__.py` 是必需要的, 它让 Python 将目录当作包对待. 最简单的使用是空的 `__init__.py` 文件.
- `from package import item`, item 可以是子模块/子包 或者包内定义的其他`名称`, 比如函数/类/变量
- `import` 语句首先检测 `item` 在包内是否有定义; 如果没有, 则假设这是一个模块, 并尝试加载模块; 如果找不到, 抛出 `ImportError` 异常
- `import item.subitem.subsubitem` 则除了最后的 `subsubitem`, 所有的其他 `item` 必须是包; 但是 `subsubitem` 可以是模块或包, 但不能是函数/类/变量
- `from item import * ` 会在文件系统 (goes out to filesystem) 的包目录查找子模块, 并全部导入. 导入时间长, 且导入的子模块会产生副作用 (混淆命名空间).
- 对于 `from item import * `, 包的作者应该构建明晰的索引. `import` 语句的机制: 如果包的 `__init__.py` 定义了 `__all__`, 则遇到 `from item import * ` 时, 将加载 `__all__` 所列的模块名; 否则如果没有 `__all__`, 则`from item import * ` 不会导入 item 下所有的子模块到当前命名空间, Python 解释器只会确保已经导入了 `item`, 然后导入 item 层面上所有的名称.
- `from package import submodule` 是推荐做法

#### 包内引用

- 模块之间可能需要相互引用. 事实上, `import` 语句首先会查看上层的包, 其次才会查看要导入的模块. 因此, 包内模块间相互引用是很平常的. 如果当前子模块的上层包没有需要导入的模块, 则会再向上级包进行搜索, 最后到顶层包
- 隐式或显式的相对导入, 都是基于当前模块名的. 主模块名总是 `__main__`

## Chapter 7 Input and Out

- 通过 `repr()` 或 `str()` 函数, 可以将任何值转化为 string: 前者生成解释器可读的内容, 后者生成人可读的. 
- 字符串和浮点数, 实际上, 有两种不同的表示方式
- `str.rjust()` - 右对齐. 类似的还有 `str.ljust()`, 和 `str.center()`
- 对于数字字符串, `str.zfill()` 会在数字前补零, 会智能识别正负号
- `"{0}".format("kissg")` - 花括号中的数字表示传入 `str.format()` 方法的对象的位置, 也可以不要; 如果 `str.format()` 使用了关键字参数, 则花括号内也可用参数名; 关键字参数和位置参数可以任意组合; `!s` 应用于 str() 或 repr(), 可以在格式化之前对值进行转换; 字段名之后可跟 `:` + 格式说明符 (specfier), 提供对格式化更多的控制;
- 字典加 `str.format()`:

```python

>>> table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 8637678}
>>> print ('Jack: {0[Jack]:d}; Sjoerd: {0[Sjoerd]:d}; '
...        'Dcab: {0[Dcab]:d}'.format(table))
Jack: 4098; Sjoerd: 4127; Dcab: 8637678

>>> table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 8637678}
>>> print 'Jack: {Jack:d}; Sjoerd: {Sjoerd:d}; Dcab: {Dcab:d}'.format(**table)
```

- 内建的 `vars()` 函数将以字典的形式泛湖所有的局部变量
- 旧的格式化字符串方式: `%` 占位替换
- `open()` 的 `r+` 模式, 可读可写
- Windows 平台上, Python 对于文本和二进制文件做了区分; 文本文件, 行结束符会被自动转换, 这种对于文件数据的静默修改, 对文本文件是友好的, 对二进制文件会出错. 
- Unix 平台上, 追加 `b` 是无害的
- `f.readline()` - 会返回带换行符 (\n) 的字符串. 尾行没有换行符, 因此不带 `\n`.
- 按行读取文件, 高效简单的方法:

```python
for line in f:
    print line,
```

- `list(f)` or `f.readlines()` - 以 list 的形式返回所有的行. 后者应该说更 Pythonic 吧
- `f.write(string)` - 对于非 str 的值, 需要转为 str 先
- `f.tell()` - 返回表示文件对象当前位置的整数. (位置以字节计算, 参考位置是文件头); `f.seek(offset, from_what)` - 修改文件对象的位置, 在参考点 from_what 上加上 offset, from_what: {0: 文件头, 1: 当前位置, 2: 文件尾}, 缺省时为 0
- `with` 语句和文件对性更搭哦. 任务完成或抛出异常时, 会恰当地关闭文件

#### saving structured data with json

- `f.read()` - only returns strings. 因此字符串-文件的读写很方便, 但数值型就需要多一点处理
- 当需要保存更多复杂的数据类型, 比如嵌套的列表或字典时, 手动解析与序列化会使工作变得方便一点
- 将层级数据转换成字符串的过程称为序列化 (serializing)
- json 只能对列表和字典进行序列化, 各种语言通用; pickle 可以对任意类型的对象进行序列化, 但是只适用于 Python, pickle 默认是不安全的: 其反序列化的数据如果来自不可信的源, 可能会执行任意代码

## Chapter 8 错误与异常

- 运行时检测到的错误称为 `异常`: 可处理的, 不是致命的 (fatal).
- 大多数异常, 程序是不会自动处理的, 会抛出错误消息
- [Built-in Exceptions](https://docs.python.org/2/library/exceptions.html#bltin-exceptions)
- `try ... except ...` 语句, 异常如果是 `except` 的, 执行其下的语句, 否则将抛至 `try` 语句之外, 若外围还是没有相应的 handler, 没有处理的异常会导致执行停止
- `except ValueError, e:` 是 `except ValueError as e:` 的变形, 有别于 `except (valueError, TypeError):`
- `except`可以省略异常名, 但是要千万小心. 这种方式很容易使造成真正的程序错误

```python
try:
    pass
except IOError as e:
    pass
except ValueError:
    pass
except:
    raise
```

- `try ... except ... else ...`
- 异常可能有相应的值, 称为异常参数. 是否有参数以及参数的类型根据异常类型有不同
- 可以为异常指定变量, 这样变量将绑定到异常实例上, 保存在 `instance.args` 中. 异常实例定义了 `__str__()` 方法, 可以直接打印, 而不必使用 `.args` 引用:

```python
try:
    raise Exception("spam", "eggs")
except Exception as inst:
    pritn inst
    print inst.args
```

- 带参数的异常, 如果未处理, 参数将作为错误消息的最后一部分被打印
- `raise` 的唯一参数是待抛出的异常, 可以是异常实例或异常类. 其实还可缺省, 这样捕获的异常将再次被抛出
- 自定义异常类, 需要继承自 `Exception`, 直接或间接的.
- 异常类通常保持简单, 只提供一些向 handler 提供信息的属性即可.
- 当创建可以抛出多个不同异常的模块时, 常规的做法是创建一个异常的基类, 然后再根据不同的错误条件创建不同异常子类
- 大多数异常都以 `Error` 结尾, 以保持与标准异常的一致
- `finally` 的作用是作为 `clean-up` 行为, 其一定会被执行.
- 未被捕获异常, 在 `finally` 语句块之后被抛出.
- `finally` 语句块还被当作 `on the way out` 使用, 当 try 语句被 `break`, `continue`, `return` "耽误"的时候
- 实际应用中, `finally` 语句块对于释放外部资源有用 (打开文件或网络连接).


## Chapter 9 Classes

- 多父类继承，可覆盖任何父类方法，方法可通过相同的方法名调用父类方法，属性数量不限
- 类成员都是公有的，所有成员函数都是虚的，
- 成员函数显示地声明第一个参数是对象本身，但隐含地使用，
- 类本身就是对象
- 内建类可以作为基类用于扩展
- 带特殊语法的内建操作符可被类实例重定义
- 对象有私有特征，并且同一个对象可以绑定的多个名字。别名在一些方面有点像指针

### 命名空间
 
- 命名空间是名称到对象的映射。目前，大多数的命名空间是以 Python `字典`形式实现的
- 对象的属性集也是命名空间的一种形式
- 不同命名空间的名称绝对没有任何联系，所以不同模块下定义的同名函数不会有冲突
- 严格地讲，模块下对名称的引用是对属性的引用
- 模块也是一个对象吧？
- 模块属性是可写的，可写的属性可能可以用 del 删除
- 命名空间在不同的时刻被创建，拥有不同的生存周期。带内建名称的命名空间在 Python 解释器起来的时候被创建，并永远不会被删除
- 模块的全局命名空间在模块定义被读入的时候创建，正常情况下，也会持续到解释器退出
- 内建名称实际上都放在 `__builtin__` 模块中
- 解释器顶层调用执行的语句, 无论是交互式的还是从脚本执行, 都被视为 `__main__` 模块的一部分

### 作用域

- 作用域是 Python 程序的一个字面概念, 它表示命名空间是"直接可访问". 所谓"直接可访问"的意思是, 对名称不合格的引用尝试着在命名空间查找名称
- 运行时, 至少有 3 个嵌套的作用域的命名空间是直接访问的:
    1. 最内层的作用域, 首先被搜索, 包含局部名称
    2. 闭包函数的作用域, 包含非局部, 但也非全局的名称
    3. 当前模块的全局名称
    4. 最外层的作用域, 包含内建名称
- 若某个名称被声明是全局的, 则对其所有的引用和赋值都直接作用于上述包含模块的全局变量名的作用域.
- 所有最内部作用域之外的变量都是只读的 (对于这些变量的写, 会在最内层作用域创建一个新的局部变量, 而保持同名的外部变量不变)
- 通常地, 局部作用域引用当前函数的局部名称; 对于外部函数, 局部作用域引用全局作用域的的相同命名空间: 模块的命名空间. 类定义会在局部作用域设置另一个命名空间
- `作用域是字面的概念`: 定义在模块内的函数的全局作用域是模块的命名空间
- 名称的搜索是动态进行的
- 如果没有 `global` 语句, 则对名称的赋值总是在最内层的作用域. `赋值不会复制数据, 只是将名称绑定到对象上`. 同样地, `del 只是从命名空间删除绑定`.
- 所有使用到新名称的操作都是用的局部命名空间

### 初窥类

- 进入类定义之后, 会创建一个新的命名空间, 作为局部作用域. 因此, 所有对局部变量的赋值都是在新的命名空间下进行的, 函数定义会在此绑定一个新的函数名
- 退出函数定义后, 就创建了一个类对象. 类对象被绑定到类定义时给的类名上

#### 类对象

- 类对象支持两类操作: `属性引用`, `实例化`
- 属性引用就是: `obj.name`. 有效的属性名称就是类对象被创建之后, 类命名空间中有的名称.
- 类的实例化使用函数的记法.
- 当类定义了 `__init__()` 方法, 类的实例化会自动调用 `__init__()` 用于类的实例化.

#### 实例对象

- 实例对象明白的唯一的操作就是属性引用.
- 有 2 种有效的属性名称: 数据属性和方法
- Python 中, `方法` 的概念不是类实例独有的. 比如 list 对象就有 append 等方法
- 根据定义, 类中定义的函数对象, 与其类实例的方法是相对应的.`x.f` 是有效的方法引用, `MyClass.f` 是一个方法, 但是这两者又是不同的, `x.f` 是一个`方法对象`, 而不是函数对象
- `x.f()` 实际等价于 `MyClass.f(x)`.
- 当一个实例的属性 (非数据属性) 被引用时, 其类将被搜索. 如果名称是一个有效的类属性, 即一个函数对象, 那么用实例对象创建一个方法对象. (可以说, 方法对象是函数对象的一个抽象对象). 当通过一个参数列表调用方法时, 会自动创建一个新的参数列表, 由实例对象和给定的参数列表组成, 然后用新的参数列表调用函数对象.

#### 类与实例变量

- 实例变量对于每个实例都是独有, 类变量赠诗该类的所有实例共享的属性和方法
- 通过可变对象来共享数据可能会产生意想不到的作用.

### 随机备注

- 同名数据属性会覆盖方法属性. 避免冲突的一种方法是: 数据名用名词, 方法名用动词
- 数据属性可以被方法或用户引用, Python 无法实现纯抽象数据类型. 事实上, 在 Python 中, 没法使数据真正隐藏
- 一个类绝不会作为全局作用域使用, 一般也不会在方法中使用全局数据.
- 全局作用域的合法使用: 被导入全局作用域的函数和模块, 可以全局作用域内的方法, 函数, 类使用

### 继承

- 继承类时, 父类名必须在包含子类的作用域内有定义. 可用任意表达式表示父类名称, 比如 `class DerivedClassName(modname.BaseClassName):`
- 当类对象被构造时, 父类信息被保存, 这解决了属性引用的问题: 若请求的属性在当前类中找不到, 则会 (递归地) 在父类中查找
- c++ 的概念, Python 的所有方法都是`虚`的
- 调用父类方法的直接方式: `BaseClassName.methodname(self, arguments)`. (该写法只对 `BaseClassName` 在全局作用域可访问有效)
- 两个与继承有关的内建函数:
    1. `isinstance()`
    2. `issubclass()`
- Python 有限制地提供对多重继承的支持. 旧式风格的类, 多重继承的顺序是: `深度优先, 从左到右`. 新式风格的类, 方法的继承顺序改为动态的, 以支持对相应地调用 `super()` 的支持. 在其他多继承语言中, 这种方式又被称为"调用下一个方法", 比单一继承语言的调用更强大
- 新式风格的类, 继承的动态顺序是必要的. 多重继承的总体关系呈菱形. 所有的父类最终都继承自 `object`. 与那次, 多重继承就提供了到 `object` 的多条路径...?

### 私有变量与类局部引用

- "私有" 实例变量 (只能在对象内部被访问) 在 Python 中是不存在的.
- 但有一条普遍接受的规范: 以单下划线作为前缀的名称 (如 `_spam`) 应该当作 API 的非公开部分对待
- 名称转换机制, 任何以双下划线作为前缀的属性名, 会被转化为 `_classname__spam` 的形式, 即在前面又加上了 `_classname`
- 名称转化机制对于子类在不破坏类间方法调用的前提下覆盖方法很有帮助.
- 名称转化机制大多数情况下被设计用于避免冲突. 有时也可以用于处理"私有"的问题
- 传给 `exec`, `eval()`, `execfile` 的代码不会将调用类的类名作为当前类; 类似于 `global` 语句, 其效果限于一起被字节编码的代码.
- 以上限制, 对于 `getattr()`, `setattr()`, `delattr()` 同样适用. 直接引用 `__dict__` 也一样.

### Odds and Ends

- 抽象数据类型 - 仿真, 类 XX 对象
- `raise` 的 两种格式:
    1. `raise Class, instance` - instance 必须是 Class 或其子类的实例
    2. `raise instace` - raise instance.__class__, instance 的简写
- 多 `except` 语句, 逐层向外抛, 逐层捕获
- 错误消息的格式: `异常类名: str(异常实例)`

### Iterators and generators

- `for` 语句对容器对象调用 `iter()`, 并返回一个 `iterator obj`, 该对象定义了 `next()` 方法用于一次返回一个元素. 当容器没有元素时, `next()` 会抛出 `StopIteration` 异常 作为 `for` 循环的结束
- 定义 `iterator`, 需要定义一个 `__iter__` 方法, 该方法利用 `next()` 返回一个对象.
- 若类定义了 `next()`, 则 `__iter__()` 返回 `self` 即可.

```python
class Reverse:
    """Iterator for looping over a sequence backwards."""
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def next(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]
```

- `generator` 是 iterator 的优雅实现方式, 像写函数一样, 使用 `yield` 语句返回数据.
- generator 自动实现了 `__iter__()` 和 `next()`, 并且会自动保存局部变量和执行状态, 并自动抛出 `StopIteration` 终止 generator.
- 每次调用 `next()`, generator 从上一次暂停点恢复.
- `generator exp` 相比完整的 generator 更紧凑, 但没那么通用; 与列表推导式相比, 内存的使用更合理

## Chapter 10 Brief Tour of the Standard Library

### 操作系统接口

- `os` 模块提供了大量与操作系统交互的函数
    - `os.getcwd()` - # Return the current working directory
    - `os.chdir(path)`
    - `os.system(cmd)` - Execute the command (a string) in a subshell
## Chapter 10 Brief Tour of the Standard Library
- `dir`, `help()`
- `shutil` - 提供了文件和目录管理的更高层接口. (Utility functions for copying and archiving files and directory trees)

### 文件通配符

- `glob` 提供了使用通配符从目录获取匹配的文件列表的函数

### 命令行参数

- 命令行的参数保存在 `sys` 模块的 `argv` 属性中, 以列表保存.
- `getopt` 模块使用 Unix `getopt()` 的惯例处理 `sys.argv`.
- `argparse` 模块提供了更强大灵活的命令行处理机制

### 错误输出重定向与程序终止

- `sys` 模块提供了 `stdin`, `stdout`, `stderr`.
- `stderr` 对于发送警告饿错误消息有帮助, 即使 `stdout` 被重定向了.
- 最直接终止脚本的方式: `sys.exit()`

### 字符模式匹配

- `re` 模块提供了正则表达式工具, 用于复杂的匹配或操作, 以及优化操作.
- 简单的操作, 使用字符串方法即可

### 数学

- `math` 模块提供了对底层 C 库函数的访问, 以提供对浮点数学的支持
- `random` 模块提供了随机选择的工具

### 访问 Internet

- `urllib2` 用于从 URLs 解析数据
- `smtplib` 用于发送邮件

### 日期与时间

- `datetime` 模块同时提供了简单和复杂的用于日期和时间操作的类, 以及日期与时间的算术运算. 该模块的核心是输出格式化与操纵. 提供时区信息

### 数据压缩

- 相关的模块有 `zlib`, `gzip`, `bz2`, `zipfile`, `tarfile`

### 性能检测

- `timeit`
- `profile`, `pstats` 模块提供了鉴别大型代码块关键部分的功能.

### 质量控制

- `doctest` 模块提供了扫描模块, 并验证程序的 docstrings
- `unittest` 允许在分离的文件中写更多复杂的测试用例

### 自带电池

- `xmlrpclib` 和 `SimpleXMLRPCServer` 模块使远程进程调用变得简单. 无论模块名为何, 也不需要处理 XML 的知识
- `email` 是管理 Email 消息的库, 提供了创建或解码复杂消息结构的完整工具集, 也可以用于协议头的编码
- `stmplib` 和 `poplib` 收发邮件.
- `xml.dom`, `xml.sax` 提供了对解析 xml 的支持.
- `csv` 提供了对 csv 文件的直接读写
- `gettext`, `locale`, `codecs` 提供了国际支持

## Chapter 11 Brief Tour of the Standard Library 2

### 输出格式化

- `repr` 模块提供了另一个版本的 `repr()`, 用于自定义展示大型或深度嵌套的容器
- `pprint` 模块提供了更精致的打印控制
- `textwrap` 模块对于给定的屏幕宽度, 格式化段落
- `locale` 模块以特定的数据格式访问数据库

### 模板

- `string` 模块包含了一个通用 `Template` 类, 允许用户自定义应用. 使用 `$` 作为占位符, 调用 `substitute` 进行替换, 该方法在数目不匹配等情况下会抛出 `KeyError` 异常, 更安全的写法是 `safe_substitute()`, 在填充不足时, 原样输出.
- 模板的一个用途是, 批量处理

### 二进制数据记录展示

- `struct` 模块提供了 `pack()` 和 `unpack()` 函数用于可变长度二进制记录的格式化.
- 压缩时, `H`, `I` 分别表示 2 个, 4 个字节无符号数.
- `<` 表示标准尺寸, 字符编码顺序是小端

### 多线程

- 多线程是将顺序无关的多个任务解耦的技术.
- 多线程可以提高应用的响应速度. 一个用例是, 当一个线程在做计算时, 进行 IO
- `threading` 模块提供了高级的多线程操作
- 多线程应用的主要挑战是`合作进程间的数据或其他资源共享`. `threading` 模块提供了一些同步原子操作, 包括锁, 事件, 条件变量, 信号量
- 尽管多线程工具很强大, 但极小的设计错误都会导致巨大的问题. 因此, 一个更好的方式可能是`合作的任务集中在一个线程对资源进行访问, 使用 Queue 模块来发送消息请求资源的访问`
- 使用 `Queue.Queue` 对象作为进程间通信与合作的应用易于设计, 且具有更好的可读性可靠性

### 日志

- `logging` 模块提供了全功能灵活的日志系统.
- info 和 debug 消息默认是禁用的, 并且其输出是到标准错误. 其他的输出还包括通过 email, 数据报, sockets, 或 HTTP 服务器的路由消息.
- 日志系统可直接通过代码进行配置, 也可以加载配置文件

### 弱引用

- Python 自动管理内存: 对对象最后的引用被移除之后, 对象从内存中被删除, 释放内存
- 有时候可能有主要的需求: 跟踪对象, 只要它们被使用了. 但是跟踪对象需要创建一条引用, 从而使得对象一直存在. `weakref` 模块提供了跟踪对象但不创建引用的方法: 当对象不再被需要的时候, 将自动从 weakref table 中删除, 并由 weakref 对象触发一个回调. 典型的应用包括缓存创建消耗大的对象:

```python

>>>
>>> import weakref, gc
>>> class A:
...     def __init__(self, value):
...         self.value = value
...     def __repr__(self):
...         return str(self.value)
...
>>> a = A(10)                   # create a reference
>>> d = weakref.WeakValueDictionary()
>>> d['primary'] = a            # does not create a reference
>>> d['primary']                # fetch the object if it is still alive
10
>>> del a                       # remove the one reference
>>> gc.collect()                # run garbage collection right away
0
>>> d['primary']                # entry was automatically removed
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    d['primary']                # entry was automatically removed
  File "C:/python26/lib/weakref.py", line 46, in __getitem__
    o = self.data[key]()
KeyError: 'primary'
```

### 与 List 配合的工具

- `array` 模块提供 `array()` 对象, 类似于 list, 只存储同治数据, 更紧凑
- `collections` 模块提供了 `deque()` 对象, 也类似于 list, 但从左侧 append 或 end 更高效, 但是对于中间的查找更慢. 该对象适合用于实现队列, 以及广度优先搜索树
- `bisect` 模块提供了对有序 list 更好的操作
- `heapq` 模块提供了用于实现基于常规 list 的堆的函数: 最小的值总是被存放在位置 0. 这对于需要重复访问最小的元素, 但是又不必对整个 list 进行排序的应用很有帮助

### 十进制浮点算术

- `demical` 模块提供了 `Decimal` 数据类型, 与内建的 `float` (二进制浮点)相比的优点是:
    - 金融应用与其他需要更精确十进制表示的应用
    - 精度控制
    - 舍入控制, 以满足法律法规要求
    - 跟踪重要的小数位
    - 手动匹配结果
