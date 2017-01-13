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
