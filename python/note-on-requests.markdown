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
- Cookies 以 `RequestsCookies
