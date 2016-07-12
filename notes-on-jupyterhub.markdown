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
 3. 代理认证符号(c.JupyterHub.proxy_auth_token)
  - hub使用hub和proxy都同意的加密token向代理发起请求认证. 字符串的值需要是一个随机字符(比如, 可通过`openssl rand -hex 32`生成).
  - 通过设置`CONFIGPROXY_AUTH_TOKEN`环境变量, 向hub和proxy同时传递该加密token
  - `export CONFIGPROXY_AUTH_TOKEN=\`openssl rand -hex 32\``
  - 该环境变量需要对hub和proxy同时可见
