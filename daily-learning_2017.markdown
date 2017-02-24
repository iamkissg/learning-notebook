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
