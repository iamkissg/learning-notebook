# Tornado 入门

## Chapter 1 引言

- Tornado 提供了 `tornado.options` 来从命令行读取配置
- `define("port", default=8000, help="run on the given port", type=int)` 比较显而易见. Tornado 使用 type 参数进行基本的参数类型验证
- `Tornado.RequestHandler.get_argument(query, default)` - 从查询字符串中取值
- `Tornado.RequestHandler.write(str)` - 将 str 写入 HTTP 响应中.
- 解析命令行, 创建 Application 类实例 (传给 Application 类 __init__ 最重要的参数是 `handlers`, 告诉 Tornado 应该用哪个类来响应请求), 将 Application 传给 Tornado 的 HTTPServer 对象, 监听端口. 在程序准备好接收 HTTP 请求后, 创建一个 Tornado IOLoop 实例.

```python
def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
```

- `handlers` 参数, 由一个元组组成, 用于匹配 HTTP 请求路径 (不包括查询字符串和碎片) 的 regex 和 RequestHandler 类. 

```python
app = tornado.web.Application(handlers=[
    (r"/reverse/(\w+)", ReverseHandler),
    (r"/wrap", WrapHandler)
])
```

- 括号的含义是让 Tornado 保存匹配括号里面表达式的字符串，并将其作为请求方法的一个参数传递给 RequestHandler 类

```python
class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])
```

- `get` 方法的参数 `input`, 将包含匹配处理函数正则表达式第一个括号里的字符串。（如果正则表达式中有一系列额外的括号，匹配的字符串将被按照在正则表达式中出现的顺序作为额外的参数传递进来。）
- RequestHandler 对象的 `get_argument` 方法来捕获请求查询字符串的的参数. 还能获得 POST 请求传递的参数
- 从一个传入的HTTP请求中获得信息: 使用 `get_argument` 和传入到 `get` 和 `post` 的参数
- `RequestHandler.set_status()` 显式地设置 HTTP 状态码. 在某些情况下, Tornado 会自动设置 HTTP 状态码
- 当发生错误时, Tornado 将默认向客户端发送给包含状态码和错误信息的简短片段. 若要自定义错误响应, 在 RequestHandler 中重写 `write_error` 方法.

## Chapter 2 表单和模板

- 模板是一个允许你嵌入 Python 代码片段的 HTML 文件.
- `RequestHandler.render()` 方法告诉 Tornado 读入模板文件, 插入模板代码, 并将结果返回给浏览器
- `{{ expression }}` 占位, 渲染模板时用实际值来代替. 通过 `render()` 方法传递关键字参数指定值到模板的对应位置

### 模板语法

- Tornado 是被 Python 表达式和控制语句标记的简单文本文件. 
- 可以在 `{{ expression }} 中嵌入任何表达式, 变量也是表达式, 因此可以放在双括号中. Tornado 将插入一个包含表达式计算结果的字符串到输出中.
- 用 `{% statement %}` 表示 Python 的条件和循环语句. Tornado 模板你语言在 `if` 和 `for` 语句块中可以使用的表达式没有限制, 可以在模板中执行所有的 Python 代码. 可以在控制语句块中使用 `{% set  foo = "bar" %}` 来设置变量. 但最好使用 UI 模块来做更复杂的划分
- Tornado 在所有模板中默认提供了一些便利函数, 包括:
    - escape(s) - 替换字符串 s 中的&, <, >为对应的 HTML 字符
    - url_escape(s) - 使用 urllib.quote_plus 替换字符串 s 中的字符为URL编码形式
    - json_encode(val) - 将 val 编码成 JSON 格式
    - squeeze(s) - 过滤字符串 s, 把连续的多个空白字符替换成一个空格
- 创建 APP 实例时, 若使用 `debug=True`,会调用一个便利的测试模式: `tornado.autoreload` 模块, 此时, 一旦主要的 Python 文件被修改, Tornado 会重启服务器, 并在模板改变时刷新. 这对于快速改变和实时更新有用, 但生产环境不要使用! 因为这将防止 Tornado 缓存模板
- `static_path` 指定静态文件路径; `template_path` 指定模板路径
- Tornado 模板模块提供了一个 `static_url` 的函数以生成 static 目录下文件的 URL.

```html
<link rel="stylesheet" href="{{ static_url("style.css") }}">

<link rel="stylesheet" href="/static/style.css?v=ab12">
```

- 使用 `static_url` 而不是硬编码的原因是:
    1. static_url 函数创建了一个基于文件内容的 hash 值, 并将其添加到 URL 末尾 (查询字符串的参数 v), hash 值确保浏览器总是加载一个文件的最新版而不是之前的缓存版本
    2. 可以改变 URL 的结构, 而不必改变模板的代码

## Chapter 5: 异步 Web 服务器

Tornado 相比与其他 Web 框架, 其特点是: 异步取得和提供内容的能力. 它使得处理非阻塞请求更容易, 最终使处理更高效, 扩展性更好.

### 异步 Web 亲请求

- 大部分 Web 应用都是阻塞性质的, 当一个请求被处理时, 进程会被挂起直至请求完成.
- 异步的方式: 应用程序在等待第一个处理完成的过程中, `让 I/O 循环打开以便服务于其他客户端`, 直到处理完成时启动一个请求并给予反馈, 而不再是等待请求完成的过程中挂起进程
