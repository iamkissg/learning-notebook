# Python学习手册

标签（空格分隔）： Python

---

[TOC]

##基本信息

- Python可以做什么？r可以做日常任务，比如自动备份你的MP3；可以做网站，很多著名的网站包括YouTube就是Python写的；可以做网络游戏的后台，很多在线游戏的后台都是Python开发的。总之就是能干很多很多事啦。

- Python当然也有不能干的事情，比如写操作系统，这个只能用C语言写；写手机应用，只能用Swift/Objective-C（针对iPhone）和Java（针对Android）；写3D游戏，最好用C或C++。
- Python的哲学：简单优雅，尽量写容易看明白的代码，尽量写少的代码
- Python的定位是“优雅”、“明确”、“简单”
- 安装Python，自带的解释器是CPython
- 弱类型，动态语言（变量本身类型不固定），严格区分大小写
- 输入与输出：input()与print()函数
- 在Unix下可直接运行.py文件，只需在文件的第一行加上***#!/usr/bin/env python3***注释，但得确保文件有执行权限
- 当语句以冒号“：”，结尾时，之后缩进的语句视为一个代码块

##字符串与编码
- UTF-8编码把一个Unicode字符根据不同的数字大小编码成1-6个字节，常用的英文字母被编码成1个字节，汉字通常是3个字节，只有很生僻的字符才会被编码成4-6个字节。ASCII编码实际上可以被看成是UTF-8编码的一个子集。
- 在计算机内存中，统一使用Unicode编码，当需要保存到硬盘或者需要传输的时候，就转换为UTF-8编码。
- 用记事本编辑的时候，从文件读取的UTF-8字符被转换为Unicode字符到内存里，编辑完成后，保存的时候再把Unicode转换为UTF-8保存到文件：
- 浏览网页的时候，服务器会把动态生成的Unicode内容转换为UTF-8再传输到浏览器
- ***Python 3的字符串使用Unicode***，直接支持多语言
- 对于单个字符的编码，Python提供了**ord()**函数获取字符的整数表示，**chr()**函数把编码转换为对应的字符
- 由于Python的字符串类型是str(以字符为单位)，在内存中以Unicode表示，一个字符对应若干个字节。如果要在网络上传输，或者保存到磁盘上，就需要把str变为以字节为单位的bytes。Python对bytes类型的数据用带b前缀的单引号或双引号表示。
- 以Unicode表示的str通***过encode()***方法可以编码为指定的bytes。纯英文的str可以用ASCII编码为bytes，内容是一样的；含有中文的str无法用ASCII编码，因为中文编码的范围超过了ASCII编码的范围，可以用UTF-8编码为bytes。
- 在bytes中，无法显示为ASCII字符的字节，用\x##显示
- 如果从网络或磁盘上读取了字节流，那么读到的数据就是bytes。要把bytes变为str，需要用***decode()***方法
- 为了避免乱码问题，应当始终坚持使用UTF-8编码对str和bytes进行转换。
- ***#!/usr/bin/env python3***：告诉Linux/OS X系统，这是一个Python可执行程序
- ***# -*- coding: utf-8 -*-***：告诉Python解释器，按照UTF-8编码读取源代码

---

##格式化字符串
- 形如：'Hello, %s' % 'world'。‘%s’称为占位符，有几个***%?***占位符，后面就跟几个变量或者值，顺序要对应好。有多个%?时，要使用***()***
- 还可以通过限定占位符，再做更细致的格式化
- 字符串里面的%是一个普通字符，用%%来转义

---

##数据类型

- 整型：Python可以处理任意大小的整数，在程序中的表示方法和数学上的写法一模一样,十六进制用0x前缀。***Python的整数没有大小限制***
- 浮点数：之所以称为浮点数，是因为按照科学记数法表示时，一个浮点数的小数点位置是可变的。***Python的浮点数也没有大小限制，但是超出一定范围就直接表示为inf***
- 整数和浮点数在计算机内部存储的方式是不同的，整数运算永远是精确的（包括除法），而浮点数运算则可能会有四舍五入的误差。
- 字符串："..."或'...'或'''...'''，转义[print('\\\n\\')]，r'...'表示字符串内默认不转义
- 布尔变量：True或False，
- 空值：None
- 变量：引用值。对变量赋值就是把数据和变量给关联起来。Python的变量是“标签”，C/C++的变量是“盒子（抽屉）”
- 常量：不变的量，Python中通常全部用大写的变量名表示常量。Python没有任何机制保证定义的常量不被改变，全部用大写的变量名表示只是习惯用法

---

##除法
- /：计算结果是浮点数，即使是两个整数恰好整除，结果也是浮点数（其他语言是整除的意思）
- //：计算结果只取结果的整数部分，整数与浮点数作运算，或两个浮点数作运算，结果将为“x.0”
- %：取模

---

##list[]
- 可变的有序集合，即可添加插入删除替换元素
- 可通过索引访问各元素，用-1做索引，直接获取最后一个元素，依次可以使用-2，-3等
- 因为Python是一门动态弱类型语言，list中的元素类型可以不同
- list的元素还可以是另一个list

---

##tuple().
- 不可变有序列表，即不支持增删改
- tuple的陷阱：当你定义一个tuple时，在定义的时候，tuple的元素就必须被确定下来
- 要定义只有一个元素的tuple，必须加一个逗号来消除歧义。a=(1)，()将被认为是数学算式中的小括号，而使a的值为整数1
- 当tuple包含list时，list本身是可变的，但tuple对该list的指向并没有变化。因此，tuple的所谓“不变”是说，tuple的每个元素的，指向永远不变

---

##条件判断
- Python中，“else if”缩写为“elif”
- 0，'',()，等价于False
- 短路：x and y，当x，y均为真时，将返回y；x or y，只要x为真，就返回x；if条件满足，将忽略后面的elif以及else
- 作条件判断时，要注意==，<，>等的左右变量类型相同
- input("xxx")，将输出提示信息xxx，再读入用户的输入

---

##循环
- for x in ... 把集合中的每个元素代入变量x，然后执行缩进块的语句
- range(stop) -> range object
- range(start, stop[, step]) -> range object
- list() -> new empty list
- list(iterable) -> new list initialized from iterable's items
- while 条件表达式

---

##dict
- ditc：在其他语言中也称为map，使用键-值（key-value）存储，具有极快的查找速度
- dict快速查找的原因：dict查找的方法与我们查字典一样。先在字典的索引表里（比如部首表）查这个字对应的页码，然后直接翻到该页，找到这个字
- key-value的存储方式，在放进去的时候，必须根据key算出value的存放位置，这样，取的时候才能根据key直接拿到value。
- D= {x：y}， 初始化指定dict
- D[x]=y    ， 通过key修改值，a为字典名
- x in y       ，判断x是否在y中
- D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None
- dict是用空间来换取时间的一种方法,用在需要高速查找的很多地方
- *dict的key必须是不可变对象,因为dict根据key来计算value的存储位置。通过key计算位置的算法称为哈希算法（Hash）。保证hash的正确性，作为key的对象就不能变*

---

##list vs. dict
- ***dict***
查找和插入的速度极快，不会随着key的增加而变慢；
需要占用大量的内存，内存浪费多
- list
查找和插入的时间随着元素的增加而增加；
占用空间小，浪费内存很少

---

##set
- set和dict类似，也是一组key的集合，但不存储value。由于key不能重复，所以，在set中，没有重复的key。
- 要创建一个set，需要提供一个list作为输入集合，重复元素在set中自动被过滤
- 通过add(key)方法可以添加元素到set中；通过remove(key)方法可以删除元素
- set和dict的唯一区别仅在于没有存储对应的value
- set可以看成***数学意义上***的无序和无重复元素的集合，因此，两个set可以做数学意义上的交集(&)、并集(|)等操作

---

##不可变对象
```python
#对可变对象进行操作，内容可发生改变
>>> a = ['c', 'b', 'a']
>>> a.sort()
>>> a
['a', 'b', 'c']
#对不可变对象进行操作，如下。虽然出现了'Abc'，但字符串a的内容实际上并不发生改变
>>> a = 'abc'
>>> a.replace('a', 'A')
'Abc'
>>> a
'abc'
#
>>> a = 'abc'
>>> b = a.replace('a', 'A')
>>> b
'Abc'
>>> a
'abc'
```
###解释（针对以上例子）：
- a是变量，而'abc'才是字符串对象。
- 变量a指向的对象的内容才是'abc'。所谓“不可变对象”，即指此处的'abc'
！[变量与值](http://www.liaoxuefeng.com/files/attachments/001389580505217f87b492b060b4b0ea60c8e5e70a1b53c000/0)
！[变量与值2](http://www.liaoxuefeng.com/files/attachments/001389580620829061e426d429640ddb1d17174a82a7244000/0)
- 对于不变对象来说，调用对象自身的任意方法，也不会改变该对象自身的内容。相反，这些方法会创建新的对象并返回，这样，就保证了不可变对象本身永远是不可变的。

----

##函数
- 函数就是最基本的一种代码抽象的方式。
- 函数也是对象，函数名其实就是变量。***函数名就是变量名***，对函数名赋新值，将切断函数名对原函数对象的引用，而指向新的对象。这将使函数失效！
- 自定义函数形式：def func_name(args): blocks
- 定义函数时，需要确定函数名和参数个数；如果有必要，可以先对参数的数据类型做检查；
- 若函数无return语句，在函数执行结束时将返回None作为结果。return None 可简写为 return
- 空函数:

```python
def nop():
    pass  #pass语句什么都不做，可用作占位符（比如现在还没想好怎么写函数的代码，就可以先放一个pass，让代码能运行起来）
```

- 类型检查函数：isinstance(object, class-or-type-or-tuple) -> bool
- Python函数返回的是单一值，有时候看似返回多值其实就是返回一个*tuple*。返回一个tuple可以省略括号，而多个变量可以同时接收一个tuple，按位置赋给对应的值
- 定义函数的时候，把参数的名字和位置确定下来，函数的接口定义就完成。除了正常定义的必选参数外，还可以使用*默认参数*、*可变参数*和*关键字参数*，使得函数定义出来的接口，不但能处理复杂的参数，还可以简化调用者的代码

##默认参数

-调用函数不指定该参数时，函数将使用默认值。使用默认参数时，需注意：
 1. 必选参数在前，默认参数在后。（如果默认参数写在函数定义的最前面，调用函数时，写入的参数将首先作为默认参数，后续的参数如果未指定，将导致参数数目不匹配而出错。）
 2. 如何设置默认参数：当函数有多个参数时，把变化大的参数放前面，变化小的参数放后面。变化小的参数就可以作为默认参数
- 默认参数陷阱：

```puthon
def add_end(L=[]):
    L.append('END')
    return L
>>> add_end()
['END']
>>> add_end()
['END', 'END']
>>> add_end()
['END', 'END', 'END']
#Python函数在定义的时候，默认参数L的值就被计算出来了，即[]，因为默认参数L也是一个变量，它指向对象[]，每次调用该函数，如果改变了L的内容，则下次调用时，默认参数的内容就变了，不再是函数定义时的[]了。因此，默认参数必须指向不变对象！！！
```

- 为什么要设计str、None这样的不变对象呢？因为不变对象一旦创建，对象内部的数据就不能修改，这样就减少了由于修改数据导致的错误。此外，由于对象不变，多任务环境下同时读取对象不需要加锁，同时读一点问题都没有。我们在编写程序时，如果可以设计一个不变对象，那就尽量设计成不变对象。

##可变参数

- 可变参数就是传入的参数个数是可变的，包括0个
- 定义可变参数时，仅在参数前面加了一个 * 号，在函数调用时这些参数将自动组装为一个**tuple**
- 另，Python允许在list或tuple前面加一个*号，把list或tuple的元素变成可变参数传进去。因此，调用使用可变参数的函数有2种方法：
1. func_name(arg1,arg2,arg3,arg4,...)
2. func_name(*list_name or *tuple_name,...)

##关键字参数（可选项的填写？）

- 关键字参数允许你传入0个或任意个***含参数名的参数***，这些关键字参数在函数内部自动组装为一个**dict**，参数名作为key，参数值作为value
- 定义关键字参数时，在参数前面加2个星号 **，
- 调用使用关键字参数的方法也有多种：
 1. func_name(arg1,arg2,a_name=a_value,...)
 2. func_name(arg1,arg2,a_name=D_key,...)
 3. func_name(arg1,arg2,**D_name,...) **extra表示把extra这个dict的所有key-value用关键字参数传入到函数的 **kw参数，kw将获得一个dict，*注意kw获得的dict是extra的一份拷贝，对kw的改动不会影响到函数外的extra。*

##命名关键字

- 命名关键字，用于限制关键字的名字，即让函数只接收指定的名字作为关键字参数。
- 函数定义时，要用一个'*'作为分隔符，'*'之后的参数被视为命名关键字参数
- 命名关键字可以使用默认值，像使用默认参数一样

##参数组合

> - 参数定义的顺序必须是：必选参数、默认参数、可变参数/命名关键字参数和关键字参数。

###小结

- 默认参数一定要用不可变对象，如果是可变对象，程序运行时会有逻辑错误
- *args是可变参数，args接收的是一个tuple；
- **kw是关键字参数，kw接收的是一个dict。
- 使用*args和**kw是Python的习惯写法，当然也可以用其他参数名，但最好使用习惯用法。
- 命名的关键字参数是为了限制调用者可以传入的参数名，同时可以提供默认值。
- 定义命名的关键字参数不要忘了写分隔符*，否则定义的将是位置参数。

##递归函数

- 在计算机中，函数调用是通过栈（stack）这种数据结构实现的，每当进入一个函数调用，栈就会加一层栈帧，每当函数返回，栈就会减一层栈帧。栈的大小有限，使用递归函数时要要注意防止栈溢出
- 尾递归：在函数返回的时候，调用自身本身，并且，return语句不能包含表达式。这样，编译器或者解释器就可以把尾递归做优化，使递归本身无论调用多少次，都只占用一个栈帧，不会出现栈溢出的情况。
- 尾递归事实上和循环是等价的
- Python标准的解释器没有针对尾递归做优化，任何递归函数都存在栈溢出的问题

---

##Python高级特性

- 1行代码能实现的功能，决不写5行代码。代码越少，开发效率越高

###切片（slice）

- slice(stop)
- slice(start, stop[, step])
- list, tuple, string都能进行切片操作,并各自返回list, tuple, string。(亲测,dict不能进行切片操作)

###迭代 iteration

- 迭代是重复反馈过程的活动，其目的通常是为了逼近所需目标或结果。每一次对过程的重复称为一次“迭代”，而每一次迭代得到的结果会作为下一次迭代的初始值
- 在Python中，迭代是通过`for ... in ...`来完成的，而很多语言比如C或者Java，迭代list是通过下标完成的
- 在python中,只要是可迭代对象,不论有没有下表,都能进行迭代,并且能对多个对象同时进行迭代,例如对于dict:

```python
for key in d: ...
for value in d.values(): ...
for k,v in d.items(): ...
```

- 可通过 collections模块的 Iterable类型判断一个对象是否可迭代对象:
```python
from collections import Iterable
isinstance('abc', Iterable) # str是否可迭代
```
- Python内置的`enumerate`函数可以把一个`list`变成索引-元素对，这样就可以在for循环中同时迭代索引和元素本身

###列表生成式

- 列表生成式即List Comprehensions，是Python内置的非常简单却强大的可以用来创建list的生成式
- [表达式 for ... in ... [for .. in ..]|[if 表达式] ] 中间的[]表示可选项

###生成器 generator

- 一边循环-一边计算的机制,叫做生成器
- 创建生成器的最简单方式,就是将列表生成式外围的[]改成()即可
- generator保存的是算法。当generator计算到最后一个元素,下一次将抛出StopIteraion错误
- generator是可迭代对象,使用for循环进行迭代时,不用担心StopIteration错误
- 如果一个函数中包含yield关键字,函数将不在是一个普通函数,而是   一个generator  (函数也是对象)
- generator和函数的执行流程不一样。函数是顺序执行，遇到return语句或者最后一行函数语句就返回。而变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行
- 因为generator是可迭代对象,变成generator的函数也可以用作 for ... in ...
- 用for循环调用generator时，得不到generator的return语句的返回值。如果想要拿到返回值，必须捕获StopIteration错误，返回值包含在StopIteration的value中
- generator的工作原理:是在for循环的过程中不断计算出下一个元素，并在适当的条件结束for循环。对于函数改成的generator来说，遇到return语句或者执行到函数体最后一行语句，就是结束generator的指令，for循环随之结束
- 普通函数调用直接返回结果;generator函数调用返回的是一个generator对象
- `can't send non-None value to a just-started generator`,不是for循环来进行generator的时候,要
- 生成器只能被迭代一次
- 生成器保存的是一个算法


###迭代器

- 直接作用于`for`循环的有1. 集合数据类型,包括`list`、`tuple`、`dict`、`set`、`str`等;2. `generator`,包括生成器与`generator function`
- 可直接作用于`for`循环的对象,统称为可迭代对象:`Iterable`
- 可以被`next()`函数调用并不断返回下一个值的对象称为迭代器：`Iterator`
- 生成器都是`Iterator`对象，但`list`、`dict`、`str`虽然是`Iterable`，却不是`Iterator`
- 把`list`、`dict`、`str`等`Iterable`变成`Iterator`可以使用`iter()`函数
- Python的`Iterator`对象表示的是一个数据流，`Iterator`对象可以被`next()`函数调用并不断返回下一个数据，直到没有数据时抛出StopIteration错误。可以把这个数据流看做是一个有序序列，但我们却不能提前知道序列的长度，只能不断通过next()函数实现按需计算下一个数据，所以Iterator的计算是惰性的，只有在需要返回下一个数据时它才会计算
- Iterator是一个惰性对象,可通过使用`list()`获得所有的结果
- Python的for循环本质上就是通过不断调用next()函数实现的
- 可迭代对象,实现的是`__iter__()`方法,可迭代对象是你可以从其获取一个迭代器的任意对象
- 迭代器,实现的是`__next__()`方法,迭代器是那些允许迭代可迭代对象的对象
- 迭代是一个实现可迭代对象和迭代器的过程
-

##函数式编程

- 函数是Python内建支持的一种封装，我们通过把大段代码拆成函数，通过一层一层的函数调用，就可以把复杂任务分解成简单的任务，这种分解可以称之为面向过程的程序设计。函数就是面向过程的程序设计的基本单元。
- 函数式编程就是一种抽象程度很高的编程范式，纯粹的函数式编程语言编写的函数没有变量，因此，任意一个函数，只要输入是确定的，输出就是确定的，这种纯函数我们称之为没有副作用。而允许使用变量的程序设计语言，由于函数内部的变量状态不确定，同样的输入，可能得到不同的输出，因此，这种函数是有副作用的。
- Python对函数式编程提供部分支持

###高阶函数

- 函数也是一个对象,故函数也可以赋给一个变量。前文已经提到了`函数名`其实就是一个指向函数对象的变量,但最好最好是不要修改函数名对函数对象的引用
- 由于函数就是一个对象,因此可以将函数作为另一函数的参数。以函数的参数的函数就是高阶函数
- 我感觉,高阶函数是函数作为参数或者返回值,使用的时候就是一层层把函数剥开来。函数调用函数,特殊情况不就是递归(函数调用自身)嘛!

##map/reduce

- map()函数接收2个参数,一个是`函数`,一个是`Iterable`,map将传入的函数依次作用到序列的每个元素，并把结果作为新的`Iterator`返回
- 根据定义,map()是一个高阶函数,将运算抽象化
- reduce()把一个函数作用在一个序列上[x1,x2,...]上,这个函数必须接收2个参数,reduce将结果继续和下一个元素作累计,

###fliter

- filter用于过滤序列,接收一个函数与一个序列。filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素,返回Iterator结果。此时,作为filter参数的函数相当于一个判定器

###sorted

- sorted(iterable, key=None, reverse=False) --> a new sorted list
- key指定的函数作用在每个元素上,根据key函数返回的结果,对原序列进行排序。key仅起到排序的作用,并没有对序列进行真实的影响
- reverse参数的值,决定正向还是反向排序

###返回函数

- 高阶函数除可以接受函数作参数以外,能可以作为结果值返回

```python
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum
```
- 当我们调用lazy_sum()时，返回的并不是求和结果，而是求和函数:
```python
>>> f = lazy_sum(1, 3, 5, 7, 9)
>>> f
<function lazy_sum.<locals>.sum at 0x101c6ed90>
```
- 调用函数f时，才真正计算求和的结果：

```python
>>> f()
25
```

- 在函数lazy_sum中又定义了函数sum，并且，内部函数sum可以引用外部函数lazy_sum的参数和局部变量，当lazy_sum返回函数sum时，相关参数和变量都保存在返回的函数中,这种程序结构称为“闭包”
- 当调用lazy_sum时,每次调用都会返回一个新的函数,即传入相同的参数,每次调用的结果各不相等,互不影响
- 返回的函数sum在其定义内部引用了局部变量,当一个函数返回另一个函数后,$\color{red}{ 其内部的局部变量仍然被新函数引用}$,当局部变量被修改时,新函数返回的值也可能被修改。因此,使用闭包时,返回函数不要引用任何循环变量,或后续可能会改变的量
- 返回函数并没有立即执行,而是直到被调用时才被执行

###匿名函数

- 关键字`lambda`表达匿名函数,冒号之前的变量作为参数
- 匿名函数只能有一个表达式,且返回值就是该表达式的结果
- 匿名函数也是一个函数对象,可以将其赋给一个变量,再利用变量来调用该函数:
```python
>>> f = lambda x : x*x
>>> f(5)
```
- 匿名函数还可以作为返回值:
```python
def build(x,y):
    return lambda : x*x + y*y
```

###装饰器
- 在代码运行期间动态增加功能的方式,即称为`装饰器`(Decorator),它起装饰函数的作用
- 本质上,$\color {red}{装饰器就是一个返回函数的高阶函数}$
- 使用:在被装饰的函数定义处,前缀`@decorator_name`
- 调用被装饰函数时,不仅会运行被装饰的函数本身,在这之前,还会执行装饰器的代码
```pythonaaa
def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

@log
def now():
    print('WTF')
```
- log是一个装饰器,它接收一个函数作为参数,并返回一个参数。
- 把@log放在now()函数的定义处,相当于执行了now=log(now)。由于log()是一个decorator，返回一个函数，所以，原来的now()函数仍然存在，只是现在同名的now变量指向了新的函数，于是调用now()将执行新函数，即在log()函数中返回的wrapper()函数。
```
>>> print(now.__name__)
>>> 'wrapper'
```
因为返回的那个wrapper()函数名字就是'wrapper'，所以，需要把原始函数的__name__等属性复制到wrapper()函数中，否则，有些依赖函数签名的代码执行就会出错。
不需要编写wrapper.__name__ = func.__name__这样的代码，Python内置的functools.wraps就是干这个事的，所以，一个完整的decorator的写法如下
```
import functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
```
- 若要使用装饰器在调用函数之后显示效果,则需要将其裹在调用函数的里层,并在函数返回之后,将其返回。如:
```
def log3(func):
    def wrapper(*args, **kw):
        print("begin call")
        def log3_2():
            print("end call")
        return func(*args, **kw) , log3_2()
    return wrapper
```

###偏函数
- 把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数
- 使用方法:functools.partial(func_name, args=val [,...])
- 创建偏函数时，实际上可以接收函数对象、*args和**kw这3个参数。传入关键字参数时,将使用**kw部分设置默认值;当传入非关键字参数时,将参数值加入到*args
```python
>>> import functools
>>> int2 = functools.partial(int, base=2)   #将int()函数的base的参数固定为2,构造处新的函数
>>> int2('1000000')
64
```
- 当函数的参数个数太多，需要简化时，使用functools.partial可以创建一个新的函数，这个新函数可以固定住原函数的部分参数，从而在调用时更简单。

##模块

- 最大的好处是大大提高了代码的可维护性。其次，编写代码不必从零开始。当一个模块编写完毕，就可以被其他地方引用
- 使用模块还可以避免函数名和变量名冲突。相同名字的函数和变量完全可以分别存在不同的模块中
- 为了避免模块名冲突，Python又引入了按目录来组织模块的方法，称为包（Package）。
- 每一个包目录下面都会有一个__init__.py的文件，这个文件是必须存在的，否则，Python就把这个目录当成普通目录，而不是一个包。__init__.py可以是空文件，也可以有Python代码
- 可以有多级目录，组成多级层次的包结构
- 一个模块的标准写法:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' xxxx '                #模块的文档注释,任何模块代码的第一个字符串都被视为模块的文档注释
__author__ = 'Engine'   #著名作者
```

- 导入一个模块,比如`sys`后,就得到了一个`sys`变量指向该模块,通过`sys`变量,可以访问`sys`模块的所有内容,使用所有功能
- `says`模块的argv变量,用list存储了所有命令行参数,即通过 python3 xx.py a, b, c, ...方式传入的参数。
- `argv`至少包含一个元素,且第一个元素就是该.py文件的名称
```python
if __name__=='__main__':
    test()
```
- 上述代码一般加在模块代码的底部。当在命令行下运行该模块文件时,Python解释器将__name__置为__main__;而将其他地方导入该模块时,__name__!=__main__,条件判断失败
- 作用域:
> - 正常函数和变量名(无前后_)是`public`型的,可以被直接引用
- __xx__(前后有双下划线的)是特殊变量,也可以被直接引用,但有特殊用途
- _xxx(前导一个下划线的)或__xx(前导2个下划线)函数或变量是`private`型,属于不应该引用的类型。
- 外部不需要引用的函数或变量应定义为`private`,而只将外部需要的函数或变量设为`public`,实现了代码的封装与抽象
- 当加载一个模块时,Python解释器默认依次搜索当前目录、所有已安装的内置模块和第三方模块。搜索路径存放在`sys`模块的`path`变量中
- 添加包的搜索目录:
 1. 修改sys。path变量。此方法在运行时修改,运行结束时退出
 2. 设置`PYTHONPATH`环境变量,该环境变量的内容会被自动添加到模块的搜索路径中。

##面向对象程序设计
- 面向过程的程序设计把计算机程序视为一系列的命令集合，即一组函数的顺序执行。为了简化程序设计，面向过程把函数继续切分为子函数，即把大块函数通过切割成小块函数来降低系统的复杂度。
- 而面向对象的程序设计把计算机程序视为一组对象的集合，而每个对象都可以接收其他对象发过来的消息，并处理这些消息，计算机程序的执行就是一系列消息在各个对象之间传递。
- 在Python中，所有数据类型都可以视为对象
- 面向对象的抽象程度又比函数要高，因为一个Class既包含数据，又包含操作数据的方法

###类与实例
- 面向对象最重要的概念就是类（Class）和实例（Instance），必须牢记类是抽象的模板，比如Student类，而实例是根据类创建出来的一个个具体的“对象”，每个对象都拥有相同的方法，但各自的数据可能不同。
```python
class Student(object):
    pass
```
- 类型通常是大写字母开头,紧跟着的(object)表示该类从哪个类继承下来的,`object`是所有类的父类
- 可以自由地给一个实例变量绑定属性:
```python
>>> bart.name = "Bart Simpson" #bar是Student的一个实例
>>> bart.name
'Bart Simpson'
```
- 类可以起到模板的作用,因此,在创建实例时,可以将一些必须绑定的属性强制写进类的定义中去:通过定义__init__方法。
```python
class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
```
- __init__方法的第一个参数永远是self，表示创建的实例本身，因此，在__init__方法内部，就可以把各种属性绑定到self，因为self就指向创建的实例本身。
- 有了__init__方法，在创建实例的时候，就不能传入空的参数了，必须传入与__init__方法匹配的参数
- 与普通函数相比,类的方法的第一个参数永远是实例变量self,但使用时不用传递该函数。
- 类的一个重要作用是:数据封装。可以使外部的调用忽略掉内部实现细节
- 方法是与实例绑定的函数,方法可直接访问实例的数据
- 由于可以自由地给实例变量绑定属性,因此,同一个类的不同实例可以拥有不同的变量名称

###访问限制
- 在类的内部,可以有属性与方法,而外部代码可以通过直接调用实例变量的方法来操作数据,从而隐藏额内部的复杂逻辑
- 如前所属,__xx的函数或变量为`private`(私有的),因此,可以在定义时将类的一些属性定义为私有属性,从而限制了外部对这些属性的访问
```python
a.score='560'
a.set_score(56)
```
- 在方法中,可以对参数进行检查,避免传入无效参数。如上,直接使用`a.score='560'`并没有对值进行限制,可能赋错值
- __xx__型的特殊变量,可以直接访问,并不是`private`变量
- _xx型的变量,表示外部可以访问,但不能随意访问,一般视为私有变量
- __xx型的变量,可通过_ClassName__xx访问,但最好不要这么做

###继承与多态
- 继承,使子类获得了父类全部的功能,并可以添加属于子类自己的属性与方法;还可以覆盖父类的方法
- 在继承关系中,一个实例的数据类型是某个子类,也可以看作是父类
- 多态的好处:子类调用父类的方法时,将自动根据实际子类的不同,而调用子类自身的方法
- 多态的威力:调用方只管调用,不管细节
- 开闭原则:
 - 对扩展开放:允许新增子类
 - 对修改封闭:不需要修改依赖父类的方法
- 静态语言 vs. 动态语言:
 - 对于静态语言,调用方法时,如果需要传入某一类型,则传入的对象必须是该类型或其子类,否则无法调用该方法
 - 而动态语言,只要保证传入的对象有该方法,就可以调用方法。
 - 鸭子类型:一个对象只要看起来像鸭子,走起来像鸭子,就可以看作是鸭子。比如对于真正的文件对象,有一个`read()`方法,返回其内容。但许多对象只要有`read()`,都被视为`file-like-object`。许多函数接收的参数是`file-like-object`,此时,不一定要传入真正的文件对象,完全可以传入任何实现了`read()`的对象

###获取对象信息
- `type`返回对应的Class类型,可以对变量、函数、类使用
- 加强版,使用`types`模块:
```python
>>> import types
>>> def fn():
...     pass
...
>>> type(fn)==types.FunctionType
True
>>> type(abs)==types.BuiltinFunctionType
True
>>> type(lambda x: x)==types.LambdaType
True
>>> type((x for x in range(10)))==types.GeneratorType
True
```
- 判断class类型时,可使用`isinstance()`函数,用法`isinstance(var, class)`
- 用`isinstance()`函数还可以判断一个变量是否某些类型的一种:`isinstance([1,2,3], (list, tuple))
- `dir()`,获得一个对象的所有属性与方法
- __len__方法,返回长度。在Python中,调用`len()`方法获取一个对象的长度时,实际上,在`len()`函数的内部自动调用了该对象的`__len__()`方法:
```python
>>> len('a')
1
>>> 'a'.__len__()
1
```
- `getattr()`,`setattr()`,`hasattr()`,功能如其名描述,不限于属性,方法亦可。使用`setattr()`时,需指定3个参数(对象名,属性名,属性值)。使用`getattr()`时,获取不存在的属性时,将抛出错误;并可以指定默认值,当属性不存在时,抛出该值

###实例属性与类属性
- 给实例绑定属性,可通过实例变量,或通过self变量
- 给class本身绑定属性,可直接在class中定义属性,称为类属性
```python
class Student(object):
    name = 'Student'
```
- 实例属性优先级高于类属性,相同名称的实例属性将屏蔽掉类属性,但删除实例属性后,再次访问同名属性,将访问类属性。

##面向对象高级编程

###__slots__
- Python作为动态语言,可以自由地给实例绑定属性和方法,但这种绑定仅限于当前实例,即对同类的另一实例不起作用
- 为了动态地给所有实例都绑定属性与方法,Python允许对class进行绑定,方法与实例的绑定类似
- 在类定义时,使用__slots__变量,可以限制class实例能添加的属性:
```python
class Students(object):
    __slots__ = ("name", "age)  #用tuple定义允许绑定的属性名称
```
- __slots__定义的属性仅对当前类的实例起作用,对继承的子类不起作用。除非在子类中也定义__slots__,这样,子类实例允许定义的属性就是自身的__slots__加上父类的__slots__

###@property
- 可以通过类似'get_xxx()','set_xxx()'的方法,对属性的获取与修改加以限制
- 对于类的方法,装饰器仍然有用。Python内置的`@property`装饰器就是负责把一个方法"当作"属性访问:
```python
class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
```
- 将一个getter方法“当作”属性,只需用装饰器`@property`。而`@property`本身会创建另一个装饰器`@x.setter`(其中,x就是被变的属性名),其负责把一个setter方法当作属性赋值。
- 用`@property`,可定义可读写属性,也可以定义只读属性,此时只需定义getter方法,不定义setter方法即可


###多重继承
- class son(father1, father2,...)
- 多重继承,子类可获得多个父类的所有功能
- 设计继承关系时,通常主线时单一继承的。另外有需要的话,在增加其他继承,称为`MixIn`。`MixIn`的目的就是给一个类增加额外的功能。在设计类时,可以优先考虑多重继承来组合多个MixIn功能,而不是设计多个层次的复杂继承关系

###定制类
- `__str__()`方法,返回用户看到的字符串;`__repr__()`返回程序开发者看到的字符串,`__repr__()`常用于调试
- 如果一个类想被用于`for ... in ...`循环,就必须实现一个`__iter__()`,该方法返回一个迭代对象,Python的for循环将不断调用该迭代对象的`__next__()`方法取到循环的下一个值,直到遇到`StopIteration`错误
- `__getitem__()`可以实现按下标提取元素,也可以实现与`list`一样的切片功能。依据是传入的参数不同,int or slice。当把对象看作是`ditc`时,`__getitem__()`的参数还可以时一个作为`key`的对象
- `__setitem__()`把对象视作list或dict来对集合赋值;`__delitem__()`,删除元素
- `__getattr__()`动态返回一个属性。只有在没有找到指定属性的情况下,才调用`__getattr__()`。除非指定了不存在某属性,如`age`的返回值,否则设置了`__getattr__()`方法,将默认返回None
```python
class Student(object):

    def __getattr__(self, attr):
        if attr=='age':
            return lambda: 25
        raise AttributeError('\'Student\' object has no attribute \'%s\'' % attr)
```
- 将一个类的所有属性和方法调用全部动态化处理,完全动态调用,可以针对完全动态的情况调用
- `__call__()`,直接对实例进行调用:
```python
class Student(object):
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print('My name is %s.' % self.name)

>>> s = Student('Michael')
>>> s() # self参数不要传入
My name is Michael.
```
- `__call__()`还可以定义参数。对实例进行直接调用,模糊了函数与对象的概念
- `callable()`用于判断一个对象是否可调用

###枚举类
- 常量,通常用大写的变量来定义
- 使用Enum类,为枚举类型定义一个class类型,则每个常量都是class的一个唯一实例
```python
from enum import Enum
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
```
- 这样将得到一个`Month`类型的枚举类,其中`Jan`称为name,可通过Month.Jan取得value。value属性是自动赋给成员的`int`常量,默认从1开始计数
- 也可以采用从`Enum`派生自定义类的方式:
```python
from enum import Enum, unique

@unique
class Weekday(Enum):
    Sun = 0
    Mon = 1
    ...
```
- `@unique`装饰器可以帮助检查保证无重复值

###元类
- 动态语言与静态语言最大的不同在于,函数与类的定义不是编译时定义的,而是运行时动态创建的
- `type()`函数用于查看一个类型或变量的类型,一个类的类型是`type`,一个实例的类型是它的类
- 动态语言中,类的定义是运行时动态创建的,创建class的方法就是使用`type()`函数:
```python
def fn(self, name='world'):
    print('Hello, %s.' % name)

Hello = type('Hello', (object,), dict(hello=fn))
```
- 要创建一个class对象,`type()`函数依次传入3个参数:
 1. class name
 2. 继承的父类集合, tuple的正确写法
 3. class的方法名称与函数绑定,如上述代码将函数`fn`绑定到方法`hello`上
- 通过type()函数创建的类和直接写class是完全一样的，因为Python解释器遇到class定义时，仅仅是扫描一下class定义的语法，然后调用type()函数创建出class。
- 正常情况下，我们都用class Xxx...来定义类，但是，type()函数也允许我们动态创建出类来，也就是说，动态语言本身支持运行期动态创建类，这和静态语言有非常大的不同，要在静态语言运行期创建类，必须构造源代码字符串再调用编译器，或者借助一些工具生成字节码实现，本质上都是动态编译，会非常复杂。
- `metaclass`,元类,创建类的类。metaclass的类名总是Metaclass结尾,以清晰地表示一个metaclass
- metaclass是类的模板,必须从`type`类型派生
```python
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)
class MyList(list, metaclass=ListMetaclass):
    pass
```
- Python解释器在创建`MyList`时,通过`ListMetaclass.__new__()`来创建,在此,可以修改类的定义(比如加上新的方法),然后返回修改的定义。
- `__new__()`的参数依次是:
 1. 当前准备创建的类的对象
 2. 类的名字
 3. 类继承的父类集合
 4. 类的方法集合
- $\color {red}{metaclass 未完待续}$

##错误、调试与测试

###错误处理
- 错误检查处理机制: `try ... except ... finally ...`
- 当执行`try`中的代码块时出错,将中断后续代码的执行,转而去执行`except`语句块,执行完`except`后,如果有`finally`语句块,则执行`finally`语句块
- 没有发生错误,则`except`语句块不会被执行,但有`finally`的话,`finally`一定会被执行
- 可以有多个`except`来捕获不同的错误
- 如果没有错误发生,可以在`except`语句块后加`else`语句块,当没有错误发生时,将执行`else`语句
- Python的错误也是class,所有的错误类型都继承自`BaseException`。使用`except`捕获到某类型的错误时,将自动忽略其子类错误。因此要将子类错误放在父类错误之前
- 使用`try ... except`捕获错误,可以跨多层调用,如下所示
```python
def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    try:
        bar('0')
    except Exception as e:
        print('Error:', e)
    finally:
        print('finally...')
```
- 此时,实际出错位置在`foo()`函数内,但只要`main()`捕获到错误,就能得到处理。因此,只要在合适的层次捕获错误就可以了。
- 当错误没有被捕获时,错误将一直向上抛,直到被Python解释器捕获,打印错误信息,并退出程序
- Python内置的`logging`模块可以记录错误信息
```python
import logging
try:
    ...
except Exception as e:
    logging.exception(e)
```
- 自定义抛出错误:定义错误的类,选择好其继承关系,使用`raise`语句抛出一个错误的实例I
```python
def foo(s):
    n = int(s)
    if n==0:
        raise ValueError('invalid value: %s' % s)
    return 10 / n

def bar():
    try:
        foo('0')
    except ValueError as e:
        print('ValueError!')
        raise

bar()
```
- 上述代码,`bar()`函数已经捕获了错误信息,但使用`raise`将错误继续上抛,让上层去处理这个错误。
- `raise`如果不带任何参数,就会把当前错误原样抛出。在`except`中`raise`一个错误,可以将一种类型的错误转化为另一类型的错误

###调试
1. 在程序可能有错误处,打印信息,简单粗暴低效
2. 断言`assert`
```python
def foo(s):
    n = int(s)
    assert n != 0, "n is zero"
    return 10 / n

def main():
    foo('0')

main()
```
 -`assert`的意思是,表达式`n != 0`应该时`True`,否则,根据程序运行的逻辑,后面的代码肯定会出错
 - 如果断言失败,`assert`语句本身会抛出`AssertionError`错误
 - Python解释器可以用 `-0`参数来关闭`assert`: python -0 xxx.py
3. logging
 - 使用`logging`替换`print`,不会抛出错误,而且可以将错误信息输出到文件:
 - `logging.info`可以输出一段文本
```python
import logging
logging.basicConfig(level=logging.INFO)

s = '0'
n = int(s)
logging.info('n = %d' % n)
print(n / 10)
```
 - `logging`允许指定记录信息的级别,有`debug`、`info`、`warning`、`error`等
4. pdb
 - 使用`-m pdb`运行python程序,将启用单步调试功能。首先将`pdb`定位到程序将执行的首行代码,输入命令`l`可以查看代码;输入`n`可以单步执行代码;输出`c`,程序运行到结尾;输入`p 变量名`查看变量;输入`q`结束调试,退出程序
5. pdb.set_trace()
 - 设置断点调试。`import pdb`,在可能出错的位置设置`pdb.set_trace()`
 - 运行代码时,程序将自动在`pdb.set_trace()`处暂停并进入pdb调试环境,
6. 使用IDE

###单元测试
- 单元测试是用来对一个模块,一个函数,或者一个类进行正确性检验的测试工作:
> 比如对函数abs()，我们可以编写出以下几个测试用例：
输入正数，比如1、1.2、0.99，期待返回值与输入相同；
输入负数，比如-1、-1.2、-0.99，期待返回值与输入相反；
输入0，期待返回0；
把上面的测试用例放到一个测试模块里，就是一个完整的单元测试。

- 对一个通过单元测试的代码做了修改,重新进行单元测试,若仍能通过,说明修改并没有对代码原有的行为造成影响。
- 这种以测试为驱动的开发模式最大的好处就是确保一个程序模块的行为符合我们设计的测试用例。在将来修改的时候，可以极大程度地保证该模块行为仍然是正确的。
- 编写单元测试时,测试类继承自`unittest.TestCase`。`test`开头的方法即为测试方法,不以`test`开头的方法不被认为是测试方法,在测试的时候不会被执行
- 通过使用`-m unittest`参数来运行单元测试
- 在单元测试中可以编写`setUp()`和`tearDown()`方法,将在每次调用测试方法的前后执行。比如测试需要启动数据库时,可以在`setUp()`中连接数据库,在`tearDown()`中关闭数据库

###文档测试
- 文档测试,是Python解释器执行注释中的示例代码,将严格按照交互式命令行的输入输出来判断测试结果的正确性。当测试异常时,可用`...`来表示输出
- 当模块被正常导入时,`doctest`不会被执行。只有在命令行直接运行时,才会执行`doctest`

##IO编程
- 同步io与异步io的区别在于是否等待io执行的结果
- 操作IO的能力都是由操作系统提供的，每一种编程语言都会把操作系统提供的低级C接口封装起来方便使用

###文件读写
- 文件读写就是请求OS打开一个`文件对象`,然后通过操作系统提供的接口从这个文件对象读取数据或把数据写入这个文件对象
- open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None) -> file object
- 调用`read()`方法读取打开的文件的内容,Python将内容全部读到内存,用`str`对象表示
- 用`close()`关闭文件,文件对象会占用系统资源,在使用完毕后要关闭它
- 由于文件读写时可以产生`IOError`,一旦出错,`close()`方法就不会调用,为了保证无论是否出错都正确地关闭文件,可以使用`try...finally`来读写文件
- 使用`with`语句来读写,可实现自动调用`close()`:
```python
with open('~/a.txt', 'r') as f:
    print(f.read())
```
- 调用`read()`会一次性读取文件的全部内容,使用`read(size)`设置每次读取的最大字节数,使用`readline()`每次读取一行的内容,`readlines()`依次读取全部内容并按行返回(得到list of str)
- 只要有`read()`方法的对象,都是`file-like object`。包括内存的字节流,网络流,自定义流等
- `StringIO`就是在内存中创建file-like object,常作临时缓冲
- 读取二进制文件,`open()`方法的`mode`设置为`rb`
- 默认以utf-8的编码形式读取文本文件,可通过`encoding`参数来设置读取的编码方式
- 读取时可能遇到`UnicodeDecodeError`,这可能是文本文件中夹杂了非法编码的字符,可通过设置`errors`参数来处理编码错误,如`errors='ignore'`
- 用`write()`来写,但要在调用`open()`函数时,将`mode`设置为`w`或`wb`。可返回调用`write()`写入文件,但调用完毕必须关闭文件
- 写文件时,OS不会立即将数据写入磁盘,而是放在内存缓存,空闲时再慢慢写入。调用`close()`时,OS才立即将没有写入的数据全部写入磁盘。因此,忘记调用`close()`的一个后果是只有一部分数据被写入磁盘
- 用`with`语句操作文件IO是个好习惯

###StringIO & BytesIO
- `StringIO`,是在内存中读写`str`
- 用`StringIO()`方法创建一个StringIO,或使用`str`初始化。StringIO是一个file-like object,可以像文件一样读写,用`getvalue()`获取写入的`str`(包括初始化时写入的)
- 使用`BytesIO`来操作二进制数据

###操作文件和目录
- Python的`os`模块提供了直接调用OS提供的接口函数
- `os`模块的一些函数是跟OS相关的
- 操作系统的环境变量全部保存在`os.environ`变量中,是一个tuple of dict
- 使用`os.environ。get('key')`来获取某个环境变量的值
- 操作文件和目录的函数一部分放在`os`模块中,一部分放在`os.path`模块中
- 查看、创建和删除目录:
```python
# 查看当前目录的绝对路径:
>>> os.path.abspath('.')
'/Users/michael'
# 在某个目录下创建一个新目录，首先把新目录的完整路径表示出来:
>>> os.path.join('/Users/michael', 'testdir')
'/Users/michael/testdir'
# 然后创建一个目录:
>>> os.mkdir('/Users/michael/testdir')
# 删掉一个目录:
>>> os.rmdir('/Users/michael/testdir')
```
- 将2个路径合成一个时,最好通过`os.path.join()`函数,这样能正确处理不同OS的路径分隔符(Windows与Unix不一样)
- 同理,拆分路径时,最好调用`os.path.split()`,将得到2部分内容,后一部分总是最后级别的目录或文件名;`os.path.splitext()`可以直接在第二部分得到文件扩展名。合并、拆分路径的函数并不要求目录和文件真实存在,它们只是进行来字符串的操作
- `os.rename('a.txt', 'b.txt')`,`os.remove('b.txt')`
- 复制文件的函数并不在`os`模块中,因为复制文件并非由OS提供的系统调用。可通过其他方式实现啊~
- `shutil`模块提供了`copyfile()`函数,其可以看作`os`模块的补充
- `os.listdir('xx')`得到目标目录下的文件列表,`isdir('xx')`测试是否目录,`isfile('xx')`测试是否文件
```python
# 列出当前目录下的所有.py文件
>>> [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']
```

###序列化
- 将变量从内存中变成可存储或传输的过程称为`序列化`,在`python`中叫`pickling`,在其他语言中可能叫`serialization`,`marshalling`,`flattening`
- 序列化之后,即可将序列化的内容写入磁盘或通过网络传输到其他设备
- 将变量内容从序列化的对象重新读到内存称为`反序列化`,即`unpickling`
- python提供了`pickle`模块来实现序列化
- `pickle.dumps()`方法将任意对象序列化为一个`bytes`。并且`pickle.dump()`可直接将对象序列化后写入一个file-like object
```python
>>> import pickle
>>> d = dict(name='Bob', age=20, score=88)
>>> pickle.dumps(d)
b'\x80\x03}q\x00(X\x03\x00\x00\x00ageq\x01K\x14X\x05\x00\x00\x00scoreq\x02KXX\x04\x00\x00\x00nameq\x03X\x03\x00\x00\x00Bobq\x04u.'
>>> f = open('dump.txt', 'wb')
>>> pickle.dump(d, f)
>>> f.close()
```
- 当要把对象从磁盘读到内存时，可以先把内容读到一个bytes，然后用pickle.loads()方法反序列化出对象，也可以直接用pickle.load()方法从一个file-like Object中直接反序列化出对象。
- 如果要在不同编程语言中传递对象,就必须把对象序列化为标准格式,如`xml`,`json`等
- `json`表示出来是一个字符串,可以被所有语言读取,也可以方便地存储在磁盘或通过网络传输。并且`json`比`xml`更快,还可直接在web页面读取
- `josn`(JavaScript Object Notation)表示的对象是标准的javascript语言的对象,与python内置的数据类型对应如下:
|JSON类型|Python类型|
|:-:|:-:|
|{}|dict|
|[]|lsit|
|"string"|str|
|123.45|int or float|
|true/false|True/False|
|null|None|
- 内置的`json`模块提供了完善的python对象到json格式的转换
```python
>>> import json
>>> d = dict(name='bob', age=20, score=88)
>>> json.dumps(d)
'{"age": 20, "score": 88, "name": "bob"}'
```
- `json.dumps()`方法返回一个`str`,内容就是标准的json。同样的,`json.dump()`可直接将json写入一个file-like object
- `json.loads()`将json的字符串反序列化为python对象,`json.load()`从file-like object中读取字符串并反序列化
- json标准规定json的编码是utf-8
- `json.dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw)`可选参数`defalut`可将任意对象转换称可序列化的json对象,因此只需一个转换函数,就可以将任意对象转换为json对象:
```python
import json

class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }

>>> print(json.dumps(s, default=student2dict))
{"age": 20, "name": "Bob", "score": 88}
```
- 一个更简易的写法是:`json.dumps(s, default=lambda obj: obj.__dict__)`通常一个类的实例都有一个`__dict__`属性,它就是一个`dict`,用于存储实例变量
- 同理,将json对象反序列化为python对象实例时,也可以写一个转换函数,传入到`object_hook`函数中
```python
def dict2student(d):
    return Student(d['name'], d['age'], d['score'])

>>> json_str = '{"age": 20, "score": 88, "name": "Bob"}'
>>> print(json.loads(json_str, object_hook=dict2student))
<__main__.Student object at 0x10cd3c190>
```

##进程与线程
- 多任务的实现有多种方式:1. 多进程模式, 2. 多线程方式, 3. 多进程+多线程方式
- 线程是任务执行的最小单元,进程是资源分配的最小单元

###
- Unix/Linux操作系统提供了一个fork()系统调用，它非常特殊。普通的函数调用，调用一次，返回一次，但是fork()调用一次，返回两次，因为操作系统自动把当前进程（称为父进程）复制了一份（称为子进程），然后，分别在父进程和子进程内返回。
- 子进程永远返回0，而父进程返回子进程的ID。这样做的理由是，一个父进程可以fork出很多子进程，所以，父进程要记下每个子进程的ID，而子进程只需要调用getppid()就可以拿到父进程的ID。
- `fork()`,一个进程在接收到新任务时就可以复制出一个子进程来处理新任务。常见的Apache服务器就是又父进程监听端口,每当有新的http请求时,就fork出子进程处理新的请求
- `multiprocessing`模块提供了`Process`类来代表一个进程对象。创建进程时,只需要传入一个执行函数和函数的参数,就可以创建一个`Process`实例,用`start()`方法启动。`join()`方法等待子进程结束后继续往下运行,通常用于进程间的同步
```python
from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
```
- 如果要启动大量的子进程,可以用进程池的方式批量创建子进程:
```python
from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
```
- 对`Pool`对象调用`join()`方法会等待所有子进程执行完毕,因此`print('All subprocesses done.')`总是在最后执行。调用`join()`之前必须调用`close()`,调用`close()`之后就不能继续添加新的`Process`了
- `Pool`的默认大小是CPU的核数,`p=Pool(5)`表示同时跑5个进程,但由于CPU核数的限制,可能最多执行4个进程(4核)
,剩下1个进程必须等待某个进程结束后才能被执行
- 通过`fork()`的方法创建的子进程是,自身的复制。有时候需要派生外部进程。
- `subprocess`模块可以方便地启动一个子进程,控制其输入和输出:
```python
import subprocess

print('$ nslookup www.python.org')
r = subprocess.call(['cat', '~/a.txt'])
print('Exit code:', r)
```
```python
import subprocess

print('$ nslookup')
p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
print(output.decode('utf-8'))
print('Exit code:', p.returncode)
```
- 上述代码中,`subprocess.call`控制子进程(shell?)输出信息,`communicate`用于向子进程输入
- `multiprocessing`模块包装了底层的机制,提供了`Queue`,`Pipes`等方式来交换数据,实现进程间通信
- 父进程所有Python对象都必须通过`pickle`序列化再传到子进程中

###多线程
- 进程由若干个线程组成,一个进程至少有一个线程
- python标准库提供了:`_thread`和`threading`模块,其中`_thread`是低级模块,`threading`是高级模块,对`_thread`进行了封装
- 任何进程默认会启动一个线程,称为`主线程`,主线程可以启动新的线程.`threading`模块的`current_thread()`函数永远返回当前线程的实例。主线程实例的名字叫`MainThread`,子线程的名字在创建时指定,如果不起名字,python将自动给线程命名为`Thread-1`...
- 多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响，而多线程中，所有变量都由所有线程共享，所以，任何一个变量都可以被任何一个线程修改，因此，线程之间共享数据最大的危险在于多个线程同时改一个变量，把内容给改乱了
- 通过`锁`机制来防止多个线程对同一变量的修改冲突,创建锁:`threading.Lock()`
```python
balance = 0
lock = threading.Lock()

def run_thread(n):
    for i in range(100000):
        # 先要获取锁:
        lock.acquire()
        try:
            # 放心地改吧:
            change_it(n)
        finally:
            # 改完了一定要释放锁:
            lock.release()
```
- 当多个线程同时执行`lock.acquire()`时,只有一个线程能成功地获取锁,然后继续执行代码,其他线程只能等待获得锁
- 获得锁的线程用完后一定要释放锁,否则其他线程将一直等待下去,造成死锁。因此,用`try ... finally...`来保证锁的释放
- 锁机制阻止了多线程并发执行,降低了效率。由于互相等待,也可能造成死锁
- Python的线程虽然是真正的线程，但解释器执行代码时，有一个GIL锁：Global Interpreter Lock，任何Python线程执行前，必须先获得GIL锁，然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。这个GIL全局锁实际上把所有线程的执行代码都给上了锁，所以，多线程在Python中只能交替执行，即使100个线程跑在100核CPU上，也只能用到1个核。
- 在python中,可以使用多线程,但不能有效地利用多核。如果一定要通过多线程利用多核,可以通过C扩展来实现
- python可以通过多进程实现多核任务,多个python进程哟各自独立的GIL锁,互不影响

###ThreadLocal
```python
import threading

local_school = threading.local()

def process_student():
    std = local_school.student
    print("Hello, %s (in %s)" % (std, threading.current_thread().name))

def process_thread(name):
    local_school.student = name
    print("My name is %s." % name)
    process_student()

t1 = threading.Thread(target=process_thread, args=('Alice',), name='Thread-A')
t2 = threading.Thread(target=process_thread, args=('Bob',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
```
- 全部变量`local_school`是一个`ThreadLocal`对象,每个线程对它都可以读写,此例中为读写`student`属性,但互不影响。可以将齐看作全局变量,但每个属性,如`local_school.student`都是线程的局部变量,可以任意读写而互不干扰,也不用管理锁的问题,`ThreadLocal`内部会处理
- 这很好地解决了同一进程的多线程共享全局变量而互相干扰的问题
- `ThreadLocal`最常用的地方是为每个线程绑定一个数据库链接,HTTP请求,用户身份信息等,这样一个线程所有调用到的处理函数都能非常方便地访问这些资源

###进程 vs. 线程
- 首先，要实现多任务，通常我们会设计Master-Worker模式，Master负责分配任务，Worker负责执行任务，因此，多任务环境下，通常是一个Master，多个Worker。
- 多进程模式最大的优点就是稳定性高，因为一个子进程崩溃了，不会影响主进程和其他子进程。（当然主进程挂了所有进程就全挂了，但是Master进程只负责分配任务，挂掉的概率低）著名的Apache最早就是采用多进程模式。
- 多进程模式的缺点是创建进程的代价大，在Unix/Linux系统下，用fork调用还行，在Windows下创建进程开销巨大。另外，操作系统能同时运行的进程数也是有限的，在内存和CPU的限制下，如果有几千个进程同时运行，操作系统连调度都会成问题。
- 多线程模式通常比多进程快一点，但是也快不到哪去，而且，多线程模式致命的缺点就是任何一个线程挂掉都可能直接造成整个进程崩溃，因为所有线程共享进程的内存。在Windows上，如果一个线程执行的代码出了问题，你经常可以看到这样的提示：“该程序执行了非法操作，即将关闭”，其实往往是某个线程出了问题，但是操作系统会强制结束整个进程。
- 在Windows下，多线程的效率比多进程要高，所以微软的IIS服务器默认采用多线程模式。由于多线程存在稳定性的问题，IIS的稳定性就不如Apache
> `线程切换`:操作系统在切换进程或者线程时，它需要先保存当前执行的现场环境（CPU寄存器状态、内存页等），然后，把新任务的执行环境准备好（恢复上次的寄存器状态，切换内存页等），才能开始执行。这个切换过程虽然很快，但是也需要耗费时间。多任务一旦多到一个限度，就会消耗掉系统所有的资源，结果效率急剧下降，所有任务都做不好

> `计算密集型`:该类型任务主要消耗CPU资源,代码运行效率至关重要。Python这样的脚本语言运行效率很低，完全不适合计算密集型任务。对于计算密集型任务，最好用C语言编写。

> `IO密集型`:涉及到网络、磁盘IO的任务都是IO密集型任务，这类任务的特点是CPU消耗很少，任务的大部分时间都在等待IO操作完成。对于IO密集型任务，任务越多，CPU效率越高，但也有一个限度。常见的大部分任务都是IO密集型任务，比如Web应用。对于IO密集型任务，最合适的语言就是开发效率最高（代码量最少）的语言，脚本语言是首选

> `异步IO`:如果充分利用操作系统提供的异步IO支持，就可以用单进程单线程模型来执行多任务，这种全新的模型称为事件驱动模型，Nginx就是支持异步IO的Web服务器，它在单核CPU上采用单进程模型就可以高效地支持多任务。在多核CPU上，可以运行多个进程（数量与CPU核心数相同），充分利用多核CPU。由于系统总的进程数量十分有限，因此操作系统调度非常高效。用异步IO编程模型来实现多任务是一个主要的趋势。
- 对应到Python语言，单进程的异步编程模型称为协程，有了协程的支持，就可以基于事件驱动编写高效的多任务程序。

###分布式进程
- 在Thread和Process中，应当优选Process，因为Process更稳定，而且，Process可以分布到多台机器上，而Thread最多只能分布到同一台机器的多个CPU上。
- Python的`multiprocessing`模块不但支持多进程，其中`managers`子模块还支持把多进程分布到多台机器上。一个服务进程可以作为调度者，将任务分布到其他多个进程中，依靠网络通信。
- python的分布式进程接口简单，封装良好，适合需要把繁重任务分布到多台机器的环境下。
- Queue的作用是用来传递任务和接收结果，每个任务的描述数据量要尽量小。

###正则表达式
- 如果给出字符,就是精确匹配。
- `\d`可以匹配一个数字
- `\w`可以匹配一个字母或数字
- `.`可以匹配任意字符
- `*`表示任意个字符(包括0个)
- `+`表示至少一个字符
- `?`表示0个或1个字符
- `{n}`表示n个字符,加在后头
- `{n, m}`表示n-m个字符,加在后头
- `\s`表示匹配空白符(空格或tab等)
- 特殊字符需用`\`转义
- `[]`表示范围,`[0-9a-zA-Z\_]`可以匹配一个数字、字母或下划线,`[0-9a-zA-Z\_]+`可以匹配至少由一个数字、字母或下划线组成的字符串
- `A|B`表示匹配A或B
- `^`表示行的开头,`^\d`表示必须以数字开头
- `$`表示行的结束,`\d$`表示必须以数字结束
- python的字符串本身就是用`\`转义的,因此,建议使用`r`前缀,这样就不用考虑转义的问题了
- `match()`方法用于判断re与字符串是否匹配,若匹配成功,则返回一个`Match`对象,否则返回`None`。`Match`对象的布尔值为`True`,`None`为`False`
- 用re切分字符串比用固定的字符串更灵活:
```python
>>> 'a b   c'.split(' ')
['a', 'b', '', '', 'c']
>>> re.split(r'[\s\,\;]+', 'a,b;; c  d')
['a', 'b', 'c', 'd']
```
- re还可以用于提取子串,用`()`表示就是要提取的分组,如`^(\d{3})-(\d{3,8})$`:
```python
>>> m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
>>> m
<_sre.SRE_Match object; span=(0, 9), match='010-12345'>
>>> m.group(0)
'010-12345'
>>> m.group(1)
'010'
>>> m.group(2)
'12345'
```
- 如果正则表达式中定义了组，就可以在`Match`对象上用`group()`方法提取出子串来。`group(0)`永远表示原始字符串。`groups()`方法,将以tuple的形式返回全部分组,即不包括`group(0)`
- re默认采用贪婪匹配的原则,即匹配尽可能多的字符。在re后加`?`可以让该分组采用非贪婪匹配,即尽可能少匹配。解释:(0*)就是匹配任意个0，(\d+?)是匹配至少一个数字，加?是尽可能少的匹配
```python
>>> re.match(r'^(\d+)(0*)$', '102300').groups()
('102300', '')
>>> re.match(r'^(\d+?)(0*)$', '102300').groups()
('1023', '00')
```
- 使用re时,re模块内部做了2件事: 1.编译正则表达式，如果正则表达式的字符串本身不合法，会报错；2.用编译后的正则表达式去匹配字符。因此,出于效率考虑,可预编译正则表达式,从而省掉了之后若干次的重复编译:
```python
- >>> import re
# 编译:
>>> re_telephone = re.compile(r'^(\d{3})-(\d{3,8})$')
# 使用：
>>> re_telephone.match('010-12345').groups()
('010', '12345')
```
- 编译后生成Regular Expression对象，由于该对象自己包含了正则表达式，所以调用对应的方法时不用给出正则字符串

##常用内建模块
###datetime
- `datetime`是模块,还包含一个`datetime`类。如果仅导入`datetime`,必须引用全名`datetime.datetime`,来表示使用的是datetime模块下datetime类
- `datetime.now()`返回当前日期与时间,类型是`datetime`。也可以用`datetime(yyyy,mm,dd,hh,mm,ss)获取指定日期与时间
- 计算机存储的当前时间是以`timestamp`(时间戳)表示的,全球各地的计算机在任意时刻的`timestamp`都是相同的,时区已经没有意义了
- `timestamp`方法可将`datetime`类型转换得到timestamp,返回。timestamp是一个浮点数,小数位表示毫秒数。其他编程语言的timestamp可能使用整数表示毫秒数,做除法即可
- `fromtimestamp()`将timestamp转化为datetime。timestamp是浮点数,没有时区概念,但datetime是有时区的,`fromtimestamp`实际上是将时间戳与本地时间做转换
- `utcfromtimestamp`将时间戳直接转换到UTC标准时区事件,即格林威治时间
- `strftime`将datetime转换为字符串,需要指定一个时间的格式`format`
- 时间的加减,使用`timedelta`可以方便计算,而不用利用timestamp来回转化和计算
```python
>>> from datetime import datetime, timedelta
>>> now = datetime.now()
>>> now
datetime.datetime(2015, 5, 18, 16, 57, 3, 540997)
>>> now + timedelta(hours=10)
datetime.datetime(2015, 5, 19, 2, 57, 3, 540997)
>>> now - timedelta(days=1)
datetime.datetime(2015, 5, 17, 16, 57, 3, 540997)
>>> now + timedelta(days=2, hours=12)
datetime.datetime(2015, 5, 21, 4, 57, 3, 540997)
```
- `datetime`类有一个时区属性`tzinfo`,默认是`None`,因此无法区分是哪个时区。可以强行设置:
```python
>>> from datetime import datetime, timedelta, timezone
>>> tz_utc_8 = timezone(timedelta(hours=8)) # 创建时区UTC+8:00
>>> now = datetime.now()
>>> now
datetime.datetime(2015, 5, 18, 17, 2, 10, 871012)
>>> dt = now.replace(tzinfo=tz_utc_8) # 强制设置为UTC+8:00
>>> dt
datetime.datetime(2015, 5, 18, 17, 2, 10, 871012, tzinfo=datetime.timezone(datetime.timedelta(0, 28800)))
```
- `utcnow()`获取当前的UTC时间。要做时区转换,要为设置好当前时间的时区,否则无可比较性。
- 利用`astimezone`来进行时区转换,得到对应时区的时间 ![python_time_format.png-134.7kB][1]

###collections
- collectionshs是python内建的`集合模块`,提供了许多集合类
- `namedtuple`是一个用来创建自定义的`tuple`对象的函数,规定了`tuple`元素的个数,并可以用属性而不是索引来引用`tuple`的某个函数:
- namedtuple(typename, field_names, verbose=False, rename=False).Returns a new subclass of tuple with named fields
- 使用list存储数据时，按索引访问元素很快，但是插入和删除元素就很慢了，因为list是线性存储，数据量大的时候，插入和删除效率很低。
- `deque`是为了实现高效插入和删除操作的双向列表,适合于队列和栈。它实现了`list`的`append()`和`pop()`,还支持`appendleft()`和`popleft()`
- 使用`dict`时,引用的key不存在,将抛出`KeyError`。使用`defaultdict`,可以在key不存在时,返回一个默认值。默认值由调用函数返回,而函数在创建`defaultdict`对象时传入:
```python
>>> from collections import defaultdict
>>> dd = defaultdict(lambda: 'N/A')
>>> dd['key1'] = 'abc'
>>> dd['key1'] # key1存在
'abc'
>>> dd['key2'] # key2不存在，返回默认值
'N/A'
```
- 使用`dict`时,key是无序的。在对`dict`做迭代时,无法确定key的顺序,如果要保持key的顺序,可以使用`OrderedDict`,其key是按插入的顺序排列的,而非key本身顺序。`OrderedDict`可以实现FIFO的`dict`,当容量超出限制时,先删除最早添加的key
- `Counter`是一个简单的计数器,实际是`dict`的一个子类。更多内容,查看帮助文档好啦,很详细

###base64
- Base64是用64个字符表示任意二进制数据的方法
- Base64编码将3字节的二进制数据编码为4字节的文本数据,长度增加了33%,但编码后的文本数据可在邮件正文,网页等直接显示
- Base通过查表的编码方法,因此不能用于加密,适用于小段内容的编码,如数字证书签名、cookie等
- Base64是一种任意二进制到文本字符串的编码方法,常用于URL、cookie、网页中传输少量二进制数据

###struct
- python中,`str`既是字符串又可以表示字节,所以,字节数组 = str
- `struct`模块,解决`bytes`与其他二进制数据类型的转换
- `struct`的`pack`函数把任意数据类型变成`bytes`
```python
>>> import struct
>>> struct.pack(">I", 10240099)
b'\x00\x9c@c'
```
- `>I`,`>`表示字节顺序是big-endian,即网络序,`I`表示4字节无符号整数,参数个数要和处理指令一致
- unpack把bytes变成相应的数据类型：
```python
>>> struct.unpack('>IH', b'\xf0\xf0\xf0\xf0\x80\x80')
(4042322160, 32896)
```
- 根据`>IH`的说明，后面的`bytes`依次变为`I`：4字节无符号整数和`H`：2字节无符号整数
- 在`bytes`中,无法显示为ASCII字符的字节,用`\x##`表示

###hashlib
- `摘要算法`(哈希算法、散列算法):通过一个函数,将任意长度的数据转换为一个长度固定的数据串。摘要算法是一个单向函数,反向通过哈希值计算数据很难
```python
import hashlib

md5 = hashlib.md5()
md5.update("Engine".encode('utf-8'))
print(md5.hexdigest())
....
```
- 当数据量很大时,可分多次调用`update()`,结果与一次性调用`update()`一样
- MD5是最常见的摘要算法,速度快,生成结果是固定的128bit字节,通常用一个32位的16进制字符串表示
- SHA1摘要算法的使用与MD5一样,其结果是160bit字节,通常用40位的16进制字符串表示
- 越安全的摘要算法越慢,且摘要长度更长
- 摘要算法的用途: 1.正确的保存口令(密码),不存储用户的明文口令,而是存储用户口令的摘要; 2.用于验证网络上下载的东西是否被篡改过
- 由于常用口令的MD5值容易被计算出来,要确保存储的用户口令的安全性,通过对原始口令加复杂字符串来实现。如果多个用户使用了相同的简单密码,数据库中将存储多条相同的MD5值。一种解决办法是使用用户名作为复杂字符串的一部分
- 摘要算法不是加密算法,因为无法通过摘要反推明文,只能用于防篡改。它的单向计算特性决定了可以在不存储明文口令的情况下验证用户口令

###itertools
- `itertools`模块提供了许多用于操作迭代对象的函数
- `count()`会创建一个无限的迭代器
- `cycle()`会把传入的序列无限重复下去
- `repeat()`负责把一个元素无限重复下去,可以通过第二个参数限定重复次数
- 无限序列只有在`for`迭代时,才会无限迭代下去。
- 通常可以通过`takewhile()`等函数条件,从一个无限序列中截取出一个有限序列:
```python
>>> natuals = itertools.count(1)
>>> ns = itertools.takewhile(lambda x: x <= 10, natuals)
>>> list(ns)
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```
- `chain()`将一组迭代对象串联起来,形成更大的迭代器
- `groupby()`将迭代器中相邻的重复元素挑出来放在一起。实际上挑选规则是通过函数完成的,只要作用于函数的两个元素返回的值相等,就认为是一组,而函数返回值作为组的key。
```python
>>> for key, group in itertools.groupby('AaaBBbcCAAa', lambda c: c.upper()):
...     print(key, list(group))
...
A ['A', 'a', 'a']
B ['B', 'B', 'b']
C ['c', 'C']
```

###XML
- 操作XML有两种方法：DOM和SAX。DOM会把整个XML读入内存，解析为树，因此占用内存大，解析慢，优点是可以任意遍历树的节点。SAX是流模式，边读边解析，占用内存小，解析快，缺点是需要自己处理事件
- 在Python中使用SAX解析XML非常简洁，通常我们关心的事件是start_element，end_element和char_data，准备好这3个函数，然后就可以解析xml了。
- 最简单有效的生成xml的方法是拼接字符串

###HTML Parser
- HTML本质上是XML的子集,HTML的语法没有XML那么严格,不能用DOM或SAX来解析HTML
- `feed()` - feed data to the parser

###urllib
- urllib提供了一系列操作URL的功能
- urllib的`request`模块可以非常方便地抓取URL内容，也就是发送一个GET请求到指定的页面，然后返回HTTP的响应
- 通过往`Request`对象添加http头,可以将请求伪装称浏览器
- 要以POST发送一个请求,需要将`data`已bytes形式传入
- 如果需要利用proxy来访问,则可以利用`ProxyHandler`来处理

##图形界面
- 我们编写的Python代码会调用内置的Tkinter,Tkinter封装了访问Tk的接口;Tk是一个图形库,支持多操作系统,使用Tcl语言开发;Tk会调用操作系统提供的本地GUI接口,完成最终的GUI
- 从`Frame`中派生出一个自定义类,如`Application`,这是所有`Widget`的父容器
- 在gui中,每个Button, Label, 输入框,都是一个Widget,Frame是可以容纳其他Widget的Widget,所有的Widget组合起来就是一棵树
- `pack()`方法将Widget加到父容器中,并实现布局。`grid()`可实现更复杂的布局
- gui程序的主线程负责监听来自OS的消息,并依次处理每条消息

##网络编程
- 网络通信,实际是两台计算机上的两个进程之间的通信
- 用Python进行网络编程,就是在Python程序本身这个进程内,连接别的服务进程进行通信

###TCP编程
- 通常用一个Socket表示“打开了一个网络链接”,打开一个Socket需要知道IP地址与端口号,再指定协议类型
```python
# 导入socket库:
import socket

# 创建一个socket:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('www.sina.com.cn', 80)) #参数是tuple,包含地址与端口号,IP地址由域名自动解析
```
- 创建`Socket`时,`AF_INET`指定使用IPv4协议,若要使用IPv6,应指定`AF_INET6`,`SOCK_STREAM`指定使用面向流的TCP协议
- `80`端口是Web服务器的标准端口,STMP服务是`25`端口,FTP是`21`端口。作为服务器,提供什么样的服务,端口号必须固定下来
- 建立TCP连接之后,就可以向服务器发送请求:
```
# 发送数据
s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
# 之后就可以接收数据了
# 通信完成通过close关闭连接

```
- TCP连接创建的是双向通道,双方都可以同时给对方法发数据.
- 服务器进程首先要绑定一个端口来监听来自其他客户端的连接.每个连接都需要一个新的进程或新的线程来处理
- 一个Socket依赖4项:服务器地址,服务器端口,客户端地址,客户端端口,依次来唯一地确定一个SOcket
- `0.0.0.0`表示将服务器程序绑定到所有网络地址(一个服务器可能有多块网卡), `127.0.0.1`表示本机的地址
- TCP服务器的编程一般步骤是:
 1. 创建SOcket, 绑定并监听
 2. 通过一个while循环来处理连接
- 一个端口,被一个SOcket绑定之后,就不能被别的SOcket绑定了


### UDP编程
- UDP是面向无连接的协议,使用时不需要建立连接,传输数据不可靠,但速度快
- 服务器端UDP编程,不需要调用`listen`方法,而直接接收来自任何客户端的数据
- 客户端使用UDP,不需要调用`connect`方法,直接通过`sendto`将数据发给服务器
- 服务器绑定UDP和TCP端口互不冲突,同一个端口可以各自绑定

###电子邮件
- 一封邮件的旅程: `发件人- MUA - MTA - MTA ... - MTA - MDA - MUA -收件人`
- 发送邮件时,MUA与MTA之间使用的协议是STMP, MTA与MTA之间也是用STMP
- 接收邮件时,MUA与MDA之间使用POP3或IMAP.IMAP的优点是能取邮件,还能直接操作MDA上存储的邮件
- python的`email`模块负责构造邮件,`stmplib`模块负责发送邮件
- 构造`MIMEText`对象时,第一个参数是邮件正文,第二个参数是MIME的subtype,传入`plain`表示纯文本,传入`html`即发送html邮件,使用`alternative`同时支持html与纯文本
- 带附件的邮件可以看作文本与各附件的组合,构造`MIMEMultipart`对象代表邮件本身,往其中添加`MIMEText`作为正文,添加`MIMEBase`对象表示附件
- 发送图片的方法是:把图片作为附件添加,在HTML中通过`src="cid:0"`把附件作为图片嵌入,多张图片编号即可
- 使用标准的25端口连接smtp服务器,使用的是明文传输.要更安全地发送邮件,可通过加密会话,即先创建ssl安全链接,再用smtp发送邮件
- gmail的smtp端口是587,提供安全stmp邮件服务.
- 构造邮件对象就是`Message`对象,如果构造一个`MIMEText`对象,就表示文本邮件对象.如果构造一个`MIMEImage`对象,就表示一个作为附件的图片.可用`MIMEMultipart`对象,将多个对象组合起来,`MIMEBase`可以表示任何对象
- POP3协议收取的是邮件的原始文本,需要使用`email`模块来解析原始文本.因此收取邮件的2步:
 1. 用`poplib`下载邮件的原始文本
 2. 用`email`解析原始文本,还原邮件对象


##数据库
- SQLite是一种嵌入式数据库,数据库即一个文件.由C写成,体积小,常被集成到各种应用程.Python3内置了SQLite3
- 表是数据库存放关系数据的集合,一个数据库通常包含多张表,表与表之间通过外键连接
- 操作数据库的第一步是连接,一个数据库连接称为Connection
- 连接到数据库之后,需要打开游标,称为Cursor,通过Cursor执行SQL语句,然后获得结果
- 使用python的db-api时,`Connection`与`Cursor`使用完毕切记要关闭. 使用`try ... finally ...`确保正确关闭
- 插入\更新\删除操作,执行结果由`rowcount`返回影响的行数,
- 选择操作,通过`fetchall()`拿到结果集,结果集是一个list,每个元素是一个tuple,对应一条记录
- 如果sql语句带有参数,需要将参数按位置传给`execute`方法,用`?`占位
- sqlite的特点是轻量级,可嵌入,但不能承受高并发访问,适合于桌面及移动应用;mysql是为服务器设计的数据库,能承受高并发访问,占内存资源远大于sqlite
- 使用mysql,执行插入\更新\删除等操作后要调用`commit`提交事务
- mysql的占位符用`%s`
- ORM: Obeject-Relational Mapping,将关系数据库的表结构映射到对象上
- `create_engine()`用来初始化数据库连接,连接信息表示为:`数据库类型+数据库驱动名称://用户:口令@机器地址:端口/数据口名`
- 使用`sqlalchemy`,`DBSession`对象可视为当前数据库连接
- orm将数据库的行与相应的对象建立关联,互相转换

##网络编程
> HTTP请求的流程
- 步骤1：浏览器首先向服务器发送HTTP请求，请求包括：
 - 方法：GET还是POST，GET仅请求资源，POST会附带用户数据；
 - 路径：/full/url/path；
 - 域名：由Host头指定：Host: www.sina.com.cn
 - 以及其他相关的Header；
 - 如果是POST，那么请求还包括一个Body，包含用户数据。
- 步骤2：服务器向浏览器返回HTTP响应，响应包括：
 - 响应代码：200表示成功，3xx表示重定向，4xx表示客户端发送的请求有错误，5xx表示服务器端处理时发生了错误；
 - 响应类型：由Content-Type指定；
 - 以及其他相关的Header；
 - 通常服务器的HTTP响应会携带内容，也就是有一个Body，包含响应的内容，网页的HTML源码就在Body中。
- 步骤3：如果浏览器还需要继续向服务器请求其他资源，比如图片，就再次发出HTTP请求，重复步骤1、2。

 - Web采用的HTTP协议采用了非常简单的请求-响应模式，从而大大简化了开发。当我们编写一个页面时，我们只需要在HTTP请求中把HTML发送出去，不需要考虑如何附带图片、视频等，浏览器如果需要请求图片和视频，它会发送另一个HTTP请求，因此，一个HTTP请求只处理一个资源。
- HTTP响应如果包含body,通过`\r\n\r\n`分隔.body的数据类型由`Content-Type`决定,而非后缀名
- HTML的<head>,<body>与HTTP的header,body不是一个玩意!!
- HTML是富文本类型,定义了网页内容
- CSS(Cascading Style Sheets,层叠样式表),用来控制html元素的展现方法
- JavaScript是为了让html具有交互性的脚本语言
- web应用程序,入口都是一个wsgi函数,http请求的所有输入信息通过`environ`获得,http响应的输出通过`start_response`加上函数返回值作为body
- 使用框架,可以将注意力从wsgi处理函数转移到url+对应的处理函数
- 使用模板,就是预先准备好一个html文档,之后传入数据,替换就可得到最终的html
- MVC:model-view-controller
- 通过mvc,在python中处理model,controller,而view通过模板处理,实现python与html的分离
- 在jinja2模板中,{{ name}}表示要替换的变量,{{% ... %}}表示指令


##异步IO
- 同步IO模型即,遇到IO操作,必须等待IO操作完成,才能继续下一步操作
- 一种解决CPU处理速度与IO操作速度不匹配的方法是多线程和多进程
- 同步IO模型的代码无法实现异步IO模型,异步IO模型需要一个消息循环,在消息循环中,主线程重复"读取消息-处理消息"的过程
- `消息模型`,当遇到IO操作时,代码只负责发出IO请求,不等待IO结果,然后直接结束本轮消息处理.进入下一轮消息处理过程.当IO操作完成,将收到一条"io完成"的消息,处理该消息时就可获得IO操作结果
- 在"发出IO请求"到"消息完成"的时间里,同步io模型下,主线程只能挂起,而在异步io模型中,主线程继续处理消息循环中的其他消息
- 子程序在所有编程语言中都是层级调用的,通过栈实现.一个线程就是执行一个子程序.子程序调用总是一个入口,一个返回,调用顺序是明确的.
- `协程`看上去像子程序,但在执行过程中,子程序内部可中断,然后转而执行其他子程序.子程序的中断不是函数调用.
- 协程的最大优势在于执行效率高,切换子程序不是线程切换,而是有程序自身控制,不存在线程切换的开销.线程数量越多,协程的优势越明显.第二大优势在于不需要多线程的锁机制,共享资源不加锁,只需判断状态就可以了
- python对协程的支持通过generator实现.
- 子程序是协程的一个特例.
- `asyncio`的编程模型就是一个消息循环,使用时,获取一个`EventLoop`引用,然后将需要执行的协程放在`EventLoop`中执行.
- 通过装饰器`@asyncio.coroutine`将generator标记为coroutine类型,然后将`coroutine`放到`EventLoop`中执行.使用`asyncio`,异步操作需要在`coroutine`中通过`yield from`调用另一个coroutine实现异步操作.多个`coroutine`可以封装在一组task中并发执行
- python3.5中引入新的语法`async`和`await`,用于替换`asyncio.coroutine`和`yield from`
- `async`实现单线程并发io操作,用于服务器端时,可以实现单线程+`coroutine`的多用户高并发支持

##实战部分
1. 编写web app骨架
2. 创建连接池(全局),封装数据库操作,建立orm,Models
3. 编写web框架
4.
- 在web app中,所有数据,都存储在数据库中(不然还能存在哪里- -)
- 应将数据的代码,包括`select`,`insert`,`update`,`delete`等操作用函数封装起来,方便维护,以及代码复用
- 协程,不能用普通的同步io操作,所有用户都由一个线程服务.
- 异步编程的一个原则:一旦决定使用异步,则系统的每一层都必须是异步,"开弓没有回头箭"
- 数据库连接池负责分配、管理和释放数据库连接，它允许应用程序重复使用一个现有的数据库连接，而不是再重新建立一个；释放空闲时间超过最大空闲时间的数据库连接来避免因为没有释放数据库连接而引起的数据库连接遗漏.
- 连接池基本的思想是在系统初始化的时候，将数据库连接作为对象存储在内存中，当用户需要访问数据库时，并非建立一个新的连接，而是从连接池中取出一个已建立的空闲连接对象。使用完毕后，用户也并非将连接关闭，而是将连接放回连接池中，以供下一个请求访问使用。而连接的建立、断开都由连接池自身来管理。同时，还可以通过设置连接池的参数来控制连接池中的初始连接数、连接的上下限数以及每个连接的最大使用次数、最大空闲时间等等。也可以通过其自身的管理机制来监视数据库连接的数量、使用情况等
- 要坚持使用带参数的sql,而不是拼接字符串,防止sql注入攻击
- `yield from`的作用是调用子协程,并直接获得子协程的返回结果
- 设计ORM时,在类级别上定义的属性用来描述对象和表的映射关系,而实例属性必须通过`__init__()`方法初始化
- 编写ORM狂简,所有的类都只能动态定义,因为只有使用者才能根据表的结构定义出对应的类来?
- `metaclass`可隐式地被子类继承,而子类自己感受不到
- `ModelMetaclass`做了2件事情:
 1. 排除掉对`Model`类的修改
 2. 在当前类中查找定义的类的所有属性.如果找到一个Field属性,将其保存到一个`__mappings__`dict中,同时从类属性中删除该Field属性,
 3. 将表名保存到`__table__`中,

### web server
- 编写URL的处理函数的一般步骤:
 1. 编写用`@asyncio.coroutine`装饰的函数
 2. 从`request`中获取参数
 3. 构造`response`对象
- web框架的设计完全从使用者出发,目的是让使用者编写尽可能少的代码
- 编写简单的函数,而非引入`request`和`web.Response`的好处是可以单独测试,否则需要模拟一个`request`才能测试
- 一个定义了`__call__()`方法的类,其实例可视为函数
- 实现一个web server的一般步骤是:
 1. 创建一个`request handler`,可以是协程也可以是普通函数,其接受一个请求实例作为参数,并返回一个应答实例
 2. 创建Application实例,并将`request handler`注册到一个特定的http方法(get, post等)和路径
 3. 之后就可运行应用了
- handler
 - 接受一个请求实例作为唯一的参数,并返回`SteamResponse`的可调用的对象
 - handler可以是一个协程
 - handlers are setup to handle requests by registering them with the Application.router on a paticular route(http method and path pair):`app.router.add_route("GET", "/", hanler)`(http method参数接受通配符)
- resources and routes
 - 在`router`内部,是一张资源的列表(list of resources)
 - 每个资源至少有一个路径
 - 资源是相应被请求的url在路由表中的一个条目
 - 路径(route)通过相应的web handler处理http method
- `REST` is short for Representational State Transfer(具象状态传输),是一个种www软件架构风格,其特点是:
 1. 资源由URI来指定
 2. 对资源的操作包括获取,创建,修改和删除,对应http协议的get,post,put,delete
 3. 通过操作资源的表现形式来操作资源
 4. 资源的表现形式是xml,或html,或json,取决于读者是机器还是人,是消费weib服务的客户端还是web浏览器
- REST的要求:
 1. C/S架构: 通信只能由客户端单方面发起,表现为请求-响应形式
 2. 连接协议具有无状态性: 通信的会话状态(Session state)应该全部由客户端负责维护
 3. 能利用cache机制增进性能: 响应内容可以在通信链某处被缓存,以改善网络效率
 4. 一致性的操作界面: 通信链的组件之间通过统一的接口相互通信,以提高交互的可见性
 5. 层次化的系统: 通过限制组件的行为(即每个组件只能看到与其交互的紧邻层), 将架构分解为若干等级的层
 6. 所需代码: 支持通过下载并执行一些代码,对客户端的功能进行扩展
- 如果一个url返回的不是html,而是机器能直接解析的数据,则这个url就可以看作是一个web api
- web api将web app的功能全部封装了,通过api就能操作数据,极大地将前端和后端的代码隔离,使得后台易于测试,前端代码编写更简单
- 客户端调用api时,必须通过`错误代码`来区分api调用是否成功.错误码用来告诉调用者错误的原因.很多api用整数表示错误码,这种方式很难维护,客户端拿到错误码还需查表得知错误信息,更好的方式是使用字符串表示错误代码
- 用户管理是绝大部分web网站都需要解决的问题,设计用户的注册与登录
- 通过API实现用户注册功能, 用户口令是客户端经过sha1计算后的hash字符串,服务器也并不知道用户的原始口令.(这一定程度上保证了安全)
- 写好用户注册API后,创建一个注册页面,让用户填写表单,然后**提交数据到注册用户的api**(前端后台就是这么联系起来的)
- http协议是无状态协议,服务器要跟踪用户状态,只能通过cookie实现.大多数web框架提供session功能来封装保存用户状态的cookie
- session的优点是简单,可以直接从session中提取用户登录信息;其缺点是服务器需要在内存中维护一个映射表来存储用户登录信息
- 通过cookie验证用户登录,每次用户访问任意url时,都会对cookie进行验证.保证了服务器处理任意url都是无状态的,可以扩展到多台服务器
- 登录成功后,由服务器生成一个cookie发送给浏览器,保证了cookie不会被客户端伪造出来
- web开发,后台代码相对容易,前端由于混合了html,css,JavaScript,相对较难
- 前端页面通常是动态页面,即前端页面往往由后台代码生成.
- asp,jsp,php等都是通过模板方式生成前端页面的,如果在页面上大量使用js,模板方式会导致js代码与后台代码耦合性较高,以致难于维护.其根本原因在于负责显示的html dom模型与负责数据和交互的js代码没有分隔清楚
- mvvm(model view viewmodel)借鉴了桌面应用程序的mvc思想,在前端页面中,把model用纯js对象表示,view是纯html.由于model表示数据,view负责显示,两者做到了最大限度的分离.通过viewmodel将model,view关联起来,它负责把model的数据同步到view显示出来,还负责把view的修改同步回model
- 用js编写通用的viewmodel,而实现整个mvvm模型的复用
- angular JavaScript, knockoutjs,vuejs等就是mvvm框架0 0
- 初始化vue时,需要指定3个参数:
 1. el: 根据选择器查找绑定的view,如`#vm`,是一个id为`vm`的dom,对应一个`<div>`标签
 2. data: JavaScript 对象表示的model,
 3. methods: view可以触发的js函数,`submit`就是提交表单时触发的函数
- 之后通过`v-model`将model与view关联起来
- mvvm中,model与view可以双向绑定
- 在js逻辑中修改了model,这个修改会立即反应到view上,
- 借助mvvm,可以将复杂的显示逻辑交给框架完成.由于后台编写了独立的rest api,所以前端用ajax提交表单非常容易,前后端分离得非常彻底
- mvvm模式不但可以用于表单,还能用于复杂的页面管理.模板页面首先通过api`get /api/blogs?page=?`取得model,再通过Vue初始化MVVM.通过`v-repeat`将model中的数组`blogs`直接变层多行
- django的开发环境在debug模式下,可以自动重新加载,
- pyton本身提供了重新载入模块的功能,但不是所有模块都被重新载入
- 检测代码改动,一旦有改动,就自动重启服务器.--从而提高开发效率,不必每次修改代码都手动重启服务器
- 实现方法:编写辅助程序`pymonitor.py`,让它启动`wsgiapp.py`,并时时监控`www`目录下的代码改动,一旦检测到代码改动,首先将`wsgiapp.py`进程杀死,再重启,就完成了服务器进程的自动重启
- python的第三方库`watchdog`利用os的api来监控目录文件的变化,并发送通知.利用`watchdog`接收文件变化的通知,如果是`.py`文件,就自动重启`wsgiapp.py`.利用python自带的`subprocess`实现进程的启动与终止,并将输入输出重定向到当前进程的输入输出中
- 选择nginx作为服务器,用于处理静态资源,同时作为**反向代理**将动态请求交给python代码处理:模型如下

```text
nginx <--> awesome <--> mysql
```

- nginx负责分发请求

```text
browser
  /\
  ||
  \/
nginx <-(url=/static/)-> /srv/awesome/www/static
  /\
  ||
(url=/)
  \/
awesome <--> /srv/awesome/www
```

- 在服务器上部署,要考虑新版本运行不正常的情况.因此每次用新的代码覆盖掉旧的文件是不可取的,需要一个类似版本控制的机制--利用linux提供软连接功能,将`www`作为软连接,它指向哪个目录,那个目录就作为当前运行的版本,而nginx和python代码的配置文件只需指向`www`即可
- nginx可作为服务进程直接启动,但`app.py`不行.因此用`supervisor`管理进程工具,它时刻监控服务进程,若服务进程意外退出,supervisor可以自动重启服务
 - nginx: 高性能web服务器 + 负责反向代理
 - supervisor: 监控服务进程的工具
 - mysql: 数据库服务
- 正确的部署方式应该是使用工具配合脚本来完成自动部署,此处选用fabric.fabric使用ssh直接登录服务器并执行部署命令

  [1]: http://static.zybuluo.com/KissG/s7h8s5xcx8vk9zs4ryazz0tq/python_time_format.png
