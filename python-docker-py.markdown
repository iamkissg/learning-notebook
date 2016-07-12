# Notes on docker-py

- docker-py是一个python写作成docker api客户端

## Client API

- `Client`类的实例允许用户与docker daemon进行通信
- 参数:
 - base\_url (str): 协议+主机名+端口, 指定docker服务器的位置
 - version (str): 客户端将会使用的api版本, `'auto'`使用服务器提供的api版本
 - timeout (int): http请求超时时间, 以秒为单位
 - tls(bool or TLSConfig): 等价于`docker --tls`

### attach

- 函数`.logs`包装了该方法. 当需要获取或流化容器的输出时, 可调用, 而不需要先下载完整的日志
- 参数:
 - container (str): 连接到的容器
 - stdout (bool): 获得标准输出 STDOUT
 - stderr (bool): 获得标准输入 STDERR
 - stream (bool): 返回一个迭代器(iterator)
 - logs (bool): 获得之前所有的输出
- 以generator或str返回镜像的日志或输出

### build

- 类似于`docker build`命令, 需要设置`path`和`fileobj`. `path`可以是本地路径或远程url. `fileobj`必须是dockerfile的一个可读的类文件对象
- 如果已有tar文件作为docker build context(包含了dockerfile), 向`fileobj`传递可读类文件对象的同时, 需要指定`custom_context=True`. 若流(Stream?)也被压缩了, 需要设置`encoding`为恰当的值(比如gzip)
- 参数:
 - path (str): Path to the directory containing the Dockerfile
 - tag (str): A tag to add to the final image
 - quiet (bool): Whether to return the status
 - fileobj: A file object to use as the Dockerfile. (Or a file-like object)
 - nocache (bool): Don't use the cache when set to True
 - rm (bool): Remove intermediate containers. The docker build command now defaults to --rm=true, but we have kept the old default of False to preserve backward compatibility
 - stream (bool): Deprecated for API version > 1.8 (always True). Return a blocking generator you can iterate over to retrieve build output as it happens
 - timeout (int): HTTP timeout
 - custom\_context (bool): Optional if using fileobj
 - encoding (str): The encoding for a stream. Set to gzip for compressing
 - pull (bool): Downloads any updates to the FROM image in Dockerfiles
 - forcerm (bool): Always remove intermediate containers, even after unsuccessful builds
 - dockerfile (str): path within the build context to the Dockerfile
 - container\_limits (dict): A dictionary of limits applied to each container created by the build process. Valid keys:
  - memory (int): set memory limit for build
  - memswap (int): Total memory (memory + swap), -1 to disable swap
  - cpushares (int): CPU shares (relative weight)
  - cpusetcpus (str): CPUs in which to allow execution, e.g., "0-3", "0,1"
  - decode (bool): If set to True, the returned stream will be decoded into dicts on the fly. Default False.
- 以generator形式返回创建的输出

### commit

- 与`docker commit`命令相同
- 参数:
 - container (str): The image hash of the container
 - repository (str): The repository to push the image to
 - tag (str): The tag to push
 - message (str): A commit message
 - author (str): The name of the author
 - changes (str): Dockerfile instructions to apply while committing
 - conf (dict): The configuration for the container. See the Docker remote api for full details.

### containers

- 列出容器. 与`docker ps`命令相同
- 参数:
 - quiet (bool): Only display numeric Ids
 - all (bool): Show all containers. Only running containers are shown by default
 - trunc (bool): Truncate output
 - latest (bool): Show only the latest created container, include non-running ones.
 - since (str): Show only containers created since Id or Name, include non-running ones
 - before (str): Show only container created before Id or Name, include non-running ones
 - limit (int): Show limit last created containers, include non-running ones
 - size (bool): Display sizes
 - filters (dict): Filters to be processed on the image list. Available filters:
  - exited (int): Only containers with specified exit code
  - status (str): One of restarting, running, paused, exited
  - label (str): format either "key" or "key=value"
  - id (str): The id of the container.
  - name (str): The name of the container.
  - ancestor (str): Filter by container ancestor. Format of <image-name>[:tag], <image-id>, or <image@digest>.
  - before (str): Only containers created before a particular container. Give the container name or id.
  - since (str): Only containers created after a particular container. Give container name or id.
- 以字典的形式返回系统中容器(们)的信息

### connect\_container\_to\_network

- 将容器连接到网络上
- 参数:
 - container (str): 容器的id或名称
 - net\_id (str): 网络 id

### copy

- 与`docker cp`命令相同. 从容器中获取文件或目录. 对于1.20版以上已过时, 用`get_archive`替代
- 参数:
 - container(str): 指定容器
 - resource(str): 资源路径
- 以str形式返回文件内容

### create\_container

- 创建容器. 参数类似于`docker run`命令的各参数, 但不支持`-a`参数
- `mem_limit`变量接受浮点值或能指明容量的字符串(如'1000k', '1g'). 若使用字符串, 但未指定单位, 默认使用bytes
- 在1.10版本以上, 使用`volumes_from`和`dns`将引起TypeError异常. 这些参数需要作为`host_config`字典的一部分进行传递
- 参数:
 - image (str): The image to run
 - command (str or list): The command to be run in the container
 - hostname (str): Optional hostname for the container
 - user (str or int): Username or UID
 - detach (bool): Detached mode: run container in the background and print new container Id
 - stdin_open (bool): Keep STDIN open even if not attached
 - tty (bool): Allocate a pseudo-TTY
 - mem_limit (float or str): Memory limit (format: [number][optional unit], where unit = b, k, m, or g)
 - ports (list of ints): A list of port numbers
 - environment (dict or list): A dictionary or a list of strings in the following format ["PASSWORD=xxx"] or {"PASSWORD": "xxx"}.
 - dns (list): DNS name servers
 - volumes (str or list):
 - volumes_from (str or list): List of container names or Ids to get volumes from. Optionally a single string joining container id's with commas
 - network_disabled (bool): Disable networking
 - name (str): A name for the container
 - entrypoint (str or list): An entrypoint
 - cpu_shares (int): CPU shares (relative weight)
 - working_dir (str): Path to the working directory
 - domainname (str or list): Set custom DNS search domains
 - memswap_limit (int):
 - host_config (dict): A HostConfig dictionary
 - mac_address (str): The Mac Address to assign the container
 - labels (dict or list): A dictionary of name-value labels (e.g. {"label1": "value1", "label2": "value2"}) or a list of names of labels to set with empty values (e.g. ["label1", "label2"])
 - volume_driver (str): The name of a volume driver/plugin.
 - stop_signal (str): The stop signal to use to stop the container (e.g. SIGINT).
- 以带镜像`Id`和`Warnings`键的字典形式返回
- `docker.utils.parse_env_file`是一个用于环境文件的函数

```python
>>> import docker.utils
>>> my_envs = docker.utils.parse_env_file('/path/to/file')
>>> docker.utils.create_container_config('1.18', '_mongodb', 'foobar',  environment=my_envs)
```

### create\_network

- 创建网络, 类似于`docker network create`命令
- 参数:
 - name (str): Name of the network
 - driver (str): Name of the driver used to create the network
 - options (dict): Driver options as a key-value dictionary
- 以dict的形式返回网络引用对象

### create\_volume

- 创建并注册一个命名卷
- 参数:
 - name (str): Name of the volume
 - driver (str): Name of the driver used to create the volume
 - driver_opts (dict): Driver options as a key-value dictionary
- 以dict的形式返回卷引用对象

### diff

- 检查容器上的文件系统的变化
- 参数:
 - container (str): 指定容器
- 返回str

### disconnect\_container\_from\_network

- 将容器从网络断开
- 参数:
 - container (str): container-id/name to be disconnected from a network
 - net\_id (str): network id

### events

- 与`docker events`命令相同: 从服务器获得实时事件. `events`函数返回blocking generator, 用户可以对其进行迭代以解析出事件
- 参数:
 - since (UTC datetime or int): get events from this point
 - until (UTC datetime or int): get events until this point
 - filters (dict): filter the events by event time, container or image
 - decode (bool): If set to true, stream will be decoded into dicts on the fly. False by default.

### execute

- 与1.2.0版本以上过时, 使用`exec_create`和`exec_start`替代
- 参数:
 - container (str): Target container where exec instance will be created
 - cmd (str or list): Command to be executed
 - stdout (bool): Attach to stdout of the exec command if true. Default: True
 - stderr (bool): Attach to stderr of the exec command if true. Default: True
 - since (UTC datetime or int): Output logs from this timestamp. Default: None (all logs are given)
 - tty (bool): Allocate a pseudo-TTY. Default: False
 - user (str): User to execute command as. Default: root
- 返回带执行`Id`的字典

### exec\_inspect

- 返回exec命令的低层信息
- 参数:
 - exec\_id (str): ID of the exec instance
- 返回字典

### exec\_resize

- 通过指定exec命令调整ttf会话的大小
- 参数:
 - exec\_id (str): ID of the exec instance
 - height (int): Height of tty session
 - width (int): Width of tty session

### exec\_start

- 启动先前设置的exec实例
- 参数:
 - exec\_id (str): ID of the exec instance
 - detach (bool): If true, detach from the exec command. Default: False
 - tty (bool): Allocate a pseudo-TTY. Default: False
 - stream (bool): Stream response data. Default: False
- 返回generator或str. 若`steam=True`, generator产生响应块(a generator yielding response chunks). 字符串包含响应数据

### export

- 以tar压缩包的形式向标准输出stdout输出文件系统的内容
- 参数:
 - container (str): 指定容器
- 以str形式返回文件系统的tar档案

### get\_archive

- 从容器中, 以tar档案形式解析文件或目录
- 参数:
 - container (str): The container where the file is located
 - path (str): Path to the file or folder to retrieve
- 返回tuple, 第一个元素是原始的数据流, 第二个参数是一个包含指定`path`上`stat`信息的字典

### get\_image

- 从docker daemon获得镜像. 类似于`docker save`命令
- 参数:
 - image (str): Image name to get
- 返回一个urllib3.response.HTTPResponse对象.

### history

- 显示镜像历史
- 参数:
 - image (str): The image to show history for
- 返回包含镜像历史的str

### images

- 列举镜像. 与`docker images`命令相同
- 参数:
 - name (str): Only show images belonging to the repository name
 - quiet (bool): Only show numeric Ids. Returns a list
 - all (bool): Show all images (by default filter out the intermediate image layers)
 - filters (dict): Filters to be processed on the image list. Available filters:
  - dangling (bool)
  - label (str): format either "key" or "key=value"
- 若`quiet=True`, 则返回list; 否则返回dict

### import\_image

- 与`docker\_import`命令相同
- 若`src`是字符串, 将首先视为本地系统上的tarball的路径. 若读取错误, src被视作远程url以获取image. 可以传入一个开放式文件处理(open file handle)作为`src`, 此时将从指定的文件读取数据
- 若没有使用`src`, 但指定了`image`, `image`参数将被用于导入一个存在的镜像
- 参数:
 - src (str or file): Path to tarfile, URL, or file-like object
 - repository (str): The repository to create
 - tag (str): The tag to apply
 - image (str): Use another image like the FROM Dockerfile parameter

### import\_image\_from\_data

- 类似于`.import_image()`, 但是允许从内存中导入字节数据
- 参数:
 - data (bytes collection): Bytes collection containing valid tar data
 - repository (str): The repository to create
 - tag (str): The tag to apply

### import\_image\_from\_file

- 类似于`.import_image()`, 但是仅支持从磁盘上的tar文件导入. 若文件不存在, 抛出IOError
- 参数:
 - filename (str): Full path to a tar file.
 - repository (str): The repository to create
 - tag (str): The tag to apply

### import\_image\_from\_url

- 类似于`.import_image()`, 但是仅支持从url文件导入.
- 参数:
 - url (str): A URL pointing to a tar file.
 - repository (str): The repository to create
 - tag (str): The tag to apply

### import\_image\_from\_image`

- 类似于`.import_image()`, 但是仅支持从另一个镜像导入, 类似于dockerfile参数的`FROM`
- 参数:
 - image (str): Image name to import from
 - repository (str): The repository to create
 - tag (str): The tag to apply

### info

- 显示系统范围内的信息, 与`docker info`命令相同
- 以字典形式返回

### inspect\_container

- 与`docker inspect`命令相同. 但仅支持容器(检查)
- 参数:
 - container (str): The container to inspect
- 返回dict. 与`docker inspect`的输出几乎一样, 只是以单个dict返回

### inspect\_image

- 与`docker_inspect`命令相同, 但仅支持镜像
- 参数:
 - image\_id (str): The image to inspect
- 返回dict. 与`docker inspect`的输出几乎一样, 只是以单个dict返回

### inspect\_network

- 通过id解析网络信息
- 参数:
 - net\_id (str): network id
- 返回网络信息的字典

### inspect\_volume

- 通过name解析卷
- 参数:
 - name (str): volume name
- 返回卷信息的字典

### kill

- 杀死一个容器, 或向一个容器发送一个信号
- 参数:
 - container (str): The container to kill
 - signal (str or int): The signal to send. Defaults to SIGKILL

### load\_image

- 加载先前被`Client.get_image`(或`docker save`)保存的镜像. 类似于`docker load`
- 参数:
 - data (binary): Image data to be loaded

### login

- 与`docker login`命令几乎相同, 但不是交互式的
- 参数:
 - username (str): The registry username
 - password (str): The plaintext password
 - email (str): The email for the registry account
 - registry (str): URL to the registry. Ex:https://index.docker.io/v1/
 - reauth (bool): Whether refresh existing authentication on the docker server.
 - dockercfg\_path (str): Use a custom path for the .dockercfg file (default $HOME/.dockercfg)
- 返回dict. 对于登录请求的响应

### logs

- 与`docker logs`命令相同. `stream`参数使`logs`函数返回一个blocking generator.
- 参数:
 - container (str): The container to get logs from
 - stdout (bool): Get STDOUT
 - stderr (bool): Get STDERR
 - stream (bool): Stream the response
 - timestamps (bool): Show timestamps
 - tail (str or int): Output specified number of lines at the end of logs: "all" or number. Default "all"
 - since (datetime or int): Show logs since a given datetime or integer epoch (in seconds)
 - follow (bool): Follow log output

### networks

- 列举当前网络. 与`docker nerwork ls`命令类似
- 参数:
 - names (list): List of names to filter by
 - ids (list): List of ids to filter by
- 返回dict, 字典项是网络对象的列表

### pause

- 暂停容器中的所有进程
- 参数:
 - container (str): The container to pause

### ping

- 访问远程api的`/_ping`端点, 并返回结果. 若无响应, 将引发异常
- 返回布尔值

### port

- 查找以NAT方式连接到`private_port`的公共端口(public\_facing port). 与`docker port`命令相同
- 参数:
 - container (str): The container to look up
 - private\_port (int): The private port to inspect
- 返回list of dict.

### pull

- 与`docker pull`命令相同
- 参数:
 - repository (str): The repository to pull
 - tag (str): The tag to pull
 - stream (bool): Stream the output as a generator
 - insecure\_registry (bool): Use an insecure registry
 - auth\_config (dict): Override the credentials that Client.login has set for this request  auth_config should contain the username and password keys to be valid.
- 返回generator或str

### push

- 向注册表(registry)推送镜像或仓库. 与`docker push`命令相同
- 参数:
 - repository (str): The repository to push to
 - tag (str): An optional tag to push
 - stream (bool): Stream the output as a blocking generator
 - insecure\_registry (bool): Use http:// to connect to the registry
- 以generator或str形式返回上传输出

### put\_archive

- 以tar档案作为源, 将文件或目录插入到已存在的容器
- 参数:
 - container (str): The container where the file(s) will be extracted
 - path (str): Path inside the container where the file(s) will be extracted. Must exist.
 - data (bytes): tar data to be extracted
- 返回布尔值. 若调用成功, 则返回True. 若出错, 抛出`docker.errors.APIError`

### remove\_container

- 删除容器. 类似于`docker rm`命令
- 参数:
 - container (str): The container to remove
 - v (bool): Remove the volumes associated with the container
 - link (bool): Remove the specified link and not the underlying container
 - force (bool): Force the removal of a running container (uses SIGKILL)

### remove\_image

- 删除镜像. 类似于`docker irm`命令
- 参数:
 - image (str): The image to remove
 - force (bool): Force removal of the image
 - noprune (bool): Do not delete untagged parents

### remove\_network

- 删除网络. 类似于`docker network rm`命令
- 参数:
 - net\_id (str): The network's id
- 删除失败将抛出`docker.errors.APIError`异常

### remove\_volume

- 删除卷. 类似于`docker volume rm`命令
- 参数:
 - name (str): The volume's name
- 删除失败将抛出`docker.errors.APIError`异常

### rename

- 重命名容器. 类似于`docker rename`命令
- 参数:
 - container (str): ID of the container to rename
 - name (str): New name for the container

### resize

- 重置tty会话大小
- 参数:
 - container (str or dict): The container to resize
 - height (int): Height of tty session
 - width (int): Width of tty session

### restart

- 重启容器. 类似于`docker restart`命令
- 若`container`是dict, 必须带`Id`键
- 参数:
 - container (str or dict): The container to restart
 - timeout (int): Number of seconds to try to stop for before killing the container. Once killed it will then be restarted. Default is 10 seconds.

### search

- 与`docker search`命令相同
- 参数:
 - term (str): A term to search for
- 返回list of dicts.

### start

- 类似于`docker start`命令, 但不支持附加选项(attach options). 使用`.logs()`恢复`stdout`/`stderr`
- 参数:
 - container (str): The container to start
- 对于版本大于1.15的, 强烈建议在`host_config`提供主机配置选项, 作为`create_container`的参数接口

### stats

- The Docker API parallel to the `docker stats` command. 将以流的格式返回指定容器的统计信息
- 参数:
 - container (str): The container to stream statistics for
 - decode (bool): If set to true, stream will be decoded into dicts on the fly. False by default.
 - stream (bool): If set to false, only the current stats will be returned instead of a stream. True by default.

### stop

- 停止一个容器. 类似于`docker stop`命令
- 参数:
 - container (str): The container to stop
 - timeout (int): Timeout in seconds to wait for the container to stop before sending a SIGKILL. Default: 10

### tag

- 为仓库中的镜像打标记. 与`docker tag`命令相同
- 参数:
 - image (str): The image to tag
 - repository (str): The repository to set for the tag
 - tag (str): The tag name
 - force (bool): Force
- 返回布尔值.

### top

- 显示容器中运行的进程
- 参数:
 - container (str): The container to inspect
 - ps\_args (str): An optional arguments passed to ps (e.g., aux)
- 返回str

### unpause

- 为容器中的所有进程取消暂停
- 参数:
 - container (str): The container to unpause

### update\_container

- 更新一个或多个容器的资源配置
- 参数:
 - container (str): The container to inspect
 - blkio\_weight (int): Block IO (relative weight), between 10 and 1000
 - cpu\_period (int): Limit CPU CFS (Completely Fair Scheduler) period
 - cpu\_quota (int): Limit CPU CFS (Completely Fair Scheduler) quota
 - cpu\_shares (int): CPU shares (relative weight)
 - cpuset\_cpus (str): CPUs in which to allow execution
 - cpuset\_mems (str): MEMs in which to allow execution
 - mem\_limit (int or str): Memory limit
 - mem\_reservation (int or str): Memory soft limit
 - memswap\_limit (int or str): Total memory (memory + swap), -1 to disable swap
 - kernel\_memory (int or str): Kernel memory limit
- 返回包含`Warnings`键的dict

### version

- 几乎与`docker version`命令相同
- 返回服务器版本信息的dict

### volumes

- 列举当前卷. 类似于`docker volume ls`命令
- 参数:
 - filters (dict): Server-side list filtering options.
- 返回字典. 键`Volumes`的对应的值是卷对象的列表

### wait

- 与`docker wait`命令相同. 阻塞容器, 直到取消等待, 并返回退出码. 若API响应中不带`StatusCode`属性, 返回`-1`
- 若`container`是一个字典, 必须带`Id`键
- 若超时, 抛出`requests.exceptions.ReadTimeout`异常
- 参数:
 - container (str or dict): The container to wait on
 - timeout (int): Request timeout
- 返回int, 表示容器的退出码.

## Port bindings

- 端口绑定分成2部分.
 1. 使用`Client().create_container()`创建容器时, 在容器内部提供开放的端口的列表
 2. 通过`host_config`参数声明绑定(声明映射)

```python
container_id = cli.create_container(
    'busybox', 'ls', ports=[1111, 2222],
    host_config=cli.create_host_config(port_bindings={
        1111: 4567,
        2222: None
    })
)
```

- 还可以通过`cli.create_host_config(port_bindings={1111: ('127.0.0.1', 4567)})`限制主机地址
- 默认使用TCP, 若希望使用UDP, 需要在配置和主机配置中同时指定, 如下所示:

```python
container_id = cli.create_container(
    'busybox', 'ls', ports=[(1111, 'udp'), 2222],
    host_config=cli.create_host_config(port_bindings={
        '1111/udp': 4567, 2222: None
    })
)
```

- 通过列表的形式, 将多个主机端口绑定到单个容器端口上. 事实上, 也可以绑定多个IP地址到单个容器端口

## Using Volumes

- 卷的声明也分2步:
 1. 使用`Client().create_container()`创建容器时, 在容器内部提供一个挂载点列表
 2. 在`host_config`部分声明主机卷到容器卷的映射

## Using TLS

- 稍后补充

## Host devices

- 若需要将主机设备直接暴露给容器, 则可以在`Client.create_containe`的`host_config`中指定`devices`参数

```python
cli.create_container(
    'busybox', 'true', host_config=cli.create_host_config(devices=[
        '/dev/sda:/dev/xvda:rwm'
    ])
)
```

- 每条形如`<path_on_host>:<path_in_container>:<cgroup_permissions>`的字符串都是一个单一的映射.

### Host configuration

- 强烈建议用户将`HostConfig`对象作为`host_config`参数传递给`Client.create_container`, 而不是`Client.start`.

### Network configuration

- 在docker1.9版本, 用户可管理自定义的网络.
- 如下所示, 创建了一个名为network1, 使用bridge驱动的网络:

```python
docker_client.create_network("network1", driver="bridge")
```

## Using tmpfs

- 稍后

## Using with DOcker Machine

- Docker建议使用[Docker Toolbox](https://www.docker.com/products/docker-toolbox)来设置docker. 它包括名为`Machine`的工具, 通过它, 可以创建运行docker engine的虚拟机, 并使用环境变量将用户shell指定到虚拟机.
