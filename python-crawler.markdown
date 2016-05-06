##Python Crawler


###My older Records(based on python2)

- 网页是一张网, 其上的图片, 文字, 链接都是这张网上粘住的资源
- 浏览网页的过程: 用户输入网址，经过DNS服务器, 找到服务器主机, 向服务器发出一个请求, 服务器经过解析之后, 发送给用户浏览器HTML、JS、CSS 等文件, 浏览器解析后将网页展示出来.
- 用户看到的网页实质是由HTML代码构成的，爬虫爬来的便是这些内容，通过分析和过滤这些HTML代码，实现对图片、文字等资源的获取。
- 所谓网页抓取，就是把URL地址中指定的网络资源从网络流中读取出来，保存到本地。
- 爬虫程序的推荐写法: 创建`request`对象, 以便添加更多的内容, 再以`request`为参数调用`urlopen`方法. 逻辑上, `request`和`response`的应答也显得更清晰, 自然.
- get vs. post:
 1. 最重要的区别是GET方式是直接以链接形式访问, 链接中包含了所有的参数, 包括输入的密码; POST则不会在网址上显示所有的参数
 2. GET 和 POST 请求的不同之处是 POST 请求通常有"副作用"，它们会由于某种途径改变系统状态
- 使用`data`来传递数据:
 1. post方式 : 构造字典, 调用urllib.urlencode方法将字典编码, 再将编码得到的`data`作为参数传入`request`
 2. get方式  : 构造字典, 对字典进行编码, 通过形如 geturl = url + '?' + data的方式直接将参数写在网址上
- 设置`headers`
 1. 原因: 一些网站会对访问进行识别, 如果识别有问题, 站点将不会响应. 设置`headers`属性, 是为了`模拟浏览器的工作`
 2. 设置方法: 构造headers字典, 将headers作为参数构造request实例
 3. 服务器会识别headers中的referer是否自己, 如果不是, 一些服务器不会响应(防盗链). 解决办法: 可以在headers中加入referer项
- 设置代理
 1. 原因: 一些网站可能会检测某段时间内, 某个ip的访问次数, 如果访问次数过多, 网站将禁止访问
 2. urllib2默认使用环境变量`http_proxy`来设置HTTP Proxy. 解决上述问题, 可以设置一些代理服务器来帮助工作, 每隔一段时间换一个代理
- `cookie的`使用
 1. `cookie`, 指某些网站为了辨别用户身份, 进行session跟踪而储存在用户本地终端上的数据(通常经过加密)
 2. 有些网站需要登录后才能访问某个页面, 可以使用urllib2库保存Cookie, 然后再抓取其他页
- 正则表达式
 1. 正则表达式是对字符串操作的一种逻辑公式，就是用事先定义好的一些特定字符、及这些特定字符的组合，组成一个“规则字符串”，这个“规则字符串”用来表达对字符串的一种过滤逻辑
 2. 正则表达式的大致匹配过程是：
  1. 依次拿出表达式和文本中的字符比较
  2 如果每一个字符都能匹配，则匹配成功；一旦有匹配不成功的字符则匹配失败
  3. 如果表达式中有量词或边界，这个过程会稍微有一些不同
 3. 正则表达式相关注解:
  1. 数量词的贪婪模式与非贪婪模式: Python里数量词默认是贪婪的, 总是尝试匹配尽可能多的字符(所以, 非贪婪就意味着总是尝试匹配尽可能少的字符). 一般使用非贪婪模式提取
  2. 反斜杆问题: Python中的原生字符串能较好地解决多次使用反斜杆转义带来的漏写问题, 而且表达式更直观
- Beautiful Soup

###New Records

```python
# a crawler framework
seen = set()
urls = queue()

begin_site = "kissg.me"
seen.insert(begin_site)
urls.put(begin_site)

while True:
    if u

while True:
    if urls.size > 0:
        current_url = urls.get()
        store(current_urk)
        for next_url in extract_urls(current_url):
            if next_url not in seen:
                seen.insert(next_url)
                urls.put(next_url)
    else:
        break
```

- 三利器:`regex`, `set`, `deque`
- 在爬虫程序中, 为了不重复爬取已经爬过的网站, 需要将爬过的页面的url放进`集合`中, 每次爬某个url之前, 先看集合中是否已经存在, 若已经存在, 则跳过; 否则将url放入集合中, 再去爬网页
- 集合的创建可以是`set()`, 也可以用`{}`只是没有键. 空集的创建不能用`{}`, 因为它创建的是一个空的`dict`
- 爬虫爬回来的数据是一个字符串, 字符串的内容是页面的html代码, 因此要从页面中提取中所有url, 要求爬虫程序有简单的字符串处理能力, `正则表达式`
- 在爬虫程序中用到`广度优先搜索(BFS)算法`, 用到的数据结构是队列, 并且用`colletions.deque`来高效地完成任务
- `response.getheader(name)`获取头部字段, 返回字符串
- 伪装浏览器: 为爬虫请求添加头部模拟浏览器:
 1. 利用原始的urlopen, 简单, 但可拓展性差
 2. 自定义opener
- 模拟登录:
 1. 观察浏览器的行为
 2. 解压缩(如果有必要)
 3. 获取登录必要的额外信息
 4. 发送post请求, 一旦登录, 服务器会设置一个cookie并发回给用户, 这时需要做的就是处理cookie
- 第三方库: `Request`, `BeautifulSoup`
- 
- 

