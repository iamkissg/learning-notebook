# Flask Web 开发

- Python, 修饰器是 Python 语言的标准特性，可以使用不同的方式修改函数的行为。惯常用法是使用修饰器`把函数注册为事件的处理程序`。
- Flask，`@app.route(/user/<int:id>)` 尖括号中为 URL 的动态部分，此处，`int` 表示只匹配路由中使用 int 的动态部分。还有 `float`，`path`，其中 `path` 也是字符串，但不把斜杆视作分隔符，而当作动态片段的一部分
- Flask，Web 服务器启动后，会进入轮询，等待并处理请求（我以为是类似中断的方式呢）
- Flask，使用 *context* 让特定的变量在一个线程中全局可访问，而不干扰其他线程。（比如`request`)
- 多线程 Web 服务器会创建一个线程池，再从线程池中选择一个线程用于处理接收到的请求。

![Flask Context Global Variables](flask_context_global_variables.png)

- Flask 在分发请求之前激活（或推送）程序和请求上下文，请求处理完成后再将其删除。
- ，Flask 会在程序的 URL 映射中查找请求的 URL。`URL 映射`是 URL 和视图函数之间的对应关系。Flask 使用 `app.route` 修饰器或者非修饰器形式的 `app.add_url_rule()` 生成映射。

```python
app.url_map  # 查看 Flask 程序的 URL 映射
```

- 请求钩子 - 和视图函数之间共享数据一般使用上下文全局变量 g
    - `before_first_request`：注册一个函数，在处理第一个请求之前运行。
    - `before_request`：注册一个函数，在每次请求之前运行。
    - `after_request`：注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。
    - `teardown_request`：注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。
- `重定向` 的特殊响应类型，没有页面文档，仅告诉浏览器一个新地址用以加载新页面。`return redirect("http://kissg.me")` 或 `return make_response("", 302, {"Location": "http://kissg.me"})`
- `abort` - 生成特殊的响应，用于处理错误。不会把控制权交还给调用它的函数，而是抛出异常把控制权交给 Web 服务器。
- 专为 Flask 开发的扩展都暴漏在 flask.ext 命名空间下
- REST 的 6 个特征
    - C-S - 客户端与服务器之间必须有明确的界限
    - 无状态 - 客户端发出的请求中必须包含所有必要的信息。服务器不能在两次请求之间保存客户端的任何状态
    - 缓存 - 服务器发出的响应可以标记为可缓存或不可缓存，这样出于优化目的，客户端（或客户端和服务器之间的中间服务）可以使用缓存。
    - 接口统一 - 客户端访问服务器资源时使用的协议必须一致，定义良好，且已经标准化。（REST　Web　服务最常用的统一接口是　
    - 系统分层 - 在客户端和服务器之间可以按需插入代理服务器、缓存或网关，以提高性能、稳定性和
伸缩性
    - 按需代码 - 客户端可以选择从服务器上下载代码，在客户端的环境中执行。
- `资源`是 REST 架构的核心概念。URL 的内容无关紧要，只要资源 URL 只表示唯一的资源即可。表示资源集合的 URL 习惯是在末尾加一个 `/`，表示目录
- Flask 会特殊对待末端带有斜线的路由。如果客户端请求的 URL 的末端没有斜线，而唯一匹配的路由末端有斜线，Flask 会自动响应一个重定向，转向末端带斜线的 URL。反之则不会重定向
- REST 架构不要求必须为一个资源实现所有的请求方法。如果资源不支持客户端使用的请求方法，响应的状态码为 405，返回“不允许使用的方法”。Flask 会自动处理这种错误。
- 在设计良好的 REST API 中,客户端只需知道几个顶级资源的 URL,其他资源的 URL 则从响应中包含的链接上发掘
- 客户端程序和服务器上的程序是独立开发的，有时甚至由不同的人进行开发。因此，Web 服务的容错能力要比一般的 Web 程序强,而且还要保证旧版客户端能继续使用。通常的解决办法是`使用版本区分 Web 服务所处理的 URL`
- `request.json` - 获得请求中包含的 JSON 数据；`jsonify()` 将 Python 字典转为包含 JSON 的响应
- REST API 相关的路由是一个自成一体的程序子集，为了更好地组织代码，最好将路由放到独立的 Blueprint 中。
    - Flask 用 蓝图（blueprints） 的概念来在一个应用中或跨应用制作应用组件和支持通用的模式
    - 一个 Blueprint 对象与 Flask 应用对象的工作方式很像，但它确实不是一个应用，而是一个描述如何构建或扩展应用的 蓝图 。Flask uses a concept of blueprints for making application components and supporting common patterns within an application or across applications.
- 为所有客户端生成适当响应的一种方法是，在错误处理程序中根据客户端请求的格式改写响应，这种技术称为`内容协商`。
- 在 REST
- Web 服务中使用 cookie 有点不现实,因为 Web 浏览器之外的客户端很难提供对 cookie 的支持

