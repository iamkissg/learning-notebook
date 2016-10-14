# PEP8 编程风格

## A Foolish Consistency is the Hobgoblin of Little Minds

> 愚蠢的代码一致性是小心思的怪胎

- 代码被读的频率比被写高得多, 因此代码的可读性, 很重要!!!
- `一致性`很重要, `一个项目内的一致性` (Consistency within a project) 更重要, `模块或函数内部的一致性` (Consistency within one module or function) 又是这其中最重要的
- 然而最重要的还是: 知道什么时候不需要`一致性`. 所谓的编程风格其实并不适用于所有情况. 当有疑虑时, 使用你的最佳判断.
- `保持向后兼容`
- 可忽略编程规范的情况:
    - 应用此编程规范会使代码可读性下降
    - 需要保持上下文代码的一致性
    - 写于此编程规范之前的代码
    - 代码需要与旧 Python 版本兼容, 并且它不支持编程规范的功能

## 代码布局

#### 缩进

- 使用 4 空格的缩进
- 行的连续需要垂直对齐, 比如圆括号, 方括号, 花括号内的元素. 或者使用悬挂缩进, 此时需要注意: 第一行不应有任何参数, 应能从缩进清晰地看出这是多行连续

```python
# 正确示范
# Aligned with opening delimiter.
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# More indentation included to distinguish this from the rest.
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# Hanging indents should add a level.
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)

```

```python
# 错误示范
# Arguments on first line forbidden when not using vertical alignment.
foo = long_function_name(var_one, var_two,
    var_three, var_four)

# Further indentation required as indentation is not distinguishable.
def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)
```

- 对于多行连续, 4 空格缩进是可选的, 只要满足上述条件(能清晰地表示多行连续), 合适就好:

```python
# Hanging indents *may* be indented to other than 4 spaces.
foo = long_function_name(
  var_one, var_two,
  var_three, var_four)
```

- 当 if 语句的条件过长, 需要写成多行时, 使用`关键字`加`空格`加`子行的 4 空格缩进`来表示. 但是这可能会造成视觉上的混乱. 因此, 以下几种方式都可以:

```python
# No extra indentation.
if (this_is_one_thing and
    that_is_another_thing):
    do_something()

# Add a comment, which will provide some distinction in editors
# supporting syntax highlighting.
# 插入注释, 对于带语法高亮的编辑器, 可一眼就看出哪里是条件, 哪里是代码块
if (this_is_one_thing and
    that_is_another_thing):
    # Since both conditions are true, we can frobnicate.
    do_something()

# Add some extra indentation on the conditional continuation line.
if (this_is_one_thing
        and that_is_another_thing):
    do_something()
```

- 连续多行情况下, 右括号既可以和最后一行保持相同的缩进, 也可以和第一行保持相同的缩进:

```python
my_list = [
    1, 2, 3,
    4, 5, 6,
    ]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
    )

my_list = [
    1, 2, 3,
    4, 5, 6,
]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
)
```

#### Tabs 还是 Spaces

- Spaces are the preferred indentation method
- Tabs 应只用于已经用 tabs 缩进的旧式代码, 以保持`一致性`
- Python 3 不允许 tabs 和 spaces 的混合缩进 (会直接报错)
- Python 2 应将使用混合缩进的代码转换为只使用空格缩进
- 当使用 `-t` 启用 Python 2 的解释器时, 会对非法的 tabs 和 spaces 混合使用发出警告. 使用 `-tt`, 警告会变成错误, 因此, 强烈建议这样使用

#### Maximum Line Length

- 限制所有行在 79 个字符以内
- 对于 docstrings 或 注释, 行长应限制在 72 个字符之内
- 限制编辑器窗口的宽度, 就可以横向排列同时打开多个文件. 尤其适用于使用代码 review 工具来进行比对的情况.
- 大多数工具的自动换行会严重破坏代码的视觉结构, 影响阅读理解. 因此, 79 个字符的限制, 可以在窗口宽度为 80 的情况下避免自动换行, 即使工具会在最后一列添加字形标记 (marker glyph).
- Python 标准库采用了保守的 79/72 的长度限制.
- 长行换行的推荐方式是, 在各种括号中, 将长行切分成多行. 或者使用 Python 的隐含行连续 `\`
- 使用 `\`, 可以处理很长的 `with 语句`, `if 语句`, `assert 语句`等很多情况
- 在控制行长度的时候, 要确保恰当的缩进. 恰当的断行应在二进制操作符 (哥们, 是什么) 之后, 而不是之前.

```python
class Rectangle(Blob):

    def __init__(self, width, height,
                 color='black', emphasis=None, highlight=0):
        if (width == 0 and height == 0 and
                color == 'red' and emphasis == 'strong' or
                highlight > 100):
            raise ValueError("sorry, you lose")
        if width == 0 and height == 0 and (color == 'red' or
                                           emphasis is None):
            raise ValueError("I don't think so -- values are %s, %s" %
                             (width, height))
        Blob.__init__(self, width, height,
                      color, emphasis, highlight)
```

#### 空行

- 顶层函数和类的定义, 应用 `2` 行空行标明
- 类内方法用 `1` 行空行标记
- 额外的空行用于分离相功能相近的代码块 (惜行).
- 一堆相近的单行之间可省略空行, 比如 a set of dummy implementations
- 在函数内使用空行, 以区分逻辑块
- Python 接受 `ctrl-L` (`^L`) 作为空白字符, 许多工具也将这个标记作为换页符, 因此可以用 `^L` 作为文件中相近块的页分离. 另一些编辑器和基于网页的代码查看器可能无法识别 `^L`, 而将其替换为另一种字形标记

#### 源文件编码

- Python 发行版的核心代码是 UTF-8 编码的 (Python 2 也可以是 ASCII 编码)
- 以 ASCII (Python 2) 或 UTF-8 (Python 3) 编码的文件不需要编码声明
- 在标准库中, 非默认编码应只用于测试, 或者注释和 docstring 涉及非 ASCII 字符的作者名字的. 否则, 建议使用 \x, \u, \U, \N 转义非 ASCII 字符串
- 对于 Python 3.0, 下述规则在标准库 (PEP 3131) 已经描述过:
    - Python 标准库的标识符`必须`使用 ASCII 字符, 并且`应该` 用英文字符
    - 此外, 描述性字符串和注释必须使用 ASCII. 唯一的例外是:
        1. 对非 ASCII 的功能测试
        2. 作者名字, 若不是拉丁语系的名字, 必须提供一个音译版名字
- 全球性的开源项目都提供类似的规则

#### 导入

- 导入应该使用分离的行, 即一行只导入一项:

```python
# 正确示范
import os
import sys

# 错误示范
import os, sys
```

- 但从一个库导入多个模块是可行的: `from subprocess import Popen, PIPE`
- 导入应总是位于文件顶部, 在模块注释和 docstrings 之后, 模块内定义的全局变量和常量之前
- 导入应下列顺序分好组, 每组之间用空行区分
    1. standard library imports
    2. related third party imports
    3. local application/library specific imports
- 建议使用`绝对导入`, 它们通常可读性更强, 在导入系统配置不正确时表现也会更好 (至少错误消息会更准确)
