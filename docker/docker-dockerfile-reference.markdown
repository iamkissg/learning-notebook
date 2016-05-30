# Dockerfile Reference

- docker 可以通过读取`Dockerfile`的指令自动地生成镜像.
- `Dockerfile`是包含了用户需要调用的所有命令的文本文档.

## Usage

- `docker build` 命令通过读取`Dockerfile`和`context`来创建镜像. `context`是指定`PATH`或`URL`的文件, 它可以被递归地处理
- 镜像的创建由`Docker daemon`执行, 而非CLI. 首先将完整的`contex`发送到`daemon`. 大多数情况下, 最好以一个空目录为`contex`, 并在该目录下编写`Dockerfile`. 仅将创建镜像时需要的文件写入`Dockerfile`
- `Dockerfile`根据指令使用`context`的文件. 为了提高性能, 通过编写`.dockerignore`文件将指定文件排除在`context`之外
- 一般的, `Dockerfile`被命名为`Dockerfile`, 并位于`context`的根目录下. 可以用`-f`参数来指定文件系统下任意位置的`Dockerfile`.
- `-t`参数, 在创建时为镜像打上标签, 可同时指定多个标签名:

```shell
$ docker build -t shykes/myapp:1.0.2 -t shykes/myapp:latest .
```

- docker daemon 按行执行`Dockerfile`中的指令, 并且每条指令都是**独立**的, 即一条指令与后一条指令是上下文无关的
- docker will re-use the intermediate images(cache), to accelerate the docker build process siginificantly.

## Format

- docker指令大小写不敏感, 但一般写成大写形式, 以示与参数的区别(与数据库类似)
- 第一条指令必须是`FROM`, 用于指定`Base Image`(基镜像)
- 与python不同, docker将以`#`开头的行作为注释, 但句中的`#`将被视为参数

### Environment replacement

- `Dockerfile`中, `Environment variables`(环境变量)可以被用在指令中, 作参数使用. 同样, 有转义的语法
- `Dockerfile`中, `Environment variables`用`$variable_name`或`${variable_name}`的形式使用, 二者一样
- (我看不懂的!)the brace syntax is typically used to address issues with variable names with no whitespace, like `${foo}_bar`
- `${variable_name}`支持一部分标准`bash`修饰符:
 - `${variable:-word}` - 指示若`variable`已被设置, 则返回其值; 否则返回`word`
 - `${variable:+word}` - 指示若`variable`已被设置, 则返回`word`; 否则返回空串
 - `word`可以是任意字符串, 包括额外的环境变量
- 转义仍通过`\`字符
- 环境变量可用于这些指令: `ADD` COPY` `ENV` `EXPOSE` `LABEL` `USER` `WORKDIR` `VOLUME` `STOPSIGNAL`, `ONBUILD`
- 在一行命令中, 每个环境变量的替换使用相同的值, 这一点还是看例子吧:

```shell
ENV abc=hello
# 变量def的值是hello, 而非bye; 变量ghi的值是bye
ENV abc=bye def=$abc
ENV ghi=$abc
```

### .dockerignore file

- 在docker cli 将`context`传入`docker daemon`之前, 将首先查看`context`的根目录下是否有`.dockerignore`文件. 若存在`.dockerignore`文件, cli 将修改`context`, 剔除不需要的文件. 这就避免了不必要的大文件或敏感文件传入`daemon`. 之后可通过`ADD`或`COPY`将它们加入镜像
- cli 按行对`.dockerignore`文件进行解释.
- `context`的根目录, 既被视为工作目录, 又被视为根目录. 举例来说, 在`.dockerignore`中使用`/foo/bar`和`foo/bar`的效果一样
- 可在`.dockerignore`文件中使用正则表达式, 使用`go`语言的语法
- 预编译过程将会移除字符串前后的空格, 并忽略空行
- 通配符`**`可以匹配任意数量的目录, 包括0个
- `!`用于反转, 如`!README.md`就表示不包括README.md
- 除了用`dockerfile`将文件摒弃之外, 还可以先用通配符`*`将所有文件都摒弃, 再通过`!`来添加需要的文件


## FROM

- `FROM <image>` 或 `FROM <image>:<tag>` 或 `FROM <image>@<digest>`
- `FROM`指令用于设置基镜像. 一个有效的`Dockerfile`必须以`FROM`作为第一条指令
- 可一次设置多个基镜像
- `tag`或`digest`可选, 若省略, 创建时默认使用最新版

## MAINTAINER

- 用于设定作者字段

## RUN

- `RUN` 指令有2种形式:
 1. `RUN <command>` (shell 形式, 命令运行在shell里)
 2. `RUN ["executable", "param1", "param2"]` (exec )
- `RUN`在当前镜像的最顶层(栈?)执行命令, 并提交结果.
- (docker有点像包心菜呀, 只不过是一层一层包起来)
- 分层的`RUN`指令以及生成提交, 符合docker的核心概念, 使得提交更简单, 容器可以从镜像历史的任意节点构建.
- `exec`形式可以避免shell string munging(改写?), 并可以在基镜像没有`/bin/sh`的情况下使用
- `shell`形式可以用`\`, 实现续写
- `exec`形式, 使用JSON数组, 这意味着必须使用双引号`"`包裹字符
- `exec`形式, 不回调用shell, 举例来说, 就是`RUN [ "echo", "$HOME" ]` 不会对`$HOME`进行解释替换
- 因为使用JSON格式, 需要对`\`进行转义
- `RUN`指令的缓存不会自动失效. 这意味着下一次创建镜像时, 可能使用上一次`RUN`命令的缓存(不太懂). `--no-cache`参数, 不适用缓存
- `RUN`缓存会在使用`ADD`指令的情况下失效

## CMD

- `CMD` 有3种形式:
 - `CMD ["executable","param1","param2"]` (exec form, this is the preferred form)
 - `CMD ["param1","param2"]` (as default parameters to ENTRYPOINT)
 - `CMD command param1 param2` (shell form)
- `Dockerfile`只能有一条`CMD`指令, 若有多条`CMD`指令, 仅最后一条会生效
- `CMD`指令的主要目的是提供容器默认的执行命令(?). 执行命令可以包括`executable`(如形式1), 也可以忽略`executable`, 但此时必须给定一个`ENTRYPOINT`指令
- 若以`CMD ["param1","param2"]`形式使用`CMD`, 即为`ENTRYPOINT`提供参数, 则`CMD`与`ENTRYPOINT`都需要使用JSON数组格式
- 使用shell形式或exec形式, `CMD`指令将在image运行时被执行
- 使用shell形式, 则命令将在`/bin/sh -c`中执行
- 若希望在shell之外运行命令, 必须以JSON数组格式来写指令, 并给出`executable`的完整形式(即形式1), 其他参数均已字符串形式表示
- 若希望容器每次都运行相同的`executable`, 使用`ENTRYPOINT`, 并用`CMD`提供参数
- 在使用`docker run`时指定了参数, 将覆盖默认的`CMD`
- `RUN` vs `CMD`:
 - `RUN` - 执行命令并提交结果
 - `CMD` - 创建镜像时, 不执行任何命令, 但为image设置了预期的命令(有点像python的argparse, 提供默认参数)

## LABEL

- `LABEL <key>=<value> <key>=<value> <key>=<value> ...`
- 为镜像设置元数据(metadata), 一个`LABEL`是一个键值对

```docker
LABEL "com.example.vendor"="ACME Incorporated"
LABEL com.example.label-with-value="foo"
LABEL version="1.0"
LABEL description="This text illustrates \
that label-values can span multiple lines."
```

- 一个镜像可拥有多个label, 建议写在一条`LABEL`指令中. 因为若有多个label, 每条`LABEL`指令都会产生新的一层, 这将使镜像变得低效.

```docker
LABEL multi.label1="value1" multi.label2="value2" other="value3"
```

或

```docker
LABEL multi.label1="value1" \
      multi.label2="value2" \
            other="value3"
```

- 在基镜像中可能已存在一些label, 当docker遇到相同的label时, 新的将覆盖旧的
- `docker inspect`命令可查看镜像的label

## EXPOSE

- `EXPOSE <port> [<port>...]`
- `EXPOSE`指令告诉docker, 容器运行时将监听指定的网络端口.
- `EXPOSE`指定的容器的端口, 主机是不可访问的. 除非使用`-p`公开部分端口或`-P`公开所有端口
- 向外公开的端口号可以与监听的端口号不同. (You can expose one port number and publish it externally under another number.)

## ENV

```docker
# The entire string after the first space will be treated as the <value>
ENV <key> <value>
# allows for multiple variables to be set at one time
ENV <key>=<value> ...
```

- 设置环境变量.
- 同样地, 建议使用`ENV myName="John Doe" myDog=Rex`的形式, 因为只会产生一个缓冲层
- `docker inspect`查看信息, 或用`docker run --env <key>=<value>`在运行前修改环境变量
- 环境的持久存在可能会带来意想不到的副作用. 因此若非必要, 可以使用`RUN <key>=<value> <command>`来为单一命令设置值

## ADD

- `ADD`有2种形式:
 - `ADD <src>... <dest>`
 - `ADD ["<src>",... "<dest>"]` (this form is required for paths containing whitespace)
- `ADD`指令将文件, 目录, 或远程文件从`<src>`复制并添加到`<dest>`指定的容器的文件系统的路径上
- `<src>`资源的路径必须是相对于`context`的, 可以使用通配符, 可匹配多个多文件或目录
- `<dest>`是绝对路径或相对于`WORKDIR`的的路径
- 所有的新文件或目录在被创建时, 其`UID`和`GID`都是0. (设置权限为root)
- 当`<src>`是一个url指定的远程文件时, 在容器的文件系统上, 其权限是`600(rw-------)`
- 若远程文件在解析时, 带有htpp`Last-Modified`头, 该头部字段的值(时间戳)将用于设置目的文件的`mtime`
- 若通过`重定向`的方式创建镜像(`docker build - < somefile`), 将不存在`context`, 因此, 该`Dockerfile`只能使用基于URL的`ADD`
- 还可以通过压缩包的形式创建镜像(`docker build - < archive.tar.gz`), `Dockerfile`仍需要位于根目录下, 其余部分将作为`context`
- 若url指定的远程文件需要认证, 需要用`RUN wget`, `RUN curl`或其他容器中包含的工具下载, `ADD`指令不支持认证
- 当`<src>`的内容发生改变时, 第一条`ADD`指令将使之前所有的缓存都失效, 包括`RUN`指令的缓存
- `ADD`指令的准则:
 - `<src>`路径必须是`context`内的, `ADD ../something /something`是错误的, 因为`docker build`的第一步就是将`context`发送到`docker daemon`
 - 如果`<src>`是一个url, 并且`<dest>`不是以反斜杆结尾, 指定的远程文件将从url下载到`<dest>`下, 文件名由url推出
 - 若`<src>`是一个目录, 目录本身不会被复制, 目录下的所有内容都会被复制, 包括文件系统元数据(filesystem metadata)
 - 若`<src>`是一个普通文件, 它将单独被复制. 此时若`<dest>`以`/`结尾, 它将被视为一个目录, `<src>`表示的文件将被写到`<dest>/base(<scr>)`
 - 需要添加多文件时, `<dest>`必须是一个目录, 且必须以`/`结束
 - `<dest>`不以`/`结束时, 将被视为普通文件, `<src>`的内容将被写入`<dest>`
 - If `<dest>` doesn’t exist, it is created along with all missing directories in its path.(不太懂)

## COPY

- `COPY`有2种形式:
 - `COPY <src>... <dest>`
 - `COPY ["<src>",... "<dest>"]` (this form is required for paths containing whitespace
- 怎么看, 怎么像`ADD`, 只是似乎少了远程文件

## ENTRYPOINT

- `ENTRYPOINT`有2种形式:
 - `ENTRYPOINT ["executable", "param1", "param2"]` (exec form, preferred)
 - `ENTRYPOINT command param1 param2` (shell form)
- `ENTRYPOINT`允许用户配置容器, 使其像一个`executable`一样
- `docker run <image>`之后的参数, 都将作为`ENTRYPOINT`的`exec`形式的参数, 会覆盖`CMD`指定的元素.
- shell形式防止任何`CMD`或`run`命令行参数被使用, 缺点是, `ENTRYPOINT`将作为`/bin/sh -c`的子命令被执行, 并且不支持传入信号. 这意味着这个`executable`不是容器的`PID 1`的进程, 它不会接收任何Unix信号, 包括`SIGTERM`, 因此无法结束.
- 与`CMD`类似, 只有最后一条`ENTRYPOINT`才会生效
- 参数`--entrypoint`将会覆盖`ENTRYPOINT`, 但仅可用于`exec`的二进制设置?
- 与shell形式不同, exec形式不会调用shell.
- shell形式会使用shell来进行处理, 将会忽略`CMD`或`docker run`命令参数
- 为确保`docker stop`能向`ENTRYPOINT executable`正确地发送信号(signal), 切记要以`exec`作为shell命令的参数:

```docker
FROM ubuntu
ENTRYPOINT exec top -b
```

- 若忘了添加在命令前添加`exec`, 用`docker stop`并不能正确地关闭容器, 超时之后, `stop`命令将会强制发送`SIGKILL`信号关闭容器
- `CMD`和`ENTRYPOINT`指令都定义了运行容器时, 需要被执行的命令. 使用规则如下:
 1. Dockerfile需要指定至少一条`CMD`或`ENTRYPOINT`命令
 2. 当容器被当作可执行文件使用时, 定义`ENTRYPOINT`
 3. `CMD`一般用于为`ENTRYPOINT`命令设定默认参数, 或指定容器需要执行的特定命令
 4. 运行容器时, 给定的参数(`<image>`之后的)会覆盖`CMD`

![What command is executed for diffrent ENTRYPOINT/CMD combinations](CMD-ENTRYPOINT.png)

## VOLUME

- `VOLUME ["/data"]`
- `VOLUME`指令用给定的字符串创建一个挂载点, 并将它标记为本地主机或其他容器的外部挂载卷.
- `VOLUME`指令的值(后接的一大串内容), 可以是JSON数组, 或普通字符串(`VOLUME /var/log /var/db`)
- `docker run`命令在初始化时, 会将新加卷挂载到基镜像的指定位置

## USER

- `USER daemon`
- 设置用户名或UID. 之后`Dockerfile`中的`RUN`, `CMD`和`ENTRYPOINT`都将以该用户执行, 镜像运行时也是以该用户的身份

## WORKDIR

- `WORKDIR /path/to/workdir`
- 为`RUN`, `CMD`, `ENTRYPOINT`, `COPY`和`ADD`命令设置工作目录.
- 若`WORKDIR`不存在, 即使没有`Dockerfile`中后续没有任何指令用到, 也会创建一个`WORKDIR`
- 若使用相对路径, 路径是相对于前一条`WORKDIR`指令的
- (有点像, mkdir && cd 啊)

## ARG
-
- `ARG <name>[=<default value>]`
- `ARG`指令定义了创建镜像时, 用户可传递给构造器的变量, 使用方法是:`docker build --build-arg <varname>=<value>`
- 若参数不存在(未在Dockerfile中定义), 创建过程中会报错
- `ARG`就是argument的缩写吗- -.
- `ARG`变量定义在`Dockerfile`中, 其定义的那一行生效, 而非参数被使用的那一行或其他地方
- 在`ARG`指令之前, 变量的值为空串
- 不建议在创建时, 通过传递变量的方式传递密码或证书
- `ENV`定义的环境变量会覆盖`ARG`指令给定的同名变量
- docker预定义的一些变量:
 - HTTP_PROXY
 - http_proxy
 - HTTPS_PROXY
 - https_proxy
 - FTP_PROXY
 - ftp_proxy
 - NO_PROXY
 - no_proxy
- `ARG`定义的变量并不能像`ENV`定义的环境变量一样, 在镜像中长存.


## ONBUILD

- `ONBUILD [INSTRUCTION]`
- `ONBUILD`指令为镜像添加一个触发器指令, 在当前镜像作为基镜像被使用时被执行.
- 触发器在`downstream build`的`context`中被执行(子镜像的创建context?)
- 任何创建指令都能作为触发器
- 工作原理:
 1. 当遇到`ONBUILD`指令时, 构建器将触发器加入正被创建的镜像的元数据中. 这条指令不影响当前的创建过程
 2. 在创建结束时, 所有触发器以一个列表的形式存储在镜像中, 作为`OnBuild`的值. 可通过`docker inspect`查看
 3. 在镜像被作为基镜像用于创建新镜像时, 在`FROM`指令被执行时, 将会查看`ONBUILD`触发器, 并按它们被注册的顺序依次执行. 若任何触发器指令执行失败, `FROM`指令中止, 创建镜像失败
 4. 触发器被执行之后就失效了, 换言之, 它们不会被孙子镜像继承

## STOPSIGNAL

- `STOPSIGNAL signal`
- `STOPSIGNAL`指令用于设置系统调用的终止信号. 可以是内核系统调用表上的任意有效无符号数, 可用数字表示, 也可用信号名表示, 例如SIGKILL
