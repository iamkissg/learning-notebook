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
