# Akka HTTP with Scala

## Introduction

- The Akka HTTP modules implement a full server- and client-side HTTP stack on top of akka-actor and akka-stream.
- 不是一个 Web 框架, 更像一个通用工具箱, 提供和消费基于 HTTP 的服务. 还包括与浏览器的交互, 但这并不是 Akka HTTP 关注的焦点
- Akka HTTP 采用开放式设计, 许多时候为"同一件事"提供了不同的 API 级别. 实现高层 API 有困难时, 可以尝试更灵活的底层 API, 但需要写更多的代码
- In a way a framework is like a skeleton onto which you put the “flesh” of your application in order to have it come alive.
- Web 应用的核心是浏览器与 Web 服务器代码的交互. The framework makers have chosen one “proven” way of designing such applications and let you “fill in the blanks” of a more or less flexible “application-template”.
- Akka HTTP 用于构建基于 HTTP 的集成层 (integration layers). 因此, 应用并不是构建在 Akka HTTP 顶层, 而是 on the top of whatever makes sense. 仅使用 Akka HTTP 用于集成的需要
- `akka-http` 依赖于 `akka-http-core`
- Akka HTTP 的高层路由 API 提供了描述 HTTP 路由和处理的 DSL.
- Marshalling - the process of converting a higher-level (object) structure into some kind of low-level representation, often a "wire format". 换个名词就是 `Serialization` 或 `Pickling`
- Akka HTTP 中, Marshalling 意味着 T 类型对象转换成低级的目标类型
- `spray-json`
- Akka HTTP 的一个强项是, 流化数据 (streaming data) 是其核心功能: both request and response bodies can be streamed through the server achieving constant memory usage (恒定的内存使用) even for very large requests or responses.
- 流式响应会被远程客户端 backpressure, 因此服务器推送数据的不会快到客户端无法处理的程度; 流式请求意味着由服务器决定远程客户端可以多快的速度推送请求主体的数据
- 低层次的 Akka HTTP server API 由 `akka.http.core` 提供, 允许通过接收 `HTTPRequest` 并产生 `HTTPResponse` 来处理连接与私人请求.
- Client API 提供了调用 HTTP server 的方法, 增加了连接池的概念, 通过复用 TCP 连接高效地处理对同一个服务器的多个请求
- The modules that make up Akka HTTP:
    - akka-http - 高级功能, (反)序列化, 解/压缩等; DSL, 用于定义服务端基于 HTTP 的 API (用 Akka HTTP 写 HTTP server 的推荐方式)
    - akka-http-core - 完整的, 底层的, 服务端与客户端 HTTP 实现
    - akka-http-testkit - 验证服务端服务实现的工具集
    - akka-http-spray-json - 预定义的胶水代码, 用于 JSON 格式的(反)序列化
    - akka-http-xml - 预定义的胶水代码, 用于 XML 格式的(反)序列化
