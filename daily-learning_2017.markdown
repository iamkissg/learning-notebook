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
