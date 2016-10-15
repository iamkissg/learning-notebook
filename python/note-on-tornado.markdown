# Note on Tornado

## Introduction

- Tornado is a Python `web framework` and `asynchronous networking library`.
- By using `non-blocking network I/O`, Tornado can scale(衡量?) to tens of thousands of open connections, making it ideal for long polling(轮询), WebSockets, and other applications that require a long-lived connection to each user.
- 4 major components:
 - A `web framework` (including RequestHandler which is subclassed to create web applications, and various supporting classes). `web 框架`
 - `client`- and `server`-side implementions of HTTP (`HTTPServer` and `AsyncHTTPClient`). `HTTP 客户端和服务器端实现`
 - An `asynchronous networking library` including the classes IOLoop and IOStream, which serve as the building blocks for the HTTP components and can also be used to implement other protocols. `异步网络库`
 - A `coroutine library` (`tornado.gen`) which allows asynchronous code to be written in a more straightforward way than chaining callbacks. `异步协程库`
- The Tornado web framework and HTTP server together offer a full-stack alternative to WSGI(web server gateway interface).
- While it is possible to use the Tornado web framework in a WSGI container (`WSGIAdapter`), or use the Tornado HTTP server as a container for other WSGI frameworks (`WSGIContainer`).
<<<<<<< HEAD

## Asynchronous and non-Blocking I/O

- To minimize the cost of concurrent connections (使同步连接的消耗最小), Tornado uses a `single-threaded` event loop. This means that all application code should aim to be asynchronous and non-blocking (异步非阻塞) because only one operation can be active at a time. (单线程一次只能做一个操作)
- 异步 vs. 非阻塞
    - **Blocking** - A function blocks when it waits for something to happen before returning. (阻塞, 等待事件的发生) A function can be blocking in some respects (方面) and non-blocking in others. `tornado.httpclient `默认在DNS解析时阻塞, 在其他网络访问时不阻塞. Tornado, 只在 网络 I/O context 谈论阻塞, 所有的阻塞都最小化了.
    - **Asynchronous** - An asynchronous function returns **before it is finished** (异步函数在完成之前就返回了), and generally causes some work to happen in the background before triggering some future action in the application. (后台在触发一些未来的行为之前会做一些操作)
        - 几种异步接口的实现:
            - Callback argument (回调参数)
            - Return a placeholder (`Future`, `Promise`, `Deferred`)
            - Deliver to a queue
            - Callback registry (回调注册) (e.g. POSIX signals)
        - Regardless of which type of interface is used, asynchronous functions by definition interact differently with their callers (无论使用什么类型的接口, 根据定义, 异步函数与它们的调用者之间的交互都是不同的)
        - There is no free way to make a synchronous function asynchronous in a way that is transparent to its callers

#### Examples

###### 同步函数

```python
from tornado.httpclient import HTTPClient

def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body
```

###### 重写的使用回调参数实现的异步函数

```python
from tornado.httpclient import AsyncHTTPClient

def asynchronous_fetch(url, callback):
    http_client = AsyncHTTPClient(
    def handle_response(response):
        callback(response.body)
    http_client.fetch(url, callback=handle_response))
```

###### `Future` 版本

```python
from tornado.concurrent import Future

def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result()))
    return my_future
```

- 原生的 `Future` 更复杂, 但更推荐, 因为其有 2 点主要的优势: 错误处理更连贯, 因为 `Future.result` 方法可以简单地抛出异常; `Future` 能更好地与协程配合.

###### 协程版

```python
from tornado import gen

@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)
```

- 上述的语句 `raise gen.Return(response.body)` 是 Python 2 特有的. 对于 Python 2, generator 不允许返回值. 为了解决该困难, Tornado 协程通过抛出特殊的异常 `.Return`, 协程捕获异常, 并将其作为返回值. (Python 3.3 以后的版本可直接使用 `return.response.body`)

## 协程

- 协程是 Tornado 推荐的写异步代码方式.
- 使用 `yield` 关键字以暂停和恢复执行过程, 来代替一系列的回调
- 协程几乎同步代码一样简单, 但没有线程消耗. 协程使并发更简单, 因为减少了 context 的切换

#### Python 3.5 async 和 await

- Python 3.5 引入了 `async` 和 `await` 关键字. 使用 `async def foo()` 代替 `@gen.corountine` 装饰器来定义函数, 用 `await` 代替 `yield`
- `async` 和 `await` 会比旧版本的 `yield` 实现的协程更快
- `await` 关键字不如 `yield` 关键字多功能. 比如基于 `yield` 的协程可以生成一个 `Futures` 的列表, 但是 native 协程必须将列表包装成 `tornado.gen.multi`
- 用 `tornado.gen.convert_yielded` 可将 `yield` 生成的一切转换成适配 `await` 的形式
- native 协程并不适合特定框架. (并非所有的协程都彼此兼容)
- Tornado coroutine runner 的设计原则就是多功能, 尽可能接收任意框架的 awaitable 对象 (`asyncio` coroutine runner 不支持其他框架的协程). 因此, 建议在应用中使用 Tornado  coroutine runner 整合多个框架. 使用 Tornado runner 在一个已经使用了 asyncio runner 调用协程: `tornado.platform.asyncio.to_asyncio_future`

#### 协程是如何工作的

- 所有 generator 都是异步的, 调用一次, 将返回一个 generator 对象, 而不是一次性跑完. `@gen.coroutine` 装饰器通过 `yield` 表达式和生成器进行通信, 通过返回 `Future` 对象 与协程调用者通信

```python
# 这是一个协程装饰器内循环的简化版本
# 装饰器从生成器接收一个 `Future`, 等待(非阻塞地) `Future` 的完成
# 然后 "unwrap" `Future` 并将结果作为 `yield` 表达式的结果返回生成器
def run(self):
    # send(x) makes the current yield return x.
    # It returns when the next yield is reached
    future = self.gen.send(self.next)
    def callback(f):
        self.next = f.result()
        self.run()
    future.add_done_callback(callback)
```

- 大多数异步代码不会直接使用 `Future` 类

#### 如何调用一个协程

- 正常情况下, coroutine 不会抛出异常: 任何协程抛出的异常直到它被 yield 才会被 `Future` 捕获. 这意味着, 以正确的方式调用协程很重要, 否则会报错却收不到通知
- 在几乎所有的例子中, 任何调用协程的函数其本身都必须是一个协程, 并用 `yield` 关键字调用子协程.
- 有时候, 可能想要 "fire and forget" (释放) 一个协程, 不等待其结果. 此时, 建议使用 `IOLoop.spawn_callback`, 利用 `IOLoop` 来全权负责本次调用. 当调用失败, `IOLoop` 将打印回溯日志.

```python
# The IOLoop will catch the exception and print a stack trace in
# the logs. Note that this doesn't look like a normal call, since
# we pass the function object to be called by the IOLoop.
IOLoop.current().spawn_callback(divide, 1, 0)
```

- 在程序的顶层, 若 `IOLoop` 没有运行, 需要首先启动 `IOLoop`, 然后运行协程, 之后用 `IOLoop.run_sync` 来停止 `IOLoop`. 这通常适用于面向批处理的程序的 `main` 函数

#### 协程模式

###### 与 回调交互

- 要与使用回调而不是 `Future` 的代码交互, 使用 `Task` 来包装调用. 它将添加回调参数, 并返回 `Future` (可 yield)

```python
@gen.coroutine
def call_task():
    # Note that there are no parens on some_function.
    # This will be translated by Task into
    #   some_function(other_args, callback=callback)
    yield gen.Task(some_function, other_args)
```

###### 调用阻塞函数

- 用协程调用阻塞函数最简单的方式是使用 `ThreadPoolExecutor`, 其将返回兼容协程的 `Futures`:

```python
thread_pool = ThreadPoolExecutor(4)

@gen.coroutine
def call_blocking():
    yield thread_pool.submit(blocking_func, args)
```

###### 并行

- 协程装饰器能认得列表以及值为 `Futures` 的字典, 并等待所有的 `Futures` 并行完成


```python
@gen.coroutine
def parallel_fetch(url1, url2):
    resp1, resp2 = yield [http_client.fetch(url1),
                          http_client.fetch(url2)]

@gen.coroutine
def parallel_fetch_many(urls):
    responses = yield [http_client.fetch(url) for url in urls]
    # responses is a list of HTTPResponses in the same order

@gen.coroutine
def parallel_fetch_dict(urls):
    responses = yield {url: http_client.fetch(url)
                        for url in urls}
    # responses is a dict {url: HTTPResponse}
```

###### 交错

- 有时候需要保存 `Future` 而不是立即 yield, 此时需要在等待之前启动另一个操作:


```python
@gen.coroutine
def get(self):
    fetch_future = self.fetch_next_chunk()
    while True:
        chunk = yield fetch_future
        if chunk is None: break
        self.write(chunk)
        fetch_future = self.fetch_next_chunk()
        yield self.flush()
```

###### 循环

- 对于协程, 循环很棘手. there is no way in Python to `yield` on every iteration of a `for` or `while` loop and capture the result of the yield
- 因此需要将结果和循环条件分离, 以下是使用 [Motor](://motor.readthedocs.io/en/stable/) 的例子:

```python
import motor
db = motor.MotorClient().test

@gen.coroutine
def loop_example(collection):
    cursor = db.collection.find()
    while (yield cursor.fetch_next):
        doc = cursor.next_object(O
```

###### 后台运行

- 协程通常不用 `PeriodicCallback` (周期性回调). 相反的, coroutine 会包含一个 `while True` 循环 并使用 `tornado.gen.sleep`

```python
@gen.coroutine
def minute_loop():
    while True:
        yield do_something()
        yield gen.sleep(60)

# Coroutines that loop forever are generally started with
# spawn_callback().
IOLoop.current().spawn_callback(minute_loop)
```

- 有时候可能需要更复杂的循环. 比如上面的例子每个循环执行 `60+N` 秒, `N` s 时间消耗在 `do_something()` 上. 为了刚刚好使循环执行 60 s, 使用 interleaving 模式:

```python
@gen.coroutine
def minute_loop2():
    while True:
        nxt = gen.sleep(60)   # Start the clock.
        yield do_something()  # Run while the clock is ticking.
        yield nxt             # Wait for the timer to run out.
```

## Queue 例子 - 并发的网络爬虫

- Tornado 的 `tornado.queues` 模块实现了异步的生产者/消费者模式的协程, 类似于 Python 标准库 `queue` 模块实现多线程
- 协程 yield `Queue.get` 以暂停, 直到队列中有元素. 若队列有一个最大集合, 协程产生 `Queue.put` 以暂停, 直到有空间存放另一个元素
- 一个 `Queue` 包含一系列未完成的任务, 从 0 开始, `put` 增加任务数, `task_done` 减少任务数
=======
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
>>>>>>> 9c24f89f471f22640b0b49c215fbd02a65552a02
