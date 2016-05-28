# Docker

## Learn about images & containers

- `docker run hello-world`
 - `docker` - 告诉os, 使用docker
 - `run` - 子命令, 创建并运行docker container(容器)
 - `hello-world` - 要加载到容器的image(镜像)
- `container` - a stripped-to-basics version of a Linux operating system(最基本的Linux 操作系统)
- `image` - a software you load into a container(加载到容器的软件)
- 因此`docker run hello-world`的执行步骤是:
 1. 检查本地是否有`hello-world`镜像. 若没有, 则先下载
 2. 将镜像加载到容器, 并运行
- 一个镜像, 可能是简单的一条命令, 执行完即退出, 也可能很数据库一样复杂.
- Using Docker Engine, you don’t have to worry about whether your computer can run the software in a Docker image — a Docker container can always run it.(这句话, 有点霸气的)
- `docker images` - 显示本地的所有镜像

## Build your own image

- docker has two distinct functions. It is used for starting the Docker daemon and to run the CLI (i.e., to command the daemon to manage images, containers etc.) So docker is both a server, as a daemon, and a client to the daemon, through the CLI.\\
docker有2个完全不同的功能(就像python的type函数). 作为daemon(守护进程), 它是服务器; 通过CLI, 它又是客户端
- docker 命令一览:
 - `attach` - Attach to a running container
 - `build` - Build an image from a Dockerfile
 - `commit` - Create a new image from a container's changes
 - `cp` - Copy files/folders between a container and the local filesystem
 - `create` - Create a new container
 - `diff` - Inspect changes on a container's filesystem
 - `events` - Get real time events from the server
 - `exec` - Run a command in a running container
 - `export` - Stream the contents of a container as a tar archive
 - `history` - Show the history of an image
 - `images` - List images
 - `import` - Create a new filesystem image from the contents of a tarball
 - `info` - Display system-wide information
 - `inspect` - Return low-level information on a container or image
 - `kill` - Kill a running container (which includes the wrapper process and everything inside it)
 - `load` - Load an image from a tar archive
 - `login` - Log in to a Docker Registry
 - `logout` - Log the user out of a Docker Registry
 - `logs` - Fetch the logs of a container
 - `pause` - Pause all processes within a container
 - `port` - Lookup the public-facing port which is NAT-ed to PRIVATE_PORT
 - `ps` - List containers
 - `pull` - Pull an image or a repository from a Docker Registry
 - `push` - Push an image or a repository to a Docker Registry
 - `rename` - Rename a container.
 - `restart` - Restart a container
 - `rm` - Remove one or more containers
 - `rmi` - Remove one or more images
 - `run` - Run a command in a new container
 - `save` - Save an image to a tar archive
 - `search` - Search for an image in the Docker index
 - `start` - Start a container
 - `stats` - Display a live stream of one or more containers' resource usage statistics
 - `stop` - Stop a container
 - `tag` - Tag an image into a repository
 - `top` - Lookup the running processes of a container
 - `unpause` - Unpause all processes within a container
 - `version` - Show the Docker version information
 - `wait` - Block until a container stops, then print its exit code
- docker的目录将作为`context`(上下文), 它包含了创建镜像所需的一切
- 编写`Dockerfile`:
 1. `FROM docker/whalesay:latest` - 加载基镜像
 2. `RUN apt-get -y update && apt-get install -y fortunes` - 将指定软件安装到镜像中
 3. `CMD /usr/games/fortune -a | cowsay` - 指示软件运行
- `docker build -t docker-whale .` - 创建docker镜像. `-t 镜像名`, `.`表示当前目录
 1. `Step 0 : FROM docker/whalesay:latest` - docker加载`whalesay`镜像, 若本地不存在,需要下载
 2. `Step 1 : RUN apt-get -y update && apt-get install -y fortunes` - 下载安装所需的软件到镜像中
 3. `Step 2 : RUN apt-get install -y fortunes` - 安装镜像
 4. `Step 3 : CMD /usr/games/fortune -a | cowsay` - 完成创建过程

## Tag, push, and pull your image

- 镜像列表`REPOSITORY`字段若形如`docker-whale`, 只是展示了仓库名, 不包括命名空间. 为了方便将镜像发布到Docker Hub上, 需要加上自己的Docker Hub用户名, 编程`kissg/docker-whale`的形式
- `docker tag 7d9495d03763 maryatdocker/docker-whale:latest` - 为镜像打上标签
- 当本地存在与远端同名的镜像, `pull`操作将不会进行
- `docker rmi`命令即可以接 image ID, 也可以接 image name
