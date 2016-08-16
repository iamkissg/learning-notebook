# IPython Notebook: Interactive Computing

IPython notebook是基于网络的交互式计算系统, 允许用户在文档中插入实时代码, 叙述性的文字, LaTeX公式, 图片和视频等. 这些文档包含了计算与结果的完整记录.


## IPython Notebook简介

- IPython Notebook文档可包含以下内容:
 - 实时代码
 - 交互式小部件
 - 图表
 - 描述性文本
 - 公式
 - 图片
 - 视频
- IPython Notebook包含以下3部分组件:
 - web application: 用于写作与交互式运行代码的网页应用
 - kernels: 由web application启动的分离式进程, 运行用户代码并向web application返回运行结果. 同时能处理交互式小部件的计算, tab的补全和自检
 - notenbook documents: 自包含的文档, 包含了所有能web application上可见的内容. 每个notebook document都有其自身相应的kernel

## Notebook基础

- `ipython notebook` - 启动notebook服务器. 默认URL是127.0.0.1:8888, 可通过指定`--port`参数更改端口号. 默认自动开启浏览器, 通过`--no-browser`参数设置不自动启动浏览器. `--help`查看帮助:)
- 启动notebook服务器之后, 浏览器将打开notebook dashboard, 此处会显示当前目录下的所有文件, 包括notebooks
- 点击页面上方的"New", 选择kernel, 并创建一个新的notebook
- 当列表中某项notebook图标显示为绿色, 并带有"Running"字样, 表示该notebook正在运行. 除非显式地选择关闭, 否则将一直保持运行状态, 单单关闭网页是不行的
- 点击页面最上方的"Running"可查看正在运行的notebook
- notebook有2种模式: 编辑模式与命令模式.
 - 编辑模式: 绿色边框, 在编辑器区域有命令提示符, 敲击"Enter"或鼠标点击进入编辑模式
 - 命令模式: 灰色边框, 可将notebook当作一个整体进行编辑, 但不会在任何独立的单元进行输入. 有一系列快捷键可供使用: 比如快捷键`c`用于复制当前单元. 与Vim类似, 通过`Esc`键或鼠标点击单元区域之外的区域返回命令模式
 - 常用的命令模式快捷键:
  1. 导航: enter, shift-enter, up/k, down/j
  2. 保存notebook: s
  3. 单元输入: y, m, 1-6, t
  4. 创建单元: a, b
  5. 编辑单元: x, c, v, d, z, shift+=
  6. kernels操作: i, .

## 运行代码

- 两个快捷键:
 1. `Alt-Enter` - 运行当前单元的代码, 并在其后插入一个新单元
 2. `Ctrl-Enter` - 运行当前单元的代码, 并返回命令模式
- 代码是在被称为IPython Kernel的分离进程中运行的, 该进程可被中断或重启
- 当kernel出错挂掉时, 会提示重启
- 标准输出(stdout)和标准错误(stderr)将以文本的形式在输出区域显示
- 所有的输出都以异步的方式显示, 事实上, 在kernel内部就是异步产生的.
- 输出区域是可折叠的(鼠标单击打开折叠的输出区域, 双击折叠), 当输出太巨大时, 输出会自动卷屏

## Markdown单元

- 好吧, Markdown的语法请自学.
- IPython notebook服务器同时是通用文件服务器. 对于notebooks目录以外的访问是不被授权的, 正因此, 用户不应该在文件系统的高级目录下运行notebooks服务器(比如家目录).
- 当以密保形式运行notebook时, 本地文件的访问需要严格验证用户信息, 除非只是查看只读文件

## 配置notebook和服务器

### 配置notebook

- notebook web server的配置在`ipython_notebook_config.py`文件中进行设置, 文件位于IPython配置文件目录(profile directory)下. 而配置文件目录是用户的IPython目录的一个子目录, 通常在家目录下, 名为`.ipython`
- `!ipython profile locate default`命令查看默认的配置文件目录
- 可自定义配置文件`!ipython profile create my_profile`, 通过命令行选项`--profile=custom_profile`会覆盖默认的配置文件
- IPython Notebook允许执行任意代码. 因此, notebook web server不应该在没有安全保证的前提下, 在开放网络上运行.
- 通过以下2步可提升notebook服务器的安全性:
 1. 设置密码
 2. 使用SSL加密网络

```python
from IPython.lib import passwd
password = passwd("your_secret")
password
```

- 可用上述代码生成密码的hash值, 再将该哈希值添加到ipython\_notebook\_config.py
- 使用SSL, 就不需要再向web server传递密码. 当在公共网络上运行notebook时, SSL绝对是必须的:
 1. 生成SSL证书. 在大多数情况下, 可在配置文件目录下生成SSL证书及密钥, 如此, 对于使用生成的密钥和证书更方便
 2. 生成密钥和证书之后, 将它们加入到 ipython\_notebook\_config.py(当启用SSL后, 需要以https访问notebook服务器)
- `ipython notebook --ip=* --no-browser` - 为所有ip对notebook服务器的访问都步自动打开浏览器. 也可以在ipython\_notebook\_config.py文件中进行配置

```python
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False

c.NotebookApp.base_url = '/ipython/'
c.NotebookApp.webapp_settings = {'static_url_prefix':'/ipython/static/'}
```

- 通过上述后2条配置, 还可以更改notebook服务器运行时的url前缀
- 默认地, notebook服务器将notebook文档保存到它的工作目录下

## 自定义快捷键

- ipython的快捷键可通过使用IPython JavaScipt API自定义. 以下是例子:

```JavaScript
%%javascript

IPython.keyboard_manager.command_shortcuts.add_shortcut('r', {
    help : 'run cell',
    help_index : 'zz',
    handler : function (event) {
        IPython.notebook.execute_cell();
        return false;
    }}
);
```

- 要点:
 - `help_index`字段用于为快捷键分类, 分类的快捷键将以不同的对话框弹出. 默认是zz
 - 当事件需要暂停, 默认行为不能正常执行时, handler返回false作为提示
 - 若不需要help或help\_index字段, 可以简单地向add\_shortcut传递一个函数作为第二个参数
- 通过remove\_shortcut删除快捷键
- 若想要快捷键在所有notebooks中都有效, 将API的调用加入到<yourprofile>/static/custom/custom.js文件中

## JavaScript 扩展

- Coming soon...

## 利用NbConvert转换notebook

- NbConvert既然一个库, 又是一个允许你将notebook转换成其他格式的命令行工具. 转换的格式包括: html, latex, markdown, python, rst, slides. NbConvert依赖于Jinja2模板引擎, 因此实现新的格式或修改已有的, 不难.
- 通过`ipython nbconvert <options and arguments>`调用nbconvert. `--help`查看帮助, `--help-all`查看更细节的信息
- 在转换之前, 确认所有转换的类型. 不显式地声明请求, nvconvert将不能正确地执行代码单元, 默认的目标格式是html
- `--to=xxx`指定目标格式. latex转换的结果是latex, 而不是pdf. 若要创建pdf文件, 需要第三个包来编译latex, `--post=pdf`
- 自定义模板继承自python模板, 并会覆盖markdown块

```
%%writefile simplepython.tpl
{% extends 'python.tpl'%}

{% block markdowncell -%}
{% endblock markdowncell %}

## we also want to get rig of header cell
{% block headingcell -%}
{% endblock headingcell %}

## and let's change the appearance of input prompt
{% block in_prompt %}
# This was input cell with prompt number : {{ cell.prompt_number if cell.prompt_number else ' ' }}
{%- endblock in_prompt %}
```

- notebook文件格式支持将任意JSON元数据附到单元上
- IPython nbconvert可通过使用默认的配置文件进行配置, 或通过`--profile`指定配置文件. 若`config.py`文件存在于当前工作目录, nbconvert以其作为默认的配置文件

## 使用nbconvert作为库

- Coming soon...

