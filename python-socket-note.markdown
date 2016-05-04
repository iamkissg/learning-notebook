- 网络传输,首先要考虑的是如何准确地定位网络上的主机,其次是传输:
 - ip层负责网络主机的定位,由ip地址可以唯一地确定internet上的一台主机
 - 传输层负责面向应用的可靠或不可靠的数据传输机制

> - **A network socket is an endpoint of a connection across a computer network. More precisely, a socket is a handle that a local program can pass to the the networking api to use the connection.**
- **A socket api is an api, usually provided by the os, that allows application program to control and use network sockets.**
- In the Berkeley sockets standard, sockets are a form of file descriptor(a file handle): you can read, write, open, and close.
- **A socket address is the combination of an ip address and a port number.**
- Sockets need not have an address, but if a program binds a socket to an address, the socket can be used to receive data sent to that address. Based on this, internet sockets deliver incoming data packets to the appropriate application process or thread.
- An Internet socket is charaterized by at least the following:
 - Local socket address: Local ip address and port number
 - Protocol: tcp, udp, raw ip
 - (a socket that has been connected to another socket also has a remote socket address)
- A tcp server may serve clients concurrently, the server creates one socket for each client, each mapped to its own server-client process. **These sockets share the same local socket address from the point of view of the tcp server, and have a different remote address for each client**
- A udp server does not create new child process for every concurrently served client, but the same process handles incoming data packets from all remote clients sequentially through the same socket. It implies that udp sockets are not identified by the remote address, but only by the local address, although each message has an associated remote address.
- Internet socket types:
 - datagram sockets, which use udp
 - stream sockets, which use tcp
 - raw sockets(or raw ip sockets), typically available in routers and other network equipment. **Here the transport layer is bypassed, and the packet headers are made accessible to the application**
 - ...
- Communicating local and remote sockets are socket pairs, i.e. local and remote socket addresses. In the p tcp case, each unique socket pair is assigned a socket number, while in the udp case, each unique local socket address is assign a socket number.
- The socket is primarily a concept used in the **transport layer** of the Internet model.

> - Berkeley socket is an api for Internet sockets and Unix domain sockets, used for IPC.
- The api represents a socket - an abstract representation(handle) for the local endpoint of a connection - as a file descriptor.

> - In computer science, IPC refers specifically to the mechanism an os provides to allow processes it managees to **share data.**
- Typically, applications can use IPC categorized as clients and servers, where the client requests data and the server responds to the client requests.

> - In computer networking, a port is an endpoint of communication in an os.
- **A port is a logical construct that identifies a specific process or a type of service.**
- The protocols that primarily use ports are the transport layer protocols.
- Ports are unnecessary on direct point-to-point linkswhen the computers at each end can only run one program at a time.
- **Ports became necessary after computers became capable of executing more than one program at a time and were connected to modern packet-switched networks.**
- In the client-server model of application architecture, the ports that network clients connect to for server initiation provide a multiplexing service. After initial communication binds to the well-known port number, this port is freed by switching each instance of service requests to a dedicated, connection specific port number, so that additional clients can be served.

> Why we use port instead of pid to specific a process?
1. A process can listen on multiple ports
2. Several programs can listen on the same port?
3. Socket should be sperated from process.

> - A tcp socket is an endpoint instance defined by an ip address and a port in the context of either a particular tcp connection or the listening state.
- A port is a virtualisation identifier defining a service endpoint.
- A TCP socket is not a connection, it is the endpoint of a specific connection
- There can be concurrent connections to a service endpoint, because a connection is identified by both its local and remote endpoints, allowing traffic to be routed to a specific service instance.
- j
- socket是操作系统内核的一个数据结构,是网络中节点进行通信的门户,是网络进程的id.

> - 应用层所有的应用进程都可以通过运输层再传送到ip层,这是**复用**.运输层从ip层收到数据后必须指明交付的应用进程,这是**分用**
- 在单个计算机中的进程用进程标识符(process identifier)来标识.在因特网环境下,不能使用pid来标识运行在应用层的各种应用进程,因为因特网上的计算机操作系统种类繁多,不同的操作系统可能使用不同格式的pid.
- 把一个特定机器上运行的特定进程指明为因特网上通信的终点是不可行的,因为进程的创建与撤销都是动态的,通信的一方几乎无法识别对方机器上的进程.另外,往往需要利用目的主机提供的功能来识别终点,而不需要知道具体实现这个功能的进程是哪一个.
- 使用port.虽然通信的终点是应用进程,但只要把传送的报文交到目的主机的某个合适的目的端口,剩下的工作就由tcp来完层.此处的端口为软件端口,有别于路由器或交换机上的硬件端口,它是应用层的各种协议进程与运输实体进行层间交互的一种地址.不同的os具体实现端口的方法可以不同.
- 端口号只具有本地意义,它只是为了标识本地计算机应用层中各进程在和运输层交互时的层间接口.
- 同一个名词socket可以表示多种不同的意思:
 1. 允许应用程序访问联网协议的应用编程api,即运输层与应用层之间的一种接口,称socket api,简称socket
 2. 在socket api中使用的一个函数名也叫socket
 3. 调用socket函数的端口称为socket
 4. 调用socket函数时,其返回值称为socket描述符,也可简称为socket
 5. 在os内核中联网协议中的Berkeley实现,称为socket实现
- 大多数os使用系统调用(system call)的机制在应用程序与操作系统之间传递控制权.系统调用和一般程序设计的函数调用非常相似,只是系统调用将控制权传递给了os内核
- 当某个应用进程启动系统调用时,控制权就从应用进程传递给了系统调用接口,次接口再将控制权传递os,os再将调用传递给某个内部过程,并执行所请求的操作.内部过程一旦执行完毕,控制权再依次返回给应用进程.
- 只要应用程序需要从os获得服务,就要将控制权交给os,os在执行必要的操作后,把控制权返还给应用进程.因此系统调用接口实际上就是应用进程的控制权与os的控制权进行转换的一个接口
- socket是应用进程与传输层协议的接口

- 网络通信,归根结底是进程间的通信!(神来之笔,醍醐灌顶)
- 在网络中,用一个ip地址表示一个节点(计算机或路由);*而在一台计算机中,一个端口号一次只能分配给一个进程,即在一台计算机中,端口号与进程之间是一一对应关系.因此,可以使用ip地址+端口号的方式唯一地确定整个网络中的一个网络进程*(不是太科学的说法)
- 每个socket都用一个半相关描述{协议,本地地址,本地端口}来表示;一个完整的socket则用一个相关描述{协议,本地地址,本地端口,远程地址,远程端口}来表示
- TCP通信的基本步骤:
 - server: socket->bind->listen->while(True){accept->recv->send}->close
 - client: socket->connect->send->recv->close
- UDP通信的基本步骤:
 - server: socket->bind->recvfrom->sendto->close
 - client: socket->sendto->recvfrom->close

Reference:
- www.jianshu.com/p/e062b3dd110c
- en.wikipedia.org/wiki/Network_socket
