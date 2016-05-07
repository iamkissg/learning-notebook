#图解HTTP

##Chapter1 了解Web及网络基础

- 最初设想的基本理念: 借助多文档之间相互关联形成的超文本(HyperText), 连成可互相参阅的WWW.
- 现在已经提出的3项www构建技术:
 1. 以SGML(standard generalized markup language, 标准通用标记语言)作为***页面***的文本标记语言的html(hypertext markup language, 超文本标记语言)
 2. 作为文档传递协议的http
 3. 指定文档所在地址的url(uniform resource locator, 统一资源定位符)
- 通常使用的网络是在tcp/ip协议族的基础上运作的, http是其一个子集
- tcp/ip是在ip协议的通信过程中, 使用到的协议族的统称
- tcp/ip协议族分4层: 应用层, 传输层, 网络层, 数据链路层:
 1. 应用层 - 决定了向用户提供应用服务时通信的活动
 2. 传输层 - 对应用层, 提供处于网络连接中的两台计算机之间的数据传输
 3. 网络层 - 处理网络上流动的数据包, 数据包是网络传输的最小数据单位
 4. 链路层 - 用来处理连接网络的硬件部分
- ip协议, 网络层, 作用是将各种数据包传送给对方, 其中两个重要的条件是ip地址与mac地址. arp(address resolution protocol). 路由选择. 没人能全面掌握互联网中的传输状况
- tcp协议, 传输层, 作用是提供可靠的**字节流(byte stream)**服务(为了方便传输, 将大块数据分割成以报文段为单位ied数据包进行管理). 3次握手.
- dns服务, 应用层, 提供域名到ip地址的解析服务(计算机既可以被赋予ip地址, 也可以被赋予主机名和域名)
- url是web浏览器等访问web页面时需要输入的网页地址
- uri(uniform resource identifier, 统一资源标识符):
 - uniform - 规定统一的格式可方便处理多种不同类型的资源, 而不用根据上下文环境来识别资源指定的访问方式. 另外, 加入新的协议方案也更容易
 - resource - 资源的定义是"可标识的任何东西", 可以是单一的, 也可以是多数的集合体. 除了文档文件, 图像或服务等能区别于其他类型的, 全都可以作为资源?
 - identifier - 表示可标识的对象
- uri就是由某个协议方案表示的资源的定位标识符, 协议方案指访问资源所使用的协议类型名称
- uri用字符串标识某一互谅网资源, 而url表示资源的地点. 因此url是uri的子集
- 绝对uri的格式:

```text
http://      user:passwd   @    www.example.com   :    80    /dir/index.html    ?uid=1         #ch1
   |              |                    |                |           |              |             |
协议方案名   登录信息(认证)        服务器地址         端口号   带层次的文件路径  查询字符串  片段标识符
```

- 按实际情况, 两台计算机作为客户端和服务器端的角色可互换, 但就仅一条通信路线而言, 服务器端和客户端的角色是**确定的**, http协议能明确区分客户端与服务器端
- 请求报文由`请求方法`, `请求uri`, `协议版本`, 可选的`请求首部字段`和`内容实体`构成

```text
方法        uri         协议版本
 |           |              |
post    /form/entry     HTTP/1.1
Host: kissg.me
Connection: keep-alive                               ---请求首部
Content-Type: application/X-www-form-urlencoded
Content-Length: 16
name=kissg&age=22
     |
  内容实体
```

- 响应报文基本上由`协议版本`, `状态码`, `用以解释状态码的原因短语`, 可选的`首部响应字段`和`实体主体`构成

```text
协议版本     状态码   状态码的原因短语
   |            |         |
HTTP/1.1       200        OK
Date: Tue, 10 Jul 2012 06:50:15 GMT           ----响应首部字段
Content-Length: 362
Content-Type: text/html
//此处有空行!!!
<html>
...
  |
 主体
```

- http是无状态的协议, 它自身不对请求和响应之间的通信状态进行保存, 这是为了更快速地处理大量事务, 确保协议的可伸缩性, 而特意将http协议设计得简单
- 状态保持的功能由cookie提供
- 指定请求uri的几种方式:
 1. uri为完整的uri: `GET http://hackr.jp/index.htm HTTP/1.1`
 2. 请求首部Host中写明网络域名或ip地址:

```text
GET /index.htm HTTP/1.1
Host: hackr.jp
```

- 如果不是访问特定资源而是对服务器本身发起请求, 可用`*`代替uri, 如下面的例子是查询http服务器支持的http method种类:

```text
OPTIONS * HTTP/1.1
```

- http方法:
 1. get: 获取资源. 请求访问已被uri识别的资源, 指定的资源经服务器端解析后返回响应内容
 2. post: 传输实体主体. get方法也可以传输实体的主体, 但一般不用get, 而用post. post的主要目的并不是获取响应的主体内容
 3. put: 传输文件. 要求在报文的主体中包含文件内容, 然后保存到请求uri指定的位置. HTTP/1.1的put方法自身不带验证机制, 任何人都可以上传文件, 存在安全性问题
 4. head: 获取报文首部. 与get一样, 只是不返回报文主体内容. 用于确认uri的有效性及资源更新的日期时间等
 5. delete: 删除文件. 与put方法相反, 同样不带验证机制
 6. options: 询问支持的方法.
 7. trace: 




