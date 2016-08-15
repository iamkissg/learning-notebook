# Note on Pandas - powerful Python data analysis toolkit

## Pandas 一览

- Pandas 的标准导入姿势: `import pandas as pd`
- 简单到哭文件读取: `pd.read_filetype(filename, ...)`
- 类似 shell 命令的查看前几行与末几行语句: `df.head(n)` 或 `df.tail(n)`
- 改变列名, 长度必须匹配: `df.columns = list_of_column_names`
- Pandas 中, 一条记录对应一行, 使用 `len` 方法, 将返回数据集的总行数, 即记录数
- 获取基本统计信息, `df.describe()`. 另可对显示格式进行设置, 比如: `pd.options.display.float_format = '{:,.3f}'.format # Limit output to 3 decimal places.`
- Pandas 的 dataframe 可看作 series 的字典, 因此, 提取列的时候, 会得到一个 series, 可以用 `df[column_name]` 或点标记法提取列
- 无敌的`布尔过滤`: `df.rain_octsep < 1000`, 将返回一个布尔值的列. 可充当索引: `df[df.rain_octsep < 1000]`
- 复合条件过滤: `df[(df.rain_octsep < 1000) & (df.outflow_octsep < 4000)]` 不能用 `and` 关键字, 会引发操作顺序问题, 必须用 `&` 和圆括号
- 字符串方法过滤: `df[df.water_year.str.startswith('199')]` 必须以 `.str.str_method`
- Pandas 的行也有标签, 行标签可以是基于数字的或者是标签. 数字标签: `df.iloc[index]`, 返回给定行的 series; 字符标签: `df.loc[str]`; 另, `df.ix[index]` 同时起到 `loc` 和 `iloc` 的作用, 速度更快, 但具有轻微不可预测性
- 排序与索引回复: `df.sort_index()` 与 `df.reset_index()`
- `df.water_year.apply(func)` - 对一列数据应用函数.
- `applymap` - 对整个数据集应用函数
- `groupby` - 按照选择的列对数据进行分组, 可应用于多列, 通常与 `max`, `min`, `mean` 等配合使用
- `unstack` - 将一列数据设置为列标签, 例如 `decade_rain.unstack(0)` 将第 0 列设置为列的标签
- `pivot` - 轴旋转, 相当于 `set_index()` + `sort_index()` + `unstack`, 设置新的索引, 对索引进行排序, 调用 `unstack`\\
`high_rain.pivot('year', 'rain_octsep')[['outflow_octsep', 'outflow_decfeb', 'outflow_junaug']].fillna('')`
- `pivot` 会产生很多空的记录, 即 `NaN`, 用 `fillna()`填补空的记录
- `dropna()` - 删除匹配的行, `dropna(how='any')` 删除所有行
- 关联数据集:

```python
rain_jpn = pd.read_csv("jpn_rain.csv")
rain_jpn.columns = ["year", "jpn_rainfall"]

uk_jpn_rain = df.merge(rain_jpn, on="year")
```

- 通过 `on` 关键字指定需要合并的列. 若省略该参数, Pandas 会自动选择要合并的列
- Pandas 的 `plot` 方法会调用 `Matplotlib`绘制数据图
- `to```

- 通过 `on` 关键字指定需要合并的列. 若省略该参数, Pandas 会自动选择要合并的列
- `to_file_type(filename)` - 将处理后的数据保存到文件

---

- pandas 适用于各种数据:
 - 各种异质类型的表格数据
 - 时间有序或无序的数据
 - 任意的矩阵数据
 - 其他任意类型的观察/统计数据集
- pandas 的两个主要数据结构是 一维的 **Series** 和二维的 **DataFrame**
- pandas 是在 Numpy 的基础上建立的，也致力于与其他科学计算的第三方库配合
- pandas 的优点：
 - 处理缺失的数据，浮点或非非浮点数（代表是 NaN）
 - 大小可变：可轻易地对 DataFrame 更高维度的对象进行插入或删除
 - 自动、精确的数据赋值
 - 高效、灵活的功能分组，提供数据集的分离、应用、整合操作
 - 能轻易地将其他 Python 或 NumPy 的数据结构转换成 DataFrame 对象
 - 基于标签的智能切片、索引、划分子集
 - 直观的数据集融合
 - 灵活的数据集重塑与置换
 - 分级的多标签
 - 提供稳定的 IO，可从无格式文件（flat files），Excel 文件，数据库加载数据，从 HDF5 格式加载或存储数据
 - 具体的时间系列功能：日期范围生成，频率转换，统计，线性回归，时期超前与滞后等等
- 对于数据科学家，工作大致可分为：加工与清洗数据，分析与模型化，将分析结果组织成合适的图标展示。
- pandas 快，依赖于统计模型，被广泛地用于商业应用
