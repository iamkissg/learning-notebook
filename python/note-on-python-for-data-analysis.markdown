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
- `pd.Series.unstack()` - Unstack, a.k.a. pivot, Series with MultiIndex to produce DataFrame. Series -> DataFrame
- `pd.DataFrame.sum(self, axis=None, skipna=None, level=None, numeric_only=None, **kwargs)` - Return the sum of the values for the requested axis
- `pd.DataFrame.plot` - 直接利用 matplotlib 绘图
- `pd.DataFrame.plot(kind="barh", stacked=True)` - 生成堆积条形图
