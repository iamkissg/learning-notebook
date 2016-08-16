# Note on Jupyter Client

## Messaging in Jupyter

![frontend-kernel.png](front-kernel.png)

- 一个内核可同时与多个前端连接通信, 内核有四个 sockets 提供以下服务:
 - Shell - 该单一的 ROUTER socket 允许来自前端的多个连接. 它用于处理来自前端的代码执行, 对象信息, 提示等的请求. 该 socket 上的通信是前端与内核的请求/应答动作序列
 - IOPub - 该 socket 是广播通道, kernel publishes all side effects (stdout, stderr, etc) as well as the requests coming from any client over the shell socket and its own requests on the std socket. 许多 Python 语句都会产生 side effects: `print()` 会写到 `sys.stdout`, 错误将生成回溯信息, 等等. 在一个多客户端场景, 想要让所有的前端都互相知道各自向内核发送了什么请求. This socket allows both side effects and the information about communications taking place with one client over the shell channel to be made available to all clients in a uniform manner.
 - stdin: ROUTER socket, 连接到所有前端. 当调用 `raw_input` 时, 允许内核向活跃的前端请求输入. 此时前端有一个 DEALER socket, 通信时, 其相当于 Kernel 的 "virtual keyboard". 实际上, 前端会以一种特殊的输入方式显示这类 kernel 的请求, 或提示用户是输入到 kernel 而不是前端命令. 所有的消息都被打上足够的信息, 如此, 客户端才能辨别自身与内核的通信消息和其他客户端与内核的消息.
 - Control - 该通道与 Shell 完全一样, 但在一个分离的 socket 上执行操作, 使重要消息必须排队等待
 - Heartbeat - 该 socket 允许前端与内核之间发送简单的 bytestring 消息, 用于确认是否连接
- Message 是字典的字典, values 以 JSON 格式表示. 但以后可能不会用 JSON, 大量复制时, JSON 的性能不高. 但应该会提供一种简单的方式在 JSON 与原生对象之间轻松转换
