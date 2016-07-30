# Docker Overview

- Docker is an open platform for developing, shipping, and running applications.
- Docker 实现了应用与基础设施的分离，基础设施也可能被看作应用来进行管理。
- Docker 将内核容器化与工作流、工具相结合，从而使应用的管理和部署更好更快。
- Docker Engine is a client-server application with these major components:

---

### Docker Engine
 - A server which is a type of long-running program called a daemon process. 作为守护进程的服务器
 - A REST API which specifies interfaces that programs can use to talk to the daemon and instruct it what to do. 用 REST API 向外界提供访问
 - A command line interface (CLI) client.

![Docker Engine Components Flow](engine-components-flow.png)

- CLI 使用脚本或直接的命令，通过Docker REST API 与 Docker 守护进程交互与操作
- 守护进程创建并管理 Docker 对象，包括镜像（image），容器（container)），网络，数据卷（data volume）等等。

---

- Faster delivery of your applications
 - Docker 允许开发者在本地容器上进行开发，然后整合到持续集成与部署的工作流中。
- Deploying and scaling more easily
 - 基于 Docker 容器的平台是高度可移植的，Docker 容器可以在开发者本地主机，数据中心的物理机或虚拟机，云上运行
 - Docker 的移植性与轻量特性使得动态的管理更容易。可以快速地，几乎实时地扩展或削减应用与服务。
- Achieving higher density and running more workloads
 - Docker 适用于高密度（high density）环境，比如在云或PaaS

---

### Docker architecture

- Docker 使用 C/S 架构，客户端与 Docker 守护进程进行通信。Docker 守护进程肩负 **building**，**running**，**distributing containers**的重担。
- Docker client 和 Docker daemon 可以在同一系统下运行，也可以在不同系统下，此时，Docker client 连接到远程 Docker daemon
- Docker client 与 Docker daemon 的通信通过 socket 或 RESTFUL API

![Docker Architecture](architecture.svg)

- Docker daemon 在 Docker Host 上运行，用户不能直接与守护进程交互，必须通过 Docker client
- 以 `docker` 二进制的形式存在，是主要的用户接口，接受用户命令，并与守护进程通信

#### Docker images

- Docker 镜像是**只读**的模板，比如说带 Apache 和其他 Web 应用的 Ubuntu 操作系统。
- 镜像被用于创建容器。
- 可以创建，更新，或直接下载镜像
- Docker images are the **build** conponent of Docker

#### Docker registries

- Docker registries hold images. 包括公有的与私有的
- 公有的 Docker registry 由 Docker Hub 提供。
- Docker registries are the **distribution** component of Docker.

#### Docker containers

- Docker containers are similar to a directory
- A Docker container holds everything that is needed for an application to run.
- Each container is created from a Docker image.
- Each container is an isolated and secure application platform.
- Docker containers are the **run** component of Docker.

---

### How

#### How does a Docker image work

- 镜像由多个层次组成
- Docker 使用 [union file symtem](https://en.wikipedia.org/wiki/UnionFS) 将多个层次组合到一个镜像中
- Union file systems allow files and directories of separate file systems, known as branches, to be transparently overlaid, forming a single coherent file system.\\
Union 文件系统允许分离的文件或目录，被透明地覆盖，从而形成一个单一连贯的文件系统
- Docker 如此轻量的一个原因就在于**多层**。当修改一个镜像时，就创建了一个新层。因此，与虚拟机替换整个镜像或完整地重建镜像不同，Docker 只是添加或修改了一层。不需要发布新的镜像，只要更新就可以了，所以 Docker 镜像的发布快而简单
- 每个镜像都从一个基镜像开始，通过一步步描述式的**指令**在基镜像的基础上创建新的镜像。每一条指令，会在镜像中创建一个层次。指令包括：
 - Run a command
 - Add a file or directory
 - Create an environment variable
 - What process to run when launching a container from this image
- 创建镜像的指令保存为 `Dockerfile` 文件，这是一个基于脚本的文本。当创建一个镜像时，Docker 读取 `Dockerfile` 文件，并执行指令，返回最终的镜像

#### How does a Docker registry work

- The Docker registry is the store for your Docker images.
- 新建好镜像之后，可以推送到公共的 registry，如 Docker Hub，或者保存到私有的 registry
- 使用 Docker client，可以搜索公有 Docker registries 上的镜像，并下载到个人 Docker Host 上，利用下载的镜像创建容器
- Docker hub 提供公有和私有的镜像存储服务

#### How does a Docker container work

- 一个容器由操作系统，用户添加的文件，元数据组成
- 容器由镜像创建而来。
- 镜像告诉 Docker 容器需要包含哪些内容，当容器启动时运行什么进程，以及一些配置数据
- 重要的事情说三遍：Docker image is read-only
- 当 Docker 运行一个容器时，就在镜像的顶部追加了一个读写层（使用 union file system 技术），之后才跑应用

---

### What happens when run a container

- 通过 `docker` 二进制或 API，Docker client 告诉 Docker daemon 运行容器
- 使用 `docker` 加 `run` 选项启动 Docker Engine client 来运行容器
- 比如 Docker client 通过最简单的命令 `docker run -i -t ubuntu /bin/bash` 告诉 Docker daemon：
 - 创建容器的镜像，此处为 `ubuntu`
 - 容器启动时运行的命令，此处为 `/bin/bash`
- 执行上述命令之后，Docker Engine 做了以下工作：
 - 拉取 `ubuntu` 镜像：Docker Engine 会检查本地是否存在名为 `ubuntu` 的镜像。若存在，则用其创建新的容器，否则默认从 Docker Hub 下载镜像
 - 创建新容器：容器由镜像创建而来
 - 分配文件系统，并挂载读写层
 - 分配网络/桥式接口：创建网络接口，用于容器与本地主机的交互
 - 设置 IP 地址：从地址池中查找可用的 IP 地址，绑定
 - 执行指定的进程：运行应用
 - 捕获并提供应用的输出：连接并记录标准输入、标准输出、标准错误，以便用户查看应用的运行情况

---

### The underlying technology

- Docker 以 Go 语言写就，使用了多种内核的功能

#### 命名空间

- Docker 充分利用了 `namespaces` 的技术，以提供隔离的工作区，即所谓的容器。
- 当运行一个容器时，Docker 为容器创建了一个命名空间集
- 这就提供了一个隔离层，每个容器在自己的命名空间内运行，并无法访问外界
- Linux Docker Engine 用到的 命名空间:
 - `pid` 命名空间：进程隔离
 - `net` 命名空间：管理网络接口
 - `ipc` 命名空间：管理 IPC 资源的访问（IPC：InterProcess Communication，进程间通信）
 - `mnt` 命名空间：管理挂载点
 - `uts` 命名空间：隔离内核与版本标识符（UTS：Unix Timesharing System）

#### Control groups

- Linux Docker Engine 还使用了 `cgroups` 技术。
- 隔离地运行应用的一个关键是：让应用们只使用限定的资源，从而确保了主机上同时运行多个容器。
- Control groups 允许 Docker Engine 共享可用的硬件资源给容器，若必要，设置限制与约束，比如限制容器可访问的内存

#### Union file systems

- Union file systems 用于创建层，是 Docker 轻量，快速的关键
- Docker Engine 使用 union file system 为容器提供构建模块（building blocks）
- Docker Engine 可以使用多种 union file system 的变种，如 AUFS，btrfs，vfs，DeviceMapper

#### Container format

- Docker Engine 将所有的组件整合进称为 container format 的包装器
- 默认的容器格式是 `libcontainer`
- 未来，可能会支持 BSD Jails 或 Solaris Zones
