# 21 Internet Protocols and Support

## 21.6 urllib.request

- The urllib.request module defines functions and classes which help in opening URLs (mostly HTTP)
- `urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)`
 - `url`参数可以是字符串也可以是`request`对象
 - 使用`data`参数时, 发送的请求变为一个`POST`请求. 用二进制对象来指定发送给服务器的额外的数据; 当请求头部带有`Content-Length`字段时, `data`可以是一个`iterable`对象
 - `data`需要是标准的`application/x-www-form-urlencoded`的格式, 因此需要用`urllib.parse.urlencode`来将数据转换成这种格式, 其接受映射或元素是2元元组的序列
 - `urllib.request`模块使用`HTTP/1.1`协议, 并默认在HTTP请求头部包含了`Connection: close`字段
 - `timeout`字段用于设置超时时间, 单位是秒
 - `cafile`和`capath`用于设置HTTPS请求的CA证书, `cafile`指向包含CA证书的单一文件, `capath`指向包含证书文件的目录
 - `urlopen`方法返回的对象, 拥有以下方法:
  - `geturl` - 返回资源的url
  - `info` - 返回页面的`meta-information`(元信息), 其中包括头部信息
  - `getcode` - 返回响应的http状态编码
 - 对于使用http或https的url, 返回`http.client.HTTPResponse`对象.
 - 当产生错误时, 其类型维`URLError`
 - 若检测到使用了代理(proxy), 将默认使用`ProxyHandler`来将请求通过代理发出
- `urllib.request.install_opener(opener)` - 创建一个`OpenerDirector`实例, 作为全局的默认opener.
- `urllib.request.build_opener([handler, ...])` - 返回一个`OpenerDirector`实例, 其将给定的handlers级联起来, handlers可以是`BaseHandler`或其子类. 若Python支持SSL, 将默认添加`HTTPSHandler`
- `urllib.request.pathname2url(path)` - 将资源的路径名转换为能用于URL的格式, 如下所示:

```python
In [2]: path="头脑风暴"

In [3]: url = urllib.request.pathname2url(path)
#  '%E5%A4%B4%E8%84%91%E9%A3%8E%E6%9A%B4'

In [5]: urllib.request.url2pathname(url)
Out[5]: '头脑风暴'
```

- `urllib.request.url2pathname(path)` - 用法与`pathname2url`相反
- `urllib.request.getproxies()` - 扫描`<scheme>_proxy`的环境变量, 并返回代码服务器的url字典
- `class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)`
 - 该类是url 请求的抽象
 - `url`是包含合法url的字符串
 - `data` 的用法与`urlopen` 中的用法一样
 - `headers`是一个包含请求头部字段的字典, 最常用的头部字段是`User-Agent`用于伪装成浏览器, 该字段的默认值是`Python-urllib/版本号`
 - `method`是一个字符串, 指示http 请求方法.
- `class urllib.request.OpenerDirector` - `OpenerDirector`类通过级联的handlers打开url, 它管理着handlers之间的级联关系, 以及错误恢复
- `class urllib.request.BaseHandler` - 所有注册的handlers的基类, 只能处理简单的注册机制
- `class urllib.request.HTTPDefaultErrorHandler`- 错误响应handler, 所有的响应都被当作`HTTPError`异常处理
- `class urllib.request.HTTPRedirectHandler` - 重定向处理handler
- `class urllib.request.HTTPCookieProcessor(cookiejar=None)` - cookie handler
- `class urllib.request.ProxyHandler(proxies=None)` - proxy handler. `proxies`必须是协议名到代理url的字典. 默认将读取`<protocol>_proxy`环境变量. 创建该handler时, 传入一个空字典, 将取消自动检测.
- `class urllib.request.HTTPPasswordMgr` - 保存`(realm, uri) -> (user, password)`的映射
- `class urllib.request.HTTPPasswordMgrWithDefaultRealm` - 与上类似, 值为`None`的`realm`, 若没有合适的`realm`, 将在所有realm中搜索
- `class urllib.request.HTTPPasswordMgrWithPriorAuth` - 上面的变形, 带`uri -> is_authenticated mappings`映射. 被`BasicAuth handler`调用, 用于立即发送认证证书, 而不是等待401响应
- `class urllib.request.AbstractBasicAuthHandler(password_mgr=None)` - 处理到远程主机或代理的http认证的混合类. 若`password_mgr`需要与`HTTPPasswordMgr`兼容. 若`passsword_mgr`提供了`is_authenticated`和`update_authenticated`方法, 当`is_authenticated`为真时, 在发送请求时, 同时发送证书; 当`is_authenticated`为假时, 再收到401响应时, 再发送证书. 当认证通过, `update_authenticated`将被调用, 用于设置`is_authenticated`为真
- `class urllib.request.HTTPBasicAuthHandler(password_mgr=None)` - 处理与远程主机的认证
- `class urllib.request.ProxyBasicAuthHandler(password_mgr=None)` - 处理与代理的认证
- `class urllib.request.AbstractDigestAuthHandler(password_mgr=None)` - 处理到远程主机或代理的http认证的混合类.
- `class urllib.request.HTTPDigestAuthHandler(password_mgr=None)` - 处理与远程主机的认证. 当`数字认证`handler与`基础认证`handler同时被添加时, 优先处理数字认证. 若数字认证还是收到40x响应, 将由基础认证来处理. 当认证方案既不是数字方式也不是基础方式, 将抛出`ValueError`错误
- `class urllib.request.ProxyDigestAuthHandler(password_mgr=None)` - 处理与代理的认证
- `class urllib.request.HTTPHandler` - 处理http urls打开的类
- `class urllib.request.HTTPSHandler` - 处理https urls打开的类
- `class urllib.request.FileHandler` - 打开本地文件
- `class urllib.request.DataHandler` - 打开data urls
- `class urllib.request.FTPHandler` - 打开ftp urls
- `class urllib.request.CacheFTPHandler` - 打开ftp urls, 并为打开的ftp连接保存一个缓存, 以使延迟最小
- `class urllib.request.UnknownHandler` - 处理未知urls
- `class urllib.request.HTTPErrorProcessor` - 处理http错误响应

### 21.6.1 Request objects

- `Request.full_url` - 包含完整的url信息的属性, 带有`setter`, `getter`, `deleter`
- `Request.type` - 协议
- `Request.host` - 主机名(域名), 可能带有端口号
- `Request.origin_req_host` - 不带端口号的域名
- `Request.selector` - uri路径, 若`Request`对象使用了代理, `selector`属性是传入代理的完整url
- `Request.data` - 请求的实体主体, 若没有使用将为`None`
- `Request.unverifiable` - 布尔值, 指示请求是否是不可验证的
- `Request.get_method()` - 返回http request method的类型的字符串. 默认http request method是`GET`
- `Request.add_header(key, val)` - 添加请求头部字段
- `Request.add_unredirected_header(key, header)` - 添加不会被加入重定向请求的头部字段
- `Request.has_header(header)` - 检查请求是否含有头部字段
- `Request.remove_header(header)` - 删除头部字段
- `Request.get_full_url()` - 获取url, 返回值即为`Request.full_url`
- `Request.set_proxy(host, type)` - 设置代理服务器
- `Request.get_header(header_name, default=None)` - 返回头部字段的值
- `Request.header_items()` - 返回头部字段信息, 二元元组的列表

### 21.6.2 OpenerDirector objects

- `OpenerDirector.add_handler(handler)` - 添加handler, 将搜索以下方法, 并加入到可能的链中:
 - protocol_open() — signal that the handler knows how to open protocol URLs.
 - http_error_type() — signal that the handler knows how to handle HTTP errors with HTTP error code type.
 - protocol_error() — signal that the handler knows how to handle errors from (non-http) protocol.
 - protocol_request() — signal that the handler knows how to pre-process protocol requests.
 - protocol_response() — signal that the handler knows how to post-process protocol responses.
- `OpenerDirector.open(url, data=None[, timeout])` - 打开url, 参数, 返回值, 异常都与`urlopen`一样. `urlopen`函数是简单地调用了全局`OpenDirector`的`open`方法. `timeout`只对`http`, `https`, `ftp`连接有效
- `OpenerDirector.error(proto, *args)` - 处理给定协议的错误, 将会调用已注册的错误handler. http协议, 通过http响应编码指定错误handler.
- `OpenerDirector`对象打开urls的三种情况:
 1. 调用每个带有如`protocol_request`的方法的handler的`protocol_type`预处理请求
 2. 调用带有如`protocol_open`方法的handlers去处理请求, 当某个handler返回了非空值或抛出了异常, 结束.  事实上, 先调用`default_open`方法, 若全部这些方法都返回`None`, 再调用`protocol_open`方法, 还是fanhui`None`, 调用`unknown_open`方法.
 3. 调用如`protocol_response`的方法`后处理(post-process)`响应

### 21.6.3 BaseHandler objects

- `BaseHandler.add_parent(director)` - add a director as parent(就是`OpenerDirector`)
- `BaseHandler.close()` - remove any parents
- 定义了`protocol_request()`或`protocol_response()`方法的handlers被命名为`*Processor`, 所有其他的都被命名为`*Handler`
- `BaseHandler.parent` -  有效的`OpenDirector`
- `BaseHandler.default_open(req)` - 该方法并不在`BaseHandler`中定义, 但若其子类若希望捕获?(catch) urls, 需要定义该方法. 该方法由`OpenDirector`调用, 返回`file-like`对象或`None`, 或抛出异常
- `BaseHandler.protocol_open(req)` - 该方法并不在`BaseHandler`中定义, 但若其子类若希望处理urls, 需要定义该方法. 同上, 由`OpenerDirector`调用
- `BaseHandler.unknown_open(req)` - 同上
- `BaseHandler.http_error_default(req, fp, code, msg, hdrs)` - 该方法并不在`BaseHandler`中定义, 但若其子类若希望捕获?(catch) 未处理的http errors, 需要定义该方法. 该方法应由`OpenerDirector`再出错时自动调用.\\
`req`是一个`Request`对象, `fp`是一个带有http error主体的类文件对象, `code`是错误代码, `msg`是用户可见的错误原因, `hdrs`是消息的头部字段的字典
- `BaseHandler.http_error_nnn(req, fp, code, msg, hdrs)` - 基本同上, `nnn`是错误编码. 若定义了该方法, 当nnn错误编码被返回时, 将被调用
- `BaseHandler.protocol_request(req)` - 该方法并不在`BaseHandler`中定义, 但若其子类若希望预处理请求, 需要定义该方法. 由OpenerDirector调用, req和返回值都是Request对象
- `BaseHandler.protocol_response(req, response)` - 该方法并不在`BaseHandler`中定义, 但若其子类若希望后处理响应, 需要定义该方法. `response`是与`urlopen`函数的返回值实现了同样接口的对象, 返回值同样如此.

### 21.6.4 HTTPRedirectHandler objects

- `HTTPRedirectHandler.redirect_request(req, fp, code, msg, hdrs, newurl)` - 对于重定向的响应, 返回Request或None. 当收到服务器的重定向响应, 由`http_error_30*()`方法自动调用.
- `HTTPRedirectHandler.http_error_30*(req, fp, code, msg, hdrs)` - 重定向到新的url, 由OpenerDirector调用
-
### 21.6.5 HTTPCookieProcessor Objects

- `HTTPCookieProcessor`的实例有属性`cookiejar`, 储存了cookies信息

### 21.6.6 ProxyHandler Objects

- `ProxyHandler.protocol_open(request)` - 修改请求, 设置代理, 再由后续的handler执行协议

### 21.6.7 HTTPPasswordMgr Objects

- 以下方法对`HTTPPasswordMgr`和`HTTPPasswordMgrWithDefaultRealm`对象是可用的
 - `HTTPPasswordMgr.add_password(realm, uri, user, passwd)` - uri可以是单个uri或uri的序列, realm, user, passwd是字符串. 使用(user, passwd)作为验证的token.
 - `HTTPPasswordMgr.find_user_password(realm, authuri)` - 寻找user和password
 - 对于`HTTPPasswordMgrWithDefaultRealm`对象, 若给定的realm没有任何匹配的user/passwd, realm被置为None

### 21.6.8 HTTPPasswordMgrWithPriorAuth Objects

- 拓展了`HTTPPasswordMgrWithDefaultRealm`, 支持跟踪总是需要发送认证证书的uris
- `HTTPPasswordMgrWithPriorAuth.add_password(realm, uri, user, passwd, is_authenticated=False)` - 基本同`HTTPPasswordMgr.add_password()`, `is_authenticated`用于设置对应的标识位, 若为真, realm将被忽略
- `HTTPPasswordMgr.find_user_password(realm, authuri)` - 同前
- `HTTPPasswordMgrWithPriorAuth.update_authenticated(self, uri, is_authenticated=False)` - 修改`is_authenticated`标志
- `HTTPPasswordMgrWithPriorAuth.is_authenticated(self, authuri)` - 返回标志位当前状态

### 21.6.9 AbstractBasicAuthHandler Objects

- `AbstractBasicAuthHandler.http_error_auth_reqed(authreq, host, req, headers)` - 获取user/password, 处理认证请求(重新尝试). `authreq`是请求中关于`realm`的头部字段名, `host`指定了url和路径, `req`是之前失败的请求对象, `headers`是错误头部
-

### 21.6.10 HTTPBasicAuthHandler Objects

- `HTTPBasicAuthHandler.http_error_401(req, fp, code, msg, hdrs)` - 用认证信息重新尝试请求

### 21.6.11 ProxyBasicAuthHandler Objects

- `ProxyBasicAuthHandler.http_error_407(req, fp, code, msg, hdrs)` - 同上

### 21.6.12 AbstractDigestAuthHandler Objects

- `AbstractDigestAuthHandler.http_error_auth_reqed(authreq, host, req, headers)` - 同上述`AbstractBasicAuthHandler`的方法

### 21.6.13 HTTPDigestAuthHandler Objects

- `HTTPDigestAuthHandler.http_error_401(req, fp, code, msg, hdrs)` - 同上

### 21.6.14 ProxyDigestAuthHandler Objects

- `ProxyDigestAuthHandler.http_error_407(req, fp, code, msg, hdrs)` - 同上

### 21.6.15. HTTPHandler Objects

- `HTTPHandler.http_open(req)` - 发送http请求

### 21.6.16. HTTPSHandler Objects

- `HTTPSHandler.https_open(req)` - 发送https请求

### 21.6.17. FileHandler Objects

- `FileHandler.file_open(req)` - 若五主机名或主机名是`localhost`, 打开本地文件

### 21.6.18. DataHandler Objects

- `DataHandler.data_open(req)` - 读取data url. 这类url将内容编码在url中了

### 21.6.19. FTPHandler Objects

- `FTPHandler.ftp_open(req)` - 打开ftp文件, 以空用户名和密码登录

### 21.6.20. CacheFTPHandler Objects

- `CacheFTPHandler`对象是增加了以下方法的`FTPHandler`:
 - `CacheFTPHandler.setTimeout(t)` - 设置超时
 - `CacheFTPHandler.setMaxConns(m)` - 设置最大连接数

### 21.6.21. UnknownHandler Objects

- `UnknownHandler.unknown_open()` - 抛出`URLError`异常

### 21.6.22. HTTPErrorProcessor Objects

- `HTTPErrorProcessor.http_response()` - 处理http错误响应. 若编码为200, 立即返回响应对象
- `HTTPErrorProcessor.https_response()` - 同上
