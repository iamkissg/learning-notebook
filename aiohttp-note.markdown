- keep-alive: 在服务器发回响应之后,保持服务器与客户端之间的通信连接,以便之后通过同一socket发送请求.
- resource: a concept reflects the http path, every resource corresponds to uri(一个路径就是一个资源)
- route: a apart of resource, resouces' path coupled with http mehthod
- 实现web server的一般步骤:
 1. 创造`request handler`, 其接收一个`Request`实例作为唯一参数,并返回一个`Response`实例
 2. 创建一个`Application`实例,将特定的`http method`,`path`以及`request handler`注册到该application的`router`(路由分析器)
 3. 调用`run_app()`运行application
- 一个`handler`接收`Request`实例作为唯一参数,并返回`StreamResponse`(http response的基类)实例
- `add_route`还支持通配符
- `router` is a list of resources
- `resource` is a entry in route table which corresponds to requested url
- `route` corresponds to handling http method by calling web handler(通过调用相应的web处理器,处理http method的过程)
- resource可包含可变的路径.比如`/a/{name}/c`可以匹配`/a/b/c`也可以匹配`/a/d/c`等.如前所示,其可变部分用`{identifier}`的形式表示,其中`identifier`可以在之后的`request handler`中被使用,通过在`Request.match_info`映射中查找`identifier`实现.默认的,每个这样的部分都被正则表达式`[^{}/]+`匹配的,因此,可以用`{identifier:regex}`的形式指定自定义的regex
- 可以给一个`route`取一个名字,如`resource = app.router.add_resource("/root", name = "root")`,这在之后可以被用于访问和建立url
- `handlers`可以是一级函数或协程.有时候,方便起见,也可以将逻辑相似的handlers组织进一个python类
- `aiohttp.web`支持Django风格的基于类的视图,可以从`View`派生出子类,定义方法用于处理http请求.Hanlers应该是一个只接受自身作为参数,并返回response对象的协程,就像常规的web-handler一样.Request对象会被`View.request`属性检索.
- 实现了view之后,像handler一样将其注册到应用的router上: `app.router.add_route("*", "/path/to", MyView)`
- 所有注册到一个`router`的资源都可以通过`urlDispatcher.resources()`方法查看.类似的,可以通过`urlDispatcher.named_resources()`方法查看resources的子集
- `aiohttp`的作者们提供了一个第三方库`aiohttp_jinja2`,提供了`aiohttp.web`的模板支持
- 最简单的在处理器中使用模板引擎的方法是,使用`aiohttp_jinja2.template()`装饰器
- `aiohttp.web`没有内建的会话概念,但有第三方库`aiohttp_session`.会话用于存储用户数据
- The Expect request-header field is used to indicate that particular server behaviors are required by the client
- aiohttp.web支持Expect header.默认的,它将会发送`HTTP/1.1 100 Continue`行给客户端,或者当头部的值不等于"100-continue"时抛出异常`HTTPExpectionFailed`.
- 可以为每个route都指定自定义的expect header handler.当请求指定了expect header, 在请求的所有头部都被接收后,在处理应用的middleware与route handler生效之前,会调用`expect header handlers`.若handler返回None,则对请求的处理将如正常进行;若返回值是一个`StreamResponse`实例,`request handler`将会把它作为响应;若处理器抛出异常,后续的处理将不再进行,并返回客户端一个合适的http响应
- aiohttp.web内建支持通过浏览器的上传,使用步骤:
 1. 确保html的`<form>`元素具有属性`enctype="multipart/form-data"
 2. 在`request handler`中通过`FileField`实例访问文件输入域
- aiohttp.web支持`WebSockets`,在request handler中创建`WebSocketResponse`,之后就可以用于通信了.从*WebSocket*的读取工作只能在request handler中进行,但写操作可以委派给其他协程
- 每个异常都是HTTPException的一个子类,并且都有一个唯一的http 状态码与之对应.同时,异常还是Response的一个子类,因此可以抛出异常,也可以返回异常,效果一样
- 异常状态码:
 1. 100~300并非真的错误
 2. 400s是客户端出错
 3. 500s是服务器出错
- aiohttp.web不建议使用全局变量,每个变量都应有它自己的上下文环境
- `aiohttp.web.Application`和`aiohttp.web.Request`支持`collection.abc.MutableMapping`接口,并允许他们被用于存储数据,从而实现非全局变量的数据共享

```python
app["my_private_key"] = data

@asyncio.coroutine
def handler(request):
    data = request.app["my_private_key"]
```

- 只在一个请求内生效的变量,可以被储存在一个Request内.这对于`Middlewares`和`Signals`handlers,将数据储存起来,以便在后续的handlers中继续使用十分有效.
- `middlewares`是一强大的自定义request handler的机制
- 在创建应用时,通过指定命名关键字为一些`middle factories`的列表,创建中间件

```python
app = web.Application(middlewares=[middle_factory_1, middle_factory_2])
```

- 一个middle factory是一个实现了中间件逻辑的协程:

```python
@asyncio.coroutine
def middleware_factory(app, handler):
    @asyncio.coroutine
    def middleware_handler(request):
        return yield from handler(request)
    return middleware_handler
```

- 每个middle factory接收两个参数,一个app实例,一个处理器,其返回一个新的handler
- 传入一个middle factory的handler是另一个middle factory返回的handler. 最后一个middle factory总是接收request handler作为参数
- middle factory需要返回一个新的handler,这个handler与request handler有相同的签名,即它接收一个单一的Response(难道不是Request)实例,并返回一个Response,或抛出一个异常
- 实际上,一个单一request handler的构造是对源handler,反向应用中间件链,并被`RequestHandler`调用作为一个常规handler
- 中间件通常调用内部的handler,但也可能选择忽视
- 中间件可以自定义对请求的响应的前后的request handler,而signals可以在响应过程中自定义request handler.signal handler不需要return,但可能会修改可变参数
- aiohttp.web有一套完善的流控制机制.默认的,流数据与websocket使用`NODELAY`模式的流控制形式,即小片的数据总是尽可能快地发送出去,而常规响应与静态文件处理器工作在CORK模式下,即不发送局部的tcp/ip帧,全部的局部帧只有在选项再次声明的时候才发送,其适合于大量数据的发送(帧数最少).通过`set_tcp_cork()`或`set_tcp_nodelay()`方法手动设置流控制
- aiohttp没有优雅地关闭应用的手段,官方推荐可以注册一个`Application.on_shutdown`signal handler,并在关闭server时调用该signal
- 恰当的关闭过程如下所示:
 1. 停止接收新的客户端连接,调用`asyncio.Server.close()`和`asyncio.Server.wait_closed()`
 2. 调用`Application.shudown()`事件
 3. 关闭已经建立的客户端连接,调用`RequestHandlerFactory.finish_connections()`
 4. 调用注册的应用结束器,`Application.cleanup()`

```python
loop = asyncio.get_event_loop()
handler = app.make_handler()
f = loop.create_server(handler, '0.0.0.0', 8080)
srv = loop.run_until_complete(f)
print('serving on', srv.sockets[0].getsockname())
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    srv.close()
    loop.run_until_complete(srv.wait_closed())
    loop.run_until_complete(app.shutdown())
    loop.run_until_complete(handler.finish_connections(60.0)
    loop.run_until_complete(app.cleanup())
loop.close()
```

- 
