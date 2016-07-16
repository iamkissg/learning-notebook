#Built-in Functions

- `abs(x)` - 返回数字的绝对值. 可以是整型数, 浮点数, 甚至复数, 复数将返回"模"
- `all(iterable)` - 检验可迭代对象的所有元素, 只有当所有元素的值都非空, 才返回`True`
- `any(iterable)` - 只要可迭代对象有一个元素的值没空, 就返回`True`
- `ascii(object)` - 对于给定的对象, 返回一个可打印的字符串, 非ascii字符将被转移.

```python
>>> ascii(1)
'1'
>>> ascii("I")
"'I'"
```

- `bin(x)` - 将整型数转化为二进制字符串, 结果是合法的python表达式

```python
>>> bin(35)
'0b100011'
```

- `class bool([x])` - 返回布尔值. x 将首先被标准的`truth testing procedure`测试. `bool`类是整型类的子类, 不能再被继承
- `class bytearray([source[, encoding[, errors]]])` - 返回二进制数组. `bytearray`是0-255的可变整数序列, 拥有大多数可变序列的方法, 并拥有`bytes`类的方法.
 - 若`source`为`str`, 则必须给定`encoding`, 将用`str.encode`方法将字符串转为二进制类型
 - 若为一个整数, 数组大小被设为给定值, 但元素全被初始化为空字节
 - 若为`iterable`, 必须是0-255的整型数的可迭代对象, 将被初始化为数组的内容
 - 若为实现了`buffer`接口的对象, 该对象的只读缓存内容将被用于初始化数组

```python
In [1]: bytearray("Engine")
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-1-329f6e44ee12> in <module>()
----> 1 bytearray("Engine")

TypeError: string argument without an encoding

In [2]: bytearray("Engine", "utf-8")
Out[2]: bytearray(b'Engine')

In [3]: bytearray(15)
Out[3]: bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

In [4]: bytearray([1,2,3,4,5])
Out[4]: bytearray(b'\x01\x02\x03\x04\x05')
```

- `class bytes([source[, encoding[, errors]]])` - 返回一个二进制对象, `bytes`是`bytearray`的不可变形式
- `callable(object)` - 根据对象的可调用特性, 返回布尔值. 即使返回值为真, 调用也可能失败
- `chr(i)` - 返回对应`Unicode`码的字符, 注意python没有单独的字符类型, 一个字符就是一个长度为1的字符串. 有效范围是0-1,114,111
- `classmethod(function)` - 将函数作为参数, 并返回一个类方法. 因此, 常被用作装饰器`@classmethod`
- `compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1)` - 将`source`编译成代码或抽象语法树(AST). 先跳过, 详情看[这里](https://docs.python.org/3/library/functions.html#compile)
- `class complex([real[, imag]])` - 将字符串或数字转为复数. 如果`real`是字符串, 那么不需要(不能)再给出第二个参数. 两个参数可以是任意数字类型的值, 包括复数- -.使用字符串作为参数时, 字符串内部不允许出现空格, 否则会出错.

```python
In [5]: complex("1 + 2J")
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-5-af478b56c019> in <module>()
----> 1 complex("1 + 2J")

ValueError: complex( arg is a malformed string

In [6]: complex("1+2J")
Out[6]: (1+2j)

In [7]: complex()
Out[7]: 0j
```

- `delattr(object, name)` - 删除对象的属性. 因此, `name`必须是给定对象的一个属性. `delattr(x, 'foobar')`等价于 `del x.foobar`
- `class dict(**kwarg)`\\`class dict(mapping, **kwarg)`\\`class dict(iterable, **kwarg)` - 返回一个字典对象
- `dir([object])` - 当不给定参数时, 返回当前作用域的名称列表; 给定参数时, 将尽力去返回给定对象的合法属性的列表
 - 如果一个对象有`__dir__()`方法, 使用`dir(object)`时, 将调用`__dir__()`方法. 但该方法必须返回一个属性的列表. 这就允许对象自定义`__getatt__()`或`__getattribute__`()`函数来自定义`dir()`的行为
 - 如果对象没有`__dir__()`方法, 则`dir()`函数将从对象的`__dict__`属性获取对象信息.
 - 对于不同类型的对象, `dir()`将提供不同的机制. 目的是为了提供相关性更强的信息, 而非完整的:
  - 针对`模块对象`, 返回模块属性的列表
  - 针对一个类型(type)或类对象, 递归地返回其属性以及所有基类的属性的列表
  - 其他情况, 返回包含对象的属性名, 类属性, 基类的属性的列表

```python
In [8]: dir()
Out[8]:
['In', 'Out', '_', '_2', '_3', '_4', '_6', '_7', '__', '___', '__builtin__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', '_dh', '_i', '_i1', '_i2', '_i3', '_i4', '_i5', '_i6', '_i7', '_i8', '_ih', '_ii', '_iii', '_oh', '_sh', 'exit', 'get_ipython', 'quit']

In [9]: a = dict()

In [10]: dir(a)
Out[10]:
['__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']
```

```python
>>> class Shape:
...     def __dir__(self):
...         return ['area', 'perimeter', 'location']
>>> s = Shape()
>>> dir(s)
['area', 'location', 'perimeter']
```

- `divmod(a, b)` - 参数为两个非复数, 范围两个数商和余数的元组.

```python
In [11]: divmod(5, 3)
Out[11]: (1, 2)
```

- `enumerate(iterable, start=0)` - 返回一个枚举对象. 使用`start`指定计数的开始
- `eval(expression, globals=None, locals=None)` - `expression`参数将被解析为一条python表达式, 专业的说法是`a condition list`, 并以`globals`和`locals`字典为命令空间. 返回值为该表达式的值.

```python
>>> x = 1
>>> eval('x+1')
2
```

- `exec(object[, globals[, locals]])` - `object`可以是字符串也可以是`code`对象.\\
以上2个函数`exec`he`eval`是动态执行python代码的一种形式
- `filter(function, iterable)` - 过滤. 等价于`(item for item in iterable if function(item))`
- `class float([x])` - 从数字或字符串构造一个浮点数. 字符串作为参数, 可包含空格,  可以表示非数字或正负无穷. 语法如下:

```python
sign           ::= "+" | "-"
infinity       ::= "Infinity" | "inf"
nan            ::= "nan"
numeric_value  ::= floatnumber | infinity | nan
numeric_string ::= [sign] numeric_value
```

- `format(value[, format_spec])` - 将`value`转为格式化的字符串表示. `format_spec`由`value`的类型决定.
- `class frozenset([iterable])` - 返回一个`frozenset`对象
- `getattr(object, name[, default])` - 返回给定对象的给定属性值, `dfefault`为不存在相应属性时的返回值
- `globals()` - 返回当前全局符号表:

```python
> a = 1
> b = 2
> globals()
{'__spec__': None, '__name__': '__main__', '__package__': None, 'a': 1, '__builtins__': <module 'builtins' (built-in)>, '__doc__': None, 'b': 2, '__loader__': <class '_frozen_importlib.BuiltinImporter'>}
```

- `hasattr(object, name)` - 返回对象是否含有属性的真值
- `hash(object)` - 返回对象的哈希值.  哈希值是整型数, 一般快速查询

```python
>>> hash("Engine")
-7462574746322254619
```

- `help([object])` - 帮助.
- `hex(x)` - 将整型数转为小写的16进制字符串, 以`0x`作为前缀
- `id(object)` - 返回对象的身份标签, 在`Cpython`中就是对对象在内存中的地址. 两个生命周期非重叠的对象可能拥有相同的`id()`值
- `input([prompt])` - 以整行的方式读取输入, 将输入转化为字符串. `prompt`为提示信息
- `class int(x=0)`\\`class int(x, base=10)` - 从数字或字符串构造整型数. 浮点数的小数部分将被截去. 若`x`不为数字, 或给定了`base`参数, 则`x`必须是一个`str`, `bytes`或`bytearray`的实例.(基数, 不太懂)
- `isinstance(object, classinfo)` - 判断是否`classinfo`类型的实例, 直接, 非直接的或者虚拟(?)的都可以. `classinfo`除了可以是类名外, 还可以是一个类名的tuple
- `issubclass(class, classinfo)` - 用于判断是否子类(直接子类, 间接子类, 虚拟子类?). 一个类被认为是它本身的一个子类. `classinfo`可以是类的tuple, 每一项都会被检查.
- `iter(object[, sentinel])` - 返回一个迭代器对象. 根据`sentinel`的不同, `object`将以不同的形式被解读.
 - 当不指定`sentinel`时, `object`必须是支持迭代协议(`__iter__()`)的对象, 或者支持序列协议(`__getitem__()`)并带有整型参数的对象.
 - 若指定了`sentinel`(哨兵), 则必须是可调用对象, 以这种方式创建迭代器, 将无参地调用其`__next__()`方法, 当返回值遇到`sentinel`的值时, 抛出`StopIteration`异常.
 - 第二种形式的`iter()`的一种有效应用是从文件按行读取, 直到遇到特定行:

```python
with open('mydata.txt') as fp:
    for line in iter(fp.readline, ''):
            process_line(line)
```

- `len(s)2` - 返回对象的长度, 即元素的数目.\\
原来, `sequence` != `collection`\\
`sequence`包括`string`, `bytes`, `tuple`, `list`, `range`等
`collection`包括`dict`, `set`, `frozen set`等
- `class list([iterable])` - list是一个可变序列类型
- `locals()` - 与`globals()`功能类似, 返回的作用域不同
- `map(function, iterable, ...)` - 对`iterable`的每个元素都运用`funtion`, 返回一个迭代器. 若给定了多个`iterable`, 相应的, `funtion`需要能接受这些iterable. 另外, 当最短的`iterable`迭代结束时, 整个map的过程也就结束了
- `max(iterable, *[, key, default])`\\`max(arg1, arg2, *args[, key])` - 当只有一个参数时, 这个参数必须是`iterable`, 将返回值最大的元素. 当以第二种形式调用时, 返回这些参数中值最大的. `key`关键字参数用于指定排序函数, `default`关键字参数用于指定默认返回值. 存在多个最大元素时, 返回第一个.
- `memoryview(obj)` -  返回给定对象的`memory view`对象(不懂)
- `min(iterable, *[, key, default])`\\`min(arg1, arg2, *args[, key])` - 与`max`相反
- `next(iterator[, default])` - 通过调用迭代器的`__next__()`方法, 返回下一个元素. `default`的用法还是作为默认值, 可避免抛出`StopIteration`
- `class object` - 返回一个"无面"对象. 它具有所有类的公有方法. 该函数不接受任何参数. `object`没有`__dict__`, 因此不能动态地添加属性
- `oct(x)` - 将给定的整数转为八进制, 并返回字符串表示. 若`x`不是`int`对像, 它必须有`__index__()`方法
- `open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)` - 打开文件, 并返回相应的`file`对象. 可选的模式有:

```text
'r' open for reading (default)
'w' open for writing, truncating the file first
'x' open for exclusive creation, failing if the file already exists
'a' open for writing, appending to the end of the file if it exists
'b' binary mode
't' text mode (default)
'+' open a disk file for updating (reading and writing)
'U' universal newlines mode (deprecated)
```

- 模式可选择性组合.\\
python区分二进制和文本io对象, 当文件以二进制模式打开时, 文件内容就以`bytes`对象形式返回, 不作任何解码. 以文本模式打开时, 文件内容将以`str`形式返回, 编码形式用`encoding`指定, 或使用`platform-dependent`编码格式.\\
- `buffering`用于设置缓冲策略. 0表示关闭缓冲(只在二进制模式下有效), 1表示行缓冲(只在文本模式下有效), >1用于设置缓冲块大小. 使用默认值(-1)时, 二进制文件将以合适大小的缓冲块; ""交互式文本文件使用行缓冲, 其他文本文件的缓冲策略同二进制文件
- `errors`字符串, 用于指示如何处理编解码错误. 可选的字符串如下:

```text
'strict' to raise a ValueError exception if there is an encoding error. The default value of None has the same effect.
'ignore' ignores errors. Note that ignoring encoding errors can lead to data loss.
'replace' causes a replacement marker (such as '?') to be inserted where there is malformed data.
'surrogateescape' will represent any incorrect bytes as code points in the Unicode Private Use Area ranging from U+DC80 to U+DCFF. These private code points will then be turned back into the same bytes when the surrogateescape error handler is used when writing data. This is useful for processing files in an unknown encoding.
'xmlcharrefreplace' is only supported when writing to a file. Characters not supported by the encoding are replaced with the appropriate XML character reference &#nnn;.
'backslashreplace' replaces malformed data by Python’s backslashed escape sequences.
'namereplace' (also only supported when writing) replaces unsupported characters with \N{...} escape sequences
```

- `newline`用于控制换行符, 可选`None`, `''`, `'\n'`, `'\r'`, `'\r\n'`\\
读取时, 若`newline`设置为`None`, 所有换行符都将被转为`'\n'`; 若为`''`, 则换行符不转换. 若为其他任意项, 则只有遇到给定的换行符, 才算一行的终结\\
写回时, 若`newline`为`None`, 则`'\n'`将被转换为系统默认的换行符; 若为`''`或`'\n'`, 不进行转换; 若为其他任意项, `'\n'`将被转为该指定的换行符
- 若使用`文件描述符`而不是`文件名`来打开文件, 并指定`closefd`为`False`, 那么底层的文件描述符将保持打开的状态直到文件被关闭. 以文件名方式打开文件, 则`closefd`必须是`True`
- `opener`参数可通过传入一个可调用的`opener`来使用. 当通过(file, flags)的方式调用`opener`时, 将得到文件对象底层的文件描述符. `opener`必须返回一个打开的文件描述符
- 文件对象的类型, 由`open`函数的模式决定. 当选择`w`, `r`, `wt`, `rt`时, 返回`io.TextIOBase`的子类对象; 带缓冲的二进制模式, 返回`io.BufferedIOBase`.其他, 遇到再说吧- -
- `ord(c)` - 返回单个unicode字符对应的编码号, 与`chr`相对
- `pow(x, y[, z])` - 返回x^y的结果, `z`表示模, 即`pow(x, y) % z`, 当相对更高效. 当指定`z`参数时, `x`, `y` 必须是整型数, 并且`y`必须是非负数
- `print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)` - 将对象打印到文本流`file`, 以`seq`作为分割, `end`作为结束. `file`, `seq`, `end`必须以关键字参数使用.\\
所有非关键字参数将被转为字符串, 以`seq`作为分隔, `end`作为结束符, 它们必须是字符串.\\
`file`必须是带`write(string)`方法的对象, 默认是`sys.stdout`. 由于打印的内容会被转为文本字符串, 因此`print()`不能用于二进制模式的文本对象.
- `class property(fget=None, fset=None, fdel=None, doc=None)` - 返回`property`属性, `fget`是获取属性值的函数, `fset`设置函数值的函数, `fdel`是删除属性值的函数, `doc`则为该属性创建了`docstring`:

```python
class C:
    def __init__(self):
        self._x = None
    def getx(self):
        return self._x
    def setx(self, value):
        self._x = value
    def delx(self):
        del self._x
    x = property(getx, setx, delx, "I'm the 'x' property.")
```

- `property`常用作装饰器. 如:

```python
class Parrot:
    def __init__(self):
        self._voltage = 100000
    @property
    def voltage(self):
        """Get the current voltage."""
        return self._voltage
```

- 上述列子就创建了一个只读的私有属性, `@property`装饰器将方法转变为一个`getter`. 同样地, 还有`setter`, `deleter`装饰器:

```python
class C:
    def __init__(self):
        self._x = None
    @property
    def x(self):
        ""I'm the 'x' property.""
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
    @x.deleter
    def x(self):
        del self._x
```

- `range(stop)`\\`range(start, stop[, step])` - 返回一个不可变序列
- `repr(object)` - 以字符串的形式返回对象的可打印部分:

```python
>>> a = [1, 2, 3, 4, 5]
>>> repr(a)
'[1, 2, 3, 4, 5]'
>>> re_x = re.compile(r'\\\\')
>>> re_x
re.compile('\\\\\\\\')
>>> repr(re_x)
"re.compile('\\\\\\\\\\\\\\\\')"
```

- `reversed(seq)` - 反转迭代器
- `round(number[, ndigits])` - 取近似值. 若省略`ndigits`, 则取`number`最接近的整数. `ndigits`用于指定取到小数点后几位. 需要注意的是, 并非单纯地使用**四舍五入**舍入. `5`会被截断.
- `class set([iterable])` - 返回集合对象
- `setattr(object, name, value)` - 设置对象的属性值, 用法与`getattr`类似. `setattr(x, 'foobar', 123)`等价于`x.foobar = 123`
- `class slice(stop)`\\`class slice(start, stop[, step])` - 返回一个切片对象.
- `sorted(iterable[, key][, reverse])` - 返回一个排序好的`list`. 可选参数必须以关键字参数形式使用. `key`参数表示排序函数, `reverse`表示是否反转. `sorted`是稳定的(stable), 此处的稳定与冒泡排序的稳定是一个意思, 即元素的相对位置并不发生改变
- `staticmethod(function)` - 返回一个静态方法. 一般用作装饰器. python的静态方法与java, c++的类似.
- `class str(object='')`\\`class str(object=b'', encoding='utf-8', errors='strict')` - 返回字符串
- `sum(iterable[, start])` - 数字求和. `start`指定起始位置.\\
`''.join(sequence)` - 将字符串序列串联起来\\
`math.fsum()` - 用于浮点数求和\\
`itertools.chain` - 串联多个可迭代对象.
- `super([type[, object-or-type]])` - 返回一个父类对象. 所以你看, 为什么`super`的第一个参数总是类名.\\
第二个参数省略的话, 返回的父类对象是不绑定到当前对象的. 第二个参数可以是当前类的实例, 也可以是当前类的子类\\
当一个类只有单一继承关系时, `super`将直接指向该父类, 而不比明确指出.
当存在多继承关系时, 可实现`diamond diagrams`(钻石图?), 多个基类可以实现相同的方法.(不懂诶)\\
`super`实现绑定之后, 可通过`点标记法`使用, 但不能隐性地通过`super()[name]`使用\\
无参使用, 尽在类定义时有效
- `tuple([iterable])` - 返回不可变的序列.
- `class type(object)`\\`class type(name, bases, dict)` - 单一参数使用时, 返回对象的类型, 返回值与`obj.__class__`的返回一样\\
3参数使用时, 则返回一个新的类对象, 是动态创建类的一种形式. `name`参数值将作为类名, 以及`__name__`的属性值, `bases`定义类该类的基类, 并作为`__bases__`属性, `dict`是一个命名空间, 其中就是类主体, 并作为`__dict__`属性值. 
- `vars([object])` - 返回模块, 类, 实例, 或任意带`__dict__`属性的对象的`__dict__`属性值.\\
模块与实例的`__dict__`是可更新的, 其他类型的对象对此可能有写的限制\\
无参使用时, 用法与`locals()`相同
- `zip(*iterables)` - 返回一个元组的迭代器, 第i个元组中的元组分别是各iterable的第i个元素. 当最短的迭代完时, 整个迭代就结束了. 当只有一个参数时, 返回一元元组的迭代器; 无参使用时, 返回空的迭代器.\\
使用`itertools.zip_longest()`, 如果希望迭代至最长的迭代结束.
- `__import__(name, globals=None, locals=None, fromlist=(), level=0)` - 包含在`import`语句中. 官方推荐不用, 那就不做记录了.
