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

### 21.6.24 Legacy interface

- `urllib.request.urlretrieve(url, filename=None, reporthook=None, data=None)` - Copy a network object denoted by a URL to a local file.(这描述, 我服) 若`url`指向一个本地文件, 除非给定了文件名, 否则下载不会执行. 返回值是`(filename, headers)`的元组
 - `filename`省略时, 下载的将是临时文件, 文件名自动生成
 - `reporthook`若给定, 将在网络连接建立好之后以及每一快数据被读取之后, 调用一个`hook`函数, 它有3个参数: 目前已经转换的块数, 一块的字节大小, 文件的总的大小
 - 若采用`http:`scheme, 可以给出`data`参数, 从而使用POST方法. 如上所述, data必须是`application/x-www-form-urlencoded`格式的二进制对象, 可用`urllib.parse.urlencode()`函数加工
- `urllib.request.urlcleanup()` - 清理`urltrieve`方法残留的临时文件
- 其他已过时的不再列出

### 21.6 urllib.request Restrictions

- 目前只支持http, ftp, 本地文件和data urls
- `urlretrieve()`的缓存功能被取消了
- `urlopen`和`urlretrieve`函数会造成任意长的延迟, 这意味着若不使用线程, 很难建立一个交互式的web客户端
- `urlopen`和`urlretrieve`返回的数据都是服务器发回的原生数据, 可能是二进制数据(如图像), 纯文本, html等等, 可通过查看`Content-Type`首部字段确定(若事前知道返回类型, 就省了查询的功夫)

### 21.7 urllib.response

- 该模块定义了最简单的类文件接口, 包括`read()`和`readline()`
- 典型的`response`对象是一个`addinfourl`实例, 它定义了`info`方法, 可以此查看头部信息, 并由`geturl`方法.
- 其他函数与`urllib.request`模块定义的一样

## 21.7

## 21.8 urllib.parse

- 该模块提供了将url字符串分解成各组件, 或将组件组装成url字符串, 或将相对url转换成绝对路径
- 支持的应用层协议有: file, ftp, gopher, hdl, http, https, imap, mailto, mms, news, nntp, prospero, rsync, rtsp, rtspu, sftp, shttp, sip, sips, snews, svn, svn+ssh, telnet, wais.

### 28.1 URL Parsing

- url parsing 函数专注于url 字符串的分解与组装
- `urllib.parse.urlparse(urlstring, scheme='', allow_fragments=True)` - 将url解析成6部分, 返回一个6元tuple. 既定分解方案是: `scheme://netloc/path parameters?query#fragment`:

```python
> o = urlparse('http://www.cwi.nl:80/%7Eguido/Python.html')
> o
ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
            params='', query='', fragment='')
```

- `urlparse`recognizes a netloc only if it is properly introduced by ‘//’. Otherwise the input is presumed to be a relative URL and thus to start with a path component. 即只有域名前有`//`引导的url, 域名才会被正常解析, 否则整个路径将全被视为`path`:

```python
>>> urlparse('//www.cwi.nl:80/%7Eguido/Python.html')
ParseResult(scheme='', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
           params='', query='', fragment='')
>>> urlparse('www.cwi.nl/%7Eguido/Python.html')
ParseResult(scheme='', netloc='', path='www.cwi.nl/%7Eguido/Python.html',
            params='', query='', fragment='')
```

- 当url字符串中未指定`scheme`(方案)时, 可用`scheme`参数指定默认的scheme.
- `allow_fragments`为假时, url字符串中的fragment标志符将不会被识别, 而是作为path的一部分:

```python
In [4]: a = urlparse("https://docs.python.org/3/library/urllib.parse.html#url-parsing", allow_fragments=True)

In [5]: a
Out[5]: ParseResult(scheme='https', netloc='docs.python.org', path='/3/library/urllib.parse.html', params='', query='', fragment='url-parsing')

In [6]: a = urlparse("https://docs.python.org/3/library/urllib.parse.html#url-parsing", allow_fragments=False)

In [7]: a
Out[7]: ParseResult(scheme='https', netloc='docs.python.org', path='/3/library/urllib.parse.html#url-parsing', params='', query='', fragment='')
```

Attribute | Index | Value | Value if not present
 :--:     | :---: | :--:  | :---:
scheme   | 0 |  URL scheme specifier             | scheme parameter
netloc   | 1 |  Network location part            | empty string
path     | 2 |  Hierarchical path                | empty string
params   | 3 | Parameters for last path element  | empty string
query    | 4 |  Query component                  | empty string
fragment | 5 |   Fragment identifier             | empty string
username |   |     User name                     | None
password |   |    Password                       | None
hostname |   |    Host name (lower case)         | None
port     |   | Port number as integer, if present| None

- `urllib.parse.parse_qs(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace')` - 解析查询语句, 数据类型是`application/x-www-form-urlencoded`, 返回值是字典类型的. `keep_blank_values`用于指示忽略空格(false)或将空格当空格(true). `strict_parsing`指示忽略解析错误(false)或抛出`ValueError`异常(true). `encoding`与`error`指定解码方式.
- 使用`urllib.parse.urlencode()`函数将解析得到的字典重新组装为查询字符串
- `urllib.parse.parse_qsl(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace')` - 与`parse_qs()`相同, 但返回值是二元tuple的list

```python
In [3]: url = pas.urlparse("https://www.google.co.jp/?gfe_rd=cr&ei=wqhHV-zBLOXC8gf9qZMw&gws_rd=ssl#q=kissg+%E8%B5%B5%E5%96%A7%E5%85%B8")
In [5]: pas.parse_qs(url.query)
Out[5]: {'ei': ['wqhHV-zBLOXC8gf9qZMw'], 'gfe_rd': ['cr'], 'gws_rd': ['ssl']}
In [14]: pas.parse_qsl(url.query)
Out[14]: [('gfe_rd', 'cr'), ('ei', 'wqhHV-zBLOXC8gf9qZMw'), ('gws_rd', 'ssl')]
```
- `urllib.parse.urlunparse(parts)` - 将`urlparse()`函数返回的tuple重新组装成url. 事实上, `parts`可以是任意6个元素的可迭代对象

```python
In [19]: pas.urlunparse(url)
Out[19]: 'https://www.google.co.jp/?gfe_rd=cr&ei=wqhHV-zBLOXC8gf9qZMw&gws_rd=ssl#q=kissg+%E8%B5%B5%E5%96%A7%E5%85%B8'
In [22]: t = {"a": '1', "b": '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6'}
In [23]: pas.urlunparse(t)
Out[23]: 'a://b/d;c?e#f'
```

- `urllib.parse.urlsplit(urlstring, scheme='', allow_fragments=True)` - 与`urlparse`类似, 但不再分出`params`, 因此返回值是一个5元tuple`(addressing scheme, network location, path, query, fragment identifier)`
- `urllib.parse.urlunsplit(parts)` - 与`urlunparse`类似, 只不过是将`urlsplit`得到的tuple复原, 也可以是任意5元可迭代对象.
- `urllib.parse.urljoin(base, url, allow_fragments=True)` - 用base url(`base`)和另外的url(`url`)构造新的完整的url. 相当于用base url的内容补全url. `allow_fragments`的用法见上

```python
> from urllib.parse import urljoin
> urljoin('http://www.cwi.nl/%7Eguido/Python.html', 'FAQ.html')
'http://www.cwi.nl/%7Eguido/FAQ.html'
```

- `urllib.parse.urldefrag(url)` - 若url包含片段标志符, 返回去片段标志符的url与片段标志符字符串, 即完成分离的操作, 返回2元tuple.

```python
In [26]: pas.urldefrag('https://www.google.co.jp/?gfe_rd=cr&ei=wqhHV-zBLOXC8gf9qZMw&gws_rd=ssl#q=kissg+%E8%B5%B5%E5%96%A7%E5%85%B8')
Out[26]: DefragResult(url='https://www.google.co.jp/?gfe_rd=cr&ei=wqhHV-zBLOXC8gf9qZMw&gws_rd=ssl', fragment='q=kissg+%E8%B5%B5%E5%96%A7%E5%85%B8')
```

### 21.8.3 Structured Parse Results

- `urllib.urlparse()`解析的返回值实际是tuple的子类--`urllib.parse.ParseResult`:

```python
In [28]: url.__class__
Out[28]: urllib.parse.ParseResult
In [30]: isinstance(url, tuple)
Out[30]: True
```

- 同理, `urllib.urlsplit`的解析结果是`urllib.parse.SplitReuslt`对像, `urllib.urldefrag`的解析结果是`urllib.parse.DefragResult`对象.
- 若传入`urllib.urlparse`的url是二进制形式的, 返回结果为`urllib.parse.ParseResultBytes`. 同样适用于其他二者.
- `urllib.parse.SplitResult.geturl()` - 用`SplitReuslt`对象重构url, 与原url相比, 更标准化, 比如scheme会被转为小写形式, 空的字段将被移除:

```python
> url = 'HTTP://www.Python.org/doc/#'
> r1 = urlsplit(url)
> r1.geturl()
'http://www.Python.org/doc/'
```

### 21.8.4 URL Quoting

- `urllib.parse.quote(string, safe='/', encoding=None, errors=None)` - 用`%xx`将给定字符串中的特殊字符转义. 字母, 数字, `_.-`这些字符不会被转义. 另外不希望被转义的字符用`safe`参数给定. 另外2个参数与上相同:

```python
In [37]: pas.quote("kissg.me/赵喧典")
Out[37]: 'kissg.me/%E8%B5%B5%E5%96%A7%E5%85%B8'
```

- `urllib.parse.quote_plus(string, safe='', encoding=None, errors=None)` - 与`quote()`类似, 但字符串中的空格用`+`替换, 原串中的`+`会被转义. `safe`默认不再是`/`
- `urllib.parse.quote_from_bytes(bytes, safe='/')` - 与`quote()`相类, 参数不一样
- `urllib.parse.unquote(string, encoding='utf-8', errors='replace')` - `quote()`的逆, 用单一字符替换`%xx`
- `urllib.parse.unquote_plus(string, encoding='utf-8', errors='replace')` - `quote_plus()`的逆
- `urllib.parse.unquote_to_bytes(string)` - `quote_from_bytes()`的逆
- `urllib.parse.urlencode(query, doseq=False, safe='', encoding=None, errors=None, quote_via=quote_plus)` - 将映射对象(mapping object), 或二元tuple的序列转为ascii文本串.
 - 若返回值是作为POST方法的`data`, 需要编码成二进制形式, 否则将报`TypeError`
 - 返回值是一些列的`key=value`, 用`&`连接. `quote_via`参数指定了转换的函数, `key`与`value`都将用指定函数转换
 - 当`query`的`value`本身是一个序列时, 若`doseq`参数为True, 则这每一对键值都被处理为一个`key=value`, 并用`&`分隔开; `doseq`为False, 则序列被当作一个整体对待, 有所转义.
 - `safe`, `encoding`, `errors`参数将传入`quote_via`

```python
In [39]: a = {"a": 1, "b": [1,2,3]}
In [42]: pas.urlencode(a)
Out[42]: 'b=%5B1%2C+2%2C+3%5D&a=1'
In [43]: pas.urlencode(a, doseq=True)
Out[43]: 'b=1&b=2&b=3&a=1'
```
