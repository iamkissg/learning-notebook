# [笔记] 利用 Python 进行数据分析

## 第 1 章: 准备工作

- 书中出现的"数据", 主要指"结构化数据" (structured data), 指代了所有的通用格式, 如:
 - 多维数组 (矩阵)
 - 表格型数据, 其中各列可能是不同类型 (str, int, date). 比如保存在关系型数据库中或以制表符/逗号为分隔的文本文件中的数据
 - 通过关键列相互联系的表 (对 SQL 而言, 就是主键和外键)
 - 间隔平均或不平均的时间序列
- **大部分数据集都能被转化为更加适合分析和建模的结构化形式, 虽然有时并不能很明显地看出. 如果不行的话, 也可能将数据集的特征提取为某种结构化形式**
- "我个人并不喜欢'脚本语言'这个术语, 因为它好像在说这些语言无法用于构建严谨的软件" (我也是)
- 大多数软件都是由两部分代码组成的: 少量需要占用大部分执行时间的代码, 大量不经常执行的"粘合代码" (Cython: cython.org)
- Python 不适合的场景: 1) 要求延迟非常小的程序 2) 高并发, 多线程的程序
- Python 有一个 GIL (Global Interpreter Lock, 全局解释器锁), 防止解释器同时执行多条 Python 字节码指令.
- 重要 Python 库简介:
 - NumPy - 科学计算的基础包, 提供了以下功能 (但不限于此). NumPy 除了提供快速的`数组处理能力`外, 另一个主要作用是: 作为`算法间传递数据的容器`. 对于数值型数据, NumPy 数组在存储和处理数据时要比内置的 Python 数据结构高效得多. 此外, `由低级语言 (C, Fortran 等) 编写的库可以直接操作 NumPy 数组中的数据, 无需进行任何数据复制`
  - 快速高效的多维数组对象 ndarray
  - 用于对数组执行元素级计算以及直接对数组执行数学运算的函数
  - 用于读写硬盘上基于数组的数据集的工具
  - 线性代数运算, 傅立叶变换, 以及随机数生成
  - 用于将 C, C++, Fortran 代码集成到 Python 的工具
 - pandas - 提供了能够快速便捷地处理结构化数据的大量数据结构和函数. 用得最多的可能是 `pandas.DataFrame`, 它是面向列 (column-oriented) 的二维表结构, 且含有行标签和列标签. pandas 兼具 NumPy 高性能的`数组计算功能`以及`电子表格和关系型数据库灵活的数据处理功能`. 它提供了复杂精细的`索引功能`, 以便更为快捷地完成`重塑 (reshape)`, `切片和切块`, `聚合`以及`选取数据子集`等操作. 面对金融行业, pandas 提供了大量适用于金融数据的高性能`时间序列`功能和工具 (pandas 源自 panel data 以及 Python data analysis)
 - matplotlib - 数据可视化
 - IPython - 为交互式和探索式计算提供了一个强健而高效的环境, 是增强的 Python shell, 目的是提高编写, 测试, 调试 Python 代码的速度, 主要用于交互式数据处理和利用 matplotlib 对数据进行可视化处理.
 - SciPy - 一组专门解决科学计算中各种标准问题域的包的集合, 主要包括:
  - scipy.integrate: 数值积分例程和微分方程求解器
  - scipy.linalg - 扩展了 numpy.linalg 提供的线性代数例程和矩阵分解功能
  - scipy.optimize - 函数优化器 (最小化器) 以及根查找算法
  - scipy.signal - 信号处理工具
  - scipy.sparse - 稀疏矩阵和稀疏线性系统求解器
  - scipy.special - SPECFUN (实现了许多常用数学函数的 Fortran 库) 的包装器
  - scipy.stats - 标准连续和离散概率分布 (如密度函数, 采样器, 连续分布函数等), 各种统计检验方法,以及更好的描述统计法
  - scipy.weave - 利用内联 C++ 代码加速数组计算的工具
- 导入惯例
 - `import numpy as np`
 - `import pandas as pd`
 - `import matplotlib.pyplot as plt`
- 行话
 - `数据规整 (Munge/Munging/Wrangling)` - 将非结构化或散乱数据处理为结构化或整洁形式的过程
 - `伪码 (Pseudocode)`
 - `语法糖 (Syntactic sugar)` - 编程语法, 并不会带来新的特性, 但使代码更易读, 更易写

## 第二章 引言

- 基本任务
 - 与外界进行交互 - 读写各种各样的文件格式和数据库
 - 准备 - 对数据进行清理, 修整, 整合, 规范化, 重塑, 切片切块, 变形等处理以便进行分析
 - 转换 - 对数据集做一些数学和统计运算以产生新的数据集
 - 建模和计算 - 将数据跟统计模型, 机器学习算法或其他计算工具联系起来
 - 展示 - 创建交互式的或静态的图片或文字摘要
- 通过`短链接`伪造后缀, 导致用户访问恶意域名. (以后短链接也不可轻信啊)
- 计数的多种方法:
 1. 遍历, 将计数值保存在字典中. 也分复杂的和简洁的: 普通字典 vs. defaultdict (会自动创建不存在的键的字典)
 2. 使用 collections.Counter
 3. 使用 pandas
- 对 list of multi-elements tuple 进行排序, 会按元素在 tuple 中的顺序依次排序, 即先按 0 号元素排序, 若 0 号元素相同, 再按 1 号元素进行排序, 依次类推. 因此, 对于字典的一个处理技巧是, 用列表推导式生成 list of multi-elements tuple, 再对 list 进行排序, 如下:

```python
value_key_pairs = [(v, k) for k, v in some_dict.items()]
value_key_pairs.sort()
# return value_key_pairs[-len(some_dict):]  # 逆序
```

- 创建 `pd.DataFrame` obj, 将像样点的原数据集作为参数传入即可, 比如 `frame = DataFrame(records)`
- pandas.DataFrame 的导航, 可以先列标签 (通常为 str) 后行标签 (通常为 数组), 也可以先行后列 (自悟, 不知道会不会自误)\\
但是, 如果是没有转成 `pd.DataFrame` 的 list of dict, 就别想 `a[str][int]` 的奇怪方式了, 列表下标只能是 int, ok?
- `df[str]` 返回一个 `Series` 对象, 因此, 是可以对列标签进行索引的.
- `pd.Series.fillna()` - Fill NA/NaN with "Missing"
- `pd.Series[bool_expression]` - 布尔过滤
- `Series` 对象带 `value_counts` 方法, 可以方便统计
- `pd.Series.dropna()` - Return Series without null values
- `pd.Series.notnull()` - Return a boolean same-sized obj indicating iif the values are not null
- `where(condition, [x, y])` - Return elements, either from `x` or `y`, depending on `condition`
- `pd.Series.groupby(self, by=None, axis=0, level=None, as_index=True, sort=True, group_keys=True, squeeze=False` - Group series using mapper (dict or key function, apply given function to group, return result as series) or by a series of columns, 即按列分组或按映射器的结果进行分组
- , 即按列分组或按映射器的结果进行分组
- `pd.core.groupby.DataFrameGroupBy.size(self)` - Compute group sizes, return Series
- `pd.Series.unstack()` - Unstack, a.k.a. pivot, Series with MultiIndex to produce DataFrame. `Series -> DataFrame`
- `pd.DataFrame.sum(self, axis=None, skipna=None, level=None, numeric_only=None, **kwargs)` - Return the sum of the values for the requested axis
- `pd.DataFrame.plot` - 直接利用 matplotlib 绘图, `subplots` 为 True 时, 每列 (Series) 绘在一个子图上, `figsize` - 指定图片大小
- `pd.DataFrame.plot(kind="barh", stacked=True)` - 生成堆积条形图
- 对于堆积条形图, 较小的分组无法识别相对比例, 可将各行规范为"总计为1"
- `pd.read_table()` - 将文件读取到 pandas DataFrame 对像，唯一的位置参数是路径, `sep` 指定字段间分隔符, `header` 指定有无标题, `engine` 指定解析引擎, 可选为 `c` 或 `python`, 快速与灵活的选择, `names` 类数组对象, 用作 DataFrame 的列名
- 分析散布在多张表中的数据, 可将所有数据都合并到一张表中, 利用 pandas 的 `merge` 函数, pandas 会根据列名的重叠情况推断出哪些列是合并键. 一次只能合并 2 张表, 若要合并多张表, 和多次调用 merge 函数
- `pd.DataFrame.ix` - 属性, 基于标签位置的索引, 也返回某一行
- `pd.DataFrame.pivot_table()` - 创建电子表格形式的数据透视表(pivot table), `数据聚合`的方式之一, 唯一位置参数 `data` 用 `DataFrame` 对象指定数据, `index`, `columns` 指定索引与列 (默认是数字索引), `aggfunc` 默认是 `numpy.mean` 函数, 或者可以是 list of functions,\\
(数据透视表, 是一种交互式的表, 可进行某些计算. 之所以称为数据透视表, 因为可以动态地改变版面布置, 以便按照不同方式分析数据, 也可以重新安排行号, 列标等. 每次改变版面布置, 数据透视表会立即按照新的布置重新计算数据)
- `pd.Series.index` - 返回一个 Index obj
- `pd.DataFrame.sort_values` - sort by values, 唯一位置参数 `by` 可以是 str 或 list of names, 指定排序的的列, `ascending` 指定升降序的布尔值
- 要找出两列的分歧, 可用两列的差创建新的一列, 对新列进行排序, 就可知哪些是分分歧最大的,不过要注意可能需要使用绝对值
- `pd.Series.sort_values` - 无 `by` 关键字参数
- 计算分歧的标准姿势应该是计算或标准差
- `pd.Series.std()` - 返回标准差
- `pd.read_csv` - 读取 .csv 文件到 DataFrame. 实际上, 只要是标准的逗号分隔的内容, 文件类型不重要
- pandas 可以用点标记法, 取数据
- `pd.Series.sum()` - Return the sum of the values for the requested axis
- `pd.concat(objs, ...)` - 在某一维度, 联接 pandas 对象 (Concatenate pandas objects along a particular axis with optional set logic along the other axes). 默认按行组合, `ignore_index=True` 将忽略原始行号, 有时候有用.
- `pd.DataFrame.apply()` - Applies function along input axis of DataFrame.
- `pd.obj.astype(numpy.dtype)` - Cast object to input numpy.dtype
- 进行分组处理时, 一般都应该做一些有效性检查. 对于浮点性数据, 不能判断它是否等于某个值, 用 `np.allclose(a, b)` 来检查 a 是否近似于 c
- `np.allclose(a, b, rtol=1e-05, atol=1e-08, equal_nan=False)` - 当两个数组近似时, 返回 True
- `技巧`: 通过多少加起来才够总数的 50%, for 循环是一种方式. 但 NumPy 提供了一种更聪明的矢量方式: 先排序, 计算累计和 cumsum, 然后再通过 searchsortd 方法找出 0.5 应该被插在哪个位置才能保证不破坏原顺序
-找出 0.5 应该被插在哪个位置才能保证不破坏原顺序
- `pd.DataFrame.head(self, n=5)`, `pd.DataFrame.tail(self, n=5)` - 类 shell 的 head, tail 用法, 返回首尾 n 行
- `plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False, squeeze=True, subplot_│ving file at /Untitled.ipynb
kw=None, gridspec_kw=None, **fig_kw)` - 创建子图
- `pd.Series.map(self, arg, na_action=None)` - 使用 arg 为 Series 映射值
- `pd.Series.unique()` - 返回互异值的数组. Return array of unique values in the object. Significantly fast than numpy.unique. Includes NA values.
- `pd.Series.isin(self, values)` - Return a boolean :class:`~pandas.Series` showing whether each element in the :class:`~pandas.Series` is exactly contained in the passe
- `pd.DataFrame.div()` - Floating division of dataframe and other.

## 第 3 章: IPython: 一种交互式计算和开发环境

- 大部分的数据分析代码都含有探索式操作(试错法和迭代法)
- 跟所有由键盘驱动的控制台环境一样, 锻炼对常用命令的`肌肉记忆`是学习曲线中不可或缺的一部分
- IPython 的特点:
 - 更好的格式化, 更强的可读性
 - 强大的 Tab 自动补全
 - 内省
  - 在变量的前或后加 `?`, 可以显示对象的通用信息;
  - `??` 显示源代码
  - `?` 还可用于搜索 IPython 命名空间. 与通配符 `*` 搭配, 可显示所有与通配符表达式相匹配的名称
 - Magic Function
  - `%timeit`
  - `%reset` - 重置用户命名空间
  - `%automagic` - 打开或关闭自动 Magic Function (不加 %)
  - `%quickref` - 显示 IPython 的快速参考
  - `%magic` - 显示所有的 Magic Function 命令的详细文档
  - `%debug` - 从最新的异常跟踪的底部进入交互式调试器
  - `%hist` - 打印历史命令
  - `%pdb` - 打开或关闭, 在异常发生后自动进入调试器
  - `%page obj` - 通过分页器打印输出 obj
  - `%prun statement` - 通过 cProfile 执行 statement, 并打印分析器的输出结果
  - `%time statemnet` - 报告 statement 执行时间
  - `%timeit statement` - 多次执行 statement 以计算平均执行时间, 对执行时间非常小的代码很有用
  - `%who`, `%who_ls`, `%whos` - 显示交互式命名空间中定义的变量, 信息级别/冗余度可变
  - `%xdel variable` - 删除变量, 并尝试清除其在 IPython 中对象的一切引用
  - `%run` - 脚本将在一个空的 namespace 中运行, 之前的 import 对脚本的执行不影响. 此后, 文件中所定义的全部变量 (以及各种 import, 函数, 全局变量) 就可以在当前 IPython shell 中访问了.
   - 如果执行脚本需要命令行参数, 可将参数放在文件路径后, 就跟在命令行执行一样.
   - 如果希望脚本能访问交互 IPython 命名空间, 使用 `%run -i`, `i` 是 `interactive` 的缩写
   - 中断正在执行的代码, `Ctrl-c`.
 - 执行剪贴板中的代码
  - `%paste` - 可以承载剪贴板中的一切文本, 并在 shell 中以整体形式执行. 如果剪贴板中是 `%paste` 会一直递归, 然后爆炸
  - `%cpaste` - 会出现一个用于粘贴代码的命令提示符, 方便用户手动粘贴代码. 若代码有错, `Ctrl-c` 终止
 - 快捷键
 - 异常和跟踪
  - 回溯的上下文代码参考的数量可通过 `%xomde` 进行控制, 可以增多减少
 - 基于 Qt 的富 GUI 控制台
 - matplotlib 集成与 pylab 模式

## 第 4 章: NumPy 基础

- NumPy 的部分功能:
    - ndarray, 一个具有矢量算术运算和复杂广播能力的快速且节省空间的多维数组
    - 用于对整组数据进行快速运算的标准数学函数(无需编写循环)
    - 用于`读写磁盘数据`的工具以及用于`操作内存映射文件`的工具
    - 线性代数, 随机数生成以及傅里叶变换功能
    - 用于集成由 C, C++, Fortran 等语言编写的代码工具
- NumPy 提供了一个简单易用的 C API, 因此很容易将数据传递给由低级语言编写的外部库, 外部库也能以 NumPy 数组的形式将数据返回给 Python. 这个功能使 Python 成为一种包装 C/C++/Fortran 历史代码库的选择, 并使被包装库拥有一个动态的, 易用的接口
- NumPy 本身并没有提供多么高级的数据分析功能
- 大部分数据分析应用的主要功能可能是:
    - 用于数据整理和清理, 子集构造和过滤, 转换等快速的矢量化数组运算
    - 常用的数组算法, 如排序, 唯一化, 集合运算等
    - 高效的描述统计和数据聚合/摘要运算
    - 用于异构数据集合的合并/连接运算的数据对齐和关系型数据库运算
    - 数据的分组运算(聚合, 转换, 函数应用等)
- `from numpy import *` 是一个坏习惯.
- ndarray(N 维数组) 是 NumPy 最重要的特点之一, 该对象是一个快速而灵活的大数据集容器, 可以利用这种数组对`整块数据`进行数学运算
- ndarray 是一个通用的`同构数据多维容器`, 其中所有的元素必须是相同类型的. 每个数组对象都有一个 `shape` (表示各维度大小的元组), 一个 `dtype` (说明数组数据类型的对象)
- 创建数组最简单的办法——使用 array 函数, 它接收一切序列型的对象(包括其他数组), 然后产生一个新的含有传入数据的 NumPy 数组
- 嵌套序列会被转换为一个多维数组
- 除非显式说明, `np.array` 会尝试为新建的数组`推断`出一个较为合适的数据类型
- `zeros`, `ones`, `empty` 等可以用于方便地创建特定的数组: 指定长度或形状的全 0 或全 1 数组, 没有任何具体值的数组. `只需传入一个表示形状的整数或元组即可.
- `np.empty` 返回的不是全 0 的数组, 而是一些未初始化的值
- `arange` 是 Python 内置函数 range 的`数组版`:

```python
In [2]: a = np.arange(9)

In [3]: a
Out[3]: array([0, 1, 2, 3, 4, 5, 6, 7, 8]
```

- NumPy 关注的是`数值计算`, 如果没有特别说明, 数据类型基本都是 float64
- 数组创建函数有这些:
    - array
    - asarray
    - arange
    - ones, ones_like
    - zeros, zeros_like
    - empty, empty_like
    - eye, identity - 创建一个 N * N 的`单位矩阵`

#### ndarray 数据类型

- `dtype` 是一个特殊的对象, 含有 ndarray 将一块内存解释为特定数据类型的所需信息.
- `dtype` 是 NumPy 强大灵活的原因之一. 多数情况下, 它们`直接映射到相应的机器表示`, 这使得"读写磁盘上的二进制数据流"以及"集成低级语言代码"等工作变得更加简单
- 数值型的 dtype 的命名方式是: 类型名 + 表示各元素位长的数字
- 标准的双精度浮点值 (Python 的 float 对象) 需要占用 8 字节 (64 bit), 因此记作 float64
- 通常只需要知道所处理的数据的大致类型是浮点数, 整数, 复数, 布尔值, 字符串, 还是普通的 Python 对象即可. 当需要`控制数据在内存和磁盘中的存储方式时(尤其对于大数据集), 就需要了解如何控制存储类型`
- NumPy 的数据类型:
    - int8(i1), uint8(u1), int16(i2), uint16(u2), int32(i4), uint32(u4), int64(i8), uint64(u8)
    - float16(f2) - 半精度浮点数
    - float32(f4 或 f) - 标准的单精度浮点值, 与 C 的 float 兼容
    - float64(f8 或 d) - 标准的双精度浮点值, 与 C 的 double , Python 的 float 兼容
    - float128(f17 或 g) - 扩展精度浮点数
    - complex64(c8), complex128(c16), complex256(c32) - 用 32 bit, 64 bit, 128 bit 浮点数表示的复数
    - bool(?)
    - object(O) - Python 对象类型
    - string_(S) - 固定长度的字符串类型(每个字符 1 个字节). 要创建一个长度为 10 的字符串, 应使用 S10
    - unicode_(O) - 固定长度的 unicode 类型(字节数由平台决定). U10
- 通过 `nparray` 的 `astype` 方法显式地转换 `dtype`, `float_arr = arr.astype(np.float64)`
- NumPy 会自动将 Python 类型映射到等价的 dtype 上: `numeric_strings.astype(float)`
- 转换失败, 抛出 TypeError 异常
- 可以用上述括号中的缩写表示类型
- 调用 `astype` 无论如何都会创建一个新的数组(原始数据的一份拷贝), 即使新 dtype 与旧 dtype 相同
- 浮点数只能表示近似的分数值. 在复杂计算中, 可能会积累浮点错误, 因此`比较操作` 只能在一定小数位以内有效
- `数组的矢量化`: 不用编写循环即可对数据执行批量运算
- 大小相等的数组之间的任何算术运算都会将运算应用到元素级
- 数组与标量的算术运算会将标量值传播到各元素
- 不同大小的数组之间的运算叫做广播(broadcasting)

#### 基本的索引与切片

- 当将一个标量值赋值给一个切片时(如 a[5:8]=12), 该值会自动传播到整个选区.
- 与列表最重要的区别在于, 数组切片是原始数组的`视图`, 这意味着数据不会被复制, 视图上的任何修改都会直接反映到原数组上. NumPy 的设计目的就是处理大数据, 而数据的复制会产生性能和内存问题
- 要得到 ndarray 切片的一份副本而非视图, 需要显式地进行复制操作, 例如 `arr[5:8].copy`
- 高维数组, 各索引位置上的元素不再是标量, 而是数组对象. 可使用以下等价的方式对各个元素进行递归地访问:
    - arr[x][y] (二维数组)
    - arr[x, y] (二维数组)
- 高维度的对象, 可以在一个或多个轴上进行切片, 也可以`跟整数索引混合使用`. 切片是`沿着一个轴向`选取元素的. 可以一次传入多个切片, 就像传入多个索引一样
- 对切片表达式的赋值操作将扩散到整个选区

#### 布尔索引

- `np.random.randn(x, y, ...)` - 生成 n 维的随机数
- 与算术运算一样, 数组的比较运算(如==)也是矢量化的
- 通过数组的比较运算, 可以得到一个`布尔型数组`, 其可以用于数组索引. 但是布尔型数组的长度必须跟被索引的轴长度一致.
- 可以将布尔型数组与切片, 整数(或整数序列)混合使用
- 利用布尔型数组进行筛选, 要排除某值, 可以使用 `!=`, 也可以用负号 `-` 对条件进行否定
- 组合条件, 使用 `&`, `|` 之类的布尔算术运算符. Python 关键字 `and` 和 `or` 在布尔型数组中无效 (所以 pandas 继承了这一点咯)
- 通过布尔型索引选取数组中的数据, 将总是创建数据的副本 (不是视图咯)
- 通过布尔型数组设置值是一个常用的手段, 比如: `data[data < 0] = 0`
- `花式索引1`: 以特定顺序选取子集, 只需传入一个用于指定顺序的 list of int 或 ndarray (负数索引从末尾开始选取行)
- `花式索引2`: 一次传入多个索引数组, 返回的是一个一维数组, 其中的元素对应各个索引元组:

```python
In [35]: arr = np.arange(32).reshape((8, 4))

In [36]: arr
Out[36]:
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11],
       [12, 13, 14, 15],
       [16, 17, 18, 19],
       [20, 21, 22, 23],
       [24, 25, 26, 27],
       [28, 29, 30, 31]])

In [37]: arr[[1, 5, 7, 2], [0, 3, 1, 2]]
Out[37]: array([ 4, 23, 29, 10])
# 依次选出的元素是(1. 0), (5, 3), (7, 1), (2, 2)
```

- 若要选取矩形区域矩阵行列子集, 可以用下述方法:

```python
n [38]: arr[[1, 5, 7, 2]]
Out[38]:
array([[ 4,  5,  6,  7],
       [20, 21, 22, 23],
       [28, 29, 30, 31],
       [ 8,  9, 10, 11]])

In [39]: arr[[1, 5, 7, 2]][:, [0, 3, 1, 2]]
Out[39]:
array([[ 4,  7,  5,  6],
       [20, 23, 21, 22],
       [28, 31, 29, 30],
       [ 8, 11,  9, 10]])
# 利用了多次整型序列
```

- `花式索引3`: `np.ix_` 函数, 它可以将 N 个一维序列转换成用于选取矩形区域的索引器:

```python
In [41]: arr[np.ix_([1, 5, 7, 2], [0, 3, 1, 2])]
Out[41]:
array([[ 4,  7,  5,  6],
       [20, 23, 21, 22],
       [28, 31, 29, 30],
       [ 8, 11,  9, 10]])
```

- 花式索引与切片不一样, 它总是将数据`复制`到新数组中

#### 数组转置与轴对换

- 转置(tanspose) 是重塑的一种特殊形式, 它返回的是源数据的视图(不进行任何复制操作).
- 数组的 `T` 属性, 返回转置后的数组. 利用 `np.dot` 计算矩阵内积: `np.dot(arr.T, arr)`
- 对于高维数组, transpose 需要得到一个由轴编号组成的元组才能对这些轴进行转置(烧脑):

```python
n [44]: arr = np.arange(16).reshape((2, 2, 4))

In [45]: arr
Out[45]:
array([[[ 0,  1,  2,  3],
        [ 4,  5,  6,  7]],

       [[ 8,  9, 10, 11],
        [12, 13, 14, 15]]])

n [48]: arr.transpose((1, 0, 2))
Out[48]:
array([[[ 0,  1,  2,  3],
        [ 8,  9, 10, 11]],

       [[ 4,  5,  6,  7],
        [12, 13, 14, 15]]])
# 真看不懂这怎么转置的
```

- ndarray 的 swapaxes 方法, 接收一对轴编号, 返回交换轴后的数组. 返回源数据的视图(不进行任何复制操作)

#### 通用函数: 快速的元素级数组函数

- 通用函数 (ufunc) 是一种对 ndarray 中的数据执行`元素级运算`的函数, 可以看作简单函数 (接受一个或多个标量值, 并产生一个或多个标量值) 的矢量化包装器
- 许多 ufunc 都是元素级变体, 如sqrt, exp:

```python
In [60]: arr = np.arange(10)

In [61]: np.sqrt(arr)
Out[61]:
array([ 0.        ,  1.        ,  1.41421356,  1.73205081,  2.        ,
        2.23606798,  2.44948974,  2.64575131,  2.82842712,  3.        ])

In [62]: np.exp(arr)
Out[62]:
array([  1.00000000e+00,   2.71828183e+00,   7.38905610e+00,
         2.00855369e+01,   5.45981500e+01,   1.48413159e+02,
         4.03428793e+02,   1.09663316e+03,   2.98095799e+03,
         8.10308393e+03])
```

- 以上的 ufunc 是一元的(unary), 另外一些接收 2 个数组, 并返回一个结果数组的 ufunc 成为二元的(binary)

```python
In [65]: x = np.random.randn(8)

In [66]: y= np.random.randn(8)

In [67]: x
Out[67]:
array([-1.10012547,  1.30853808,  0.16414726, -0.09124062, -1.374608  ,
        2.1615976 , -0.2517318 ,  0.85188825])

In [68]: y
Out[68]:
array([ 0.69178282,  0.48768847, -1.1929698 , -0.95714824, -0.51259325,
        2.40694035,  0.07017021, -0.50771628])

In [69]: np.maximum(x, y)
Out[69]:
array([ 0.69178282,  1.30853808,  0.16414726, -0.09124062, -0.51259325,
        2.40694035,  0.07017021,  0.85188825])
```

- 还有一些 ufunc 可以返回多个数组, 如 modf, 它是 Python 内置函数 divmod 的矢量化版本, 用于浮点数数组的小数和整数部分:

```python
In [70]: arr = np.random.randn(7) * 5

In [71]: arr
Out[71]:
array([ 0.10439394,  2.99345139,  0.98980447,  1.39684718,  2.23020722,
       -0.15610334,  7.45786678])

In [72]: np.modf(arr)
Out[72]:
(array([ 0.10439394,  0.99345139,  0.98980447,  0.39684718,  0.23020722,
        -0.15610334,  0.45786678]), array([ 0.,  2.,  0.,  1.,  2., -0.,  7.]))
```

#### 利用数组进行数据处理

- NumPy 数组可以将多种数据处理任务表述为简洁的`数组表达式`. 用数组表达式代替循环的做法, 通常称为`矢量化`. 一般来说, 矢量化数组运算要比等价的纯 Python 方式快一两个数量级(甚至更多), 尤其是各种数值计算
- `np.meshgrid` - 接受两个一维数组, 并产生两个二维矩阵(对应于两个数组中的所有 (x, y) 对)

```python
In [75]: points = np.arange(-5, 5, 0.01)
In [77]: xs, ys = np.meshgrid(points, points)
In [82]: z = np.sqrt(xs ** 2, ys ** 2)
In [86]: plt.imshow(z, cmap=plt.cm.gray); plt.colorbar(); plt.title("Image plot if $\sqrt{x^2 + y^2}$ for a grid of values")
Out[86]: <matplotlib.text.Text at 0x7f5f70c9dcc0>
```

###### 将条件逻辑表述为数组运算

- `numpy.where` 函数是三元表达式 x if condition else y 的矢量化版本, `np.where(condition, x, y)`, 第二和第三个参数不必是数组, 它们都可以是标量值. 若一个是标量, 一个是数组, 会传播; 若两个都是数组, 数组大小可不相同
- 在数据分析工作中, where 通常用于根据另一个数组而产生一个新的数组
- 嵌套的 where 表达式:

```python
np.where(cond1 & cond2, 0,
           np.where(cond1, 1,
                      np.where(cond2, 2, 3)))
```

- 上述的例子, 利用了`布尔值在计算过程中可以被当作 0 或 1 处理`, 因此上述语句可以写成:

```python
result = 1 * (cond1 -cond2) + 2 * (cond2 & -cond1) + 3 * -(cond1 | cond2)
```

###### 数学与统计方法

- 通过数组上的一组数学函数对整个数组或某个轴向的数据进行统计计算.
- 聚合计算(aggregation, 通常叫做约简(reduction)), 即可以当作数组的实例方法调用, 也可以当作顶级的 NumPy 函数使用
- `mean`, `sum` 等方法可以接受一个 `axis` 参数 (用于计算该轴向上的统计值), 结果是一个少一维的数组
- `cumsum`, `cumprod` 之类的方法则不聚合, 而是产生一个`由中间结果组成的数组`
- 基本数组统计方法:
    - sum - 对数组中全部或某轴向的元素求和. 零长度的数组的 sum 为 0
    - mean - 算术平均数. 零长度的数组的 mean 为 NaN
    - std, var - 标准差, 方差, 自由度可调 (默认为 n)
    - min, max - 最小和最大值
    - argmin, argmax - 分别为最小和最大元素的索引
    - cumsum - 所有元素的累计和
    - cumprod - 所有元素的累计积
- 上述方法中, 布尔值会被强制转换为 1 和 0, 因此 `sum` 经常被用来对布尔型数组中的 True 值进行统计

###### 用于布尔型数组的方法

- `any` 方法, 类似于 Python 内置的 any 方法, 用于测试数组中是否存在一个或多个 True 值
- `all` 方法, 检查数组中所有值是否都是 True
- `any` 和 `all` 还能用于非布尔型数组, 所有非 0 元素都会被当作 True

###### 排序

- 与 Python 内置的列表类型一样, NumPy 数组也可以通过 `sort` 方法排序
- 多维数组可以在任何一个轴上进行排序, 只需要传入一个轴编号
- 顶级方法 `np.sort` 与 Python 的 `sorted` 类似, 返回一个已排序的副本, 但不对数组本身进行修改
- 计算数组分位数最简单的方法是对其进行排序, 然后选取特定位置的值

###### 唯一化以及其他的集合逻辑

- `np.unique` - 找出数组中的唯一值并返回已排序的结果. 与 `np.unique` 等价的纯 Python 代码是 `sorted(set(names))`
- `np.in1d` 用于测试一个数组中的值在另一个数组中的成员资格, 返回一个布尔型数组:

```python
In [2]: values = np.array([6, 0, 3, 2, 5, 6])

In [3]: np.in1d(values, [2, 3 ,6])
Out[3]: array([ True, False,  True,  True, False,  True], dtype=bool)
```

- 其他方法:
    - intersect1d(x, y) - 计算公共元素, 并返回有序结果
    - union1d(x, y) - 计算并集, 并返回有序结果
    - setdiff1d(x, y) - 集合的差, 即元素在 x, 不在 y 中
    - setxor1d(x, y) - 集合的对称差, 存在于一个数组但不同时存在于两个数组中的元素

#### 用于数组的文件输入输出

###### 将数组以二进制格式保存到磁盘

- `np.save` 和 `np.load` 是读写磁盘数组的两个主要函数. 默认情况下, 数组是以未压缩的`原始二进制格式`保存在 `.npy` 文件中的. 保存时, 若没有指定扩展名 `.npy`, 会自动加上.
- `np.savez` 可以将多个数组保存到一个压缩文件 `.npz` 中. 加载 `.npz` 会得到一个类似字典的对象, 它会对各个数组进行延迟加载

###### 存取文本文件

- 从文本文件加载数据的函数, pandas 有 `read_csv` 和 `read_table` 等, numpy 有 `np.genfromtxt` 和 `np.loadtxt` 等. 这些函数都有许多选项可供使用: 指定各种分隔符, 针对特定列的转换器函数, 需要跳过的行等
- `np.loadtxt("array_ex.txt", delimiter=",")` - 加载文件, 分隔符为逗号. `np.savetxt` 执行相反的操作: 将数组写到以某种分隔符隔开的文本中
- `genfromtxt` 与 `loadtxt` 差不多, 但它面向的是结构化数组和缺失数据处理

#### 线性代数

- 线性代数 (矩阵乘法, 矩阵分解, 行列式以及其他方阵数学等) 是任何数组库的重要组成部分
- NumPy 提供了一个用于矩阵乘法的 `dot` 函数 (既是一个数组方法, 也是 numpy 命名空间的一个函数)
- `numpy.linalg` 模块提供了


## 第 5 章: pandas 入门

- 引入约定:

```python
from pandas import Series, DataFrame
import pandas as pd
```

- 作者因为以下需求开发了 pandas:
    - 具备按轴自动或显式数据对齐功能的数据结构. 这可以防止许多由数据未对齐以及来自不同数据源(索引方式不同)的数据而导致的常见错误.
    - 集成时间序列功能
    - 既能处理时间序列数据也能处理非时间序列数据的数据结构
    - 数学运算和约简(比如对某个轴求和)可以根据不同的元数据(轴编号)进行
    - 灵活处理缺失数据
    - 合并及其他出现在常见数据库中的关系运算

#### Series

- Series 是一种类似于一维数组的对象, 由一组数据以及一组与之相关的数据标签(即索引)组成.
- Series 的字符串表现形式为: 索引在左, 值在右
- `Series.values` - Return Series as ndarray or ndarray-like, depending on the type
- `Series.index` - Immutable (不可变的) ndarray implementing an ordered, sliceable set.
- 通过 `Series()` 方法的 `index` 关键字参数可以指定标记索引
- 与普通股 NumPy 数组相比, 可通过索引的方式选取 Series 中的单个或一组值, 如 `obj['a']`, `obj[['a', 'b', 'c']]
- NumPy 数组运算都会保留索引与值之间的链接
- 可以将 Series 看成一个`定长`的`有序字典`, 索引值到数据值的一个映射. 它可以用在许多原本需要字典参数的函数中. `in` 操作对于 dict 默认是搜索 key, 对 Series 对象是 搜索索引
- 可以用 dict 创建 Series, 会自动将 key 转为 index, value 转为 value. 此时若还指定了 `index` 关键字参数, 则与索引相匹配的值会被找出来放在相应位置, 没有找到相应索引的值被置为 `NaN`. (有点布尔过滤的味道)
- `pd.isnull` 和 `pd.notnull` 函数用于检测缺失数据, 另有 `Series.isnull`, `Series.notnull`
- Series 最重要的一个功能: `在算术运算中自动对齐不同索引的数据`

```python
In [10]: sdata = {"Ohio": 35000, "Texas": 71000, "Oregon": 16000, "Utah": 5000}
In [11]: obj3 = Series(sdata)
In [12]: states = ["Califonia", "Ohio", "Oregon", "Texas"]
In [13]: obj4 = Series(sdata, index=states)
In [14]: obj3
Ohio      35000
Oregon    16000
Texas     71000
Utah       5000
dtype: int64
In [15]: obj4
Califonia      NaN
Ohio         35000
Oregon       16000
Texas        71000
dtype: float64
In [16]: obj3 + obj4
Califonia       NaN
Ohio          70000
Oregon        32000
Texas        142000
Utah            NaN
dtype: float64
```

- Series 对象本身及其索引都有一个 `name` 属性, 该属性跟 pandas 其他的关键功能关系非常密切, 可进行设置, 如 `obj.name = 'population'`
- Series 的索引可以通过赋值的的方式修改: `obj.index = ["x"]`


#### DataFrame

- DataFrame 是一个表格型的数据结构, 含有一组有序的列, 每个列可以是不同的值类型. DataFrame 既有行索引也有列索引, 可看作 Series 组成的字典 (共用同一个索引)
- DataFrame 中面向行和面向列的操作基本上是平衡的.
- DataFrame 中的数据是以一个或多个二维块存放的 (而不是列表, 字典或其他一维数据结构). 尽管如此, 其还是能够表示更为高维度的数据(`层次化索引的表格数据结构, 这是 pandas 许多高级数据处理功能的关键要素`)
- 最常用的构建 DataFrame 的方法是: 直接传入一个由等长列表或 NumPy 数组组成的字典.
- DataFrame 会自动加上索引, 且全部列都被有序排列. 如果用 `columns` 关键字参数指定了列序列, DataFrame 的列会按指定顺序进行排列. 传入的列在数据中找不到, 也会产生 NA 值
- 同样, `DataFrame()` 方法的 `index` 关键字参数用于构建索引.
- 通过类似字典标记的方式或属性的方式, 可将 DataFrame 的列获取为一个Seires, 返回的 Series 拥有与原 DataFrame 相同的索引, 且其 `name` 属性已经被相应地设置好了, 就是列名
- 行也可以通**位置**或**名称**的方式获取, 比如使用索引字段 `ix`
- 列可以通过赋值的方式进行修改, 可以为列赋一个标量值(统一的)或一组值. 为不存在的列赋值会创建一个新列.
- 关键字 `del` 用于删除列, `del frame["year"]`
- 将列表或数组赋给某个列, 其长度`必须`跟 DataFrame 的长度相匹配. 如果赋的是一个 Series, 会精确匹配 DaraFrame 的索引, 所有的空位都会被填上缺失值:

```python
In [4]: data = {"state" : ["Ohio", "Ohio", "Ohio", "Neveda", "Neveda"],
                "year": [2000, 2001, 2002, 2001, 2002],
                "pop": [1.5, 1.7, 3.6, 2.4, 2.9]}
In [8]: frame = DataFrame(data)
In [9]: frame
Out[9]:
      pop   state  year
   0  1.5    Ohio  2000
   1  1.7    Ohio  2001
   2  3.6    Ohio  2002
   3  2.4  Neveda  2001
   4  2.9  Neveda  2002
In [10]: val = Series([-1.2, -1.5, -1.7], index=[2, 4, 5])
In [13]: frame['debt'] = val
In [14]: frame
Out[14]:
      pop   state  year  debt
   0  1.5    Ohio  2000   NaN
   1  1.7    Ohio  2001  -1.2
   2  3.6    Ohio  2002  -1.5
   3  2.4  Neveda  2001   NaN
   4  2.9  Neveda  2002  -1.7
```

- 通过索引的方式返回的列只是相应数据的视图, 不是副本. 因此对返回的 Series 所做的任何修改全都会反映到原 DataFrame 上. 通过 `Series.copy()` 方法可显式地复制列. (?, 现在似乎改了)
- 另一种常见的创建 DataFrame 的形式是, 使用嵌套的字典(dict of dict). 将它传给 DataFrame, 它会被解释为: 外层字典的键作为列, 内层键则作为行索引. 内层键会被合并, 排序以形成最终的索引. 如果显式地指定了索引, 则不会, 空位依旧用 NA 值补
- 由 Series 组成的字典, 创建 DataFrame, 与嵌套字典类似
- `DataFrame.T` - 返回转置的结果, 不会对对象本身造成修改
- 可以传给 DataFrame 构造器的数据:
    - 二维 ndarray
    - dict of (array | list | tuple)
    - NumPy 的结构化/记录数组
    - dict of Series
    - dict of dict
    - list of (dict | Series)
    - list of (list | tuple)
    - DataFrame
    - NumPy's MaskedArray
- 若设置了 DataFrame 的 index 和 columns 的 `name` 属性, 这些信息也会被显示出来:
- `DataFrame.values` 属性会以二维 ndarray 的形式返回 DataFrame 中的数据.
- 如果 DataFrame 各列的数据类型不同, 则值数组的数据类型会选用兼容所有列的数据类型:

```python
In [28]: frame.values
Out[28]:
array([[1.5, 'Ohio', 2000, nan],
       [1.7, 'Ohio', 2001, -1.2],
       [3.6, 'Ohio', 2002, -1.5],
       [2.4, 'Neveda', 2001, nan],
       [2.9, 'Neveda', 2002, -1.7]], dtype=object)  # object
```

#### 索引对象

- pandas 的索引对象负责管理轴标签和其他元数据(如轴名称等). 构建 Series 或 DataFrame 时, 所用到的任何数组或其他序列的标签都会被转换成一个 `Index`
- `Index` 对象不可修改(immutable)
- `Series.index`, `DataFrame.index`, `DataFrame.columns` 都是 `Index` 对象
- pandas 的索引类:
    - `pd.CategoricalIndex`
    - `pd.DatetimeIndex`
    - `pd.Float64Index`
    - `pd.Index`
    - `pd.IndexSlice`
    - `pd.Int64Index`
    - `pd.MultiIndex`
    - `pd.PeriodIndex`
    - `pd.TimedeltaIndex`
- `Index` 的功能也类似一个固定大小的集合, 其常用的方法和属性:
    - `append` - 连接到另一个 Index 对象, 形成新的 Index (类似于 list.extend)
    - `diff` - 计算差集, 得到新的 Index
    - `intersection` - 计算交集
    - `union` - 计算并集
    - `isin` - 计算一个指示各值是否都包含在参数集合中的布尔性数组
    - `delete` - 删除索引 i 处的元素
    - `drop` - 删除传入的值
    - `insert` - 将元素插入到索引 i 处
    - `is_monotonic` - 各元素均大于等于前一个元素时, 返回 True
    - `is_unique` - 当元素没有重复值时, 返回 True
    - `unique` - 计算 Index 中唯一值的数组

#### 基本功能

- pandas 对象的 `reindex` - 创建一个适应新索引的新对象, 即根据新的索引进行重新排序.
    - `index` - 用作索引的新序列,即可以是 Index 实例, 也可以是其他序列类型的 Python 数据结构
    - `fill_value` 关键字参数用于某个索引值不存在时, 自动填充值.
    - `method` 指定插值的方法, 对于时间序列这样的有序数据, 使用 `method` 来实现重新插值比较有效
        - `ffill` | `pad` - 前向插值, 即用前一个值填充当前空位
        - `bfill` | `backfill` - 后向插值
    - DataFrame 的 reindex 可以修改索引和列. 只传入一个序列时, 重新索引`行, `columns` 关键字参数可以在只传入一个索引的情况下, 重新索引列. DataFrame 可以同时对行和列进行重新索引, 但插值 (method) 只能按行应用
    - `limit` - 指定前向或后向插值时, 最大填充量
    - `level` - 在 MultiIndex 的指定级别上匹配简单索引, 否则选取其子集
    - `copy` - 默认为 True, 无论如何都复制; 若为 False, 新旧相等的索引就不复制
- pandas 对象的 `drop` - 指定索引或索引数组或列表, 丢弃某条轴上的一个或多个项, 返回一个在指定轴上删除了指定值的新的对象 (对像本身不改变)
    - 对 DataFrame, 默认丢弃行索引
    - `axis=1` 时, 并指定列名, 丢弃列
- Series 索引的工作方式类似于 NumPy 数组的索引, 但索引值不限于整数
    - 虽然指定了 `index`, 但仍然能使用数字索引
    - 可以使用 list of index 取值, `obj[['a', 'b', 'c']]`, 或 `obj[[1, 3]]`
    - 还能使用布尔过滤来取值, `obj[obj < 2]`
    - 切片也可以, `obj["b": "c"]`, `pandas 利用标签的切片是闭区间`. 对切片赋一个标量时, 将为切片区间统一赋值
- DataFrame 的索引, 其实是获取一个或多个`列`, `frame['pop']`
    - DataFrame 索引的切片或布尔过滤是对`行`的选取, `frame[:2]`, `data[data["three"] > 5]`
    - `data < 5` 会将 DataFrame 的所有值与 5 进行比较, 返回一个布尔型 DataFrame, 可用于布尔过滤
- `DataFrame.ix` 让用户可以通过 NumPy 式的标记法以及轴标签从 DataFrame 中选取行和列的子集. 这也是一种重新索引的简单手段, 闭区间
    - `DataFrame.ix[index, columns]` 同时选取行和列, 行在前, 列在后
    - `DataFrame.ix[index]` 取单行或一组行
    - `DataFrame.ix[:, columns]` 取单列或列子集, 实际是取了全部行的切片
    - 行与列都可以用布尔过滤
- 其他 DataFrame 索引选项:
    - `obj[columns]` - 选取单列或一组列. 可以使用: 布尔过滤(过滤行), 切片(行切片), 布尔型 DataFrame(根据条件设置值)
    - `xs()` - 根据标签选取单行或单列, 并返回 Series
    - `icol()`, `irow()` - 根据整数位置选取单行或单列, 并返回一个 Series
    - `get_value()`, `set_value()` - 根据行标签和列标签选取单个值

#### 算术运算和数据对齐

- pandas 最重要的功能之一: `对不同索引的对象进行算术运算`
- 在将对象相加时, 如果存在不同的索引对, 则结果的索引就是该索引对的`并集`
- 自动的数据对齐操作在不重叠的索引处引入了 NA 值. 缺失值会在算术运算过程中传播
- 对于 DataFrame, 对齐操作会同时发生在行和列上
- 在算术方法中填充值的方法, 对一个 DataFrame 或 Series 对象调用 `add` 方法, 传入 `fill_value` 参数 (与 `reindex()` 方法类似). 除 `add()` 外, 还有 `sub()`, `div()`, `mul()`
- DataFrame 与 Series 的算术运算: 默认情况下, 它们之间的算术运算会将 Series 的索引匹配到 DataFrame 的列, 然后沿行向下传播 (匹配列, 在行上广播). 同样地, 如果存在不同的索引, 会产生并集
- 如果希望匹配行, 在列上广播, 则必须使用算术运算方法, 即上述的 `add()` 之流. 利用关键字参数 `axis` 传入轴号. 如 `df.sub(series, axis=0)`
- NumPy 的 ufuncs (元素级数组方法, 一类方法的总称), 也可用于操作 pandas 对象, 比如 `np.abs(df)` 会对 df 的所有元素应用取绝对值操作
- `apply()` - 将函数应用到由各列或各行所形成的一维数组上: (默认 `axis=0`, 即`行`)

```python
f = lambda x: x.max() - x.min()

frame.apply(f)
# ouput:
# b 1.8
# c 1.7
# c 2.7

frame.apply(f, axis=1)
# output:
# Utah 1.0
# Ohio 2.5
# Texas 0.7
# Oregon 2.5
```

- 许多最常见的数组统计功能都被实现成 DataFrame 的方法(如 sum, mean)
- 除标量值外, 传给 `apply` 的函数可以返回有多个值组成的 Series:

```python
def f(x):
    return Series([x.min(), x.max()], index=["min", "max"])
frame.apply(f)
```

- `applymap` - 实现元素级的运算:

```python
format = lambda x: "%.2f" % x
frame.applymap(format)
```

- Series 的元素级函数 `map` 方法, `frame['e'].map(format)`
- `sort_index` - 返回一个已排序的新对象.
    - 对 DataFrame, 可根据任意一个轴上的索引进行排序, 默认 `axis=0`, 可以指定 `axis=1` 对列进行排序
    - 数据默认是升序排列的, 通过 `ascending=False` 使用降序排列
- 对 Series 按值排序, 使用其 `order` 方法. 排序时, 任何缺失值默认被放在 Series 末尾
- 在 DataFrame 上, 希望根据一个或多个列中的值进行排序, 可以将列名传递给 `by` 关键字参数, 可以是 str 也可以是 list of str
- 排名 (ranking) 跟排序关系密切, 且它会增设一个排名值 (从 1 开始, 一直到数组中有效数据的数量). 默认情况下, rank 是通过"为各组分配一个平均排名"的方式破坏平级关系 (?, 真心没搞明白 rank)
    - `method` - 排名时用于破坏平级关系
        - `average`: average rank of group, 在相等分组中, 为各个值分配平均排名
        - `min`: lowest rank in group, 使用整个分组的最小排名
        - `max`: highest rank in group, 使用整个分组的最大排名
        - `first`: ranks assigned in order they appear in the array, 按值在原始数据中出现的顺序分配排名
        - `dense`: like 'min', but rank always increases by 1 between groups
- 同样地, 对于 DataFrame, 可以在行或列上计算排名
- 许多 pandas 函数都要求标签唯一, 但这并不是强制性的. 索引的 `is_unique` 属性显示它的值是否是唯一的
- 对于带有重复值的索引, 数据选取的行为将有所不同. 如果某个索引对应多个值, 则返回一个 Series, 而对应单个值的, 则返回一个标量值. 对 DataFrame 的行进行索引也是如此

#### 汇总和计算描述统计

- pandas 对象拥有一组常用的数学和统计方法, 它们大部分都属于`约简和汇总`统计, 用于从 Series 中`提取单个值`(如 sum, mean) 或从 DataFrame 的行或列中提取一个 Series. 跟对应的 NumPy 数据方法相比, 它们都是基于没有缺失数据的假设而构建的
- DataFrame , 可对行或列进行操作的方法, 似乎默认都是 `axis=0`, 如 `df.sum` 默认按列计算, 返回一个含有列小计的结果. `axis=1` 将会按行进行求和
- NA 的值会自动被排除, 除非整个切片 (整行整列是切片的一种形式) 都是 NA. 使用 `skipna=False` 可禁用该功能
- 约简方法的参数:
    - `axis` - 约简的轴, DataFrame 的行用 0, 列用 1
    - `skipna` - 是否排除缺失值
    - `level` - 如果轴是层次化的索引 (MultiIndex), 则根据 level 分组约简
- 有些方法(如 idxmin, idxmax)返回的是`间接统计` (比如达到最小值或最大值的索引):

```python
In [14]: df.idxmin()
Out[14]:
one    d
two    b
dtype: object

In [15]: df.min()
Out[15]:
one    0.75
two   -4.50
dtype: float64
```

- 有些方法是`累计型`的:

```python
In [16]: df
Out[16]:
    one  two
a  1.40  NaN
b  7.10 -4.5
c   NaN  NaN
d  0.75 -1.3

In [17]: df.cumsum()
Out[17]:
    one  two
a  1.40  NaN
b  8.50 -4.5
c   NaN  NaN
d  9.25 -5.8
```

- 还有一些方法既不是约简型的, 也不是累计型的, 一次性产生多个汇总统计, 如 `describe`:

```python
In [18]: df.describe()
Out[18]:
            one       two
count  3.000000  2.000000
mean   3.083333 -2.900000
std    3.493685  2.262742
min    0.750000 -4.500000
25%    1.075000 -3.700000
50%    1.400000 -2.900000
75%    4.250000 -2.100000
max    7.100000 -1.300000
```

- 对于非数值型数据, `describe` 会产生另外一种汇总统计:

```python
In [22]: obj.describe()
Out[22]:
count     16
unique     3
top        a
freq       8
dtype: object
```

- pandas 描述与汇总统计
    - `count` - 非 NA 值的数量
    - `describe` - 针对 Series 或 DataFrame 各列计算总统计
    - `min, max` - 计算最小/大值
    - `idxmin, idxmax` - 计算能够获取到最小/大值的索引值
    - `quantile` - 计算样本的分位数 (0 到 1) (? 分位数是什么)
    - `sum` - 求总和
    - `mean` - 求平均
    - `median` - 求算术中位数
    - `mad` - 根据平均值计算平均绝对离差 (? 不明白什么是离差)
    - `var` - 样本值的方差
    - `std` - 样本值的标准差
    - `skew` - 样本值的偏度 (三阶矩) (? 什么鬼)
    - `kurt` - 样本值的峰度 (四阶矩) (? 什么鬼)
    - `cumsum` - 样本值的累计和
    - `cummin, cummax` - 样本值累计最小/大值
    - `cumprod` - 样本值累计积
    - `diff` - 计算一阶差分(读时间序列有效)
    - `pct_change` - 计算百分数变化
- `Series.corr()` - 计算两个 Series 中重叠的, 非 NA 的, 按索引对齐的值的相关关系 (`相关系数`)
- `Series.cov()` - 计算两个 Series 的协方差
- `DataFrame.corr(), DataFrame.cov()` - 以 DataFrame 的形式返回完整的相关系数或协方差矩阵 (自身)
- `DataFrame.corrwith()` - 计算列或行与另一个 Series 或 DataFrame 之间的相关系数
    - 传入 Seires, 将返回一个相关系数值 Series
    - 传入 DataFrame, 则会按计算`按列名配对`的相关系数
    - `axis=1` 按行进行计算. 无论如何, 在计算相关系数之前, 所有的数据项都会按标签对齐
- `Series.unique()` - 得到 Series 中的唯一值数组, 返回的唯一值是未排序的, 可再用 `sort()` 方法对结果再排序
- `Series.value_counts()` - 计算 Series 中各值出现的频率, 结果按值频率降序排列
- `pd.value_counts()` - 顶级 pandas 函数, 可用于任何数组或序列
- `Series.isin(), DataFrame.isin()` - 判断矢量化集合的成员资格, 可用于选取 Series 中或 DataFrame 列中数据的子集
- 将 `pd.value_counts` 作为参数传给 `DataFrame.apply` 函数, 可以得到 DataFrame 相关列的一张柱状图:

```python
In [11]: data = pd.DataFrame({'Qu1': [1, 3, 4, 3, 4],
                              'Qu2': [2, 3, 1, 2, 3],
                              'Qu3': [1, 5, 2, 4, 4]})
In [12]: data
Out[12]:
   Qu1  Qu2  Qu3
0    1    2    1
1    3    3    5
2    4    1    2
3    3    2    4
4    4    3    4
[5 rows x 3 columns]

In [13]: result = data.apply(pd.value_counts).fillna(0)

In [14]: result
Out[14]:
   Qu1  Qu2  Qu3
1    1    1    1
2    0    2    1
3    2    2    0
4    2    0    2
5    0    0    1
[5 rows x 3 columns]
```

#### 处理缺失数据

- pandas 的设计目标之一就是`让缺失数据的处理任务尽量轻松`
- pandas 对象上的所有描述统计都排除了缺失数据
- pandas 使用`浮点值` NaN 表示浮点或非浮点数组中的缺失数据, `只是一个便于被检测出来的标记而已`
- Python 内置的 None 值也会被当作 NA 处理
- NumPy 的数据类型体系中缺乏真正的 NA 数据类型或位模式
- NA 处理方法:
    - `dropna` - 根据各标签的值中是否存在缺失数据对轴标签进行过滤, 可通过阈值调节对缺失值的容忍度
    - `fillna` - 用指定值或插值方法(ffill, 或 bfill) 填充缺失数据
    - `isnull` - 返回一个含有布尔值的对象, 这些布尔值表示哪些值是缺失值, 该对象的类型与原类型一样
    - `notnull` - isnull 的否定式
- `DataFrame.dropna()` - 默认丢弃任何含有缺失值的行
    - `how=all` - 只丢弃全为 NA 的行
    - `axis=1` - 丢弃列
    - `thresh` - 只留一部分数据
- `fillna`
    - 通过一个常数调用 fillna 就会将缺失值替换为那个常数值
    - 通过一个字典调用 fillna, 可以实现对不同列填充不同值: `df.fillna({1: 0.5, 3: -1})`, key 指定列名, value 即为填充值
    - `fillna` 默认返回新对象. `inplae=True` 对现有对象进行修改
    - 对 `reindex` 有效的的插值方法可用于 `fillna`: `df.fillna(method="ffill")`, `df.fillna(method="ffill", limit=2)`
    - 可以将一些其他值作为填充值传入 `fillna`, 如 `Series.fillna(data.mean())`, 使用平均值作为插值

#### 层次化索引

- 层次化索引是 pandas 的一项重要功能, 使用户能在一个轴上拥有多个`索引级别`. 抽象点说, 它使用户能以低维度形式处理高维度数据

```python
In [50]: data = pd.Series(np.random.randn(10), index=[['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'd', 'd'],
                                                      [1, 2, 3, 1, 2, 3, 1, 2, 2, 3]])

In [51]: data
Out[51]:
a  1   -2.224864
   2   -0.234775
   3   -1.143708
b  1    0.186533
   2    0.251844
   3    0.680129
c  1   -1.360122
   2    0.906973
d  2   -0.727403
   3    1.494060
dtype: float64
```

- 以上就是带有 `MultiIndex` 索引的 Series 的格式化输出形式.
- 对于层次化索引的对象, 选取子集的操作很简单:

```python
In [53]: data['b']
Out[53]:
1    0.186533
2    0.251844
3    0.680129
dtype: float64
In [54]: data['b':'c']
...
In [55]: data[['b', 'd']]
...
```

- 甚至可以在内层选取: `In [4]: data[:, 2]`
- 层次化索引在`数据重塑`和`基于分组的操作`(如透视表生成)中扮演重要角色. 具有层次化索引的 Series 通过 `unstack` 可以重被安排到一个 DataFrame 中
- DataFrame 对象使用 `stack` 方法也可以转成具有层次化索引的Series
- 对于 DataFrame, 每个轴都可以有分层索引
- `swaplevel` - 接收 2 个级别编号或名称, 并返回一个互换了级别的新对象(数据不发生改变)
- `sortlevel` - 根据单个级别中的值对数据进行排序(稳定的). 交换级别时, 常常也会用到 `sortlevel`, 这样最终结果就是有序的了
- 在层次化索引的对象上, 如果索引是按字典方式从外到内排序(即调用 `sortlevel(0)` 或 `sort_index()` 的结果), 数据选取操作的性能会好很多
- `DataFrame.set_index()` 方法将一个或多个`列转为行索引`, 并返回一个新的 DataFrame 对象. 如 `df.set_index(['c', 'd'])`
- 默认情况下, 转换成行索引的列会从 DataFrame 对象中删除, 使用 `drop=False` 保留
- `DataFrame.reset_index()` 的功能与 `set_index()` 相反

#### 其他 pandas 话题

- `整数索引`, 使用负数(比如 -1)会带来歧义(很难推断用户想要什么), 因此会直接报错; 非整数索引, 没有这样的歧义, 使用负数索引不报错
- 为了保持良好的一致性, 如果轴索引含有索引器, 那么根据整数进行数据选取的操作将总是面向标签的
- 如果需要可靠的, 不考虑索引类型的, 基于位置的索引, 可以使用 `iloc` 属性
- `Panel` 数据结构可以看作是一个 `三维版的 DataFrame`
-  可以用一个`由 DataFrame 对象组成的字典`或一个`三维 ndarray` 来创建 Panel 对象
- `Panel.swapaxes` - 交换轴
- 基于 ix 的标签索引被推广到了三个维度, `panel.ix[items, major, minor]` 如此来指定
- 另一种呈现 Panel 数据(尤其是对拟合统计模型)的办法是 `堆积式` 的 DataFrame 形式, Panel 的 `to_frame()` 将 Panel 转为具有层次化索引的 DataFrame. DataFrame 有一个相应的 `to_panel` 方法, 是 `to_frame` 的逆运算
