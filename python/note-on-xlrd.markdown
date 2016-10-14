# xlrd 学习笔记

- excel 的导航, 按 sheets 到 cells (row, col)

#### Introspecting a Sheet

- `open_workbook` 返回的 `xlrd.book.Book` 对象包含了工作簿所有的信息.
- `open_workbook` 的参数可以是表示文件的 str, 或者文件内容, 或 `mmap` 对象
- `nsheets` - 表示工作簿 sheets 数的整数. 与 `sheet_by_index` 方法连用, 是最常用的解析单个 sheets 的方式
- `sheet_names` - 返回 list of sheet names (unicde)
- 单张 sheet 可通过 `sheet_by_name` 函数以 sheet name 的方式获得
- `sheets` 方法的结果可以用于迭代解析出工作簿中所有的 sheets
- ...其他

#### Introspecting a Sheet
- `xlrd.sheet.Sheet` 对象包含了工作表的所有信息和内容
- `name` - 表示工作表名的 unicode
- `nrows` 和 `ncols` - 行数与列数
- `sheet.cell(row, col)` - 返回 `xlrd.sheet.Cell` 对象

#### Getting a particular Cell

- `xlrd.sheet.Cell` 对象属性很少, `value` 属性包含了单元格的真实值, `ctype` 记录了单元格的类型
- `xlrd.sheet.Sheet` 对象的 `cell_value()` 方法返回特定 cell 的值, `cell_type()` 方法返回特定 cell 的类型. 这两个方法比通过 `Cell` 对象来解析 cell 值或类型更快 (`quicker`)

#### Iterating over the contents of a Sheet

- `xrld` 提供了解析一组单元格信息的方法, 对称的 (by row or by column)
- `row(n)` 和 `col(n)` 方法返回一整行或一整列的 `Cell` 对象
- `row_slice(start, end)` 和 `col_slice(start, end)` 方法返回行或列的切片, 从 `start` 开始到 `end` (end 是可选的)
- `row_types()` 和 `col_types()` 返回 list of int, int 表示 cell types
- `row_values()` 和 `col_types()` 返回 list of cell values

#### Utility Functions

- `cellname(row, col)` - 根据行列号, 返回相对 Excel Cell 索引 (A1)
- `cellnameabs(row, col)` - 返回绝对 Excel Cell 索引 ($A$1)
- `colname(n)` - 列索引转换成 Excel 列名

#### Unicode

- `xlrd` 返回的所有文本属性基本是 unicode 对象, 很少是 ascii strings
- Excel 文件的每一个文本是以下之一的编码:
    - Latin1. 如果适配的话
    - UTF_16_LE. 如果不适配 Latin1
    - 老式文件, by an encoding specified by an MS codepage. 将由 xlrd 映射到 Python 编码, 结果是 unicode 对象
- `open_workbook()` - 的 `encoding` 参数可以指定 Excel 文件的编码

#### Type of Cell

- cell type 以整型数表示, 还有对应的常量

###### Text

- `xlrd.XL_CELL_TEXT`
- 此类型单元格的值用 `unicode` 对象表示

###### Number

- `xlrd.XL_CELL_NUMBER`
- 此类型单元格的值用 `float` 对象表示

###### Date

- `xlrd.XL_CELL_DATE`
- Excel 文件实际并不存在 dates, 只是特殊格式组织的 Number
- xlrd 将根据 str 的数值格式, 将像是 `date` 的 cell type 解释为 `xlrd.XL_CELL_DATE`
- `xldate_as_tuple(xldate, datemode)` 方法将 Date cell 中的 float 值转换成一个 tuple (year, month, day, hour, minute, second)

> Excel 文件有 2 种可能的日期模式, 一种用于原生的 Windows 机创建的文件, 一种用于苹果机上创建的文件. 由 `xlrd.book.Book.datemode` 属性表示,
- `1904.01.03` 之前的日期, 有各种问题
- Excel 公式函数 `DATE()` 在某些情况下, 会返回不可预期的时期

###### Boolean

- `xlrd.XL_CELL_BOOLEAN`
- 此类型单元格的值用 `bool` 对象表示

###### Error

- `xlrd.XL_CELL_ERROR`
- 此类型单元格的值用 `int` 对象表示错误代码
- `error_text_from_code` 字典可用于将错误代码转换成错误消息

###### Empty / Blank

- Excel 文件只会保存有值或格式化的 cell. 但 `xlrd` 用 cell 的矩形网格来表示 sheets
- 没有值的 cell 其类型是 `xlrd.XL_CELL_EMPTY`.
- 此外, 只有一种"空" cell (值为空串). 因此空 cell 可以用 Python identity check
- Excel 文件中仅仅进行了格式化的 cell, 类型是 `xlrd.XL_CELL_BLANK`, 值是空串

#### Names

- Names are created in Excel by navigating to Insert > Name > Define. 要用 `xlrd` 从 `Names` 解析信息, 若对定义熟悉, 使用 names 是个好主意

###### Types

- Name 可以是:
    - 常量
        - CurrentInterestRate = 0.015
        -  NameOfPHB = “Attila T. Hun”
    - 绝对 cell 引用
        - CurrentInterestRate = Sheet1!$B$4
    - 1D, 2D, 3D cell 块的绝对引用
	- MonthlySalesByRegion = Sheet2:Sheet5!$A$2:$M$100
    - list of 绝对引用
        - Print_Titles = [row_header_ref, col_header_ref])
- 常量可被解构
- 绝对引用坐标可被解构, 这样就能从相关的 sheet 中解析出相应的数据
- 相对引用只在对 cell 充分了解的基础上才好用.
- 许多 Excel 文件包含的公式不好用, 难于 `evaluate`
- A full calculation engine is not included in xlrd.

###### Scope

- Name 的范围可以是全局的, 也可以是某张 sheet 特有的.
- Name's identifier 可在不同域中复用. 当多个 name 有相同的标识符时, 最好的使用方法是基于作用域

###### Usage

- 使用 name 的原因包括:
    - 为工作簿中多次出现值赋 textual name: `RATE = 0.015`
    - 为容易错抄的公式赋 textual name: `SALES_RESULTS = $A$10:$M$999`

#### Formatting

- 若希望复制已存在的格式化信息, 查看 `xlutils.copy` 和 `xlutils.filter`
- 若希望审查格式化信息, 看看以下类:
    - xlrd.book.Book
    	- colour_map
        - palette_record
	- font_list
	- style_name_map
 	- format_list
	- xf_list
	- format_map
    - xlrd.sheet.Sheet
	- cell_xf_index
	- default_row_height_mismatch
	- rowinfo_map
	- default_row_hidden
	- colinfo_map
	- defcolwidth
	- computed_column_width
	- gcw
	- default_additional_space_above
 	- merged_cells
	- default_additional_space_below
 	- standard_width
	- default_row_height
    - xlrd.sheet.Cell
	- xf_index
    - other classes
	- xlrd.sheet.Rowinfo
	- xlrd.formatting.XFAlignment
	- xlrd.sheet.Colinfo
	- xlrd.formatting.XFBackground
	- xlrd.formatting.Font
	- xlrd.formatting.XFBorder
	- xlrd.formatting.Format xlrd.
	- ormatting.XFProtection
	- xlrd.formatting.XF

#### 大型 Excel 文件

- `open_workbook()` 的 `on_demand` 参数为 `True` 时, 只在 worksheet 被请求时, 才将它们加载入内存
- `xlrd.book.Book` 对象的 `unload_sheet` 方法释放 worksheet, 可用索引或 sheet name
