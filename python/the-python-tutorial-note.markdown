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

## Modules

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

编译后的模块是平台独立的, 因此可以在不同架构下共享.

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

`dir()` 函数查看模块定义的 name, 返回 a sorted list of strings. 无餐调用时, 返回当前定义的 names (包括变量, 函数, 模块等等). 不会返回内建函数或变量名, 要查看这些 (Python 2 无):

```python
import builtins
dir(builtins)
```
