# 2017 Daily Learning Records

## 2017-01-03

- Scala, 获取当前目录: `def getCurrentDirectory = new java.io.File(".").getCanonicalPath`
- Scala, Http Client, 上传文件到服务器, 用 `Scalaj`: `Http(url).postMulti(MultiPart("photo", "headshot.png", "image/png", fileBytes)).asString`
- Scala, 获取网页内容:

```scala
// save as String
val s = scala.io.Source.fromURL("http://google.com").mkString

// or save as file
import sys.process._
import java.net.URL
import java.io.File
new URL("http://google.com") #> new File("Output.html") !!
```

- Scala, 以二进制形式读取文件:

```scala
import java.nio.file.{Files, Paths}
val byteArray = Files.readAllBytes(Paths.get("/path/to/file"))
```

- Scala, JSON 转 Map:

```scala
import org.json4s._
import org.json4s.jackson.JsonMethods._

def jsonStrToMap(jsonStr: String): Map[String, Any] = {
  implicit val formats = org.json4s.DefaultFormats  // 必须的

  parse(jsonStr).extract[Map[String, Any]]
}
```

- Scala, 从 URI 中解析出文件名, 最简单有效的方法 (org.apache.commons.io.FilenameUtils 也是这样做的)

```scala
val fileName = uri.drop(uri.lastIndexOf("/") + 1)
```

## 2017-01-04

- MySQL, 查看表结构: `desc tableName;`

## 2017-01-11

- Scala, `List.mkString(",")` 将 List 的元素拼接成 String, 以指定符号分隔
- Scala, 迭代 Map:
    - for ((k,v) <- m1) do something
    - m1 foreach (x => println (x.\_1 + "-->" + x.\_2))
    - m1 foreach {case (key, value) => println (key + "-->" + value)}

## 2017-01-12

- Scala, `implicit`:
    - Scala 使用隐式类型变换和隐式参数来解决自定义库和类扩展的问题
    - 标记规则: implicit 可以标记 class, method, parameter, obj
    - 范围规则: implicit 用来标记一个隐式定义, 编译器将选择其作为隐式转换的候选项, 并且编译器只会选取当前作用域的定义. 一个例外是编译器会在类的伴生对象定义中查找所需的 implicit 定义
    - 一次规则: 编译器在需要使用 implicit 定义时, 只会试图转换一次
    - 优化规则: 编译器不会在不必要隐式转换的情况下调用 implicit 规则
    - implicit 的名称只在两种情况下有用:
        1. 想在一个方法中明确指明
        2. 想引入到当前作用域
    - 编译器使用 implicit 的几种情况:
        1. 转换成预期的数据类型: 类型不匹配时, 检查当前作用域是否有到预期数据类型的隐式转换
        2. 转换到 selection 的 receiver, 允许某些方法调用
        3. 隐含参数, 有点类似缺省参数, 调用方法时没有提供参数, 编译器将检查当前作用域是否有符合条件的 implicit 对象作为参数传入

### 教训

1. `工厂模式`: 工厂只负责生产, 其他一概不必处理: 不处理业务, 不处理异常...
    - PS: 底层代码与上层业务的分离, 可复用性才高. 代码更健壮
2. 工具包, 绝不应该带业务的东西.
3. 还需要考虑到封包的问题
4. 异常的问题, 找到 Java 的 Error vs. Exception:
    java.lang.Error: An Error is a subclass of Throwable that indicates serious problems that a reasonable application should not try to catch. Most such errors are abnormal conditions.
    java.lang.Exception: The class Exception and its subclasses are a form of Throwable that indicates conditions that a reasonable application might want to catch.
5. 导入需谨慎, 小心命名空间问题
6. 对象在传递时, 比如 JSON, 不要对对象本身进行修改, 不要转换, 保持其一致性, 这样其实任何时候都可以做修改, 或者转换, 或者存储.
7. 对象像 HTTP 请求, 有同步和异步需求的, 可分别实现同步和异步的功能, 两个实现同一套接口, 使用时通过导入包做区分

## 2017-01-13

- Scala, List of Tuple flat:
    1. list map (l => l.\_1, l.\_2)
    2. list flatMap (l => List(t.\_1, t.\_2))
    3. list flatten (case (a, b) => List(a, b))
- Scala, Map -> JSON (with json4s): `org.json4s.jackson.Serialization.write(m)`
- Scala, Map's add, update or delete:
    - add/update: Map + ("Echo" -> "Engine")
    - delete: Map - ("Engine" -> "Shadow")

## 2017-01-21

- Scala, 列表生成式 `yield` 前后都是可以用 if 语句的:

```scala
val example = for(i <- List(1, 2, 3, 4, 5, 6, 7, 8, 9) if (i % 2 == 0)) yield if (i == 2) "It's 2!" else i
```

- Scala, 向上和向下取整: `math.floor(number)`, `math.ceil(number)`
- Scala, 集合的基本使用. 交并差: `&`, `|`, `--`. 添加/删除元素: `+`, `-`, 设计到多个元素时, 用元组来封装.
- Scala 的非 Set 类型的序列, `distinct` 可以用于去重, 并保持去重后类型不变
- Scala, 可以借助元组实现多值赋值: `- Scala, 可以借助元组实现多值赋值:

```scala
scala> val (a, b, c) = (1, 2, 3)
a: Int = 1
b: Int = 2
c: Int = 3
```

- Scala, 序列拆分:
    - `partition`: 将序列按是否满足某条件分成两部分
    - `span`: 按先后顺序对序列的元素进行验证, 满足条件的最长的子序列为一个序列, 从第一个不满足条件的元素开始都为一个序列, 即使后续元素仍旧满足条件.

```scala
scala> List(1,2,3,4).partition(x => x % 2 == 0)
res0: (List[Int], List[Int]) = (List(2, 4),List(1, 3))
scala> Seq(1,2,3,4).span(x => x % 2 == 0)
res0: (Seq[Int], Seq[Int]) = (List(),List(1, 2, 3, 4))
```
- Scala, 生成随机数/字符串
    - 随机整数: `scala.util.Random.nextInt` or `scala.util.Random.nextInt(maximum value)`
    - 随机 0.0 到 1.0 的浮点数: `scala.util.Random.nextDouble`
    - 设置随机种子: `scala.util.Random.setSeed(balabala)`
    - 随机可打印的字符: `scala.util.Random.nextPrintableChar`
    - 随机字符串: `scala.util.Random.alphanumeric.take(10).mkString`
    - [更多例子](http://alvinalexander.com/scala/creating-random-strings-in-scala)
- Scala, 一个奇怪的方法, 不清楚用在什么地方: `tuple.productIterator.toList`
- Scala, 异常处理小技巧: if 的一个分支计算值, 另一个抛出异常. 整个 if 表达式的类型就是实际计算值的分支的类型.
- Scala, try-catch-finally 语句, 最好避免从 finally 子句中返回值, 而将 finally 当作确保某些副作用, 如关闭打开的文件, 数据库连接等
- 可用于密码的非字母数字符号: ` !"#$%&'()\*+,-./:;<=>?@[\\]^\_\`{|}~`
- Python, 生成随机字符串: `''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))`
- Java, 组装路径: `Path path = Paths.get("foo", "bar", "baz.txt")` (import java.nio.file.{Path, Paths})
- Scala, Seq 被转成 String 后,没有简单地办法可以将 String 逆转回 Seq. 在 toString 过程中丢失了一部分信息. 只能手动解析反转

## 2017-01-24

- Python, 四舍五入有问题. 五是舍去的.

```python
In [1]: round(2.675, 2)
Out[1]: 2.67
```

## 2017-02-10

- Unix OS （Windows 不知），文件名不能代表文件的，inode 才是！
- Google, `isbn:图书编号` 搜书

## 2017-02-13

- Python, 查看未使用的端口

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 0))
addr = s.getsockname()
print addr[1]
s.close()
```

## 2017-02-15

- Flask, abort` 第二个默认参数，用于指定返回的错误信息
- Flask，`request.get_json` - 获得请求的主体，并转成 JSON 格式
- Flask, `Flask-RESTful` 嵌套验证，参考[这个](http://stackoverflow.com/questions/19234737/nested-validation-with-the-flask-restful-requestparser/27091966#27091966)
- Flask，`request.query_string` - 返回 URL 中的查询字符串
- Flask，`request.url` - 返回 URL 中的 URL，不含查询字符串
- Flask，`request.args.get("params")` - 获得查询字符串的单个参数值。`request.args` 是查询字符串参数的字典

## 2017-02-22

- Python, 删除字典的元素

```python
def removekey(d, key):
    r = dict(d)  # make a shallow copy
    del r[key]
    return r
```

- Python, 移除值为空的字典元素


```python
{k: v for k, v in d.items() if v is not None}  # 若使用条件 `if v`，会去除 0 或 ""，False 等
```

- Python, 一个好像挺好用的库：`boltons`

## 2017-02-23

- Python, 从 URL 中提取文件名，简单点还是：`url.split("/")[-1]`
    - 或者 `os.path.basename(urlparse.urlsplit("https://visualhunt.com/photos/xl/8/camera-journal-travel.jpg").path)`
- Python, 简单逻辑的 Switch 语句代替方法：

```python
var = {
    1: string.letters,
    2: string.digits,
    3: string.letters + string.digits,
    4: string.punctuation,
    5: string.letters + string.punctuation,
    6: string.letters + string.digits + string.punctuation,
}.get(key, default_value)
```

- Python, 下载的最简单方式：

```import urllib

urllib.urlretrieve(url, file)
```

- Python, SQLAlchemy 更新数据库记录：

```python
obj.attr = new attribute
db.session.commit()
```

- Python, SQLAlchemy 检查是否有查询到值：

```python
Model.query.filter_by(expression).first()
```

## 2017-02-24

- Python, 在 `with` 语句中执行 `return`，相当于最后有一个 `finally` 子句
- Python，Pillon, 直接从数据流中打开文件：`img = Image.open(io.BytesIO(content))`
- Python, 获得文件大小，`os.stat(somefile).st_size`, 返回字节数

## 2017-02-27

- PostMan, 使用 `PostMan` 上传文件时，不要设置 `Content-Type`。`PostMan` 会自动根据上传的文件设置头部
- Flask, `request.stream` 读取二进制流数据；`request.files` 是客户端上传的文件的字典，`key` 为文件名，`value` 为文件

## 2017-03-06

- Fcitx, `fcitx-diagnose` - 查看哪里 fcitx 输入法配置哪里出问题了

## 2017-03-07

- Python, concatenate dicts: `d1.update(d0)`. [More](http://stackoverflow.com/questions/1781571/how-to-concatenate-two-dictionaries-to-create-a-new-one-in-python/1784128#1784128)
- Flask, `current_app` -> 类 `werkzeug.local.LocalProxy` 的实例, 是程序上下文; `current_app._get_current_object()` 返回的才是类 `flask.app.Flask` 的实例, 即应用程序本身.

## 2017-03-08

- Linux, `chown [OPTION]... [OWNER][:[GROUP]] FILE`, `-R` - recursive

## 2017-03-09

- Proxychains-ng - ng is short for new generation

## 2017-03-13

- Vim, `source .vimrc` 是 Vim 的指令, 应该在 Vim 内执行, 而不是 Shell

## 2017-03-14

- `_arguments:450: _vim_files: function definition file not found`, 自动补全的问题. `rm ~/.zcompdump*`.  

## 2017-03-20

- Python, 权重随机: `numpy.random.choice()`, 参数 `p` 用于设置权值.

## 2017-03-21

- 文件去重, 核对 `MD5` 值 (其他如 `sha1` 都可以咯)

## 2017-03-22

- Python, `os.path.expanduser("~")` - 获得当前用户的家目录
- Python, 当前目录的父目录
    1. `dirname(dirname())`
    2. `os.path.join()` 中用一个 `../`
- Python, 当前脚本的绝对路径 - `os.path.abspath(__file__)`
- Python, 当前工作目录 - `os.getcwd()`
- Python, flat list - `[item for sublist in l for item in sublist]`
    - 如上所示, 嵌套的列表推导式使用是: `[somgthing for 外 for 内]`
- Python, `glob` 忽略大小写 - `glob.iglob('*.[xX][lL][sS]')` (方括号)
- Python, `glob.glob` 和 `glob.iglob`, 后者返回一个迭代器
- Python, `from __future__ import divisioo` - 使 `/` 成为浮点除法
- Matplotlib, 在 `Jupyter notebook` 中使用 `plt.rcParams['figure.figsize'] = (12, 9)` 放大图表
- Matplotlib, `plt.rcParams['font.sans-serif'] = ['SimHei']` 指定默认字体, 以解决中文显示问题
- Matplotlib, 画图函数的 `color` 设置颜色, 可以是 `skyblue`, 还可以是一个颜色列表; 或者 `set_color()`
- Matplotlib, `plt.grid()` - 显示网格. 参数 `axis` 可以设置 `x`, `y`, 或 `both`
- Matplotlib, 坐标轴不连续, `plt.set_xlim()`

## 2017-03-23

- use `jack server` instead of default

```shell
pulseaudio --kill
jack_control start
jack_control exit
pulseaudio --start
```

- Shell, `sudo usermod -a -G groupName userName` - add user to existing group. `the user will need to logout and log back in.`
- how to use fluidsynth - `fluidsynth -a audio-driver /usr/share/sounds/sf2/FluidR3_GM.sf2 midi_file`

## 2017-03-24

- Python, `OrderedDict` - 会删重复 `key`

## 2017-03-27

- Python, convert list of tuples to multiple lists: `zip(*[(1, 2), (3, 4), (5, 6)])`, or `map(list, zip(*[(1, 2), (3, 4), (5, 6)]))`
- Matplotlib, Plot bar graph using a dict:

```python
import matplotlib.pyplot as plt

D = {u'Label1':26, u'Label2': 17, u'Label3':30}

plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), D.keys())  # use xticks

plt.show()
```

- Python, 浮点数与分数的相互转换 -`fractions`

```python
>>> str(Fration(0.25))
"1/4"
```

- Python, sort by multiple attributes, `key` 可以是一个返回 tuple 的函数: `s = sorted(s, key = lambda x: (x[1], x[2]))` or `s = sorted(s, key = operator.itemgetter(1, 2))`
- Python, check if a float value is a whole number: `float.is_integer()`
- Python, about `zip`. In **Python 2**, `zip` returns a `list` of tuples. `itertools.izip` return iterator instead of list, `itertools.izip_longest` 顾名思义. In **Python 3**, `zip` return a iterator.
- Python, determine if an obj is iterable: `isinstance(obj, collections.Iterable)`

```python
# General pythonic approach to determine if an obj is iterable

# Pythonic programming style that determines an object's type by inspection
# of its method or attribute signature rather than by explicit relationship
# to some type object ("If it looks like a duck and quacks like a duck,
# it must be a duck.") By emphasizing interfaces rather than specific types,
# well-designed code improves its flexibility by allowing polymorphic substitution.
# Duck-typing avoids tests using type() or isinstance(). Instead, it typically employs
# the EAFP (Easier to Ask Forgiveness than Permission) style of programming.

try:
   _ = (e for e in my_object)
except TypeError:
   print my_object, 'is not iterable'
```

- Python, check list monotonicity (单调性)

```python
# Pythonic approach
def strictly_increasing(L):
    return all(x<y for x, y in zip(L, L[1:]))

def strictly_decreasing(L):
    return all(x>y for x, y in zip(L, L[1:]))

def non_increasing(L):
    return all(x>=y for x, y in zip(L, L[1:]))

def non_decreasing(L):
    return all(x<=y for x, y in zip(L, L[1:]))
```

- Python, `collections.Sequence` - key attribute: `__new__`, `__init__`, `__getitem__`, `__len__`; Python, `collections.Set` - key attribute: `__contains__`, `__iter__`, `__len__`. So 序列和集合有不同!

## 2017-03-28

- 生成字体索引信息 - `sudo mkfontscale && sudo mkfontdir`; 更新字体缓存 - `sudo fc-cache`
- Ubunt, 字体文件保存在 `/usr/share/fonts` 下

## 2017-03-29

- Python, `import` with `try except`

> Importing a module that does not exist will raise an `ImportError` exception. You can use this to define multiple levels of functionality based on which modules are available at run-time, or to support multiple platforms

- Linux, `/etc/fstab` 包含了静态文件系统信息，定义了存储设备和分区整合到整个系统的方式。`mount` 命令会读取这个文件，确定设备和分区的挂载选项
- Linux, `stat any_file` - information of file, including block sizemount
- Python, `del lst[:]` - empty list.
- Python, `lst[:] = []` does not empty the list, just creates a new object and binds it to the variable
- Python, `dict.update` 会覆盖同名键值对
- Linux, `df - report file system disk space usage`
- Python, pythonic merge two dicts (user will cover default):

```python
# 1.
context = {**default, **user}  # Python 3.5 以上可用

# 2.
context = default.copy()
context.update(user)
```

- Python, 写程序时，用户自定义配置可以覆盖默认配置，如上所示。又如 `awesome-python3-app` 的配置

## 2017-03-30

- Linux, `setxkbmap -layout us -option ctrl:nocaps`
