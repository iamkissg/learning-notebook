# Benchmark of Python Excel (Reading) Libraries

## Libraries:

有许多流行的 Python 第三库提供了对 Excel 的支持, [Anaconda](https://docs.continuum.io/anaconda/excel) 提供了一个相对详尽的列表, 有一下这些库:

- [openpyxl](https://openpyxl.readthedocs.org/en/latest/)
- [xlrd](https://github.com/python-excel/xlrd)
- [xlsxwriter](https://xlsxwriter.readthedocs.io/)
- [xlwt](https://secure.simplistix.co.uk/svn/xlwt/trunk/xlwt/doc/xlwt.html?p=4966)
- [pandas](http://pandas.pydata.org/)
- [xlwings](https://www.xlwings.org/)
- [DataNitro](https://datanitro.com/)
- [ExcelPython](https://github.com/ericremoreynolds/excelpython)
- [XLLoop](http://xlloop.sourceforge.net/)
- [ExPy](http://www.bnikolic.co.uk/expy/expy.html)
- [PyXLL](https://www.pyxll.com/)

其中, `openpyxl`, `xlrd`, `xlsxwriter`, `xlwt` 等提供了将数据从 Python 对象导出到 Excel 或将 Excel 的电子表导入 Python 的功能; 而`xlwings`, `DataNitro`, `ExcelPython`, `XLLoop`, `ExPy`, `PyXLL` 等则是不同的 Python-Excel Tool, 提供了自动化/交互计算的方法, 此时 Python 更多的像 VBA 的替代品.

根据我们的业务要求 (将 Excel 的内容读到 Python 对象), 可用的库主要有:

- [xlrd](https://github.com/python-excel/xlrd)
- [openpyxl](https://openpyxl.readthedocs.io/en/default/)
- [pandas](http://pandas.pydata.org/)

`pandas` 实际使用 `xlrd` 来读取 Excel 文件到 `DataFrame`, 因此, 仅对 `xlrd` 和 `openpyxl` 进行比较.

## 测试环境

操作系统: Ubuntu 14.04

Python 版本: 2.7.6

## xlrd 与 openpyxl 介绍

#### xlrd

> xlrd is a library for reading data and formatting information from Excel files, whether they are .xls or .xlsx files.

- `xlrd` 的开发是基于 `OpenOffice.org` 提供的 MS Excel 文档(OOo Doc), 局部有修改. 尽可能地支持 Excel 的所有特性.

- `xlrd` 是纯 Python 实现的, 仅对 Python 标准库有依赖, 全平台可用 (Linux, macOS, Windows), 兼容 `.xls` 和 `.xlsx`, 并同时支持 Python 2.6+ 与 Python 3.3+.

`.xlsx` 底层是 XML 实现的, 但是 XML 有[漏洞](https://docs.python.org/2/library/xml.html#xml-vulnerabilities). `xlrd` 按下述优先级导入 XML:

1. [xml.etree.cElementTree](https://docs.python.org/2/library/xml.etree.elementtree.html)
2. [cElementTree](http://effbot.org/zone/celementtree.htm)
3. [lxml.etree](http://lxml.de/api/lxml.etree-module.html)
4. [xml.etree.ElementTree](https://docs.python.org/2/library/xml.etree.elementtree.html)
5. [elementtree.ElementTree](http://effbot.org/zone/element-index.htm)

为避免 XML 的漏洞, 应使用 [defaultxml] 来保证安全:

```python
import defusedxml
from defusedxml.common import EntitiesForbidden
from xlrd import open_workbook
defusedxml.defuse_stdlib()


def secure_open_workbook(**kwargs):
    try:
        return open_workbook(**kwargs)
    except EntitiesForbidden:
        raise ValueError('Please use a xlsx file without XEE')
```

#### openpyxl

> Openpyxl is a Python library for reading and writing Excel 2010 xlsx/xlsm/xltx/xltm files.

`openpyxl` 也是纯 Python 实现的, 同时支持 Python 2.6+ 和 Python 3.3+. 如定义所示, 仅提供对 `.xlsx` 的支持.

`openpyxl` 利用了第三方库, 以提供了相比于 `xlrd` 更丰富的功能. 利用 `lxml` 来解析 XML; 提供了对 Chart 的支持; 支持 NumPy 和 Pandas 等...

`openpyxl` 本身由 [PHPExcel](https://phpexcel.codeplex.com/) 移植而来, 其根据的标准是 [OpenXML](https://zh.wikipedia.org/wiki/Office_Open_XML).

PS: [Comparison of Office OpenXML and OpenDocument]

#### 小结

| Library | 支持的 Excel 版本 | 行业标准 | 是否依赖第三方库 | 功能性 | 其他 |
| ------------- | :-------------: | :-------------: | :-------------: | :-------------: | :-------------: |
| xlrd          | .xls, .xlsx (Excel 97 以上所有版本) | OpenDocument | 否 | 只读 | 按可访问的优先级加载 XML |
| openpyxl      | .xlsx (Excel 2007 及以上的版本) | Office OpenXML | 是 | 可读写, 其他功能丰富 | 使用 lxml 加载 XML |

## 性能比较

#### 加载文件的速度

####
