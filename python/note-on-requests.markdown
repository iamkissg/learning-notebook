# Requests: HTTP for Humans

> Requests 是唯一的非转基因 HTTP 库 for Python, 人类友好的
对于其他 HTTP 库的二次利用, 可能会导致危险的副作用, 包括: 安全漏洞, 冗长 (verbose) 代码, 重复造轮子, 需要经常性地翻看文档, 绝望, 头痛, 甚至死亡

- Requests 允许用户发送*有机的*, *绿色的* HTTP/1.1 请求, 而不需要手动的操作. 不必为 URLs 手动添加查询字符串, 也不必手动设置 POST 数据的编码形式. 通过 urllib3, Requests 会自动保持连接 (Keep-alive), 和 HTTP 连接池 (connection pooling) (Requests 已经内嵌了 urllib3)
- Requests 支持的功能:
    - International Domains and URLs, 国际域与 URLs
    - Keep-Alive & Connection Pooling, 保持连接与连接池
    - Sessions with Cookie Persistence, Cookie 持久化的会话
    - Browser-style SSL Verification, 浏览器风格的 SSL 验证
    - Basic/Digest Authentication, 基础/摘要(?) 验证
    - Elegant Key/Value Cookies, 优雅的键值 Cookies
    - Automatic Decompression, 自动解压
    - Automatic Content Decoding, 自动解码
    - Unicode Response Bodies, Unicode 响应主体
    - Multipart File Uploads, 分段文件上传
    - HTTP(S) Proxy Support, HTTP(S) 代理支持
    - Connection Timeouts, 连接超时
    - Streaming Downloads, 流式下载
    - `.netrc` Support
    - Chunked Requests, 分块请求
    - Thread-safety, 线程安全

> Requests is the perfect example how beautiful an API can be with the right level of abstraction.

## 介绍

#### 哲学

- 沿用了 [PEP20](https://www.python.org/dev/peps/pep-0020/) 的部分哲学:
    1. Beautiful is better than ugly.
    2. Explicit is better than implicit.
    3. Simple is better than complex.
    4. Complex is better than complicated.
    5. Readability counts.

## Quickstart

- 最简单的使用: `import requests; r = requests.get("http://api.github.com/events")` 此时就获得了一个 `Response` 对象, 它包含了我们所需的所有信息
- Requests 的简单 API 意味着任何形式的 HTTP 请求都是显而易见的
- 简单例子:

```python
>>> r = requests.get("http://api.github.com/events")
>>> r = requests.post('http://httpbin.org/post', data = {'key':'value'})
>>> r = requests.put('http://httpbin.org/put', data = {'key':'value'})
>>> r = requests.delete('http://httpbin.org/delete')
>>> r = requests.head('http://httpbin.org/get')
>>> r = requests.options('http://httpbin.org/get')
```

#### 向 URL 传递参数

- 若要手动创建查询字符串, 需要在一个问号标记之后以键值对的形式给出查询字符串, 比如: `httpbin.org/get?key=val`. 使用 Requests, 可以用字典的形式封装键值对, 只需要传递给 `params` 关键字参数即可. 值为 `None` 的 key 不会被加入 URL 中; 可以用 `key: list of value` 的形式传入 a list of items as value

#### 响应内容

- Requests 会自动对服务器返回的内容进行解码. 当发起请求时, Requests 会基于 HTTP 头部, 猜测响应的编码形式. 当使用 `r.text` 访问文档内容时, Requests 才会猜测编码格式, 并解析. 可使用 `r.encoding` 查看编码格式, 对其赋值进行修改, 之后再通过 `r.text` 查看文本内容, 将以新的编码格式解析
- Requests 还允许用户自定义编码格式. 用户利用 `codecs` 创建并注册自定义的编码格式, 之后为 `r.encoding` 重复赋值即可

#### 二进制响应内容

- 对于非文本的请求, 可以 `bytes` 的形式访问响应主体 (body)
- `gzip` 和 `deflate` 转码会自动进行
- 利用请求返回的二进制数据创建图像:

```python
import requests
from PIL import Image
from io import BytesIO

r = requests.get("http://docs.python-requests.org/en/latest/_static/requests-sidebar.png")
i = Image.open(BytesIO(r.content))
i.show()
```

#### JSON 响应内容

- Requests 内置有 JSON 解码器, 使用方法是: `r.json()`. 解码失败会抛出异常
- 需要注意的是, `r.json()` 的成功调用并不意味着响应成功了. 因为一些服务器在响应失败的情况下会返回一个 JSON 对象, 比如 HTTP 500 的更多错误细节.
- 检查请求是否成功, 应调用 `r.raise_for_status()` (出错的情况下, 抛出句保存的 `HTTPError`) 或检查 `r.status_code` 是否是预期的值

#### 原始响应内容

- 在少数情况下, 可能需要从服务器获取原始的 socket response, 此时可访问 `r.raw`. 但是在发起请求时需要指定 `stream=True`
- 使用下述形式保存流式文件:

```python
with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size):
        fd.write(chunk)
```

- `Response.iter_content` 是直接使用 `Response.raw` 的一种更灵活的替代方法. 当使用流的方式下载时, 这是一种推荐的解构方法

#### 自定义头部

- 要自定义 HTTP 头部, 简单地向 `headers` 关键字参数传递一个 `dict` 即可.
- 注意: 自定义头部的优先级比更多特定的信息源要低 (?, Custom headers are given less precedence than more specific sources of information). 比如:
    - 如果在 `.netrc` 中指定了证书, 使用 `headers=` 表示的认证类头部(Authorization headers)会被覆盖. 但依旧会被 `auth=` 参数覆盖
    - 认证头部在重定向脱离主机 (get redirected off-host) 的情况下将被移除
    - 代理认证头部 (Proxy-authorization headers) 在 URL 中提供了代理证书的情况下会被覆盖
    - 当内容长度是以计量的情况下, Content-Length 头部会被覆盖
- Requests 不会因为自定义头部的指定而改变行为. 头部只是简单地传递给最终的请求

#### 更复杂的 POST 请求

- 一些时候, 用户可能想要发送非格式化编码的数据. 如果传递的是一个 `str`, 而不是 `dict`, 数据会直接被 POST
- 一些网站可能接收 JSON 格式的数据, 此时一种方式是手动将 `dict` 编码为 `json`: `data=json.dumps(payload)`. Requests 提供了更简单的方法, 将传给 `json` 关键字参数

#### POST 多部分编码的文件

- Requests 使上传多部分编码的文件变得容易:

```python
>>> url = 'http://httpbin.org/post'
>>> files = {'file': open('report.xls', 'rb')}

# tuple 的顺序是关键, 不能有差
# 显式地设置 filename, content_type, headers:
# >>> files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}

# 还可以发送字符串, 并以文件形式接收
# files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}

>>> r = requests.post(url, files=files)
>>> r.text
{
  ...
  "files": {
  "file": "<censored...binary...data>"
  },
  ...
}
```

- 当要以 `multipart/form-data` 请求方式 POST 一个超大文件时, 合适的方式是以流 (stream) 的方式发送. 但 Requests 默认不支持此, 可用一个分离的包 `request-toolbelt`. [Toolbelt 文档](https://toolbelt.readthedocs.io/)

> 强烈建议以[二进制模式](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)打开文件. 因为 Requests 会试着补全 `Content-Length` 头部, 这样, `Content-Length` 头部的值会被设置成文件的字节数. 若以文本模式打开文件, 可能会报错

#### 响应状态码

- `r.status_code` 查看响应状态码
- 为了方便检查响应结果, Requests 提供了内建的状态码检查对象. 比如: `r.status_code == requests.codes.ok`
- 当发送了一个坏的请求 (bad request), 我们可以用 `Response.raise_for_status()` 抛出异常: `bad_r.raise_for_status()`. 若状态码是 200 时, `r.raise_for_status()` 返回 `None`

#### 响应头部

- `r.headers` 将以 Python 字典的形式展示响应头部信息. 根据 [RFC 7230](https://tools.ietf.org/html/rfc7230#section-3.2), **HTTP 头部是大小写不敏感的**
- 两种方式查看某头部字段: `r.headers['Content-Type']` 或 `r.headers.get('content-type')`
- 服务器在相同的头部使用了多个不同的值. 但由于请求是绑定的, 它们在字典中只需要用一个单一映射表示, 用逗号分隔

#### Cookies

- `r.cookies[example_cookie_name]` 可以快速访问 Cookies (如果响应包含 Cookies 的话)
- 使用 `cookies` 关键字参数, 向服务器发送带 Cookies 的请求
- Cookies 以 `RequestsCookieJar` 形式返回, 类似一个 dict, 但能提供更复杂的接口, 适用于多域或多路径的情况. Cookie jars 也可以作为请求的参数

#### 重定向与历史

- 除了 `HEAD` 请求, Requests 默认会进行所有的位置重定向. 可使用 `history` 属性跟踪响应对象的重定向详情
- `Response.history` 列表包含了对于一个请求所有的响应对象, 并按时间序列排序
- GET, OPTIONS, POST, PUT, PATCH or DELETE 这些请求, 可以设置参数 `allow_redirects=False` 来取消重定向
- HEAD, 也可以设置 `allow_redirects=True` 进行重定向. 该方法默认不重定向

#### 超时

- 使用 `timeout` 参数, 设置超时. Requests 在超过超时时间之后, 就不再等待响应. 如果没有显式地设置超时, 请求将不处理超时
- `timeout` 不是对于整个响应到达的时间限制; 而是在 `timeout` 设置的时间之前, 服务器没有响应, 即底层 socket 没有收到任何字节信息, 抛出异常.

#### 错误与异常

- 由于网络问题(DNS 解析失败, 拒绝连接等等), Requests 会抛出 ConnectionError 异常
- `Response.raise_for_status()`, 在HTTP 请求没有得到成功的状态码时, 会抛出 `HTTPError` 异常
- 请求超时, 抛出 `Timeout` 异常
- 若请求超出了设置的最大重定向数, 抛出 `TooManyRedirects` 异常
- 所有 Requests 的显式异常都继承自 `requests.exceptions.RequestException`

## 高级应用

#### 会话对象

- 会话对象允许你跨请求地持久化特定的参数. 通过会话实例, 还能为所有请求持久化 cookies (使用 urlib3 的连接池). 因此如果对同一个主机发起来了多个请求, 将复用底层的 TCP 连接, 这就带来了显著的性能提升 (significant performance increase)
- 会话对象具有主要的 Requests API 提供的方法. 首先 `s = requests.Session()` 创建一个会话对象, 之后的操作与上无异.
- 会话也可以用于向请求方法提供默认数据, 通过向会话对象的属性提供数据实现, 比如:

```python
s = requests.Session()
s.auth = ('user', 'pass')
s.headers.update({'x-test': 'true'})

# both 'x-test' and 'x-test2' are sent
s.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
```

- 任何传递给请求方法的字典, 将在会话级别 (session-level) 以集合的形式混合. `方法级别 (method-level) 的参数会覆盖会话参数`
- 然而方法级别的参数不能跨请求持久化, 即使使用会话. 例如下述例子只会在第一个请求时发送 cookies:

```python
s = requests.Session()

r = s.get('http://httpbin.org/cookies', cookies={'from-my': 'browser'})
print(r.text)
# '{"cookies": {"from-my": "browser"}}'

r = s.get('http://httpbin.org/cookies')
print(r.text)
# '{"cookies": {}}'
```

- 若希望手动地添加 cookies 到会话, 使用 [Cookie utility functions](https://requests.readthedocs.io/en/master/api/#api-cookies) 操作 Session.cookies
- 会话还可以被用作上下文管理器 (context managers):

```python
# 可以确保会话的关闭
with requests.Session() as s:
    s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
```

###### 从 Dict 参数中删除值

- 有时候, 可能需要从字典参数中省略会话级别的键. 只需要对方法级别的参数, 使用同名键, 并设置值为 `None`
- 一个会话中包含的所有值都是直接可得的.

#### 请求和响应对象

- 无论什么时候调用 `requests.get()`, 主要做了 2 件事:
    1. 构建 `Request` 对象, 然后请求被发送给服务器, 以请求或查询资源
    2. 一旦请求从服务器获得了响应, 就生成一个 `Response` 对象
- `Response` 对象包含`所有`服务器返回的信息, 还包含 `Request` 对象. `r.request` 来获得当前响应对象的请求. `r.headers` 访问响应头部, `r.request.headers` 访问请求头部

#### 准备请求

- 无论何时, 收到 API 调用或会话调用的 `Response` 对象, 这个 `request` 属性实际是 `PreparedRequest`.
- 有时候, 可能想要在发送请求之前, 对 body 或 headers (或其他任何事情) 做一些额外的工作. 以下是一个例子:

```python
from requests import Request, Session

s = Session()

req = Request('POST', url, data=data, headers=headers)
prepped = req.prepare()

# do something with prepped.body
prepped.body = 'No, I want exactly this as the body.'

# do something with prepped.headers
del prepped.headers['Content-Type']

resp = s.send(prepped,
    stream=stream,
    verify=verify,
    proxies=proxies,
    cert=cert,
    timeout=timeout
)

print(resp.status_code)
```

- 如果不再对 `Request` 对象做特殊处理, 就可以马上 prepare it, 并修改 `PreparedRequest` 对象, 然后就随同其他参数一起发送请求
- 然而, 上面的代码会丧失一部分会话对象的优点. 尤其是, 会话级别的状态, 比如 cookies 将不能应用于请求.
- 为了使 `PreparedReuqest` 能应用状态, 调用 `Session.prepare_request()` 代替 `Request.prepare()`:

```python

m requests import Request, Session

s = Session()
req = Request('GET',  url, data=data, headers=headers)

prepped = s.prepare_request(req)

# do something with prepped.body
prepped.body = 'Seriously, send exactly these bytes.'

# do something with prepped.headers
prepped.headers['Keep-Dead'] = 'parrot'

resp = s.send(prepped,
    stream=stream,
    verify=verify,
    proxies=proxies,
    cert=cert,
    timeout=timeout
)

print(resp.status_code)
```

#### SSL 证书认证

- 为 HTTPS 请求认证 SSL 证书, 就像网络浏览器一样
- 默认的, SSL 认证是打开的. 若不能验证证书的有效性, Requests 将抛出 SSLError
- 通过 `verify` 关键字参数选择证书, 可以是证书文件或所在目录, 比如: `requests.get('https://github.com', verify='/path/to/certfile')`
- 持久化证书, 则可以考虑使用 Session:

```python
s = requests.Session()
s.verify = '/path/to/certfile'
```

- If verify is set to a path to a directory, the directory must have been processed using the `c_rehash` utility supplied with OpenSSL.
- 通过 `REQUESTS_CA_BUNDLE` 环境变量可设置信任 CA 列表
- 设置 `verify=False`, 可忽略 SSL 证书认证. 默认, `verify=True`, 其只会应用于主机证书
- 若要指定本地证书为客户端证书, 可以是包含私钥和证书的单个文件, 也可以是证书和密钥文件路径的 tuple (本地证书的私钥必须是非加密的! Requests 目前并不支持加密密钥):

```python
requests.get('https://kennethreitz.com', cert=('/path/client.cert', '/path/client.key'))
<Response [200]>
```

- 或通过 Session 持久化:

```python
s = requests.Session()
s.cert = '/path/client.cert'
```

- 证书路径错误, 或证书非法, 抛出 SSLError

#### CA 证书

- 默认的, Requests 绑定了一些 [Mozilla trust store](https://hg.mozilla.org/mozilla-central/raw-file/tip/security/nss/lib/ckfw/builtins/certdata.txt) 上的可信任根 CA. 但是, 证书绑定只在 Requests 更新版本时进行, 这意味着若长期使用旧版 Requests 而不进行更新, 证书将过时.
- 从版本 2.4.0 开始, 若系统上安装了 [certifi](https://certifi.io/en/latest/), Requests 将自动使用 certifi 提供的证书. 这使用户在不修改代码的情况下就可以更新信任证书.
- 安全起见, 建议定期更新 certifi

#### Body Content Workflow

- 默认的, 当发起一个请求时, 响应的主体 (body) 会被立即下载. 可覆盖此行为, 使得只有在访问 `Response.content` 时才下载响应主体, 需设置 `stream` 参数:

```python
tarball_url = 'https://github.com/kennethreitz/requests/tarball/master'
r = requests.get(tarball_url, stream=True)
```

- 此时, 只有响应头部被下载, 并保持连接开放, 因此可以有条件地获取内容:

```python
if int(r.headers['content-length']) < TOO_LONG:
  content = r.content
  ...
```

- 通过 `Response.iter_content()` 和 `Response.iter_lines()` 方法, 可以更好地控制工作流. 另外, 可以使用 `Response.raw` 来读取未解码的 body, 其底层使用的是 urllib3 的 urllib3.HTTPResponse
- 如果设置了 `stream` 为 `True`, 发送请求之后, Requests 不会释放连接回连接池, 除非所有的数据都已经取出, 或调用 `Response.close`. 这就造成了连接的低效. 当使用 `stream=True`, 而你只是部分读取了内容或压根没读取, 你应该考虑使用 [contextlib.closing](https://docs.python.org/3/library/contextlib.html#contextlib.closing):

```python
from contextlib import closing

with closing(requests.get('http://httpbin.org/get', stream=True)) as r:
    # Do things with the response here.
```

#### Keep-Alive

- 多亏了 urllib3, 在一个会话中, keep-alive 将 100 % 自动被执行. 一个会话中, 任何请求将自动复用连接
- 只有在所有 body 的数据都被读取了, 连接才会被释放回到连接池中; 因此, 要确保设置 `stream=False` 或读取 Reponse 对象的 `content` 属性

#### Streaming Uploads

- Requests 支持流式上传, 这使得可以在不将内容读取到内存, 而直接上传超大流或文件. 在 body 中提供类文件对象, 以实现流式上传:

```python
with open('massive-body', 'rb') as f:
    requests.post('http://some.url/streamed', data=f)
```

> 强烈建议以[二进制模式](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)打开文件. 因为 Requests 会试着补全 `Content-Length` 头部, 这样, `Content-Length` 头部的值会被设置成文件的字节数. 若以文本模式打开文件, 可能会报错

#### 块编码请求

- Requests 支持传出与传入请求的块转换编码 (Chunked transfer encoding). 要发送块编码请求, 为 body 提供生成器 (也可以是没有长度限制的任何迭代器):

```python
def gen():
    yield 'hi'
    yield 'there'

requests.post('http://some.url/chunked', data=gen())
```

- 对于块状编码响应, 最好的迭代方式是 `Response.iter_content()`. 理想的情况是, 对请求设置了 `stream=True`, 然后就可以调用 `iter_content` 按块进行迭代 (需要设置 `chunk_size=None`). 若要设置块的最大限制, 可以设置 `chunk_size` 为任意整数

#### POST Multiple Multipart-Encoded Files

- 在一个请求中, 可以发送多个文件. 假设, 要上传到多个图片文件到 HTML 表单的多文件字段 `images`:

```html
<input type="file" name="images" multiple="true" required="true"/>
```

- 用 list of tuples of `(form_field_name, file_info)` 即可:

```python
>>> url = 'http://httpbin.org/post'
>>> multiple_files = [
        ('images', ('foo.png', open('foo.png', 'rb'), 'image/png')),
        ('images', ('bar.png', open('bar.png', 'rb'), 'image/png'))]
>>> r = requests.post(url, files=multiple_files)
>>> r.text
{
  ...
  'files': {'images': 'data:image/png;base64,iVBORw ....'}
  'Content-Type': 'multipart/form-data; boundary=3131623adb2043caaeb5538cc7aa0b3a',
  ...
}
```

#### Event Hooks

- Requests 自带 hook 系统, 可用于操作请求的部分过程, 操作信号事件的处理
- 可用的 hooks:
    - `response` - 请求生成的响应
- 通过 `{hook_name: callback_function}` 的形式定义一个 hook, 可以在每个请求的基础上, 为请求赋一个 hook function (指定 hooks 参数):

```python
# 回调函数将接受一块数据作为第一参数
def print_url(r, *args, **kwargs):
    print(r.url)
    r.url = "http://kissg.me/"
    return(r)

hooks=dict(response=print_url)

requests.get('http://httpbin.org', hooks=dict(response=print_url))
```

- 当执行回调时发生错误, 将给出一个警告
- 若回调函数返回了一个值, 它将替换传入的的数据. 若无返回值, 则不会有任何影响. 如上所示, 传入的响应对象的 url 是 `http://httpbin.org/`, 通过 hooks 之后, 被修改为 `http://kissg.me/`
