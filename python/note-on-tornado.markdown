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
