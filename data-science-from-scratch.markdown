#数据科学入门

##Chapter2 python速成

- 数据科学家是能够从混乱数据中剥离出洞见的人
- python用`backslash`(`\`)表示特殊字符, 希望用反斜杆表示反斜杆本身, 转义或用`raw string`
- `in` 操作符 用于判断是否成员
- 希望忽略某些值时, 将其附给`_`:

```python
_, y = [1, 2]

four_with_replacement = [random.choice(range(10)) for _ in range(4)]
```

- 常用字典作为代表结构数据的简单方式
- `defaultdict`相当于一个标准字典, 当查找一个不包含在内的键时, 它会创建该键, 并用给定的函数(值生成函数)为其赋值:

```python
from collections import defaultdict

word_counts = defaultdict(int)  # int()生成0

for word in document:
    word_counts[word] += 1  # 当查找的word不存在, 创建了一个新的键, 对应的值由int()生成, 再 + 1
```

```python
dd_list = defaultdict(list)          # list(生成一个空列表
dd_list[2].append(1)                 # 现在dd_list包含{2:[1]}

dd_dict = defaultdict(dict)          # dict(产生一个新字典
dd_dict["Joel"]["City"] = "Seattle"  # { "Joel" : { "City" : Seattle"}}

dd_pair = defaultdict(lambda: [0, 0])
dd_pair[2][1] = 1                    # 现在dd_pair包含{2: [0,1]}. 分开看2是dict的key, dd_pair[2]返回对应的值, 即[0, 0]
```

- 当用字典“收集”某些键对应的结果, 并且不希望每次查找某键是否存在都遍历一遍的时候, defaultdict 非常有用。
- `Counter` 将`sequence`的值转为键到计数的对象映射. 非常方便地用于统计:

```python
from collections import Counter
c = Counter([0, 1, 2, 0])  # c是(基本的) { 0 : 2, 1 : 1, 2 : 1 }
```

- `list`的`in`操作符, 将遍历整个列表, 而`set`的`in`操作能非常快速地进行检查(原理还没了解).
- 如"Think python"中所说, 嵌套条件阅读不太方便, 应避免. 逻辑运算符(and, or, not)是一个简化嵌套条件语句的方法. 对于非嵌套条件同样适用:

```python
s = some_function_that_returns_a_string()
if s:
    first_char = s[0]
else:
    first_char = ""

# 更好的写法应该是
first_char = s and s[0]
```

- 第一个值为“真”时, `and` 运算符返回它的第二个值,否则返回第一个值
- `sort`与`sorted`的区别在于, `sort`直接对`list`进行排序, `sorted`对list的一个副本进行排序, 而并不改变原list

```python
In [7]: x = [4, 2, 3, 1]

In [8]: sorted(x)
Out[8]: [1, 2, 3, 4]

In [9]: x
Out[9]: [4, 2, 3, 1]

In [10]: x.sort()

In [11]: x
Out[11]: [1, 2, 3, 4]
```

- 排序可指定`key`关键字参数指定排序的键, `reverse`关键字参数指定是否反转(默认从小到大排序):

```python
# 通过绝对值对列表元素从最大到最小排序
x = sorted([-4,1,-2,3], key=abs, reverse=True) # 是[-4,3,-2,1]

# 从最高数到最低数排序单词和计数
wc = sorted(word_counts.items(),
            key=lambda (word, count): count,  # 以统计次数作为排序的键
            reverse=True)
```

- `[]` - 列表生成式, `{}` - 字典或集合生成式, `()` - 生成器表达式
- `random` 模块实际上生成的是基于一种内部状态的确定性的伪随机数。如果想得到可复生的结果,可以用 `random.seed` 生成随机数种子:

```python
random.seed(10)        # 设置随机数种子为10
print random.random()  # 0.57140259469
random.seed(10)        # 重设随机数种子为10
print random.random()  # 再次得到0.57140259469))
```

- `random.random` 随机生成0~1的小数, `random.randrange` 在范围内随机选择一个数
- `random.shuffle` 随机重排列表中的元素, `random.choice` 从一个非空序列中随机选取一个元素
- `random.sample(population, k)` 从序列或集合中随机抽取k个不重复的元素, 返回一个list
- 高阶函数`partial`, 固定函数的一部分参数, 得到一个新的函数:

```python
In [32]: int("10", base=2)
Out[32]: 2

In [35]: from functools import partial

In [36]: int2 = partial(int, base=2)
In [37]: int2("10")
Out[37]: 2
```

- `map`, `filter`, `reduce`, `zip`, `enumerate`
- 函数调用时在参数前加`*`, 分解序列
- `*args`, `**kw` 黑魔法

##Chapter3 可视化数据

- 数据可视化的两种主要用途:
 1. 探索数据
 2. 交流数分
- `plot.scatter(x, y, ...)` - 绘制散点图, x, y的长度要一样
- `plot.axis("equal")` - 调整座标轴到合适区间
- `plot.annotate(s, xy, xytext=None, xycoords='data', textcoords='data', arrowprops=None, **kwargs)` - 为图上的数据点叫标记
- `plot.plot(*args, **kw)` - 绘制线图
- `plot.bar(left, height, width=0.8, bottom=None, hold=None, **kw)` - 绘制条形图
- `plot.xticks(*args, **kw)` - 为x轴添加标记

##Chapter4 线性代数

- 抽象地说,向量是指可以加总(以生成新的向量),可以乘以标量(即数字),也可以生成新的向量的对象。
- 具体来说, 向量是有限维空间的点. 将数值表示为向量是非常好的处理方式
- 最简单的入门方法是将向量表示为`数字的列表`。一个包含三个数字的列表对应一个三维空间的向量.
- 用列表表示向量有利于概念阐释, 但性能太差
- 矩阵是一个二维的数据集合, 按照数学表达惯例, 通常用大写字母表示矩阵
- 矩阵的重要性:
 1. 可以将每个向量看成矩阵的一行, 那么就可以用矩阵表示一个包含多维向量的数据集
 2. 可以用 n x k的矩阵表示一个线性函数, 这个函数将k维的向量映射到n维的向量上
 3. 可以用矩阵表示2维关系
