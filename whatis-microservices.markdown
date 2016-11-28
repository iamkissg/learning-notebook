# 微服务

- Microservice - describe a particular way of designing software applications as suites of independently deployable services
- In short, the microservice architectural style is an approach to developing a single application as a suite of small services, each running in its own process and communicating with lightweight mechanisms, often an HTTP resource API.
- 微服务对服务进行最低限度的集中管理. 各服务可以不同的语言编写, 并使用不同的数据存储技术
- 企业软件主要由 3 部分组成:
    - 客户端用户接口
    - 数据库
    - 服务器端
- 微服务:
    - 各服务可独立部署与扩展
    - 每个服务都提供了稳固的模块边界
    - 不同服务可用不同语言编写的
    - 由不同团队管理
- 微服务的根源至少可以回溯到 Unix 的设计原则

## 微服务架构的特点

### 通过服务的组件化

- 组件 - 一个独立的, 可替换可更新的软件单元
- 微服务架构会使用库, 但软件组件化的主要方式是分解成各服务.
- 库 vs. 服务
    - 库 - 链接程序, 通过内存中函数调用
    - 服务 - 进程外的组件, 通过例如 web 服务请求, 远程进程调用等机制通信
    - 使用服务而不是库作为组件的一个主要原因是: `服务是独立可部署的`
    - 服务作为组件的另一个结果是: `更清晰的组件接口`. 只使用文档来防止客户端破坏组件的封装, 会导致组件间耦合度过高. 服务通过清晰的远程调用机制避免
    - 远程调用比进程调用消耗更大, 因此远程 API 需要是粗粒度的, 反而显得笨拙.

### 围绕业务组织

- 微服务的各团队是由前端, 后台, 数据库管理员组成的全栈小团队, 围绕各业务组织, 而不是所有的前端负责前端展示, 所有的后台负责后台逻辑, 所有的 DBA 负责数据库管理, 各项之间有着清晰的界限
- 微服务的"微"不在于服务的大小, 团队的大小

### 产品而不是项目

- 大多数应用开发使用的项目模型是这样的: 开发的目的是发布一些被认为已经完成的软件, 然后被标志完成的软件递交给维护组织, 而项目组就此解散
- 微服务的团队需要持有产品的整个生命周期, 开发团队对产品负全责.
- 亚马逊观点: `You build, you run it`

### 智能终端与笨管道

- 不同进程之间的通信架构, 过去许多案例都强调将"智能"加入通信机制本身.
- 但微服务社区更偏爱: 智能终端与笨管道. 微服务构建的应用, 诣在模块间尽可能解耦, 模块内部尽可能内聚.
- 使用简单的 REST 的协议, 而不是复杂的协议. 使用最普遍的 2 种协议是: HTTP 资源请求-响应 API 和轻量消息 (lightweight messaging).
- `Be of the web, not behind the web.`
- 微服务团队使用的原则与协议是 `World Wide Web` 的建造基础. 通常, 使用过的资源可以非常容易就被缓存
- Lightweight messaging 的基础设施 (infrastructure) 是笨的 (只作为消息路由器) - 实现简单, 像 RabbitMQ 或 ZeroMQ 仅提供一个可靠的异步架构 - 终端是智能的, 其产生或消费消息
- 在整体 (Monolith), 组件间的通信通过方法或函数调用实现. 整体架构的软件转变成微服务架构最大的问题就在于通信模式的转换.

### 分散治理

- 集中治理的一个结果是: 单一技术平台的标准化. The growth of JVM as a platform is just the latest example of mixing languages within a common platform.
- 相比于使用预定义的标准集, 微服务的团队更倾向于生产有用的工具, 这些工具从实现中来, 并分享给更多的团队.
- 分享有用的严格测试的代码作为库, 鼓励了其他开发者以相似的方式解决类似的问题, 但也留下了其他的可能性.
- 类似于 [Tolerant Reader](http://www.martinfowler.com/bliki/TolerantReader.html) 和 [Consumer-Driven Contracts](http://www.martinfowler.com/articles/consumerDrivenContracts.html) 的模式经常被应用于微服务. 这些帮助服务可以独立开发.
- Executing consumer driven contracts as part of your build increases confidence and provides fast feedback on whether your services are functioning.
- Define the contract for a service. This becomes part  of the automated build before code for the new service is even written
- 团队要为他们创建的软件的方方面面负责, 包括 24/7 的操作
- 微服务 vs. SOA (service oriented archiecture)

### 分散式数据管理

- 最抽象的分散式数据管理, 意味着从不同系统的角度看待, 概念模型不同.
- 应用之间看待数据管理, 有所不同. 当应用被拆分成分离的组件时, 不同组件看到的数据形态也是不同的
- Domain-Driven Design 将复杂的域分解成多个绑定上下文, 并显示出他们之间的关系. [Bounded Context](http://www.martinfowler.com/bliki/BoundedContext.html)
- 服务与上下文绑定之间的自然联系, 有助于业务划分, 使分离更彻底
- 整体设计的应用偏向于使用单一的逻辑数据库作数据持久化, 企业偏向于在多个应用之间使用单一的数据库. 许多决策是供应商的商业模式决定的
- 微服务还分散了数据存储决策, 允许每个服务管理自己的数据库, 可以是相同数据库技术的不同实例, 也可以是完全不同的数据库系统.
- 微服务之间分散数据的责任, 暗含了管理更新的意思. 处理更新的常用方法是使用事务 (transaction) 来保证多资源更新之间的一致性.
- 使用事务, 有助于一致性, 但会暂时增强耦合, 对于多服务是个问题.
- 服务间的同步调用是有害的

### 基础设施自动化

- 云技术的发展, 降低了创建, 部署, 操作微服务的复杂性
- 许多微服务的产品或系统, 都采用`持续交付` 或 `持续集成`, 这种方式广泛应用了基础设施自动化技术
- 持续交付的一个目的就是使部署更无聊, 无论是一个还是三个应用并没有区别

### Design for failure

- 使用服务作为组件的一个结果是, 应用需要设计服务失败的情况.
- 服务随时都可以挂掉, 因此快速发现失败, 如果可能的话, 自动重启服务是重要
- 微服务应用关注应用的实时监控, 检查架构与业务的相关
- 不同进程运行的服务没有连接, 相同进程中的库也提供了更强的透明性
- 微服务需要为每个服务设置复杂的监控和日志

### Evolutionary Design

- 组件的关键属性是: `独立可替换更新`
- With a monolith any changes require a full build and deployment of the entire application. With microservices, however, you only need to redeploy the service(s) you modified.
- 需要关心的是, 一个服务的改变, 可能会影响其消费者.
- 当组件是远程通信的服务时, 重构比进程内的库难多了
- 如果组件没有清晰的划分, 所做的所有事情就是将组件内部的复杂性提升到了组件间的连接复杂性
- A poor team will always create a poor system - it's very hard to tell if microservices reduce the mess in this case or make it worse.
