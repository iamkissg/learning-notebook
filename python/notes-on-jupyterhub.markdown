# Notes on JupyterHub

- JupyterHub是一个服务器, 提供Jupyter notebooks的多用户访问, 为每个用户提供独立的Jupyter notebook服务器.
- **不同的认证控制**. 默认是使用JupyterHub服务器上提供的账户登录(PAM, pluggable authentication module), 此时需要为每个用户在系统上创建一个帐号. 另一种认证方案是开放授权(OAuth), 即允许用户使用诸如Github帐号登录
- **spawner(产卵)控制**. 默认spawner以系统用户名为每个用户在同一台机器上启动一个notebook服务器. 另一个主流选择方案是为每个用户在分离的容器中启动notebook服务, 通常是使用docker.
- JupyterHub以下面3个独立的部分运行:
 - 多用户`Hub`(Python & Tornado)
 - 可配置的http代理(proxy)(NodeJs)
 - 多单用户`Jupyter notebook server`(Python & Tornado)
- 基本原则:
 - Hub产生代理(proxy)
 - 默认地, 所有到hub的请求都通过代理转发
 - hub处理登录, 并根据需求产生单用户服务器
 - hub配置代理, 以转发单用户服务器的url前缀
- JupyterHub实际是多个进程的集合, 以提供多用户的Jupyter Notebook server.
- 默认地, JupyterHub需要SSL加密运行. 代理(Proxy)通过8000端口监听所有的公共接口
- 所有的通信都只在本地服务器上进行, 包括hub, 单用户服务器(single-user servers), 其他服务.
- 默认地, 启动JupyterHub, 会在磁盘上当前工作目录下写2个文件:
 1. `jupyterhub.sqlite` - 包含了hub所有状态的数据库. 这使得hub能够记住哪个用户正在哪里运行, 以及其他信息. 这就使得分离地部分重启JupyterHub成为可能
 2. `jupyterhub_cookie_secret` - 用于cookie安全的加密密钥. 为了避免重启hub服务器时的非法cookie, 该文件必须一直存在. 相反地, 删除该文件并重启服务器, 能有效地使所有登录cookie失效.
- JupyterHub可通过以下2种方式进行配置:
 1. 配置文件
  - 默认地, JupyterHub将在当前工作目录查找`jupyterhub_config.py`.
  - jupyterhub --generate-config`可创建一个空的配置文件.
  - 空的配置文件拥有所有配置变量的描述以及它们的默认值, 通过`jupyterhub -f /path/to/jupyterhub\_config.py`指定配置文件
 2. 命令行参数
  - 用`-h`或`--help-all`查看命令行帮助.
- 默认地, JupyterHub被设置成可被8000端口上所有接口(`''`)访问. `'\*'`不能用于ip配置, 替代的, 可使用`0.0.0.0`
- 形如`jupyterhub --ip=192.168.1.2 --port=443`的命令, 即可更改ip地址与端口, 或在配置文件中进行设置(c.JupyterHub.ip)
- 端口号443是SSL/HTTPS的默认端口
- hub服务通过次要端口上的REST API与代理通信. 次要网络的接口和端口可独立配置. 默认地, REST API只在本地主机的8081端口上进行监听(c.JupyterHub.proxy_api_ip)
- 默认地, hub服务也仅在本地主机的8080端口进行监听. hub需要能被代理和所有的spawner访问. 若任一的代理或spawner是远程的或容器的镜像, hub必须在一个可访问的IP地址上侦听(c.JupyterHub.hub_ip)
- 安全性是配置Jupyter最重要的概念. 3类主要的安全配置概念:
 1. SSL加密
  - JupyterHub包含了认证, 并允许任意的代码执行, 因此不应该在没有SSL(HTTPS)的情况下运行JupyterHub.
  - 这需要用户有官方的, 可信的SSL证书, 或创建一个自签名的证书. 在配置文件中通过`c.JupyterHub.ssl\_key`和`c.JupyterHub.ssl\_cert`指定加密密钥和证书的位置
  - 将密钥文件和证书放在服务器上某个安全的位置非常重要
 2. Cookie secret(c.JupyterHub.cookie_secret)
  - cookie secret是一个加密密钥, 用于加密认证的浏览器cookie. 若其值发生改变, 所有单用户服务器都必须重启. 正常情况下, 其值保存在文件中, 同样在配置文件中指定
  - 文件内容需要是MIME Base64编码的长随机字符串. 可用`openssl rand -base64 2048 > /srv/jupyterhub/cookie\_secret`命令生成
  - 若hub启动时, cookie secret文件不存在, 将生成新的cookie secret, 并保存到文件中. 该文件推荐的权限是600
  - 若不希望依赖这些文件, 可设置环境变量`JPY\_COOKIE\_SECRET`, 该环境变量的值将自动被加载到hub进程中.
  - `export JPY\_COOKIE\_SECRET=`openssl rand -hex 1024`
  - 为安全起见, 环境变量应该只对hub可见. 若像以上那样动态地生成, 每次hub启动时, 所有用户都将被登出
 3. 代理认证令牌(c.JupyterHub.proxy\_auth\_token)
  - hub使用hub和proxy都同意的加密token向代理发起请求认证. 字符串的值需要是一个随机字符(比如, 可通过`openssl rand -hex 32`生成).
  - 通过设置`CONFIGPROXY_AUTH_TOKEN`环境变量, 向hub和proxy同时传递该加密token
  - `export CONFIGPROXY_AUTH_TOKEN=\`openssl rand -hex 32\``
  - 该环境变量需要对hub和proxy同时可见
  - 若不手动设置Proxy认证令牌, hub会自动生成一个随机的密钥, 这意味着每次重启hub, 都必须重启proxy. 若proxy是hub的子进程, 在hub重启的时候, proxy会自动重启
  - 若需要其他的服务, 则用户应该也必须手动设置代理认证令牌
- 认证设置:
 - `c.Authenticator.whitelist = {set}` - 设置允许登录的用户
 - `c.Authenticator.admin\_users = {set}` - 设置管理员
 - 若设置`JupyterHub.admin\_access`为真, 管理员用户有权用其他用户的身份登录他们各自的机器进行调试
- 添加删除用户:
 - 通过管理面板或REST API可添加或删除Hub用户. 用户添加将同时修改白名单和数据库, 但一旦hub启动了, 仅从白名单中删除用户是不够的, 必须从数据库中删除
 - 当添加用户到hub时, `LocalAuthenticator`检查用户是否已经存在. 正常情况下, 若用户不存在将报错. 通过设置`c.LocalAuthenticator.create\_system\_users = True`可以在用户不存在的情况下, 系统自动通过过`adduser`命令行工具创建用户到hub.
- 配置单用户服务器:
 - 单用户服务器(single-user server)是`jupyter notebook`的一个实例, 是一个多进程应用的完整实例.
 - 在JupyterHub层次, 可以为Spawner置值. 设置`Spawner.notebook\_dir`, 设置了一个用户服务器的根目录, 每个用户都可以对该目录进行访问
 - `c.Spawner.args = [list of str]`指定额外的命令行参数
 - 单用户服务器是notenook服务器的拓展应用, 它仍从`ipython\_notebook\_config.py`加载配置. 每个用户可以在`$HOME/.ipython/profile\_default/`目录下拥有自己的配置文件, IPython也支持系统范围内的配置文件`/etc/ipython/`
- 外部服务
 - 若要获得外部服务, 需要提供API令牌(token). 目前有2种方式注册令牌到命令行:
  1. 使用`jupyterhub token <username>`命令为指定hub用户生成一个令牌
  2. 0.6.0版本以后, 更受欢迎的做法是, 用`openssl rand -hex 32`命令生成API令牌, 再添加到配置文件中`c.JupyterHub.api\_tokens = {'token' : 'username'}`
- 文件位置
 - 建议将所有JupyterHub用到的文件都放到标准UNIX文件系统位置:
  - /srv/jupyterhub for all security and runtime files
  - /etc/jupyterhub for all configuration files
  - /var/log for log files

```python
# Example
# jupyterhub_config.py
c = get_config()

import os
pjoin = os.path.join

runtime_dir = os.path.join('/srv/jupyterhub')
ssl_dir = pjoin(runtime_dir, 'ssl')
if not os.path.exists(ssl_dir):
    os.makedirs(ssl_dir)


    # https on :443
    c.JupyterHub.port = 443
    c.JupyterHub.ssl_key = pjoin(ssl_dir, 'ssl.key')
    c.JupyterHub.ssl_cert = pjoin(ssl_dir, 'ssl.cert')

    # put the JupyterHub cookie secret and state db
    # in /srv/jupyterhub/
    c.JupyterHub.cookie_secret_file = pjoin(runtime_dir, 'cookie_secret')
    c.JupyterHub.db_url = pjoin(runtime_dir, 'jupyterhub.sqlite')
    # or `--db=/path/to/jupyterhub.sqlite` on the command-line

    # use GitHub OAuthenticator for local users

    c.JupyterHub.authenticator_class = 'oauthenticator.LocalGitHubOAuthenticator'
    c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
    # create system users that don't exist yet
    c.LocalAuthenticator.create_system_users = True

    # specify users and admin
    c.Authenticator.whitelist = {'rgbkrk', 'minrk', 'jhamrick'}
    c.Authenticator.admin_users = {'jhamrick', 'rgbkrk'}

    # start single-user notebook servers in ~/assignments,
    # with ~/assignments/Welcome.ipynb as the default landing page
    # this config could also be put in
    # /etc/ipython/ipython_notebook_config.py
    c.Spawner.notebook_dir = '~/assignments'
    c.Spawner.args = ['--NotebookApp.default_url=/notebooks/Welcome.ipynb']
```

## How JupyterHub works

- JupyterHub是一个多用户服务器, 它管理并代理多个单用户Jupyter notebook服务器实例
- proxy是唯一在公共接口上监听的进程, Hub在proxy之后, 位于`/hub`, single-user server也位于proxy之后, 位于`/user/[username]`

### 登录

- 当新的浏览器登录JupyterHub时, 将发生以下一系列事件:
 - 登录数据提交到认证系统(Authenticator)进行验证
 - 若登录信息合法, 认证系统返回用户名
 - 为登录的用户产生一个单用户服务器实例
 - 当服务器启动时, 代理收到通知, 将`/user/[username]/\*`转发到单用户服务器
 - 分别为`/hub/`和`/user/[username]`设置包含加密令牌的cookie
 - 浏览器被重定向到受单用户服务器托管的`/user/[username]`
- 登录到单用户服务器通过Hub进行认证:
 - 收到请求之后, 单用户服务器转发加密cookie到hub, 进行验证
 - 若cookie合法, hub返回用户名
 - 若用户是服务器的所有者, 允许访问
 - 若用户错误或cookie不合法, 浏览器将被重定向到`/hub/login`

### 自定义JupyterHub

- 若要自定义认证或产生(单用户服务器), 创建Authenticator和Spawner的子类, 并覆盖相关方法
- 认证被替换为任意的机制, 例如开放授权(OAuth), Kerberos等. JupyterHub默认支持PAM(可插拔认证模型), 这要求服务器需要以根用户权限运行
- 任何单用户服务器都由Spawner启动, Spawner用一个进程表示抽象接口, 执行以下3个动作:
 1. 启动进程
 2. 轮询进程是否运行
 3. 停止进程

## JupyterHub的网络安全性

- JupyterHub将Hub和单用户服务器放在proxy后的一个单一的域内. 其结果是, 若Hub正在为不可信用户提供服务, 许多跨站防护就不能在单用户服务器和hub, 或单用户服务器之间得到应用, 因为浏览器将一切(代理, hub, 单用户服务器)看作一个单一的站点
- 为了提供用户间的保护, 用户在hub域内不允许编写任意的html或将其发送给其他用户. JupyterHub的认证系统为此提供了保证, 只有单用户服务器的所有者才能查看服务器提供的用户创作页面. 为此, 认证系统必须确保:
 - 用户无权修改他们的单用户服务器
  - 用户不能在他们的服务器上安装新的python包
  - 若PATH是用于解决单用户执行问题的(非绝对路径), 用户不能在PATH目录下创建新文件
  - 用户不能修改单用户服务器的环境变量
 - 用户不能修改notebook服务器的配置信息
- 若在同一个域内, 有任何额外的服务以Hub形式在运行, 该项服务不能向任何缺少认证的用户提供用户创作html

### 缓解措施

- 子域 - 在用户各自的子域内运行单用户服务器. 解决了所有跨站问题
- 取消用户配置 - `Spawner.disable\_user\_config`防止加载用户所有的配置文件, 只加载必须的东西, 如PATH和安装包等
- For most Spawners, PATH is not something users an influence, but care should be taken to ensure that the Spawn does not evaluate shell configuration files prior to launching the server.
- 通过在一个取消了system-site-packages的虚拟环境(virtualenv)中运行单用户服务器, 可以很容易地处理包隔离问题
- 环境控制仅仅影响单用户服务器, 用户kernel可能运行在不同的环境中?(not the environment(s) in which the user’s kernel(s) may run). 在kernel环境上安装额外的包, 不会带来额外的风险.

## custom Authentication

- 用户名由认证系统传递给产生器, 因此自定义认证系统和产生器经常是一起的
- `Authenticator.authenticate(handler, data)` - 传入Tornado RequestHandler和登录表单的POST数据. 除非自定义了登录表单, 否则`data`由`username`和`password`组成. 该方法的职责是: 若认证成功, 返回认证用户的用户名, 否则返回None. 若要写一个认证器(认证系统的别名, 视场景选择表达), 在某个目录下查找密码, 则只需覆写该方法即可.
- 有时候, 需要在从认证服务收到用户名之后, 提交到hub服务之前, 对用户名进行规范化, 可在认证器内定义一个`normalize\_username`, 接收用户名, 将其转为小写形式
- `Authenticator.username\_map = {dict}`配置项用于对用户名进行映射, 也可以用于规范化
- 可在认证器内定义`validate\_username(username)`, 用于判断用户名是否合法. 默认的方法是使用`Authenticator.username\_pattern`配置项, 其值是regex.
- `c.Authenticator.username\_pattern = r'w.\*'` - 只允许'w`开头的用户名
- 开放授权(OAuth)机制, 不需要username+password.

## custom Spawner

- Spawner举例:
 - docker spawner - 以docker容器的形式产生用户服务器
  - dockerspawner.DockerSpawner - 为每个用户产生相同的容器
  - dockerspawner.SystemUserSpawner - 为每个用户产生带环境和家目录的容器
 - sudospawner - 使JupyterHub能以非root权限运行, 通过`sudo`立即产生进程
 - batchspawner - 使用批处理系统产生远程服务器
 - remotespawner - 产生notebook和远程服务器, 以及基于SSH的隧道端口(tunnel the port via ssh)
 - swarmspawner - 使用docker swarm产生容器
- spawner控制方法:
 - spawner.start - 为单个用户启动单一的服务器. 通过`self.user`解析出用户信息, 包括用户名, 认证信息, 服务器信息. 当方法返回时, 将单用户服务器的ip, port保存到`self.user.server`中, 此时单用户进程应确实在运行.
 - spawner.poll - 检查spawner是否在运行. 若是, 返回None, 否则返回表示退出状态的int. 对于本地进程, 该函数使用`os.kill(PID, 0)`检查本地进行的状态
 - spawner.stop - 停止进程. 必须是一个tornado协程, 当进程退出之后, 返回.
 - spawner.state - JupyterHub应当能够在不tear down单用户notebook服务器的情况下停止与重启服务. 因此, spawner需要保持一些信息以便之后重载. 使用可JSON化的状态字典进行信息持久化. state方法不能是协程. 对于单进程, spawner状态只是服务器的进程id
 - 设置`Spawner.options\_form`, 可以为用户提供一些可选项. 当设置好`Spawner.options\_form`, 当用户尝试启动服务器时, 将被定向到表单页; 否则, 直接产生用户服务器. 当表单数据到达时, 它将被传递给`Spawner.options\_from\_form(formdata)`, 该方法将表单数据解析成正确的数据结构, 以dict形式返回.

## JupyterHub API

[API](https://jupyterhub.readthedocs.io/en/latest/api/index.html)
