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
