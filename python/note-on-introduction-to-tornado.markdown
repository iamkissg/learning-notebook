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
    tornado.ioloop.IOLoop.instance().start(
```

- `handlers` 参数, 由一个元组组成, 用于匹配 HTTP 请求路径 (不包括查询字符串和碎片) 的 regex 和 RequestHandler 类. 
