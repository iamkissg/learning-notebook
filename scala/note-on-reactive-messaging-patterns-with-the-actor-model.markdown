# 响应式编程

## Chapter 2

### Programming with Scala

- Scala - You may find that you almost never use `var` as a `constructor argument` but maybe sometimes you will.
- Scala - Any expression outside a method is executed when a new instance of the ShoppingCart is created. The expressions within the body of the class, whether used to initialize val or var references or just invocations of methods on this or other objects, are all part of the construction process. 类定义中, 方法之外的所有表达式都将被执行, 可以视为构造函数
- Scala - 没有声明 val 或 var 的构造参数 means that Scala will not generate a field or any sort of accessor method, neither read nor write, 因此, 这种构造参数应该是临时的
- Scala - 不用 `.` 和 `()` 调用函数或方法, 实际是一种中缀表达式 (infix notation, 左-中-右, 所以第一个参数先于函数/方法名, 之后是第二个参数)
- Scala - 不需要也不应该用 `return`, Scala 将方法内的最后一条表达式的结果作为返回值
- Functional programming - Things are expected to be immutable. Scala 的可变和不可变集合在两个分离的库中
- Scala - 不同于 Java, 可以在任意位置而不仅仅是文件顶部 `import`
- Scala - 不能用符号作为方法名, 因此没有操作符重载的问题. 居然还可以用 `!` 作为方法名
- Scala - `implicit` 关键字有点像设置默认值. 在函数或方法的参数列表中使用 `implicit` 就相当于声明了一个默认参数. `implicit` 的滥用会降低代码可读性
- Scala - 创建样本类不需要 `new` 关键字, 是最简单的创建值不可变对象的方式. 定义样本类时, 参数自动被声明为 `val`, 并且 Scala 编译器会自动生成如 `equals()`, `hashCode()` 的方法. 可以像普通类参数一样通过点标记法访问.

```scala
// map + pattern matching
Vector(1,2,3) map {
  case 1 => println("One") // printed first
  case 2 => println("Two") // printed second
  case 3 => println("Three") // printed third

}
```
- Scala - You may find that you almost never use `var` as a `constructor argument` but maybe sometimes you will.
- Scala - Any expression outside a method is executed when a new instance of the ShoppingCart is created. The expressions within the body of the class, whether used to initialize val or var references or just invocations of methods on this or other objects, are all part of the construction process. 类定义中, 方法之外的所有表达式都将被执行, 可以视为构造函数
- Scala - 没有声明 val 或 var 的构造参数 means that Scala will not generate a field or any sort of accessor method, neither read nor write, 因此, 这种构造参数应该是临时的
- Scala - 不用 `.` 和 `()` 调用函数或方法, 实际是一种中缀表达式 (infix notation, 左-中-右, 所以第一个参数先于函数/方法名, 之后是第二个参数)
- Scala - 不需要也不应该用 `return`, Scala 将方法内的最后一条表达式的结果作为返回值
- Functional programming - Things are expected to be immutable. Scala 的可变和不可变集合在两个分离的库中
- Scala - 不同于 Java, 可以在任意位置而不仅仅是文件顶部 `import`
- Scala - Scala 允许用符号作为方法名, 比如用 `!` 作为方法名
- Scala - `implicit` 关键字有点像设置默认值. 在函数或方法的参数列表中使用 `implicit` 就相当于声明了一个默认参数. `implicit` 的滥用会降低代码可读性
- Scala - 创建样本类不需要 `new` 关键字, 是最简单的创建值不可变对象的方式. 定义样本类时, 参数自动被声明为 `val`, 并且 Scala 编译器会自动生成如 `equals()`, `hashCode()` 的方法. 可以像普通类参数一样通过点标记法访问.

```scala
// map + pattern matching
Vector(1,2,3) map {
  case 1 => println("One") // printed first
  case 2 => println("Two") // printed second
  case 3 => println("Three") // printed third

}
```

### Programming with Akka

- The Akka toolkit was created to address the failings of common multithreaded programming approaches, distributed computing, and fault tolerance.
- It does so by using the Actor model, which provides powerful abstractions that make creating solutions around concurrency and parallelism much easier to reason about and succeed in.
- Akka, Actor 模型移除了并发编程的常见问题, 如死锁, 活锁, 低效的代码, 将线程作为第一级编程模型.

#### Actor System

- Akka 应用必须创建一个 `ActorSystem`, 它有一个 actor 的层级结构, 所有 actor 共享同一份配置
- The Akka toolkit design prefers that all application values that are expected to change between environments are `configured` rather than hard-coded inside actors. 配置而不是硬编码
- 可以为一个单一应用创建多个 `ActorSystem` 实例, 但最好是为每个应用创建一个 `ActorSystem` (Play 框架会创建它自己的 ActorSystem, 因此应用会有 2 个 ActorSystem 实例)
- If you want one ActorSystem to collaborate with another ActorSystem, use `Akka remoting`
- A single ActorSystem can span JVMs if you use an Akka cluster
- When an actor system is created, a few actors are created along with it: root guardian, user guardian, system guardian. 应用创建的其他 actor 将安置在 user guardian 之下
- Supervision 是 Akka 提供的一个扩展, 帮助开发高度弹性的应用. 父 actor 创建了子 actor 之后, 将自动监管子 actor.
- 通过 `ActorSystem.actorOf()` 直接在 user guardian 下创建 actor
- `!` 方法基本等价于 `tell()` 方法. 使用 `tell()` 方法时, 需要传 2 个参数: 消息实例与 ActorRef
    - `processManagerRef ! BrokerForLoan(banks)` 等价于 `processManagerRef.tell(BrokerForLoan(banks), self)`
- When you ask the ActorSystem to create a new actor, it doesn’t return the actor instance. Instead, it returns an ActorRef. 不必将 value holder 命名为 xxxRef, 去掉 `Ref`
- user guardian actor 被命名为 user, 是一个自动防故障组件.
- 所有 actor 都挂在 user 之下不如创建一个 actor 的层级结构, 一个原因是: user 需要为所有应用创建的 actor 负责, 是不科学的做法.
- 防止 user 一直处理应用崩溃, 一个做法是使用一个 user 的子 actor 作为应用的顶级 actor, 并分类
- 当没有 actor 的引用时, 可调用 ActorSystem 的 `actorSelection()` 方法, 用路径创建 actor 的层级关系
- `actorSelection()` 方法返回一个 `ActorSelection`, 也可以被用于发送消息. 比 ActorRef 慢, 且功能更少. 但是`接受通配符`!, 可以广播消息

```scala
val system = ActorSystem("ReactiveEnterprise")
...
val selection = system.actorSelection("/user/*")

selection ! FlushAll()
```

#### Implementing Actors

- 所有 Akka actors 必须扩展 `akka.actor.Actor` 特质. 并且, 必须支持 `receive`
- `Actor` 特质已经定义了 `preStart`, `postStop`, `preRestart`, `postRestart`. 将在 actor 启动停止重启的时候自动调用. 被覆盖.
- actor 有一个 `ActorContext`, 通过 `context()` 方法访问. 它可用于使用一些底层实现, 比如创建子 Task actor
- Actor 模型区别的对象模型的一个特征是: actor 可以动态地改变其行为. 设计原本中称为`状态模式`. 通过使用 `ActorContext`, actor 的行为可以从一个 receive 块切换到另一个 (context.become(), context.unbecome())
- 小心 `sender()`. 因为它是函数, 而不是 `val`. 该函数只有闭包被执行时才会执行. (不解)

```scala
case calculateRisk: CalculateRisk =>
  context.system.scheduleOnce(1 minute) {
    sender ! UnfinishedCalculation()
  
}
// 应修改为
case calculateRisk: CalculateRisk =>
  val requestSender = sender
  context.system.scheduleOnce(1 minute) {
    requestSender ! UnfinishedCalculation()
  
}
```

#### Supervison

- 当子 actor 挂掉时, 父 actor 的处理方式取决于: 1. 子 actor 的挂掉方式; 2. 父 actor 的恢复策略
- 默认地, 所有父 actor 继承了默认的 `supervisorStrategy`, 实现了:
    - ActorInitializationException: 挂掉的 actor 将停止
    - ActorKilledException: 子 actor 将停止
    - Exception: 子 actor 被重启
    - 所有其他 Throwable 类型将上抛
- 覆盖 supervisorStrategy 由 2 部分组成:
    - 实例化一个 SupervisorStrategy 子类, AllForOneStrategy 或 OneForOneStrategy.
    - 声明一个 `Decider`, 可以是 Escalate, Restart, Resume, or Stop.
        - Escalate - 向上再抛出
        - Restart - 重启, 不再是原来的 actor
        - Resume - 保留了当前 actor 的完整状态.

#### 远程

- Akka 支持不同 `ActorSystem` 实例之间基于网络的远程访问, 采用`点对点`的通信机制
- 一台 JVM 上的 actor 通过发送消息与另一台 JVM 上的 actor 直接通信, (异步)
- ActorSystem 可以跨节点. 不必为每个节点上的 ActorSystem 取不同的名字, 因此 actor 的`ActorPath` 包括了主机名和 ActorSystem 名
- 综上, actor 在位置上是透明的, 就好象所有 actor 都位于一个超大的 JVM 上一样.
- JVM 不一定跑在不同物理机上, 其实也可以跑在一台物理机上分离的虚拟服务器上
- 使用网络通信的好处是, 可以跨多个服务器节点. 但也引入了网络的问题: 带宽, 延迟等
- actor 之间发送的消息本身必须经过序列化
- Akka 默认使用 Java 的序列化机制, 但是性能和 size 都不佳. 可通过配置文件指定序列化工具 (推荐 Protocol Buffers 或 Kryo Serialization), 并取消 Java 自带的. 配置如下:

```
# application.conf for ActorSystem: RiskRover
akka {
      actor {
            serializers {
      proto = "akka.remote.serialization.ProtobufSerializer"
      kryo = "com.romix.akka.serialization.kryo.KryoSerializer"
      ...
    
        }
            serialization-bindings {
      "java.io.Serializable" = none
      ...
    
        }
            kryo {
      type = "graph"
      idstrategy = "incremental"
      serializer-pool-size = 16
      buffer-size = 4096
      max-buffer-size = -1
      ...
    
        }
  
    }
}
```

- 要在单台 JVM 上对 ActorSystem 实现 Akka 远程, 最小配置如下:

```
# application.conf for ActorSystem: RiskRover
akka {
  ...
      actor {
    # default is: "akka.actor.LocalActorRefProvider"

    provider = "akka.remote.RemoteActorRefProvider"
    ...
    }

  remote {
    # actors at: akka.tcp://RiskRover@hounddog:2552/user

    enabled-transports = ["akka.remote.netty.tcp"]
    netty.tcp {
      hostname = "hounddog"
      port = 2552
    
    }
  }
}
```

- Akka 默认使用 `LocalActorRefProvider`, 但要在不同 JVM 上引用 actor, 需要使用 `RemoteActorRefProvider`.
- 远程创建: 本地 actor 可以创建远程子 actor, 这是一直减负的方式
- 远程查询: 本地 actor 可以查询远程 actor, 即使不是远程 actor 的 owner 或 supervisor. 类似于 c-s 模式, 但不同是可以相互通信
- 使用配置文件是 cleanest 和最抽象的创建远程 actor 的方式. 以下, deploymnt 表达式的意思是: 如果创建了 actor, 并命名为 `riskManager1`, 那么将其创建到 RiskyBussiness@bassethound:2552 的系统上.

```
# application.conf for ActorSystem: RiskRover
akka {
  ...
  actor {
    provider = "akka.remote.RemoteActorRefProvider"
    ...
    deployment {
          /riskManager1 {
        remote = "akka.tcp://RiskyBusiness@bassethound:2552"
      }
    }
  }
}
```

- `RemoteRefProvider` 告知 `RiskyBusiness` 系统创建一个 actor 在远程系统上. 创建完成后, 远程 actor 部署在特殊的以 `/remote` 开头的路径上, 与 `/user` 同级
- 为使远程工作正常, 远程子 actor 的类型在两个系统上都必须可用. 并且, 消息必须是可压缩的
- 尽管成功创建了 actor, 也发送了消息, 但部分远程通信还是会丢失. 因此需要收到消息的 actor 能够回应, 普通以 `ActorRef` 命名发送 actor, 远程时用 `RemoteActorRef`. 
