# 如何编写 __init__.py

(Learn from Mike Grouchy's Blog: [Be Pythonic: __init__.py](http://mikegrouchy.com/blog/2012/05/be-pythonic-__init__py.html))

- __init__.py 文件的主要作用是初始化 Python 包. The primary use of __init__.py is to initialize Python packages.
- 在目录下包含 __init__.py 文件, 就是告诉 Python 解释器, 该目录应该被当作一个 Python 包. The inclusion of the __init__.py file in a directory indicates to the Python interpreter that the directory should be treated like a Python package.
- __init__.py 可以是空文件
- __init__.py 的一个用途是, 将类或函数等导入到包的层次, 从而这些类或函数可以被方便地从包中导入. One common thing to do in __init__.py is to import selected Classes, functions, etc into the package level so they can be convieniently imported from the package.
- __init__ 的另一个用途是, 利用 `__all__` 变量, 使子包或模块在包的层次可访问. Another thing to do is at the package level make subpackages/modules available with the __all__ variable.
- 当在 __init__.py 中使用 `from package import *` 时, 解释器会导入所有 `__all__` 变量所列的模块
- `__all__` 是一个所有你希望用 `import *` 导入的模块的列表
