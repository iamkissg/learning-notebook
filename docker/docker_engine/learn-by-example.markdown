# Learn By Example

## Hello world in a container

- `docker run <image> command`
 - `-t` - assigns a pseudo-tty or terminal inside the new container.
 - `-i` - allows you to make an interactive connection by grabbing the standard in (`STDIN`) of the container.
 - `-d` -  runs the container in the background (to daemonize it).
 - `-P` - map any required network ports inside container to host
 - `<image>:<tag>` - 指定某一版本的镜像，默认是最新的（latest） - 最好每次都指定镜像的 tag
 - `--name <container-name>` - name the container
 - `--network=<network>` - add container to a network
 - `-v <volume>` - add data volume to container
 - `-v <src>:<dst>` - mount the host directory into the container at <dst>
 - `--volume-driver=<volume-driver>` - use the volume driver
 - `--volumes-from <container>` - mount data volume from another container
 - `--rm` clean up anonymous volumes when remove a container
- `docker pull` - download images，you can see that each layer of the image has been pulled down
- `docker search <term>` - search imaegs that contain the specified term
 - 官方仓库（official repositories）是由 Docker 公司维护的仓库
 - automated repositories 是自动创建的，允许用户验证源以及镜像的内容
- `docker ps` - Lists running containers.
 - `-l` - return the details of the last container started
 - `-a` - show all containers
- `docker logs` - Shows us the standard output of a container.
 - `-f` - 使 `docker logs` 打印日志像 `tail -f` 命令一样：output appended data as the file grows;
- `docker stop` - Stops running containers.
- `docker start` - start the stopped container back up
- `docker top` - examine the processes running inside a container
- `docker inspect` - return a JSON document containing useful configuration and status information for the specified container
 - `-f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}` - 返回想要的精确的信息
- `docker rm` - remove the stopped container
- `docker images` - list images on the host
 - `--digest` - list image digest values
- `docker commit <container-id> <image-name>[:tag]` - commit a copy of a container to an image
 - `-m` - 同 git commit 的 -m
 - `-a` - for author，指定作者
- `docker build` build an image
 - `-t` - 指定镜像名称
 - `.` - 指明 `Dockerfile` 的位置为当前位置。也可以是其他位置，通常是 `.`
- `docker tag` - add a tag to an existing image. such as: `docker tag 5db5f8471261 ouruser/sinatra:devel`
- `docker push` - push image to repository. By default，Docker Hub
- `docker rmi` - remove image
- `docker network` - show network information
 - `ls` - list network
 - `inspect bridge` - 查看 bridge 网络
 - `disconnect <network> <container>` - remove a container from a network.
 - `create -d <network> <cusmtom-network>` - create network using the given network
 - `connect <network> <container>` - attach container to network



## Run a simple application

- 每次在终端输入 `docker` 就是与 Docker client 进行交互。换言之，Docker client 就是命令行接口（CLI）
- 使用：`[sudo] docker [subcommand] [flags] [arguments] ..`
- 帮助：`docker --help` 或 `docker COMMAND --help`
- `docker run -d -P training/webapp python app.py`

```shell
PORTS
0.0.0.0:49155->5000/tcp
```

- Docker expose port 5000 [the default Python Flask port] to port 49155
- Docker 的网络端口绑定是可配置的。`-P` 是 `-p 5000` 的缩写，它将容器内部的 5000 端口映射到本地主机的高层端口 [临时端口范围，从32768 到 61000]。
- 可以自定义端口绑定，用法是：`-p outside_port:inside_port`。
- 不使用 1:1 的端口映射，是考虑到多个容器端口可能会映射到同一主机端口
- 查看端口映射 - `docker port <container-id> | <container-name> the_look_up_port_in_container`

## Build your own images

- Docker images are the basis of containers
- 镜像分多种：
 - 基镜像 - 由 Docker Inc 提供，用单个单词标识
 - 用户镜像（user image） - 由 Docker 社区提供，并由他们创建并维护，带前缀的，比如`training/python`
- 更新已有镜像
 1. 创建镜像的容器
 2. 进入容器系统，修改容器系统
 3. 使用 `docker commit` 命令，将修改后的容器的一份拷贝转成镜像
- 利用 `Dockerfile` 创建镜像，详情见[另一篇文章](https://github.com/Engine-Treasure/learning-notebook/blob/master/docker/docker-dockerfile-reference.markdown)
 - 每条指令会创建一个新层
 - `FROM` - 指定基镜像
 - `MAINTAINER` - 指定作者（维护者）
 - `RUN` - 在镜像中执行的命令
- 一个镜像不能超过 127 层，这个限制是全局的，用于镜像整体大小的优化
- 使用了某个镜像或其子镜像的镜像，会有一个内容可寻址标识（content-addressable identifier），称为 `digest`（摘要）。只要用于生成镜像的输入不变，摘要值是可预测的。
- When pushing or pulling to a 2.0 registry(?), the `push` or `pull` command output includes the image digest. You can `pull` using a digest value：\\
`docker pull ouruser/sinatra@sha256:cbbf2f9a99b47fc460d422812b6a5adff7dfee951d8fa2e4a98caa0382cfbdbf`
- 还可以用摘要作为 `create`，`run`，`rmi` 命令的引用，甚至 `Dockerfile` 的 `FROM` 都行
- 要删除本地镜像，需要确保基于它的容器不在运行中

## Network containers

- 容器名必须是独一无二的，重用一个容器名时，必须先删除旧的容器
- Docker 使用网络驱动容器提供网络支持。Docker 提供 2 种网络驱动：`bridge` 和 `overlay`，此外，用户还能编写自己的网络驱动扩展，但这是个技术活儿
- Docker Engine 安装好后, 自动包括了 3 个默认的网络:

```shell
$ docker network ls

NETWORK ID          NAME                DRIVER
18a2866682b8        none                null
c288470c46f6        host                host
7b369448dccb        bridge              bridge
```

- Docker 默认使用 `bridge` 网络模式.
- 用户可以断开容器与网络的连接, 但不能删除内建的 `bridge` 网络.
- 网络是一种容器间, 容器与网络间隔离的方式.
- `bridge` 网络受制于运行容器的单个主机上, `overlay` 网络可以包含多个主机
- 根据定义, 网络为容器提供了完整的隔离, 可以在第一次运行容器时为其添加网络: `$ docker run -d --network=my-bridge-network --name db training/postgres`
- Docker 支持将容器添加到多个网络 (就像将主机连接到网络一样), 也可以为运行中的容器添加网络, 使用 `connect`

## Manage data in containers

- 数据卷 (`data volume`) 是一个或多个容器内, 通过 Union File System 专门设计的目录.
- 数据卷为数据持久化与数据共享提供了多个有用的功能:
 - 当容器被创建时, 初始化数据卷. 若用于创建容器的镜像在指定挂载点包含了数据, 这些数据将在卷初始化完成之后被拷贝到新加卷上
 - 数据卷可以被多个容器共享与复用
 - 数据卷修改可直接进行
 - 更新镜像时, 不会修改数据卷
 - 即使容器被删除, 数据卷依旧存在 (数据卷的数据持久化是独立于容器周期的)
- 在使用 `docker create` 和 `docker run` 命令时, 使用 `-v` 标志添加数据卷到容器, 可多次使用 `-v`, 挂载多个数据卷
- 另一种添加数据卷的方法是, 在 `Dockefile` 中使用 `VOLUME` 指令
- 用 docker inspect <container>` 查看容器信息,`Mounts` 下的 `Source` 表示主机上目录的路径, `Destination` 表示卷在容器内部的位置, `RW` 表示容器的可读写情况
- 使用 `-v`, 还可以将主机的指定目录挂载到容器的某个位置(主动的). 若容器中已存在目标目录, 新的挂载会覆盖, 但不删除之前的内容; 当挂载被删除, 原有的内容可被重新访问. (其实很好理解, 原有的挂载是主机的另一个目录, 有新的挂载时, 重映射到新的挂载, 新的挂载退出时, 再映射回原目录)
- 挂载时, 指定的容器内目录 `container-dir` 必须以绝对路径形式给出; `host-dir` 则比较随意, 若指定绝对路径, 则 Docker 会将挂载绑定到指定路径, 若使用非绝对路径 `name`, Docker 会用 `name` 创建一个卷
- 挂载主机目录到容器, 便于测试: 比如挂载源代码到容器内, 然后修改源代码, 实时地观察效果. 此时, 必须用绝对路径指出目录在主机上的路径
- 默认以 `RW` (读写) 模式挂载. 用可以在挂载时指定模式, 比如 `$ docker run -d -P --name web -v /src/webapp:/opt/webapp:ro training/webapp python app.py`
- 由于 `mount` 函数的局限性, 在主机的源目录下移动子目录, 将暴露容器到主机的文件系统. 这为恶意攻击提供了可能
- **主机目录, 默认是主机依赖的 (host-dependent). 因此, 不应用 `Dockerfile` 挂载主机目录, 创建镜像应该是可移动, 可移植的, 而主机目录在所有潜在的主机上不一定存在**
- 共享卷, 是主机独立的 (host-independent), 这意味着任何主机上的容器, 只能有权限, 都能访问该卷
- 使用卷驱动的一种方式是使用 `docker run` 命令. 卷驱动通过 `name` 而不是路径的方式创建卷:

```shell
$ docker run -d -P \
  --volume-driver=flocker \
  -v my-named-volume:/opt/webapp \
  --name web training/webapp python app.py
```

- 另一种使用卷驱动的方式是 `docker volume create` 命令, 在容器使用卷之前, 创建卷: `$ docker volume create -d flocker --name my-named-volume -o size=20GB`
- Docker 默认不改变 OS 设置的标签. (标签系统要求给卷内容打上合适的标签. 若无标签, 安全系统可能会阻止容器内使用卷内容的进程运行)
- 在容器上下文修改标签, 在卷挂载时使用 `:z` 或 `:Z` 后缀. `z` 表示多个容器共享卷内容; `Z`, 表示只有私有卷, 只有当前容器才能使用该卷
- `-v` 还可以挂载一个单一的文件. 命令 `$ docker run --rm -it -v ~/.bash_history:/root/.bash_history ubuntu /bin/bash` 将主机的 bash 历史挂进容器, 当从容器退出时, 主机有容器内运行的 bash 历史
- Containers uses layers in common, saving disk space
- 若有一些想要在多个容器间共享的持久化数据, 最好创建一个命名的数据卷容器 (Data Volume Container), 再从其挂载数据
- 使用 `--volumes-from`, 从另一个容器挂载数据卷: `$ docker run -d --volumes-from dbstore --name db1 training/postgres`.
- 多次使用 `--volumes-from`, 可以对多个容器的数据卷进行融合
- 容器卷挂载是可继承的, 即 d1 从 d0 容器挂载了数据卷, d2 可以从 d1 挂载数据
- 删除挂载卷的容器, 卷不会被删除, 要从硬盘上删除卷, 必须显式地调用 `docker rm -v` 清除所有引用了数据卷的容器
- 除了数据共享, 数据卷还能用于备份, 数据还原, 迁移.
- 命名卷是挂载时, 指定了主机路径的卷, 匿名卷则没有
- 创建容器时, 使用 `--rm`, 将在容器被删除时, 删除幂名卷在宿主机上对应的文件
- 多个容器可共享一个或多个数据卷. 当多个容器对一个单一卷进行写时, 会造成数据损坏.
- 容器内的数据卷, 在 Docker 主机上是可以直接访问的, 因为它们本身就存在于宿主机上. 但大多数情况下, 不应该直接在主机上修改读写数据
