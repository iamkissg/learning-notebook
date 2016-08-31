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
