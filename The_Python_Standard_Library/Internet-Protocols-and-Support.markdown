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
