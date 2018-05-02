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

## 2017-04-03

- Python, 文件移动：`os.rename()` 或 `shutil.move`. 我用过 `shutil.move` 就是 shell 下 `mv` 的封装吧

## 2017-04-18

- Python, `webbrower` - Unix 下可使用多种默认查看器打开多种类型文件，包括：PDF，png，txt等

## 2017-04-24

- Pandas, 移除包含某关键字的行：`df[~df["column"].isin(list of key words)]`
- Python, 多个连续空格的替换：`re.sub(' +', ' ', string)`
- Pandas，遍历所有的单元：

```python
for column_name, column in df.items():
    for k, v in column.items():
       # do something
```

## 2017-04-25

> 在处理数据之前, 很关键的一点是, 空缺值的处理. 一定要先处理了空缺值, 再进行后续的处理!

## 2017-04-26

- Python2, `d[key]` 比`d.get(key)` 高效一倍
- Python2, 列表推导式比 `map(func, seq)` 高效一倍

## 2017-05-05

- Python 2.x, `map(None, seq1, seq2, seq3, ...)` 能实现 `itertools.iziplongest(seq1, seq2, seq3, ..., fillvalue=None)`
- Python, 排列: `itertools.permutations`, 组合: `itertools.combinations`
- Pandas, `df.head(n)` 前 n 个; `df.nlargest(n)` 值最大的 n 个, 降序排序, `series.argmax()` 返回最大值的索引

## 2017-05-15

- Scala, [提前初始化](http://stackoverflow.com/a/4716273/5337323):

```scala
abstract class X {
    val name: String
    val size = name.size

}

// 提前初始化, 将先给变量 name 赋值, 后执行父类的类体, 为 size 赋值
class Y extends {
    val name = "class Y"

} with X

// 此时, 将优先执行父类 X 的类体, 但是由于变量 name 不存在, 为 size 赋值将出错
class Z extends X {
    val name = "class Z"
}
```

- Scala, Symbol 类型
    - 该类型的对象是被拘禁的(interned), 任意的同名symbols都指向同一个Symbol对象，避免了因冗余而造成的内存开销
    - symbols对象之间可以使用操作符`==`快速地进行相等性比较，常数时间内便可以完成，而字符串的equals方法需要逐个字符比较两个字符串，执行时间取决于两个字符串的长度，速度很慢
- Scala, 多重赋值: `val (myVar1, myVar2) = Pair(40, "Foo")`
- Scala, 方法的参数是不可变的
- Scala, `继承`将继承父类所有非私有的成员 (只有主构造器的能够向父类构造器传递参数)
- Scala, 主构造器: `从类定义开始, 横跨整个类体的非字段和方法, 都是主构造器` (辅助构造器通过关键字 `this` 定义)
- Scala, 隐式类 - 只能在别的 trait / class / object 内定义; 构造函数只能有一个非隐式参数; 在同一作用域内, 不能有任何方法, 成员或对象与隐式类同名
- Scala, 访问修饰符
    - 私有成员: 只在类或包含成员定义的对象中可见, 即使是该类的外部类也无法访问;
    - 保护成员: 只在成员定义的类的子类中可访问, 即使在相同的包中, 也无法访问;
    - 公有对象: 默认, 可无限制访问
    - 访问修饰符可通过限定符进行扩充;

```scala
package society {
    package professional {
        class Executive {
            private[professional] var workDetails = null
            private[society] var friends = null
            private[this] var secrets = null
            // workDetails 可被封闭包 professional 内的任意类访问
            // friends 可被封闭包 society 内的任意类访问
            // screts 只能被实例方法内的隐式对象访问

            def help(another : Executive) {
                println(another.workDetails)
                println(another.secrets) //ERROR
            }
        }
    }
}
```

- Scala, 函数名可包含如 `+`, `++` 等字符.
- Scala, 没有方法体的方法被隐式转化为*抽象*的
- Scala, `传名`调用函数(与之相对的是, `传值调用`), `name: => type`, 不计算参数表达式而直接应用到函数内部. 优点在于, 对于不用计算参数表达式的情况, 效率更高; 但也可能重复计算值, 效率更低了:

```scala
def useOrNotUse(x: Int, y: => Int) = {
    flag match{
        case true => x
        case false => x + y
    }
}
```

- Scala, 允许用户指明函数的最后一个参数可能是可重复的 (repeated), 即在参数类型后追加 `*`:

```scala
def printStrings( args:String*  ) = {
    var i : Int = 0;
    for( arg <- args  ){
        println("Arg value[" + i + "] = " + arg );
        i = i + 1;
    }
}

printStrings("Hello", "Scala", "Python");
```

- Scala, 函数支持默认参数

## 20170516

- Scala, 函数调用的说法更近于数学的说法: `将函数应用于参数`, 如果缺少参数, 函数将偏应用于当前参数, 得到一个新的函数.
- Scala, 函数参数默认按顺序赋值, 使用命名参数, 可以以任意顺序传递参数.
- Scala, 递归对于纯函数式编程相当重要
- Scala, 匿名函数: `(参数) => 函数体`
- Scala, 柯里化: 将多参函数转换为函数链, 每个函数仅有一个参数. 比如 `def strcat(s1: String)(s2: String) = s1 + s2`
- Scala, 闭包: 函数, 但是返回值取决于一个或多个声明于函数之外的变量

```scala
val factor = 3

// facotr 不是一个正式的参数, 其声明在函数体外, 但封闭域中使用.
// 每次函数调用时, 函数引用 factor, 并读取其当前值
val multiplier = (i:Int) => i * factor
```

- Scala, `String` 类型同 Java, Python 一样是不可变的. 若要频繁地修改 String, 使用 `String Builder`
- 用去获取对象信息的方法称为访问器方法 `accessor method`.
- Scala. `String Interpolation` - 将变量引用直接嵌入到转义字符串中.
    - s String Interpolator: 直接转义. `val name = "James"; println(s"Hello, $name")`; `println(s “1 + 1 = ${1 + 1}”) //output: 1 + 1 = 2`
    - f Interpolator: 创建格式化字符串, 与 C 语言的 `printf` 相似. 后缀标明变量类型与格式. 如 `f"$name%s is $height%2.2f meters tall"`
    - raw Interpolator: 与 s Interpolator 相似, 但不会转义字符.
- Scala, `array` 是存储同类型元素的固定大小的序列集合. `var z:Array[String] = new Array[String](3)` or `var z = new Array[String](3)`. 访问是 `()`, 而不是 Python 的 `[]`
- Scala, `lazy` 集合的元素不会消耗内存, 直到被访问. 不可变的集合可能包含可变的元素
- Scala, 特质 `trait` 包含了字段和方法定义, 常用于通过指定支持的方法签名来定义对象类型. 特质允许部分实现,未实现的函数可由继承特质的类实现.
- Scala, `obj.isInstanceOf[type]` - 检查对象是否某类型; `obj.asInstanceOf[type]` - 获取对象 obj 的类型并精确转化为 type 类型
- Scala, 值类 `value class` 是通过继承 `AnyVal` 类来避免运行时对象分配的机制. 其仅有一个被用作运行时底层表示的公有 `val` 参数, 可以带 `def` 定义, 但不能再定义额外的 val, var, 内嵌的 trait, class 或 object. 值类只能继承 universal traits, 其自身不能被继承.(所谓 universal trait 就是继承自 Any, 只有 def 成员, 且不作任何初始化工作的 trait)
- Scala, 模式匹配是除了函数值和闭包之外, 最广泛使用的功能. `=>` 分离了模式与对应的表达式;
- Scala, 定义样本类的 `case` 关键字与模式匹配中的 case 表达式相关:
    1. 编译器自动将样本类的构造参数转换成不可变字段
    2. 编译器自动实现为样本类实现 `equals`, `hashCode` 和  `toString` 方法
    3. 样本类可以留空类体
- Scala, 对字符串调用 `r()` 方法, 会隐式地将 String 转换成 RichString, 并调用方法获得 Regex 实例. 或 new Regex(String) 创建正则表达式实例
- Scala, `try .. catch` 的 `catch` 代码块可使用模式匹配来分类处理异常
- Scala, 提取器 `extractor` 是带 `unapply` 方法的对象. `unapply` 方法的目的是匹配一个值, 然后拆分它. `extractor` 对像通常会定义一个 `apply` 的双重方法.
- Scala, 可以对 object 和 class 同时定义 `apply`. 编译器将自动调用 `apply` 方法
- Scala, 使用 `match` 语句比较 `extractor` 对象时, `unapply` 方法将自动执行

```Scala
object Demo {
    def main(args: Array[String]) {
        val x = Demo(5)
        println(x)

        x match {
            case Demo(num) => println(x+" is bigger two times than "+num)
            //unapply is invoked
            case _ => println("i cannot calculate")
        }
    }
    def apply(x: Int) = x*2
    def unapply(z: Int): Option[Int] = if (z%2==0) Some(z/2) else None
}

// 10
// 10 is bigger two times than 5
```

- VNC, Debian 系启动 VNC daemon: `service vncserver-x11-serviced start`; Debain 系开机自启: `update-rc.d vncserver-x11-serviced defaults`
- Server, `localhost != 127.0.0.1`
- Twirl, 模板可生成任何基于文本的格式; 模板将被编译成标准的 Scala 函数: `views/Application/index.scala.html` 模板文件会生成 `views.html.Application.index` 类, 并拥有 `apply()` 方法.
- Twirl, 模板像一个函数, 需要参数, 且参数必须声明在模板文件的顶部, 可以指定默认值;
- Twirl, 迭代: `@for(p <- products) { ... }`; 选择分支 `@if(condition) { ... } else { ... }`
- Twirl, 声明可复用的代码块:

```scala
@display(product: Product) = {
  @product.name ($@product.price)

}

@title(text: String) = @{
  text.split(' ').map(_.capitalize).mkString(" ")

}
```

- Twirl, 以 `implicit` 关键字打头的名称, 将被标记为隐式的. 如 `@implicitFieldConstructor = @{ MyFieldConstructor() }`
- Twirl, 声明可复用的值, 用 `defining` 关键字:

```scala
@defining(user.firstName + " " + user.lastName) { fullName =>
  <div>Hello @fullName</div>
 }
```

- Twirl, 导入语句写在模板开头, 在参数之后; 若要绝对解析, 使用 `root` 前缀, 如 `@import _root_.company.product.core._`
- Twirl, 若有公用的导入需要在所有模板中导入, 可以在 `build.sbt` 中声明: `TwirlKeys.templateImports += "org.abc.backend._"`
- Twirl, 注释: `@* *@`.
- Twirl, 默认情况下, 动态内容将依据模板的类型被转义, 若要输出原生的片段, 用 `@type()` 包裹内容即可:

```scala<p>
  @Html(article.content)
</p>
```

## 20170517

- Twirl, Reverse routing and fingerprinting for public assets: `@routes.Assets.versioned(path, file)`
- Twirl, 向模板添加 CSRF:
    1. @()(implicit request: play.api.mvc.RequestHeader) [Help](http://stackoverflow.com/questions/27920546/how-to-pass-request-header-from-main-view-to-partial-view-in-play-framework)
    2. @helper.form(action = com.chinapex.prism.controllers.routes.HomeController.index(), 'class -> "form-signin", 'id -> "login-form")
    3. @helper.CSRF.formField

## 20170523

- AJAX - 添加请求头部：

```javascript
$.ajax({
    url: 'foo/bar',
    headers: { 'x-my-custom-header': 'some value'  }
});

// OR
$.ajaxSetup({
    headers: { 'x-my-custom-header': 'some value'  }
});
```

- Django - (虽然我没用过 Django) Django AJAX CSRF 认证:

```python
<form>
    {% csrf_token %}
</form>

# AJAX
# 将 csrf token 作 post 的数据
$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token  }}' },
});
```

- 关于 [csrf token with ajax](https://stackoverflow.com/questions/9089909/do-i-need-a-csrf-token-for-jquery-ajax)
- JQuery - name selector: `$("[name='obj name']")`
- Play - Scala CSRF AJAX 认证:

```scala
<form>
    @helper.CSRF.formField
</form>

// AJAX
$.ajax({

    ...
    headers: {"Csrf-Token": $('[name="csrfToken"]').val()},
    ...
}),
```

- Play - I18N, 使用正则表达式 `[a-zA-Z0-9.-_]` 匹配字符, 因此, 无法匹配中文. 一个办法是, 自己继承 I18N 模块重写. 为不改变 Play 提供的一些功能, 使用继承!

## 20170524

- Matplotlib - `plt.tight_layout()` - 可以使子图的布局更好看, 太紧凑的子图会伸展开
- Matplotlib - `plt.xticks(range)` - 可设置 X 轴刻度
- Matplotlib - `fig.savefig(bbox_inches="tight")` - 对于子图图例无法显示完全的情况, 可以完整地显示图例
- Matplotlib - `ax.plot(label=somename)` - 指定的 label 可用作图例的名称
- Regex - 绝大部分 CJK 字符范围: [\u4e00-\u9fa5]

## 20170526

- Scala - 当使用 `case` 为变量赋值时，若多个 case 的返回值不一样。变量的类型将隐式向上转型:

```scala
scala> val s = 1 match {
     | case 1 => true
     | case 0 => 1
     |
}
s: AnyVal = true

//
scala> val s: Int = 1 match {
     | case 1 => true
     | case 0 => 1
     |
}
<console>:12: error: type mismatch;
 found   : Boolean(true)
 required: Int
       case 1 => true
                 ^
```

- Scala, 对于 `Option` 类型的变量，实在要用 case 去匹配的话，以 `Some(String)` 为例：

```scala
val s = objOfOption[String] match {
  case Some(s) => s
  case None => ""
}
```

- Scala - `AnyVal` 其实就是无类型. 同 Java 的 `Object`, Python 的 `Object`
- Python - 启动 Web 服务之后，也可以断点！在要打断点的地方加上：`import pdb; pdb.set_trace()`

## 20170531

- Scala －`lazy` 延迟初始化，直到第一次需要引用成员时，才去初始化成员
- `滚动日志文件` －当日志文件达到指定大小上限时，新建日志文件，并对原来的日志文件按编号重命名
- Logback - 日志级别：TRACE < DEBUG < INFO < WARN < ERROR。默认级别为 DEBUG。[博客](http://veryyoung.me/blog/2015/09/10/logback-log-lerver.html)
    1. ERROR：发生了严重的错误，必须马上处理。这种级别的错误是任何系统都无法容忍的。比如：空指针异常，数据库不可用，关键路径的用例无法继续执行。
    2. WARN：还会继续执行后面的流程，但应该引起重视。其实在这里我希望有两种级别：一个是存在解决方案的明显的问题（比如，”当前数据不可用，使用缓存数据”），另一个是潜在的问题和建议比如“程序运行在开发模式下”或者“管理控制台的密码不够安全”）。应用程序可以容忍这些信息，不过它们应该被检查及修复。
    3. INFO:消息在粗粒度级别上突出强调应用程序的运行过程。最好能打印些人类可读的信息，需要谨慎对待，不可随便。
    4. DEBUG：开发人员调试程序的时候需要的关注的事情。
    5. TRACE：更为详尽的信息，只是开发阶段使用。在产品上线之后的一小段时间内你可能还需要关注下这些信息，不过这些日志记录只是临时性的，最终应该关掉。DEBUG和TRACE的区别很难区分，不过如果你加了一行日志，在开发测试完后又删了它的话，这条日志就应该是TRACE级别的。

## 20170601

- PLAY －`evolution` 跟踪和安排数据库 schema 变化，从创表到删表，一手包办，但如果在此之外创建了表，需要手动更正。需要手动在 `conf/evolutions/{db name}` 下创建 SQL 文件。开发模式下，在每个请求之前都会检查数据库结构状态；生产模式下，在启动应用时检查数据库结构状态。
- PLAY - `${?enviroment variable name}`，以这种方式引用系统环境变量值

## 20170602

- MYSQL - 时间戳以 UTC 时间存储
－MYSQL - 创建数据表时：`timestamp not null default current_timestamp on update current_timestamp`, 将自动更新时间属性
－PLAY －`sbt "run -Dconfig.resource=application.engine.conf"` 以 application.engine.conf 为配置文件启动应用
－MYSQL －`select UTC_TIMESTAMP()` 返回当前 UTC 时间戳
- MYSQL - `sudo /etc/init.d/mysql start/stop/restart` - 启动/关闭/重启
- Slick －`coffees.map(c => (c.name, c.supID, c.price)) += ("Colombian_Decaf", 101, 8.99)` - 其他字段将使用默认值，前提是，有默认值
- Scala －当类存在伴生对象时，`(Person.apply _)`，Person 指向伴生对象，此时括号的整体指代 Person 类
- Linux - `timedatectl status` 查看系统时间信息,包括本地时间、UTC 时间、时区等
- Linux - `sudo timedatectl set-timezone UTC/CST` 修改时区
- Linux - `timedatectl list-timezones` 列出所有时区
- MYSQL - `alter table table_name modify column some_col info` 修改属性列
- MYSQL - `describe [db_name.]table_name;` 查看表结构

## 20170605

- MYSQl - MySQL converts TIMESTAMP values from the current time zone to UTC for storage, and back from UTC to the current time zone for retrieval. MYSQL 这不是搞事吗?
- MYSQL - 时间戳都是以 UTC 存储，但展示的时候，是根据当前设置的 `time_zone` 来展示的。如下, 分别是 `time_zone` 设置为 CST 与 UTC 时的值. 但是以下 `user_id=3` 的记录，是错误的

```mysql
mysql> select * from account_token;
+--------------------------------------+---------------------+---------+
| token                                | created             | user_id |
+--------------------------------------+---------------------+---------+
| a106f7dc-5871-4a8a-a89e-93ebe5151266 | 2017-06-05 16:32:25 |       3 |
| f73edb0f-b35f-4b72-859b-b0cf04a871cf | 2017-06-05 16:00:14 |       9 |
| f7d4f3461e0b4a7592892f57a0e0df61     | 2017-06-05 14:13:49 |       2 |
+--------------------------------------+---------------------+---------+

mysql> select * from account_token;
+--------------------------------------+---------------------+---------+
| token                                | created             | user_id |
+--------------------------------------+---------------------+---------+
| a106f7dc-5871-4a8a-a89e-93ebe5151266 | 2017-06-05 10:32:25 |       3 |
| f73edb0f-b35f-4b72-859b-b0cf04a871cf | 2017-06-05 10:00:14 |       9 |
| f7d4f3461e0b4a7592892f57a0e0df61     | 2017-06-05 08:13:49 |       2 |
+--------------------------------------+---------------------+---------+
```

## 20170608

- SQL - `JOIN`，[参考链接1](https://www.codeproject.com/Articles/33052/Visual-Representation-of-SQL-Joins), [so](https://stackoverflow.com/questions/38549/what-is-the-difference-between-inner-join-and-outer-join)

```MYSQL
SELECT u.*
FROM rooms AS u
JOIN facilities_r AS fu
ON fu.id_uc = u.id_uc AND (fu.id_fu='4' OR fu.id_fu='3')
WHERE vizibility='1'
GROUP BY id_uc
ORDER BY u_premium desc, id_uc desc
```

> inner join - 像两张表的交集；full outer join - 像两张表的并集；left join - 保留左边表的全部行；right join - 保留右边表的全部行

- LAN - 查看局域网 ip 地址： `ifconfig` - `eth0` －`inet`
- SLICK - for 表达式实现 inner join, [看这里](http://slick.lightbend.com/doc/3.0.0/sql-to-slick.html?highlight=join#implicit-inner-joins)：

```scala
(for(p <- people;
     a <- addresses if p.addressId === a.id
 ) yield (p.name, a.city)
).result
```

- Scala - 两种方式不用 `new` 关键字创建对象 [参考文章](http://alvinalexander.com/scala/how-to-create-scala-object-instances-without-new-apply-case-class)
    1. 创建类的伴生对象，在伴生对象中定义 `apply` 方法。可以在伴生对象中创建多个 `apply` 方法，不同参数
    2. 使用 `case class`. `case class` 会在其伴生对象中生成一个 `apply` 方法。
- MYSQL - 时间戳常用于跟踪记录的变化，每次记录有更新，时间戳值也需要更新；`datetime` 用于存储指定的时间 [参考文章](https://stackoverflow.com/questions/409286/should-i-use-field-datetime-or-timestamp/409305#409305)

## 20170613

- Python, 类变量的初始化在类实例化之前，且仅初始化一次

## 20170614

- Pycharm - 有时候犯傻，本地模块都识别不了。解决办法：`File > Invalidate Caches / Restart > Invalidate and Restart`
- Pycharm - 对 web 应用进行 debug：`Run > Edit Configurations > 设置启动脚本与参数 > Debug ... > 选择模式启动`

## 20170626

- Java - Timestamp to Date, without time info -> `dateformat.parse(dateformat.format(ts))`

## 2017-09-18

* 几种以图片方式展示数组的方法:
    - PIL + Numpy, `from PIL import Image; img = Image.fromarray(data, "RGB"); img.show()`
    - Matplolib, `plt.imshow(data, interpolation="nearest"); plt.show()`
    - Scipy,
        1. `from scipy.misc import toimage; toimage(data).show()`
        2. `from scipy.misc import imshow; imshow(data)`
    - remark: Scipy 实际就是用了 PIL 工具; Matplotlib 画出来的更好看; PIL 更接近原始照片
* pandas, `df["some_column"]` 与 `df[["some_column"]]` 效果不一样. 前者返回一个 `Series` 对象; 后者返回 `DataFrame` 对象. 但是类似于切片, `df[["a", "b"]] 得到的是一个副本`

```ipython
In[47]: a = {"a": 1}
In[48]: d1 = pd.DataFrame(list(a), columns=["a"])
In[49]: d1["a"]
Out[49]: 
0    a
Name: a, dtype: object
In[50]: d1[["a"]]
Out[50]: 
   a
0  a
In[51]: type(d1["a"])
Out[51]: pandas.core.series.Series
In[52]: type(d1[["a"]])
Out[52]: pandas.core.frame.DataFrame
```

* Pandas, 将指定格式的字符串列转为 Datetime 类型: `some_column = pd.to_datetime(some_column, format="%Y-%m-%d %H:%M:%S")`. 此时得到的列的每个元素, 有 `date()` 和 `time()` 方法, 获得 `date` 和 `time` 的属性.
* Pandas, `series_element.str` 可以从对象中抽取出字符串.
* Pandas, dict2DataFrame: `pd.DataFrame(d.items())`
* sklearn, `RandomForestClassifier` 输出 Top N 个分类结果, 先返回预测概率: `p = predict_proba(x)`; 然后通过 `idx = np.argsort(p, axis=1)[:, -N:][:, ::-1]` 返回排序好的索引; 之后再同上索引取值即可.
* Pandas, `for idx, row in df.iterrows():` 按行遍历 DataFrame
* Pickle, `dump` 与 `load` 的对象都是二进制文件, 所以要带 `d`
* Pandas, df.append() 返回拼接后的对象, 并不是原地操作.

## 20170920

* Python, 运行时检查 Python 版本:

```python
In [1]: import sys

In [2]: sys.version
Out[2]: '3.5.2 (default, Nov 17 2016, 17:05:23) \n[GCC 5.4.0 20160609]'

In [3]: sys.version_info
Out[3]: sys.version_info(major=3, minor=5, micro=2, releaselevel='final', serial=0)
```

## 20170925

* NumPy, 快速将一维数组 (N,) 转为一维列向量 (N, 1) 或一维行向量 (1, N) 的方法: arr[:, None] or arr[None, :]

```python
In [1]: import numpy as np

In [2]: a = np.arange(100)

In [3]: a.shape
Out[3]: (100,)

In [4]: a[:, None].shape
Out[4]: (100, 1)

In [5]: a[None, :].shape
Out[5]: (1, 100)
```

## 201709230

* Pandas, `df.merge` 可用于进行一些数据融合的操作, 选项很多, 包括实现集合交运算一样的计算. 最简单的 `df1.merge(df2)`
* Pandas, dataframe 可以用 `df.values` 返回 NumPy 数组, series 则可用 `s.as_matrix`

## 20171003

* Pandas, `pandas.get_dummies` 将类别变量转为类似 one-hot 型的变量. 一列就变成了好几列. 比如二值的性别变量 (male 与 female), get_dummies 之后就得到了 female 与 male 两列

## 20171007

* Numpy, `np.triu_indices` 可以快速生成矩阵上三角的坐标, 从而得到矩阵上三角的元素.

## 20171008

* Numpy, `numpy.tile` 可以将行向量复制 N 次, 从而得到矩阵:

```python
>>> np.tile(np.array([1,2,3]), (3, 1))
array([[1, 2, 3],
       [1, 2, 3],
       [1, 2, 3]])
>>> np.tile(np.array([[1,2,3]]).transpose(), (1, 3))
array([[1, 1, 1],
       [2, 2, 2],
       [3, 3, 3]])
```

* Pandas, `pd.merge` 的几种混合方式:
    - `inner` - 使用两个 df 的 key 的交集
    - `outer` - 使用两个 df 的 key 的并集
    - `left` - 使用左边 df 的 key
    - `right` - 使用右边 df 的key

## 20171106

* pytorch, `torch.optim.lr_scheduler` 提供了多种 learning rate 衰减方案, 比原来通过 weight_decay 衰减更丰富. 使用方法是:

```python
optimizer = optim.SGD(...)
scheduler = optim.lr_scheduler(optimizer, gamma=decay_factor)  # gamma 作为衰减因子, 有时候可能是 1/decay_factor, 根据公式与实现代码自己协调

for i in epochs:
    scheduler.step()  # will update optimizer's learning rate
    train...
    validate...
```

* GAN, `D(G(z))` 是假样本被判定为真的概率, 那么`1-D(G(Z))`表示的就是假样本被判定为假的概率, 因此我们要最小化 `1-D(G(z))`, 反之就是最大化`D(G(z))`. GAN 原始值函数的含义就是, 样本来自真实数据分布被判定为真的概率对数的期望+样本来自生成数据分布被判定为假的概率对数的期望, 换言之就是 D 做出正确判断的期望. 所以, 训练 D 的目标就是提高值函数的结果, G 的目标就是减小值函数的结果.

## 20171221

* Broadcasting - describes how numpy treats arrays with different shapes during arithmetic operations. Subject to certain constraints, the smaller array is “broadcast” across the larger array so that they have compatible shapes. Broadcasting provides a means of vectorizing array operations so that looping occurs in C instead of Python. NumPy is smart enough to use the original scalar value without actually making copies, so that broadcasting operations are as memory and computationally efficient as possible. When operating on two arrays, NumPy compares their shapes element-wise. It starts with the trailing dimensions, and works its way forward. Two dimensions are compatible when 1) they are equal, or 2) one of them is 1.
* Broadcasting provides a convenient way of taking the outer product (or any other outer operation) of two arrays. (see beblow)

```python
>>> a = np.array([0.0, 10.0, 20.0, 30.0])
>>> b = np.array([1.0, 2.0, 3.0])
>>> a[:, np.newaxis] + b  # newaxis index operator inserts a new axis into a, making it 2 dimensional 4x1 array.
array([[  1.,   2.,   3. ],
       [ 11.,  12.,  13. ],
       [ 21.,  22.,  23. ],
       [ 31.,  32.,  33. ]])
```
