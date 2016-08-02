# Note on Numpy and Scipy

## Overview

- NumPy 提供了多维数组对象以及各种派生对象，它还提供了数组的快速操作规范，包括数学的、逻辑的、形状操作、排序、查询、I/O、离散傅立叶变换、基础线代与统计操作、随机仿真等等等等
- NumPy 的核心是 *nbarray* 对象，囊括了 n-维同质类型的数据数组。
- NumPy 数组与 Python 序列的不同之处：
 - NumPy 数组在创建时，可灵活地选择大小。改变 nbarray 的大小将会删除原数组创建新数组
 - NumPy 数组元素需要是同一数据类型，因此每个元素占用相同的内存大小。例外是，创建对象的列表，从而使数组拥有不同大小的元素
 - NumPy 支持先进的数学运算，以及其他对海量数据的其他运算。这些操作可能比 Python 内建序列的操作更高效，代码量更少
 - 越来越多的科学/数学包都在使用 NumPy。它们通常使用 Python 内建序列进行输入，再转化为 NumPy 数组进行处理，输出 NumPy 数组。因此，要使用 Python 进行科学/数学计算是远远不够的，还要知道 NumPy。
- 逐元素的操作是 NumPy 的默认模式，它通过预编译 C 代码实现。比如矩阵运算：`c = a * b`，运算速度接近 C 代码。
- NumPy 的两大特征：矢量化与广播(?):
 - 矢量化就是没有显式的循环，索引等等，但所有的操作，包括优化，预编译 C 代码都在”幕后“进行。矢量化的好处是：
  - 矢量化的代码更简介易读
  - 更少的代码量意味着更少的 bugs
  - 代码更接近标准数学概念
  - 矢量化的结果使代码更符合 Python 哲学
 - 广播用于描述隐含的逐元素操作行为。在所有 NumPy 操作中，包括算术、逻辑、位操作、函数运算，都是隐含的逐元素操作，即广播。

## Quickstart tutorial

- NumPy 的主对象是**同质的多维度数组**。在 NumPy中，维度称为 *axes*，用 *rank* 表示
- `[1, 2, 1]` 是一维的，rank 为 1；`[[ 1., 0., 0.], [ 0., 1., 2.]]` 是二维的，rank 为 2，第一个维度长度为2，第二个维度长度为3
- NumPy 的数组类称为 `ndarray`，别称 `array`，但 `numpy.array` 不同于 Python 标准库的 `array.array`。`numpy.array` 的重要属性：
 - ndarray.ndim - 维度数。在 Python 中，维度数用 *rank* 表示。
 - ndarray.shape - 维度。用 tuple 表示各维度的数组的大小。比如 n \* m 的矩阵的 `shape` 是 `(n, m)`。显然，`shape`的长度就是 rank，或者说 `ndim`
 - ndarray.size - 数组的元素总数，等于 `shape` 的元素总和。
 - ndarray.dtype - 描述数组元素类型的对象，可用标准 Python 类型，或者 NumPy 提供的类型，比如：numpy.int32, numpy.int16, and numpy.float64
 - ndarray.itemsize -数组元素的大小（字节）。等价于 `ndarray.dtype.itemsize`
 - ndarray.data - 包含真实数组元素的缓冲。通常不需要使用该属性，元素可用下标进行访问。

#### 创建数组

- 利用 `array` 方法，用标准 Python list 或 tuple 创建数组，结果的元素类型由序列中元素的类型推导出，也可以在创建时指定（关键字参数 dtype）
- 通常，数组元素一开始是未知的，而数组大小是已知的。NumPy 提供了多种预置内容的数组创建方法，这使得扩充数组的开销将至最低（动态的扩充数组，开销是很大的）
- `zeros` 用 0 预填充数组，`ones` 用 1 预填充，`empty` 根据内存状态随机初始化。默认的，`dtype` 是 `float64`
- 自定义序列，可用 `arange` 函数，类似于 `range`，但返回数组对象而不是 list。
- 用 `arange` 生成浮点数组时，结果大小不可预测。替换的方法是使用 `linspace`，指定元素个数而不是步长

#### 打印数组

- NumPy 的打印：
 - 最底层的维度，从左到右打印
 - 最底层之上，从上到下打印
 - 当数据量太大时，NumPy 将自动跳过中心部分，只打印角落数据。
 - 可修改 `set_printoptions` 选项来修改打印的行为，比如打印全部数据

#### 基础操作

- 算术运算是广播的，`*` 操作也是广播的。数学意义上的矩阵乘法，使用 `dot` 函数：

```python
>>> A = np.array( [[1,1],
...             [0,1]] )
>>> B = np.array( [[2,0],
...             [3,4]] )
>>> A*B                         # elementwise product
array([[2, 0],
       [0, 4]])
>>> A.dot(B)                    # matrix product
array([[5, 4],
       [3, 4]])
>>> np.dot(A, B)                # another matrix product
array([[5, 4],
       [3, 4]])
```

- 如 `+=`，`*=` 的操作，同 Python 中意义，将修改现有的数组，而非创建新的数组
- 不同类型的操作，结果类型转为更通用或更精确的类型（向上转型，向下转型会报错）
- 许多一元操作，都以 `nbarray` 类的方法实现，比如求和，取大取小。这些操作默认将整个 n-维数组看作一个 list，而忽略其形态。可通过指定 `axis` 来指定操作的维度

#### 通用函数

- **一维**数组可以被索引，切片，迭代，就如 list 和其他 Python 序列一样
- **多维**数组每个轴上都有一个索引，这些索引是一个由逗号分隔开的组合给定，如 `b[2,3]` 就是 `b[2][3]`，再如 `b[1:3, : ]  `
- 多维数组的索引缺省时，索引缺省的轴（那一维）返回全部结果。即缺省的索引被自动被填充，比如三维数组 `b[i]` 被填充为 `b[i,:,:]`
- NumPy 也提供 `...` 来补全索引，比如五维数组 `x[1,2,...]` 等价于 `x[1,2,:,:,:]`，`x[...,3]` 等价于 `x[:,:,:,:,3]`
- 对多维数组的迭代，默认在第一个维度进行。使用 `flat` 属性，返回一个包含数组所有元素的迭代器，因此可对所有元素进行迭代

#### 形状操作

- 数组的形状由每一轴上的元素数量决定
- 数组的形状可通过多种方式改变：
 - `.ravel()` - 将多维数组转换成一维的
 - `a.shape = (x, y, z, ..) - 修改数组的形状属性，修改表现形式，从而改变形状。
 - `.resize((n, m, ..))` - 对数组本身修改
 - `.reshape((n, m, ..)) - 返回某一形状的数组，但不对数组本身进行修改
 - `a.T` - 返回 a 转置的结果
- `ravel()` 的结果的元素顺序是 C 风格的，即 a[0, 0] 的下一个元素是 a[0, 1]。NumPy 默认的数组存储顺序就是 C 风格的。\\
`NumPy 的内部存储就是 C 风格的形式，看上去像一维数组`
- 使用一个可选参数，可用 Fortran 风格的数组，最左边的下标先改变，即 a[0, 0] 的下一个元素是 a[1, 0]
- 在重塑形状的操作中，若某一维指定为 `-1`，该为的元素个数将根据其他维的长度自动计算出

#### 不同数组叠加

- `vstack(tuple of arrays)` - 竖直叠加
- `hstack(tuple of arrays)` - 水平叠加
- `column_stack` - 将一维数组看作多行(column)
- `r_` 和 `c_` 允许在一个轴上直接进行叠加, 可使用 `:`, `np.r_[1:4,0,4]` -> `array([1, 2, 3, 0, 4])`

#### 拆分数组

- `hsplit` - 水平方向进行拆分, 可指定将数组分成多少部分, 或指定拆分后的数组的形状
- `vsplit` - 竖直方向进行拆分

#### 是否拷贝

- 部分操作直接对数组本身进行操作, 部分操作返回对数组副本的操作结果
- Python 参数传递使用可变对象作为引用, 因此函数调用不会创建副本
- 浅拷贝, 新瓶装旧酒
- 切片实现的是浅拷贝
- 深拷贝, 新瓶装新瓶

#### 其他基础

- 广播法则1: 若所有输入的数组维度不相同, 用 `1` 扩充小数组, 直到维度相等
- 灵活的索引机制: 1. 数字下标, 2. 切片, 3. 整数数组作为索引, 4. 布尔数组作为索引
- 当数组是多维数组是, 充当索引的单一数组指向多维数组的第一维
- 索引数组可以是多维的, 但每一维形状必须相同

# 此处已经看不懂了, 先跳过

## NumPy basis

#### Data types

- NumPy 提供的数学数据类型, 数字代表该类型在内存中所占位数, 不带数字的, 通常是平台依赖的:

| Data type |  Description |
| :--:      | :-: |
| bool\_    |  Boolean (True or False) stored as a byte |
| int\_     |  Default integer type (same as C `long`; normally either `int64` or `int32`) |
| intc      |  Identical to C `int` (normally `int32` or `int64`) |
| intp      |  Integer used for indexing (same as C `ssize_t`; normally either `int32` or `int64`) |
| int8      |  Byte (-128 to 127) |
| int16     |  Integer (-32768 to 32767) |
| int32     |  Integer (-2147483648 to 2147483647) |
| int64     |  Integer (-9223372036854775808 to 9223372036854775807) |
| uint8     |  Unsigned integer (0 to 255) |
| uint16    |  Unsigned integer (0 to 65535) |
| uint32    |  Unsigned integer (0 to 4294967295) |
| uint64    |  Unsigned integer (0 to 18446744073709551615) |
| float\_   |  Shorthand for `float64`. |
| float16   |  Half precision(精度) float: sign bit, 5 bits exponent, 10 bits mantissa |
| float32   |  Single precision float: sign bit, 8 bits exponent, 23 bits mantissa |
| float64   |  Double precision float: sign bit, 11 bits exponent, 52 bits mantissa |
| complex\_ |  Shorthand for complex128. |
| complex64 |  Complex number(复数), represented by two 32-bit floats (real and imaginary components) |
| complex128|  Complex number, represented by two 64-bit floats (real and imaginary components) |

- 此外, NumPy `intc` 的变种: `short`, `long`, `longlong` 及它们的无符号形式也有定义
- NumPy 的数字类型是 `dtype` (data-type) 对象的实例, 每个都有独有的特征
- 当与低层进行交互时, 需要考虑数据类型的平台依赖性问题
- 用 `.astype(dtype)` 进行数据类型转换, 若用数据类型本身进行转换
- Python 数据类型与 NumPy 的对应关系, 只有这些: `int` -> `np.int_`, `bool` -> `np.bool_`, `float` -> `np.float_`, `complex` -> `np.complex_`
- `.dtype`属性查看数组类型
- NumPy 以标量形式返回数组元素, NumPy 标量与 Python 标量相差较大, 要混用时, 用类型函数进行显式的转换
- ?使用数组标量的主要优点是, 保存了数组类型

#### Array creation
