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

- 形如 `from subprocess import Popen, PIPE` 的导入是可以的
- 导入总是位于文件的头部, 在模块注释和 docstrings 之后, 模块的全局变量和常量之前
- 导入应当以下列顺序分组:
    1. 标准库的导入
    2. 相关第三方库的导入
    3. 本地应用/库的导入
- 应该在每组导入之间插入空行, 以示区别
- Put any relevant `__all__` specification after the imports.
- 建议使用`绝对导入` (使用绝对路径), 这样通常更具可读性, 当导入系统没有配置正确时, 往往也表现得更好 (或者说至少会给出更好的错误信息).
- `显式的相对导入`是绝对导入的可接受替代品, 特别是当包布局很复杂时,使用绝对导入会显得冗余
- 标准库代码应当避免使用复杂的包布局, 并始终使用绝对导入
- 隐式的相对导入绝不应该使用, 在 Python 3 中已经被移除
- 当从一个包含类 (class-containing) 模块导入类时, 以下写法也是可以的:

```python
from myclass import MyClass
from foo.bar.yourclass import YourClass
```

- 但是如果上述导入会造成局部命名冲突, 直接导入模块就好:

```python
import myclass
import foo.bar.yourclass
```

- 通配符导入(`from <module> import *`) 应该避免, 它使命名空间存在变得模糊, 对于读者与许多自动化工具都会造成困扰.

#### String Quoted

- 当字符串中包含单引号或双引号时, 使用另一个来避免使用反斜杆来转义, 这样可读性更好
- 三引号, 始终使用双引号来与 [PEP 257](https://www.python.org/dev/peps/pep-0257/) 中的 docstring 用例保持一致

## 表达式与语句中的空白字符

#### Pet Peeves

- 下列情况, 避免使用多余的空白字符:
    - 各种括号内, 紧随括号的情况
        - 正确示范: `spam(ham[1], {eggs: 2})`
        - 错误示范: `spam( ham[ 1 ], { eggs: 2 } )`
    - 逗号 (comma), 分号 (semicolon), 冒号 (:) 之前:
        - 正确示范: `if x == 4: print x, y; x, y = y, x`
        - 错误示范: `if x == 4 : print x , y ; x , y = y , x`
    - 然而, 切片语法中, 冒号更像是一个二进制操作符, 因此, 在其两边应使用相同数量的空白字符. 多切片的情况, 也应如此. 例外是省略切片参数的情况, 此时空格省略:

```python
# 正确示范
ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3], ham[1:9:]
ham[lower:upper], ham[lower:upper:], ham[lower::step]
ham[lower+offset : upper+offset]
ham[: upper_fn(x) : step_fn(x)], ham[:: step_fn(x)]
ham[lower + offset : upper + offset]
```

```python
# 错误示范
ham[lower + offset:upper + offset]
ham[1: 9], ham[1 :9], ham[1:9 :3]
ham[lower : : upper]
ham[ : upper]
```

- 函数调用, 参数列表的圆括号之前的:
    - 正确示范: `spam(1)`
    - 错误示范: `spam (1)`
- 索引或切片的方括号之前:
    - 正确示范: `dct['key'] = lst[index]`
    - 错误示范: `dct ['key'] = lst [index]`
- 为了保持一致, 在赋值操作符 (或其他) 周围使用多余的空格:

```python
# 正确示范
x = 1
y = 2
long_variable = 3
```

```python
# 错误示范

x             = 1
y             = 2
long_variable = 3
```

#### 其他建议

- 避免使用尾空白字符 (trailing whitespace). 它通常是不可见的, 但会造成困扰, 比如反斜杆之后跟了一个空格, 那么新行就不会被视作多行连续的一部分.
- 始终在下列二进制操作符两边使用一个空格包裹:
    - 赋值 (=)
    - 增量赋值 (augmented assignment) (+=, -= 等)
    - 比较 (==, <, >, !=, <>, <=, >=, in, not in, is, is not)
    - 布尔 (and, or, not)
- 如果使用了不同优先级的操作符, 可以考虑在优先级最低的操作符周围使用空白字符. 自己判断, 但不要使用多于 1 的空格, 在一个二进制操作符两边使用数量的操作符

```python
# 正确示范
i = i + 1
submitted += 1
x = x*2 - 1
hypot2 = x*x + y*y
c = (a+b) * (a-b)
```

```python
# 错误示范
i=i+1
submitted +=1
x = x * 2 - 1
hypot2 = x * x + y * y
c = (a + b) * (a - b)
```

- 当 `=` 用于关键字参数或默认参数值时, 不用在其两边加空格

```python
# 正确示范
def complex(real, imag=0.0):
    return magic(r=real, i=imag)
```

```python
# 错误示范
def complex(real, imag = 0.0):
    return magic(r = real, i = imag)
```

- 函数说明 (Function annotations) 应该使用正常的冒号用法, 始终在 `->` 两边使用空格:

```python
# 正确示范
def munge(input: AnyStr): ...
def munge() -> AnyStr: ...
```

```python
# 错误示范
def munge(input:AnyStr): ...
def munge()->PosInt: ...
```

- 当联合使用参数说明 (argument annotation) 和 默认值时, 在 `=` 两边使用空格 (只对同时具备参数说明和默认值的情况有效):

```python
# 正确示范
def munge(sep: AnyStr = None): ...
def munge(input: AnyStr, sep: AnyStr = None, limit=1000): ...
```

```python
# 错误示范
def munge(input: AnyStr=None): ...
def munge(input: AnyStr, limit = 1000): ...
```

- 通常不建议使用复合语句 (即多条语句写在同一行):

```python
# 正确示范
if foo == 'blah':
    do_blah_thing()
do_one()
do_two()
do_three()
```

```pyython
# 错误示范
if foo == 'blah': do_blah_thing()
do_one(); do_two(); do_three()
```

- 尽管主体很小的时候, 可以将 if/for/while 语句写成一行, 但绝对不要将此用于多条语句. 同样的, 避免折叠长行:

```python
# 错误示范
if foo == 'blah': do_blah_thing()
for x in lst: total += x
while t < 10: t = delay()
```

```python
# 错误示范
if foo == 'blah': do_blah_thing()
else: do_non_blah_thing()

try: something()
finally: cleanup()

do_one(); do_two(); do_three(long, argument,
                             list, like, this)

if foo == 'blah': one(); two(); three()
```

## Comments

- 与代码不一致的注释甚至比没有注释更差. 修改代码的时候, 保持更新注释的好习惯
- 注释应该是完整的句子. 若注释是一个词组或句子, 第一个单词应该首字母大写, 除非是标识符
- 如果注释很短, 可省略末尾的句号. 块状注释通常由段落组成, 段落由以句号结束的完整的句子组成
- 在标志结束的句号之后应使用 2 个空格
- 以英语注释!

#### 块状注释

- 块状注释写在被注释的代码之前, 与代码保持相同的缩进. 每行注释以 `# `开始 (# 还之后跟一个空格)
- 块状注释的段落间, 由单行 `#.` 分离

#### 行内注释

- 保守地使用行内注释
- 行内注释与代码之后至少有 2 个空格
- 行内注释是不必要的. 事实上, 如果代码写得很明显, 它们还会使读者分心

#### Documentation Strings

> Write docstrings for all public modules, functions, classes, and methods. Docstrings are not necessary for non public methods, but you should have a comment that describes what the method does. This comment should appear after the def line.

- [PEP 257](https://www.python.org/dev/peps/pep-0257/)
- 单行的 docstrings, `""""""` 写在同一行
- 多行的 docstrings, 以 `"""` 作为尾行结束

## Version Bookkeeping

- 如果使用版本控制, 在模块的 docstrings 之后, 在代码之前, 前后空一行, 著名 `__version__ = "$Revision$"`

## Naming Conventions (约定)

- Python 库的命令约定有点混乱, 因此不必完全保持命名一致 (也不能). 但仍有建议的命名标准. 新的模块与包(包括第三方框架), 应以这些标准编写, 现有的采用不同风格的库, 应更注重内部一致性

### 首要规则

- 名称对于用户是可见的.
- API 的公共部分应反映使用情况, 而不是实现

#### 命名风格

- 命名风格, 要能清晰地表示其用途. 以下是一些不同的风格:
    - b (单个小写字母)
    - B (单个大写字母)
    - lowercase
    - lower_case_with_underscores
    - UPPERCASE
    - UPPERCASE_CASE_WITH_UNDERSCORES
    - CapitalizedWords (or CapWords, CamelCase, StudlyCaps)
    - mixedCase (differs from CapitalizedWords by initial lowercase character)
    - Capitalized_Words_With_Underscores (丑)
- 在使用 `CapWords` 使用缩写, 注意: `HTTPServerError` 比 `HttpServerError` 更好
- 还有一种命名风格是, 使用`短前缀`来表示分组, 这在 Python 中不常见, 但表达了一种完整性. 在 Python 中不常用, 没必要的原因是, 属性或方法通常通过对象来引用 (作为前缀), 函数则以模块名为前缀
- 使用前导或后缀下划线 (`_`) 也是一种区分:
    - `_single_leading_underscore` - 弱"内部使用"标识符, `from M import *` 不会导入以单下划线开始的对象
    - `single_trailing_underscore_` - 用于避免与 Python 关键字的冲突. 例如: `Tkinter.Toplevel(master, class_='ClassName')`
    - `__double_leading_underscore` - 命名类属性时, 调用名字改编. (在 FooBar 类内部, `__boo` 会变成 `_FooBar__boo`, 之后只能通过 `_FooBar__boo` 访问属性)
    - `__double_leading_and_trailing_underscore__` - "魔法" 对象或属性 that live in user-controller namespaces
    - `__import__` 或 `__file__` - 绝不要编写这类名称; 仅在写文档的时候使用

#### 命名规范

##### 应避免的命名

- 为单字符变量命名时, 绝对不要 `l` (小写的 L), `O` (大写的 oh), `I` (大写的 eye).

##### 包与模块名

- 模块应该使用短的, 全小写的命名. 若有助于可读性, 可在模块名中使用下划线. 包也是同样的道理, 但不要使用下划线
- 当以 C/C++ 写就的扩展发布的 Python 模块提供了更高层次的接口 (更面向对象), C/C++ 模块需要前导下划线

##### 类名

- 类名使用 `CapWords` 规范
- 内建名有点不一样, 大多数是单个单词 (或 2 个单词). `CapWords` 规范只用于异常名和内建的常量

##### 异常名

- 异常是类, 类命名规范同样适用. 但要使用 `Error` 的后缀 (如果真的是错误的话)

##### 类型变量 (Type variable) 名

- 正常情况下, 类型变量名应使用 `CapWords`, 并使用短命. 建议使用 `_co` 或 `_contra` 后缀以表明相应的协变或逆变

```python
from typing import TypeVar

    VT_co = TypeVar('VT_co', covariant=True)
    KT_contra = TypeVar('KT_contra', contravariant=True)
```

##### 全局变量名

(假设这些变量只在一个模块内部使用)

- 全局变量的命名规范与函数一样. 
- 设计成可使用 `from M import *` 的模块, 应使用 `__all__` 机制以防止全局量的导出, 或使用更旧的规范: 全局量使用单下划线前缀 (表明这些全局量是模块非公开的)

##### 函数名

- 函数名应该是小写的, 必要的时候, 单词之间用下划线分离以增加可读性
- `mixedCase` 只在已经大量使用了该风格的情况下使用 (比如 threading.py), 以保持向后兼容

##### 函数与方法参数

- 确保实例方法的第一个参数总是 `self`; 类方法的第一个参数总是 `cls`
- 若一个函数参数名与保留字冲突, 通常更好的最好是添加后缀下划线, 而不是缩写或 spelling corruption. 因此 `class_` 比 `clss` 更好. (也许更好的做法是使用代名词 (synonym)  避免这种冲突)

##### 方法名和实例变量

- 方法命名使用函数的命名规范
- 为非公开方法和实例变量添加前导单下划线
- 为避免与子类的命名冲突, 使用两个前导下划线, 以调用 Python 的名称扇贝规则. Python 识别带类名的名称: 若类 `Foo` 有属性 `__a`, 就不能通过 `Foo.__a` 访问, 只能通过 `Foo._Foo.__a` 访问
- 通常, 双前导下划线应只用于避免父类与子类之间的属性命名冲突

###### 常量

- 常量一般定义在模块级别, 以全大写字母和单词间的下划线组成

##### 继承设计

- 一定要考虑的: 一个类方法或实例变量 (统称为"属性 (attributes)") 是否 public or non-public. 如果有疑惑, 选择 non-public. 将 non-public 属性转为 public 比将 public 转为 non-public 更简单
- Public attributes are those that you expect unrelated clients of your class to use, with your commitment (承诺) to avoid backward incompatible changes. (避免向后不兼容的改变)
- Non-public attributes are those that are not intended to be used by third parties (不期望被第三方使用); you make no guarantees that non-Public attributes won’t change or even be removed. (不必保证这些属性不会改编或移除)
- Python 没有 `private` 的概念, 因为没有属性是真正私有的
- 属性的另一种分类是: 子类 API 的部分 (唤作 "protected"). 一些类设计成需要被继承的, 扩展或修改类的行为. 设计这些类时, 要明确哪些属性是 public, 哪些是 part of the subclass API, 哪些是真正只在基类中使用的

###### Public attributes

- 不需要前导下划线
- 若公共属性名与保留字冲突, 为其添加后缀单下划线 (特例是, `cls` 是 `class` 的一个更普遍被接受的)
- 对于简单的公共数据属性, 最好是只暴露属性名, 不需要复杂的方法.
- Keep in mind that Python provides an easy path to future enhancement, should you find that a simple data attribute needs to grow functional behavior. In that case, use properties to hide functional implementation behind simple data attribute access syntax. (`@property`?)
    - Properties 仅在新式类 (new-style classes) 有效.
    - 尽量保持 functional behavior 无副作用, 尽管像缓存这样的副作用通常是好事
    - 避免在计算消耗型的操作上使用 properties; the attribute notation makes the caller believe that access is (relatively) cheap.
- 如果类有子类, 又有一些不希望子类使用的属性, 考虑使用前导双下划线 (没有后缀下划线). 如前所述, 这会使用 Python 的名称识别算法, 避免类父类与子类的命名冲突
    - 要使用名称识别, 使用简单的类名
    - 名称识别 make certain uses, 例如调试与 `__getattr__()`, 不太方便
    - 不是所有人都喜欢名称识别, 在避免突发名称冲突的需求和调用者的潜在使用之间找一个平衡

#### Public and internal interfaces

- 任何向后兼容的保证只适用于公共接口. 因此, 使用户能清晰地分辨公共与内部接口很重要
- 有文档说明的接口被认为是公共的, 除非文档已经显式地表明这些接口是临时的 (provisional) 或内部的.
- 所有没有文档的接口被当作内部的
- 为了更好的内省 (introspection), 模块应显式地使用 `__all__` 属性来声明公共接口. 当没有公共 API 时, 为 `__all__` 设置一个空列表
- 即使 `__all__` 得到了恰当设置, 内部接口 (包, 模块, 类, 函数, 属性或其他名称) 应该使用前导单下划线的前缀
- 包含命名空间 (包, 模块或类) 的接口也会被当作内部接口
- 导入的名称应该总是被当作实现细节. 其他模块一定不能依赖于非直接的访问, 除非已经显式地说明, 比如 `os.path` 或包的 `__init__` 模块 (暴露了子模块的功能)

## 编程建议

- 代码应以不影响 (坏的) 其他 Python 的实现的方式写就
    - 例如不要依赖于 CPython 的字符串原地 (inplace) 连接: `a += b` 或 `a = a + b`. 即使在 CPython 中, 这个优化也是脆弱的. 考虑到性能, 应使用`"".join()` 形式. 这种方式确保了各种不同实现的时间线性叠加
- 比较单个实例是否 `None`, 使用 `is` 或 `is not`, 永远不要使用相等操作符
- 仅在 `if x is not None` 的情况下, 使用 `if x`
- 使用 `is not`, 而不是 `not  ... is`. 功能相同, 但前者可读性更强
- 要实现排序操作, 最好实现所有的 6 种操作 (__eq__, __ne__, __lt__, __le__, __gt__, __ge__), 而不是依赖其他代码去仅仅实现一个特定的比较. 为了减少劳动量, `funtools.total_ordering()` 装饰器提供了生成遗失的比较方法的工具
- [PEP 207](https://www.python.org/dev/peps/pep-0207/) indicates that reflexivity rules are assumed by Python. 解释器可能会将 `y > x` 替换为 `x < y`, 将 `y >= x` 替换为 `x <= y`, 也可能将 `x == y` 和 `x != y` 的参数进行交换.
- `sort()`, `min()` 操作保证使用 `<` 操作; `max()` 使用 `>` 操作符. 然而, 最好的方式还是实现所有 6 种操作.
- 总是使用 `def` 语句替代直接将 `lambda` 表达式绑定到标识符的赋值语句:

```python
# 正确示范
def f(x): return 2*x

# 错误示范
f = lambda x: 2*x
```

- 第一种形式意味着函数对象的名称就是 `f`, 而不是通用的 `<lambda>`. 这能更好地回溯与表示. 赋值语句消除了 lambda 表达式对于明确的 def 语句独有的优势. (`lambda` 可以放在更大的表达式里使用)
