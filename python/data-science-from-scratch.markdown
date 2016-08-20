#数据科学入门

## Chapter2 python速成

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

## Chapter3 可视化数据

- 数据可视化的两种主要用途:
 1. 探索数据
 2. 交流数分
- `plot.scatter(x, y, ...)` - 绘制散点图, x, y的长度要一样
- `plot.axis("equal")` - 调整座标轴到合适区间
- `plot.annotate(s, xy, xytext=None, xycoords='data', textcoords='data', arrowprops=None, **kwargs)` - 为图上的数据点叫标记
- `plot.plot(*args, **kw)` - 绘制线图
- `plot.bar(left, height, width=0.8, bottom=None, hold=None, **kw)` - 绘制条形图
- `plot.xticks(*args, **kw)` - 为x轴添加标记
- `plot.subplot(column, row, active_area) - 使用子图, 3 个参数分别表示子图的总行数, 总列数, 已经当前子图是哪一个活跃区
- `plot.hist()` - 直方图
- `label` - 作为关键字参数, 为图形添加图例, 最后需要 `plot.legend()` 展示图例
- `plot.xlabel(str)` - 为 x 轴添加标签
- `plot.title(str)` - 添加标签

## Chapter4 线性代数

- 抽象地说,向量是指可以加总(以生成新的向量),可以乘以标量(即数字),也可以生成新的向量的对象。
- 具体来说, 向量是有限维空间的点. 将数值表示为向量是非常好的处理方式
- 最简单的入门方法是将向量表示为`数字的列表`。一个包含三个数字的列表对应一个三维空间的向量.
- 用列表表示向量有利于概念阐释, 但性能太差
- 矩阵是一个二维的数据集合, 按照数学表达惯例, 通常用大写字母表示矩阵
- 矩阵的重要性:
 1. 可以将每个向量看成矩阵的一行, 那么就可以用矩阵表示一个包含多维向量的数据集
 2. 可以用 n x k的矩阵表示一个线性函数, 这个函数将k维的向量映射到n维的向量上
 3. 可以用矩阵表示2维关系

## Chapter5 统计学

- 对于任何数据集, 最简单的描述方法就是数据本身
- 随着数据集中点数的增加,均值点会移动,但它始终取决于每个点的取值. 任意一个数值的变化, 都会引起均值的变化
- 和均值不同——中位数并不依赖于每一个数据的值. 数据集中最大的数变得更大, 也不影响中位数. 根据数据集中数据的个数不同, 中位数可能取最中间的数, 也可能是最中间的2个数的均值
- 均值对数据中的异常值敏感
- 中位数的一个泛化概念是`分位数(quantile)`,它表示少于数据中特定百分比的一个值。(中位数表示少于 50% 的数据的一个值。)
- 众数, 出现次数最多的数
- `离散度`是数据的离散程度的一种度量. 如果它所统计的值接近零,则表示数据聚集在一起,离散程度很小; 如果值很大(无论那意味着什么),则表示数据的离散度很大.
- `极差`, 最大元素与最小元素之差
- `方差`, 分母是`n-1`, 而不是n. 如果样本取自更大的总体, `x_bar` 就是真实均值的估值,意味着 `(x_i - x_bar) ** 2` 是 `x_i` 的方差对均值的低估值,所以除以 n-1 而不是 n
- `标准差`
- 极差和标准差也都有异常值问题, 一种替代的方案是计算75%的分位数和25%的分位数之差
- `协方差`是方差的一个对应词. 方差衡量了**单个变量**对均值的偏离程度,而协方差衡量了**两个变量**对均值的串联偏离程度.
- 如果向量 x 和向量 y 的对应元素同时大于它们自身序列的均值,或者同时小于它们自身序列的均值,那将为求和贡献一个正值。如果其中一个元素大于自身的均值,而另一个小于自身的均值,那将为求和贡献一个负值。因此,如果协方差是一个大的正数,就意味着如果 y 很大,那么 x 也很大,或者如果 y 很小,那么 x 也很小(同大或同小)。如果协方差为负而且绝对值很大,就意味着 x 和y 一个很大,而另一个很小。接近零的协方差意味着以上关系都不存在
- `相关`, 由协方差除以两个变量的标准差. 相关系数没有单位,它的取值在-1(完全反相关)和1(完全相关)之间。相关值 0.25 代表一个相对较弱的正相关。
- 相关系数的计算对异常值非常敏感
- `辛普森悖论`是指分析数据时可能会发生的意外。具体而言,如果忽略了混杂变量,相关系数具有误导性, 因为相关系数是假设在其他条件都相同的前提之下衡量两个变量的关系。
- 避免相关系数带来的误导性, 需要充分了解数据,并且尽可能核查所有可能的混杂因素
- 相关系数为零表示两个变量之间不存在线性关系。但它们之间还可能会存在其他形式的关系; 此外,相关系数无法表示关系有多强
- 相关 vs 因果
 - 这是个重要的论断——如果 x 和 y 强相关,那么意味着可能 x 引起了 y ,或 y 引起了 x ,或者两者相互引起了对方,或者存在第三方因素同时引起了 x 和 y ,或者什么都不是
- 进行随机试验是证实因果关系的可靠性的一个好方法。可以先将一组具有类似的统计数据的用户随机分为两组,再对其中一组施加稍微不同的影响因素,然后会发现,不同的因素会导致不同的结果。

## Chapter6 概率

- 将`概率论`视为对从事件空间中抽取的事件的不确定性进行量化的一种方式
- 如果E发生意味着F发生(或者F发生意味着E发生),就称事件E与事件F为不相互独立(dependent)。反之,E与F就相互独立(independent)。
- 从数学角度讲,事件E和事件F独立意味着两个事件同时发生的概率等于它们分别发生的概率的乘积
- `条件概率`可以理解为,已知F发生,E会发生的概率: `P(E, F)=P(E|F)P(F)`

## Chapter25 数据科学前瞻

- 要想成为一名优秀的科学家, 需要知道更多关于这些领域的知识, 而我鼓励你对每一个领域开展深入的学习
- NumPy 提供了比 list `向量`性能更好的数组, 提供了比 list of list `矩阵`性能更好的矩阵, 以及大量利用它们来工作的`数值函数`
- pandas 提供了处理 Python 数据集的更多的数据结构, 主要抽象概念是 DataFrame
- scikit-learn 处理机器学习问题的库, 决策树
- 数据可视化, 首选 matplotlib, 另外可试试 seaborn, 若想创建可以在网络上分享的`交互式可视化`, 首选 `D3.js` (Data Driven Documents), Bokeh 是一个把 D3 风格的功能整合到 Python 中的项目
- R 语言
- 数据科学的一部分, 可能包括`数据获取`, 一些好的站点:
 - Data.gov: 政府开放数据的门户网站
 - reddit 上有 r/datasets 和 r/data 两个论坛, 是一个可以请求数据和发现数据的地方
 - Amazon.com 的公用数据集: aws.amazon.com/cn/public-data-sets/
 - Robb Seaton 的博客上的专业数据集的列表: rs.io/100-interesting-data-sets-for-statistics
 - Kaggle (www.kaggle.com) 是一个举办数据科学竞赛的网站
