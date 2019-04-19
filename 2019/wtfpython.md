# WTF Python

### Strings can be tricky sometimes

- 由于 CPython 采取的一些优化手段, 有时候变量会引用已经存在的不可变对象, 而不是每次都创建新的变量, 这个过程称为`interning`
- 隐式的 interning 取决于很多因素, 以`str`为例:
  -  长度为 0 或 1 的字符串会被 interned
  - Interning 发生在编译时, 'wtf' 会被 interned, 而 ''.join(['w', 't', 'f']) 不会, 因为后者是运行时计算得的
  - 包含非 ASCII 字母, 数字和下划线的字符串不会被 interned, 所以 'wtf!' 不会被 interned, 因为包含 '!'
  - `a, b = 'wtf!', 'wtf!'`, Python 解释器会新建一个对象, 然后第二个变量也引用该变量; 但如果分行赋值, 第二次赋值时, 因为 'wtf!' 不会被 interned, 解释器不知道已经有一个 'wtf!', 会创新一个新的对象.
  - `Constant folding` (常数合并) 也是 Python 用到的一项技术, `'a'*7`在编译时, 为了减少运行时时钟, 会用 `'aaaaaaa'`代替. Constant folding 只发生在长度小于 20 的字符串中.

### Time for some hash brownies

```python
>>> 5 == 5.0
Tue
>>> hash(5) == hash(5.0)
True
```

- `a_dict[5]`会覆盖`a_dict[5.0]`, 因为 Python Dict 会检查比较两个 key 的 hash 值, 来确认 key 是否相同. 具有相同值的不可变对象的 hash 值相同, 如上所示.
  - 不同值的对象可能有相同的 hash 值, 称为 `hash collision`

### Return return everywhere

- 当在 "try ... finally" 语句中使用`return`, `break`或`continue`, `finally`最终会被执行
- 一个函数的返回值, 由最后的`return`决定. 鉴于上一条规则, `finally`一定会被执行, `finally`中的`return`会最后被执行

### Deep down, we're all the same

```python
class WTF:
    pass
    

>>> WTF() == WTF() # two different instances can't be equal
False
>>> WTF() is WTF() # identities are also different
False
>>> hash(WTF()) == hash(WTF()) # hashes _should_ be different as well
True
>>> id(WTF()) == id(WTF())
True
```

- `id`函数被调用时, Python 会创建一个对象, 然后将其传递给`id`函数, 然后对象就被销毁了. 连续两次操作, Python 为第二次操作分配相同的内存空间, 所以两个对象的`id`相同.
- 对象的`id`只在它的 lifetime 中是唯一的. 在对象创建之前或销毁之后, 不同的对象可能拥有相同的 id.
- `is` 返回了 False, 是因为, 先后创建了两个对象, 比较过后再分别销毁, 流程与上不同.

### For what

```python
some_string = "wtf"
some_dict = {}
for i, some_dict[i] in enumerate(some_string):
    pass


>>> some_dict # An indexed dict is created.
{0: 'w', 1: 't', 2: 'f'}
```

- `for`语句的定义: `for_stmt: 'for' exprlist 'in' testlist ':' suite ['else' ':' suite]`, 其中`exprlist`是赋值的目标, 也就是说每次迭代, 为每一项执行 `exprlist=next_value`.

```python
for i in range(4):
    print(i)
    i = 10

# 0
# 1
# 2
# 3
```

### Evaluation time discrepancy

```python
array = [1, 8, 15]
g = (x for x in array if array.count(x) > 0)
array = [2, 8, 22]

>>> print(list(g))
[8]
```

- 在生成器表达式中, `in`的子句在**声明**时被 evaluated (???), 而条件子句则在运行时被执行, 所以有了如上情况. 由于运行时重新赋值了, 所以 1 和 15 的计数器被清零了, 所以 g 中只包含 8.

```python
array_1 = [1,2,3,4]
g1 = (x for x in array_1)
array_1 = [1,2,3,4,5]

array_2 = [1,2,3,4]
g2 = (x for x in array_2)
array_2[:] = [1,2,3,4,5]

>>> print(list(g1))
[1,2,3,4]

>>> print(list(g2))
[1,2,3,4,5]
```

- 第一例中, array_1 被绑定到了新的对象上, 由于`in`语句在声明时被 evaluated, 生成器依然指向旧对象.
- 第二例中, array_2 是被更新了, 生成器指向的对象被更新了, 但对象还是那个对象.

### `is` is not what it is

- `is`操作符检查两个操作数是否指向同一对象; `==`比较两个操作数的值是否相等. 所以, `is`检测引用相等, `==`检测值相等.
- 启动 Python 时, `-5`到`256`会被自动创建, 并保存在内存中, 所以 `a=256; b=256; a is b`成立

### A tic-tac-toe where X wins in the first attempt

```python
# Let's initialize a row
row = [""]*3 #row i['', '', '']
# Let's make a board
board = [row]*3

>>> board
[['', '', ''], ['', '', ''], ['', '', '']]
>>> board[0]
['', '', '']
>>> board[0][0]
''
>>> board[0][0] = "X"
>>> board
[['X', '', ''], ['X', '', ''], ['X', '', '']]
```

- 以这种方式创建`board`时, 每个对象 `board[0]`, `board[1]`, `board[2]`是同一个 list 的引用.

### The sticky output function

```python
>>> powers_of_x = [lambda x: x**i for i in range(10)]
>>> [f(2) for f in powers_of_x]
[512, 512, 512, 512, 512, 512, 512, 512, 512, 512]
```

- 在循环中定义函数时, 且使用了循环变量, 循环函数闭包将被绑定到变量, 而非其值上.

### `is not ...` is not `is (not ...)`

- `is not`是一个二元操作符

### The surprising comma

- Python 函数的参数列表中, 末位的逗号并不总是合法.

### Backslashes at the end of string

```python
>>> print("\\ C:\\")
\ C:\
>>> print(r"\ C:")
\ C:
>>> print(r"\ C:\")

    File "<stdin>", line 1
      print(r"\ C:\")
                     ^
SyntaxError: EOL while scanning string literal

>>> print(repr(r"wt\"f"))
'wt\\"f'
```

- 在 raw string 中 (r'xxx'), `\`不具有特殊含义

### not knot

- `==`的优先级比`not`高

### Half triple-quoted strings

```python
>>> print('wtfpython''')
wtfpython
>>> print("wtfpython""")
wtfpython
>>> # The following statements raise `SyntaxError`
>>> # print('''wtfpython')
>>> # print("""wtfpython")
```

- 前面的例子比较好理解, 就是 string concatenation. 后面的例子, Python 解释器将 `'''`和`"""`视作一个整体, 即三引号, 但是并没有等到预期的另一半, 故报错.

### What's wrong with booleans

- Booleans 是`int`的子类, `True`的值为 1, `False`的值为 0

### Class attributes and instance attribute

- 类变量和*类实力中的变量(???)*被当作类对象的字典来处理. 如果当前类的字典中没有某个变量名, 将在其父类中中进行搜索
- `+=`操作符直接 (in-place) 更新可变对象, 不会创新新对象.

### Mutating the immutable

```python
some_tuple = ("A", "tuple", "with", "values")
another_tuple = ([1, 2], [3, 4], [5, 6])

>>> some_tuple[2] = "change this"
TypeError: 'tuple' object does not support item assignment
>>> another_tuple[2].append(1000) #This throws no error, modify list
>>> another_tuple
([1, 2], [3, 4], [5, 6, 1000])
>>> another_tuple[2] += [99, 999]  # modify tuple
TypeError: 'tuple' object does not support item assignment
>>> another_tuple
([1, 2], [3, 4], [5, 6, 1000, 99, 999])
```



- 不可变序列: 一个不可变序列一旦创建就不能再修改了, 如果该对象包含其他对象的引用, 而这些变量又是可变的话, 它们确实可以被修改, 但是直接被该不可变对象引用的对象不能被修改
- `+=`操作符的修改是 **in-place** 的.

### The disappearing variable from outer scope

```python
def f(x):
    del(x)
    print(x)

x = 5

>>>f(x)
UnboundLocalError: local variable 'x' referenced before assignment
>>>x
5
```

- Python 的函数有分离的作用域

### From filled to None in one instruction

- 一些方法更新 sequence/mapping 对象 `in-place`, 并返回 `None`. 背后的原理是: 避免创建一份对象的拷贝, 提高性能

### Subclass relationships

- Python 的子类关系是非传递的, 即**我的子类的子类不是我的子类**.

### Miracle

```python
a, b = a[b] = {}, 5

>>> a
{5: ({...}, 5)}
```

- Python 的赋值语句: `(target_list "=")+ (expression_list | yield_expression)`
- 赋值语句 evaluates 表达式列表 (可以是单个表达式, 也可以是逗号分隔的列表, 后者生成一个 tuple), 然后按从左到右的顺序, 将单个对象依次赋给目标列表中的变量.
- `(target_list "=")+`中的 `+`意味着此处可以有多个 target list. 上例中, target lists 是 `a, b` 和`a[b]`, 而`expression list`只有 1 个 `{}, 5`
- 当 expression list 被 evaluated 后, 其值被 unpacked, 按从左到右的顺序赋给 target lists, 先是 `{}, 5` 赋给 `a, b`.
- 第二个 target list `a[b]`, 是一个变量, 所以 expression list 作为一个 tuple, 不会被 unpacked, 于是被赋与了 `({}, 5)`.
- 这里存在一个循环引用, `{...}`指向 `a` 已经引用的对象, 所以 `a[b][0] is a` 为真.

```python
# 上例可以拆成
a, b = {}, 5
a[b] = a, b
```

## Appearances are deceptive

### Skiplines

```python
>>> value = 11
>>> valuе = 32
>>> value
11
```



- 一些非西文字符看起来和英文字母一毛一样, 眼睛睁得再大也很难瞧出区别, 上例中就有特殊字符, 两个*value*中一个是 e, 一个不是 e, 是两个变量名!
- `ord()`函数返回字符的 Unicode 编码, 可用于检查看起来相同的字符是否真的是同一个字符.

### Teleportaition (隐形传输)

```python
import numpy as np

def energy_send(x):
    # Initializing a numpy array
    np.array([float(x)])

def energy_receive():
    # Return an empty numpy array
    return np.empty((), dtype=np.float).tolist()

>>> energy_send(123.456)
>>> energy_receive()
123.456
```

- `energy_send`函数创建了 numpy 数组但没有返回, 使得那篇内存空间被释放, 可以再分配; `np.empty()`在没有重新初始化的情况下, 返回下一片空内存块的值, 恰好是刚刚被释放的那部分

## Watch out for the landmines

### Modifying a dictionary while iterating over it

- 一边对字典进行迭代, 一边对其进行编缉是不被支持的

### Stubborn `del` operator

- `del x` 不直接调用 `x.__del__()`.
- 调用 `del x`时, x 的计数减 1, 当计数减到 0 时, 调用 `x.__del__()`

### Deleting  a list item while iterating

```python
list_1 = [1, 2, 3, 4]
list_2 = [1, 2, 3, 4]
list_3 = [1, 2, 3, 4]
list_4 = [1, 2, 3, 4]

for idx, item in enumerate(list_1):
    del item

for idx, item in enumerate(list_2):
    list_2.remove(item)

for idx, item in enumerate(list_3[:]):
    list_3.remove(item)

for idx, item in enumerate(list_4):
    list_4.pop(idx)
    
>>> list_1
[1, 2, 3, 4]
>>> list_2
[2, 4]
>>> list_3
[]
>>> list_4
[2, 4]
```

- 不要在对对象进行迭代时对其进行修改!  正确的做法是, 对它的拷贝进行迭代, 即上例的 `list_3`的操作
- `del var_name` 只是从局部或全局命名空间中去除了 `var_name`的绑定
- `remove`去除了第一个匹配到的值, 匹配不到抛出异常`ValueError`
- `pop`去除索引指定位置的元素, 并返回它, 非法索引抛出`IndexError`
- 上例的 2 和 4, 元素被剔除之后 (以第一次为例), 下一次迭代时, 从索引 1 开始, 此时对应的值是 3.

### Loop variables leaking out

```python
for x in range(7):
    if x == 6:
        print(x, ': for x inside loop')
print(x, ': x in global')

6 : for x inside loop
6 : x in global
```

- Python 中, for 循环使用它所在的域, 并在循环结束后, 将循环变量留在了该域中. 

### Beware of default mutable arguments

```python
def some_func(default_arg=[]):
    default_arg.append("some_string")
    return default_arg

>>> some_func()
['some_string']
>>> some_func()
['some_string', 'some_string']
>>> some_func([])
['some_string']
>>> some_func()
['some_string', 'some_string', 'some_string']
```

- 函数的默认可变参数, 在每次调用函数的时候并没有真的被初始化. 相反, 最近赋给它的值将被当作默认值
- 避免上述问题的一个办法是, 给可变参数赋`None`.

### Catching the Expceptions

- `except`要捕获多个异常时, 要用 `except (FirstError, SecondError) as e`

### Same operands, different story

```python
a = [1, 2, 3, 4]
b = a
a = a + [5, 6, 7, 8]
>>> a
[1, 2, 3, 4, 5, 6, 7, 8]
>>> b
[1, 2, 3, 4]

a = [1, 2, 3, 4]
b = a
a += [5, 6, 7, 8]>>> a
[1, 2, 3, 4, 5, 6, 7, 8]
>>> b
[1, 2, 3, 4, 5, 6, 7, 8]
```

- `a += b` 并不总是等价于 `a = a + b`
- `a = a + [5, 6, 7, 8]`生成了新的 list, a 被绑定到新的对象上, 而 b 不变
- `a += [5, 6, 7, 8]` 是 in-place 操作, 修改了旧的 list

### The out of scope variable

```python
a = 1
def some_func():
    return a

def another_func():
    a += 1
    return a

>>> some_func()
1
>>> another_func()
UnboundLocalError: local variable 'a' referenced before assignment
```

- 当为域内一个变量赋值, 它就变成了该域内的局部变量, 上例的 `another_func`中的 a 即是如此.

### Be careful with chained operations

### Name resolution ignoring class scope

```python
x = 5
class SomeClass:
    x = 17
    y = (x for i in range(10))
>>> list(SomeClass.y)[0]
5



x = 5
class SomeClass:
    x = 17
    y = [x for i in range(10)]


>>> SomeClass.y[0]
5
```

- 类定义中嵌套的域, 将忽略类级绑定的名称 (其实我还是不太明白 ???)
- 生成器有它自己的域; Python 3 开始, list comprehension 也有自己的域了

## The Hidden treasures

### ### Interesting

```python
import this

>>> love = this
>>> this is love
True
>>> love is True
False
>>> love is False
False
>>> love is not True or False
True
>>> love is not True or False; love is love  # Love is complicated
True
```

### Yes, it exists

- try 之后的`else`由称为`completion clause`, 在 try 中的语句执行完毕后, 被执行

## Miscellaneous

- 在两个以上级联字符串时, `+=`比`+`更快 (`s1 += s2 + s3`)
- 不要用`+`生成长字符串, 因为在 Python 中, `str` 是不可变类, 实际上是创建了新的字符串. 在要合并的子串已经准备好的情况下, `''.join(iterable_object)`超级快
- `inf`和`nan`是特殊的字符串, 被显式地转义为`float`, 大小写不敏感

