# Click 学习笔记

## 基础概念

- click 是基于通过装饰器的声明命令
- Internally, there is a non-decorator interface for advanced use cases, but it’s discouraged for high-level usage.
- 通过 `click.command()` 将一个函数装饰成命令行工具
- `click.echo()` 是为了鲁棒性，同时支持 Python 2 和 3。`echo()` 会自动做一些矫正
- `click.group()` 装饰器创建了一个 `Group()` 对象，其下可以有多个子命令
- ` click.option()`, `click.argument()` 用于添加参数
- click 应用的好搭档：`setuptools`

## setuptools 集成

- 写命令行小工具时，建议写成模块的形式，并辅以 setuptools。理由：
    1. 传统方式的一个问题是：Python 解释器加载的第一个模块命名有问题，不是其本身的名字，而是 `__main__`
    2. Unix-like 系统易执行，但 Windows 并不。事实上，在虚拟环境运行脚本对于 Unix-like 系统也是一个问题。传统的方式，需要激活整个虚拟环境，然后才能以正确的 Python 解释器执行脚本
- 将脚本与 setuptools 绑定，只需要将脚本和 `setup.py` 放在一个 Python 包中，

```python
from setuptools import setup

setup(
    name='yourscript',
    version='0.1',
    py_modules=['yourscript'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        yourscript=yourscript:cli
    ''',
)
```

- `entry_points` - `console_scripts` 以下的每一行标识一个控制台脚本，左边是脚本名；右边是 click 命令
- 随着脚本的增多，假设目录结构如下所示：

```txt
yourpackage/
    __init__.py
    main.py
    utils.py
    scripts/
        __init__.py
        yourscript.py
```

- 此时，在 `setup.py` 中使用 `packages=find_packages()` 自动查找包：

```python
from setuptools import setup, find_packages

setup(
    name='yourpackage',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        yourscript=yourpackage.scripts.yourscript:cli
    ''',
)
```

## 参数

- click 支持两种形式的参数：options 和 arguments。
- 如名称所示，`option` 是可选的，`argument` 有些时候可以是可选的，但对于什么情况下是可选的，有更严格的要求。
- 建议，只在子命令或输入文件名/ URLs 时使用 `argument`，其他情况下都使用 `option`

#### argument vs. option

- arguments 能做的事情更少。以下是 `option` 才有的功能：
    - 对于缺失输入自动提示
    - 作为标志
    - 选项值可以来自环境变量
    - 选项有完整的帮助信息
- 不同于 option，arguments 可接受任意数量的参数值；option 只能接受固定的参数值 (默认是 1）

#### 参数类型

- str / click.STRING
- int / click.INT
- float / click.FLOAT
- bool / click.BOOL
- click.UUID
- class click.File(mode='r', encoding=None, errors='strict', lazy=None, atomic=False) - 声明参数是一个用于读写的文件。命令执行完毕之后，文件将自动关闭
- class click.Path(exists=False, file_okay=True, dir_okay=True, writable=False, readable=True, resolve_path=False) - 与 `click.File` 不同，仅返回文件名。并可以做不同的审查
- class click.Choice(choices) - ?
- class click.IntRange(min=None, max=None, clamp=False) - 类似于 click.INT，但限制了值的范围
- click.ParamType - 自定义参数类型

#### 参数名

- 参数接收位置参数，缩写或全程
- 若参数名不使用连字符 `-`，将作为内部参数名，同时也作为变量名
- 带连字符的参数名，全称将被使用，并将连字符转为下划线。`("-f", "--foo-bar")`, 参数名是 `foo_bar`, `("-x")` 参数名是 `x`， `("-f", "--foo-bar", "dest")`, 参数名是 `dest`

## Options

- Options in click are distinct from positional arguments.
- 

