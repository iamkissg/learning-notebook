# Note on Tornado

- Tornado is a Python `web framework` and `asynchronous networking library`.
- By using `non-blocking network I/O`, Tornado can scale(衡量?) to tens of thousands of open connections, making it ideal for long polling(轮询), WebSockets, and other applications that require a long-lived connection to each user.
- 4 major components:
 - A `web framework` (including RequestHandler which is subclassed to create web applications, and various supporting classes).
 - `Client`- and `server`-side implementions of HTTP (`HTTPServer` and `AsyncHTTPClient`).
 - An `asynchronous networking library` including the classes IOLoop and IOStream, which serve as the building blocks for the HTTP components and can also be used to implement other protocols.
 - A `coroutine library` (`tornado.gen`) which allows asynchronous code to be written in a more straightforward way than chaining callbacks.
- The Tornado web framework and HTTP server together offer a full-stack alternative to WSGI(web server gateway interface).
- While it is possible to use the Tornado web framework in a WSGI container (`WSGIAdapter`), or use the Tornado HTTP server as a container for other WSGI frameworks (`WSGIContainer`).
- To minimize the cost of concurrent connections, Tornado uses a single-threaded event loop. This means that all application code should aim to be asynchronous and non-blocking because only one operation can be active at a time.
- **Blocking** - A function blocks when it waits for something to happen before returning. A function can be blocking in some respects and non-blocking in others. `tornado.httpclient`默认在DNS解析时阻塞, 在其他网络访问时不阻塞.
- **Asynchronous** - An asynchronous function returns **before it is finished**, and generally causes some work to happen in the background before triggering some future action in the application.
- 几种异步接口的实现:
 - Callback argument(回调参数)
 - Return a placeholder (`Future`, `Promise`, `Deferred`)
 - Deliver to a queue
 - Callback registry(回调注册) (e.g. POSIX signals)
- Regardless of which type of interface is used, asynchronous functions by definition interact differently with their callers(无论使用什么类型的接口, 根据定义, 异步函数与它们的调用者之间的交互都是不同的)

## Structure of a Tornado web application

- Tornado web app 通常由一个或多个 `RequestHandler` 子类, 一个提供接入请求到 handlers 的 `Application` 对象, 以及一个 `main()` 方法以启动服务器

#### `Application` 对象

- The `Application` object is responsible for global configuration, including the routing table that maps requests to handlers. 负责全局配置, 包括请求到 handlers 的路由映射

#### `RequestHandler` 子类

#### 处理请求输入

#### 覆盖 RequestHandler 方法

#### 错误处理

#### 重定向

#### 异步 handlers

## Asynchronous networking

- `tornado.ioloop` - main event loop
- 为非阻塞 socket 设计的 IO 时事件循环
- 典型的应用会在 `IOLoop.instance` 单例模式下, 使用一个单一的 `IOLoop` 对象. `IOLoop.start` 方法通常应该在 `main` 函数的最后调用.
- 另一些应用可能会使用多个 `IOLoop`, 可能是一个线程一个 `IOLoop`, 或一个 `unittest` 用例一个
- `IOLoop` 可以根据基于时间的时间进行调度. `IOLoop.add_timeout` 是 `time.sleep` 的非阻塞替代品

#### IOLoop 对象

- `class tornado.ioloop.IOLoop` - 层级触发的 IO 循环
- 可能的话, 将使用 `epoll` (Linux) 或 `kqueue` (BSD), 否则就使用 `select()`. 若要实现一个能同时处理上千条连接的, 应使用支持 `epoll` 或 `kqueue` 的系统
- 默认地, 新构造的 `IOLoop` 将成为线程的当前 `IOLoop`, 除非线程已经存在一个 `IOLoop`. 该行为可用 `make_current` 参数控制

#### 运行 IOLoop

- `static IOLoop.current(instance=True)` - 返回当前线程的 `IOLoop`
- `IOLoop.make_current()` - 为当前线程启动一个 `IOLoop`
- `static IOLoop.instance()` - 返回全局 `IOLoop` 实例
- `static IOLoop.initialized()` - 若单实例被创建了, 返回 `True`
- `IOLoop.install()` - 安装 `IOLoop` 对象作为一个单一实例
- `static IOLoop.clear_instance()` - 清理全局 `IOLoop` 实例
- `IOLoop.start()` - 开始 IO 循环
- `IOLoop.stop()` - 停止 IO 循环
- `IOLoop.run_sync(func, timeout=None)` - 开始 `IOLoop`, 运行给定函数, 停止循环
- `IOLoop.close(all_fds=False)` - 关闭 `IOLoop`, 释放全部资源

#### IO 事件

- `IOLoop.add_handler(fd, handler, events)` - 将 handler 注册为接收事件. `fd` 参数可以是一个整数表示的文件描述符, 或者一个带 `fileno()` 方法的 类文件对象
- `IOLoop.update_handler(fd, events) - Changes the events we listen for fd.
- `IOLoop.remove_handler(fd)` - 为 `fd` 停止事件监听

#### 回调与超时

- `IOLoop.add_callback(callback, *args, **kwargs)` - 下一次 IO 循环迭代, 调用给定的回调函数
- `IOLoop.add_callback_from_signal(callback, *args, **kwargs)` - 同上
- `IOLoop.add_future(future, callback)` - 当给定的 `Future` 完成, 调度回调函数
- `IOLoop.add_timeout(deadline, callback, *args, **kwargs)` - 超时时调用 `callback`
- `IOLoop.call_at(when, callback, *args, **kwargs)` - 在 `when` 指定的绝对时间运行 `callback`
- `IOLoop.call_later(delay, callback, *args, **kwargs)` - `delay` 指定的延迟时间之后执行 `callback`
- `IOLoop.remove_timeout(timeout)` - 取消挂起的超时
- `IOLoop.spawn_callback(callback, *args, **kwargs)` - 下一次 IO 循环迭代时, 调用回调函数
- `IOLoop.time()` - 根据 `IOLoop` 时钟, 返回当前时间
- `class tornado.ioloop.PeriodicCallback(callback, callback_time, io_loop=None)` - 周期性调度回调函数
    - `start()` - 启动计时器
    - `stop` - 停止计时器
    - `is_running()` - 若 `PeriodCallback` 开始了, 返回 `True`

#### 调试与错误处理

- `IOLoop.handle_callback_exception(callback)` - `IOLoop` 执行回调抛出异常时, 调用该方法
- `IOLoop.set_blocking_signal_threshold(seconds, action)` - 若 `IOLoop` 被阻塞超过 `s` 秒, 发一个信号
- `IOLoop.set_blocking_log_threshold(seconds)` - 若 `IOLoop` 被阻塞超过 `s` 秒, 记录回溯栈
- `IOLoop.log_stack(signal, frame)` - 记录当前线程的回溯栈的信号 handler

#### 子类方法

- `IOLoop.initialize(make_current=None)`
- `IOLoop.close_fd(fd)` - 关闭 `fd` 的实用方法
- `IOLoop.split_fd(fd)` - 返回一个 (fd, obj) 对

## Coroutines and concurrency

- `tornado.gen` - simplif asynchronous code
- `tornado.gen` 是基于生成器但接口. 使用 `gen` 模块的代码, 技术上是异步的, 但它以单个生成器而不是一个分离的函数集写成.
- 大多数 Tornado 的异步函数返回一个 `Future` 对象, `yield` 这个对象就返回了 `result`
- 还可以 yield 一个 `Future` 的列表或字典, 那么这些生成器将同时开始, 并并行运行; 结果的 list 或 dict 将在它们全部完成之后被返回
- 当 `singledispatch` 库可用时, 可以 yield 额外更多类型的对象. `tornado.platform.asyncio` 和 `tornado.platform.twisted` 模块分别提供了对 `asyncio.Future` 和 Twisted 的 `Deferred` 的支持. [详情](http://www.tornadoweb.org/en/stable/gen.html#tornado.gen.convert_yielded)

#### 装饰器

- `tornado.gen.coroutine(func, replace_callback=True)`
    - 任何 `tornado.gen` 模块的生成器, 必须以 `gen.coroutine` 装饰器或 `engine` 包装
    - 该装饰器装饰的函数返回一个 `Future` 对象. 另外, 其可能以一个 `callback` 关键字参数调用, 回调函数只会在 future 的结果出来以后被调用. 若协程失败, 回调函数不会执行并抛出异常. 回调参数在被装饰函数内不可见, 它由装饰器自身处理
    - 从调用者的角度看, `@gen.coroutine` 近似于 `@return_future` 和 `@gen.engine` 的组合

> 当协程内部出现异常时, 异常信息将被保存在 `Future` 对象中. 因此必须对 `Future` 进行检验, 否则异常并不会有通知.

- `tornado.gen.engine(func)`
- 面向回调 (callback-oriented) 的异步生成器装饰器
- 旧的接口. 该装饰器类似于 `coroutine`, 但是它不返回 `Future`, 也不提供 `callback` 参数
- 大多数情况下, `engine` 装饰的函数,应该带一个 `callback` 参数, 并在结果出来之后进行回调

#### 工具函数

- `exception tornado.gen.Return(value=None)`
- `tornado.gen.with_timeout(timeout, future, io_loop=None, quiet_exceptions=())`
- `exception tornado.gen.TimeoutError`
- `tornado.gen.sleep(duration`
- `tornado.gen.moment`
- `class tornado.gen.WaitIterator(*args, **kwargs)`
- `tornado.gen.multi(children, quiet_exceptions=())`
- `tornado.gen.multi_future(children, quiet_exceptions=())`
- `tornado.gen.Task(func, *args, **kwargs)`
- `class tornado.gen.Arguments`
- `tornado.gen.convert_yielded(yielded)` - Convert a yielded object into a `Future`
- `tornado.gen.maybe_future(x)` - convert `x` into `Future`
