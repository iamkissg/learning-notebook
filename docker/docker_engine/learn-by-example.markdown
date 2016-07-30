# Learn By Example

## Hello world in a container

- `docker run <image> command`
 - `-t` - assigns a pseudo-tty or terminal inside the new container.
 - `-i` - allows you to make an interactive connection by grabbing the standard in (`STDIN`) of the container.
 - `-d` -  runs the container in the background (to daemonize it).
 - `-P` - map any required network ports inside container to host
 - `<image>:<tag>` - 指定某一版本的镜像，默认是最新的（latest） - 最好每次都指定镜像的 tag
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
