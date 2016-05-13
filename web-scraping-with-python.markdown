#Python网络数据采集

- 非原创即采集
- 一念清净, 烈焰成池, 一念觉醒, 方登彼岸
- 网络数据采集, 无非就是写一个自动化程序向网络服务器请求数据, 再对数据进行解析, 提取需要的信息
- 通常, 有api可用, api会比写网络爬虫程序来获取数据更加方便.

##Part1 创建爬虫

###Chapter1 初建网络爬虫

- 一旦你开始采集网络数据, 就会感受到浏览器为我们所做的所有细节, 它解释了所有的html, css, JavaScript
- 网络浏览器是一个非常有用的应用, 它创建信息的数据包, 发送, 并把获取的数据解释成图像, 声音, 视频, 或文字. 但网络浏览器就是代码, 而代码是可以分解的, 可以分解成许多基本组件, 可重写, 重用, 以及做成我们想要的任何东西
- "域名为kissg.me的服务器上<网络应用根地址>/pages目录下的html文件page1.html的源代码"
- 网络浏览器与爬虫程序的区别:
 - 浏览器遇到html标签时, 会向服务器再发起对该资源的请求, 再用请求得到的资源渲染页面
 - 爬虫程序并没有返回向服务器请求多个文件的逻辑, 它只能读取已经请求的单个html文件
- `BeautifulSoup`通过定位html标签来格式化和组织复杂的网络信息, 以python对象展示xml结构信息
- 先调用`response.read()`获取网页的内容, 再将html内容传给BeautifulSoup对象, 形成的结构如下所示:

```python
html → <html><head>...</head><body>...</body></html>
    — head → <head><title>A Useful Page<title></head>
        — title → <title>A Useful Page</title>
    — body → <body><h1>An Int...</h1><div>Lorem ip...</div></body>
        — h1 → <h1>An Interesting Title</h1>
        — div → <div>Lorem Ipsum dolor...</div>
```

- 因此可以通过`bsObj.html.body.h1`的方式提取标签
- 请求的网页在服务器上不存在时, 程序会返回http错误, urlopen函数会抛出`HTTPError`异常, 对此, 可使用`try ... except ...`语句来处理
- 服务器不错在, urlopen返回一个None对象, 可通过条件判断简单地处理
- 当调用的标签不存在时, BeautifulSoup会返回None对象, 请求None对象的子标签, 会发生`AttributeError`错误, 同样地, 也用`try ... except ... `语句来处理
- `一个良好的爬虫程序首先要具备强大而周密的异常处理能力, 随时应对网络中可能存在的异常`
- 在写爬虫的时候, 思考代码的总体格局, 让代码既可以**捕捉异常**又**容易阅读**, 很重要. 考虑代码的重用性

###Chapter2 复杂html解析

- 当米开朗基罗被问及如何完成"大卫"这样匠心独具的雕刻作品时, 他有一段著名的回答: "很简单, 你只要用锤子把石头上不像大卫的地方敲掉就行了." (大道至简)
- 解析html的前戏, 磨刀不勿砍柴功:
 1. 寻找"打印此页", 或看看网站有没有html样式更友好的移动版(将请求头设置成移动设备的状态, 然后接收网站移动版)
 2. 需找隐藏在js文件里的信息,
 3. 网页信息也许可以从网页的url链接中获取
 4. 寻找其他数据源, 有没有其他网站显示了同样的数据? 该网站的数据是不是来自其他网站
- css(cascading style sheet, 层叠样式表)为爬虫提供了便利, 它是html元素差异化, 使那些具有相同修饰的元素呈现不同的样式, 从而是爬虫的目标更明确
- `findAll()`的基础用法: `findAll(tag_name, dict_of_attributes)`
- 使用`bsObj.tagName`只能获取页面中第一个指定的标签
- `get_text()`方法正在处理的html文档中的所有标签都清楚掉, 返回只包含文字的字符串
- `findAll(tag, attributes, recursive, text, limit, **keywords)` & `find(tag, attributes, recursive, text, **keywords)`:
 - tag - 可以是单个标签名, 也可以是多个标签名组成的列表(集合)
 - attributes - 用字段封装的标签属性与属性值, 属性值可以是一个集合
 - recursive - 递归? 默认为True. 若recursive=False, findAll只会查文档的一级标签. 若对速度要求非常高, 可设置递归参数
 - text - 用标签的内容去匹配, 而不是标签名或属性,
 - limit - 限制findAll的搜索结果项
 - 关键字参数 - 允许用户自己指定属性的标签. 是BeautifulSoup在技术上做的冗余功能, 任何关键字参数能完成的任务, 都可以其他技术解决
- 通过标签参数`tag`把标签列表传到`.findAll()`里获取一列标签, 其实是一个"或"关系的过滤器. 而关键字参数可以增加一个"与"关系的过滤器来简化工作
- `Tag`对象 - `BeautifulSoup`对象通过`find`或`findAll`, 或直接调用子标签获取的一些列对象或单个对象
- `NavigableString`对象 - 用于表示标签里的文字
- `Comment`对象 - html文档的注释标签
- html页面可以映射成一棵树
- 子标签, 即一个父标签的下一级; 后代标签, 指一个父标签下面所有级别的标签. 所有子标签都是后代标签, 但不是所有的后代标签都是子标签
- 一般, bs函数总是处理当前标签的后代标签, 比如`.findAll`就是递归地在所有后代标签中查找
- 使用`.children`将只获取当前标签的子标签,  使用`descendants`将获取所有后代标签
- 使用`.next_siblings`将获得当前标签之后,所有的兄弟标签. 注意, 对象本身不能作为自己的兄弟标签; 从名字也可以看出, 是返回之后的兄弟标签. 相应的有`previous_siblings`,`next_sibling`和`previous_sibling`
- 使用`bsObj.find("table", {"id": "giftList"}).tr`而不是简单的`bsObj.table.tr`或`bsObj.tr`是为了让对象的选择更具体, 而不丢失标签的细节
- `parent`和`parents`分别用于获取标签对象的直接父标签和所有父辈标签(包括爷爷, 但不包括叔叔, 好吧, 通俗易懂)
- 在动手写正则表达式之前, 写一个步骤列表描述出目标字符串的结构
- regex:
 - `*` - 重复任意次, 包括0次
 - `|` - 表示或
 - `+` - 重复至少1次
 - `[]` - 匹配其中的任意一个字符
 - `()` - 表达式编组, 在regex的规则里编组会优先运行
 - `{m,n}` - 重复m到n次
 - `[^]` - 匹配一个任意不在方括号中的字符
 - `.` - 匹配任意单个字符
 - `^` - 标识字符串的开始
 - `\` - 转义字符
 - `$` - 标识字符串的结尾
- 在BeautifulSoup中使用regex, 提高效率, 如`images = bsObj.findAll("img",{"src":re.compile("\.\.imggifts/img.*\.jpg")})`
- regex可以作为BeautifulSoup语句的任意一个参数
- 对于标签对象, 可采用`.attrs`获取全部属性, 返回字典对象. `imgTag.attrs["src"]`就可以获取图片的资源位置
- BeautifulSoup允许将特定函数类型作为`findAll`函数的参数, 唯一的限制条件是这些函数必须将一个***标签作为参数***且***返回结果是布尔类型***. BeautifulSoup用这个函数评估遇到的每个标签对象, 将评估结果为"True"的标签保留下来, 将其他标签剔除. 如`soup.findAll(lambda tag: len(tag.attrs) == 2)`将返回具有2个属性的标签
- BeautifulSoup与regex与lambda的联合使用, 想想都无敌
- 其他的html解析模块:
 1. lxml - 底层, 大部分源代码用c写成, 因此处理速度会非常快
 2. HTML parser - 自带的

###Chapter3 开始采集

- 之所以叫网络爬虫, 是因为他们可以沿着网络爬行, 本质是一种*递归方式*: 为了找到url链接, 必须首先获取网页内容, 检查页面内容, 再寻找另一个url, 获取页面内容, 不断循环
- 使用网络爬虫的时候, 应谨慎地考虑需要消耗多少网络流量, 还要尽量思考能否让采集目标的服务器负载更低
- `维基百科六度分隔理论` - 任何2个不相干的词条, 都可以通过总数不超过6条的词条链接起来(包括原来的2个词条).
- 由此, 写爬虫时, 如何高效地通过最少的链接点击次数到达目的站点, 不仅使爬虫工作效率更高, 且对服务器的负载影响也越小
- 爬取的内容往往携带许多无用的信息, 在处理之前, 应根据实际剔除无用信息
- 随机算法都努力创造一种均匀分布且难以预测的数据序列, 但在算法初始阶段都需要提供一个随机数种子(random seed). 完全相同的种子每次将产生相同的"随机"数序列. 可以用系统当前时间作为随机数种子, 而使程序运行更具随机性.
- python的伪随机数生成器用的是梅森旋转算法(https://en.wikipedia.org/wiki/Mersenne_Twister)
- 浅网(surface web)是搜索引擎可以抓取的网络; 暗网(dark web)或深网(deep web)则是另一部分. 据不完全统计,互联网中其实约 90% 的网络都是深网.
- 暗网,也被称为 Darknet 或 dark Internet,完全是另一种“怪兽”。它们也建立在已有的网络基础上,但是使用 Tor 客户端,带有运行在 HTTP 之上的新协议,提供了一个信息交换的安全隧道。这类暗网页面也是可以采集的。
- 遍历整个网站的数据采集的好处:
 1. 生成网站地图(脉络)
 2. 收集数据
- 为了避免重复采集页面, 使用`set`来保存已采集的页面
- 如果递归运行的次数过多, 递归程序可能会崩溃. python的默认递归限制是1000次.
- 在开始写爬虫程序之前, 应充分分析待爬取网站的html文档的格式
- 在一个异常处理语句中包裹多行语句显然是有点危险的. 首先无法识别出究竟哪行代码出现了异常, 其次前面的语句出现异常, 将直接导致后面语句的执行
- 网络爬虫位于许多新式的网络技术领域彼此交叉的中心地带. 要实现跨站的数据分析, 只要构建出可以从互联网上的网页里解析和存储数据的爬虫就可以了
- 一个网站内部的爬虫, 只需要爬取以`/`开始的资源就可以了
- 在开始写爬虫跟随外链随意跳转之前, 该思考的问题:
 - 我要收集哪些数据?这些数据可以通过采集几个已经确定的网站(永远是最简单的做法)完成吗?或者我的爬虫需要发现那些我可能不知道的网站吗?
 - 当我的爬虫到了某个网站,它是立即顺着下一个出站链接跳到一个新网站,还是在网站上呆一会儿,深入采集网站的内容?
 - 有没有我不想采集的一类网站?我对非英文网站的内容感兴趣吗?
 - 如果我的网络爬虫引起了某个网站网管的怀疑,我如何避免法律责任?
- 在以任何正式目的运行代码之前, 确保已经在可能出现问题的地方都放置了检查语句
- 写代码之前拟个大纲或画个流程图, 是一个很好的编程习惯, 不仅可以为后期处理节省时间, 更重要的是可以防止自己在爬虫变得越来越复杂时乱了分寸
- `重定向` - 允许一个网页在不同的域名下显示, 有2种形式:
 1. 服务器端重定向, 网页在加载之前先改变了url
 2. 客户端重定向, 跳转到新url之前网页需要加载内容
- python3版本的urllib库会自动处理重定向. 不过要注意,有时候要采集的页面的 URL 可能并不是当前所在页面的url
- 爬虫的一些基本模式: 找出页面上的所有链接, 区分内外链, 跳转到新的页面


###Chapter4 使用API

- API的用处:为不同的应用提供了方便友好的接口。不同的开发者用不同的架构,甚至不同的语言编写软件都没问题——因为API设计的目的就是要成为一种通用语言,让不同的软件进行信息共享。
- API 可以通过 HTTP 协议下载文件,和 URL 访问网站获取数据的协议一样,它几乎可以实现所有在网上干的事情。API 之所以叫 API 而不是叫网站的原因,其实是首先 API 请求使用非常严谨的语法,其次 API 用 JSON 或 XML 格式表示数据,而不是HTML 格式。
- 通常api的验证方法都是用类似令牌(token)的方式调用, 每次api调用将令牌传递给服务器. token除了在url链接中传递, 还会通过请求头里的cookie将用户信息传递给服务器:

```
token = token
webRequest = urllib.request.Request("http://xxx", headers={"token": token})
```

- api一个重要的特征是反馈格式友好的数据, xml或json. 目前json比xml更受欢迎, 因为json文件比完整的xml文件小, 另一个原因是网络技术的改变.
- 使用get请求获取数据时, 用url路径描述获取的数据范围, 查询参数可以作为过滤器或附加请求使用.
- 一些api使用文件路径形式指定api版本, 数据和其他属性:

```text
http://socialmediasite.com/api/v4/json/users/1234/posts?from=08012014&to=08312014
```

- 一些api通过请求参数的形式指定数据格式和api版本:

```text
http://socialmediasite.com/users/1234/posts?format=json&from=08012014&to=08312014
```

- `response.read()` -> bytes
- python将json转换成字典, json数组转换成列表, json字符串转换成pyton字符串
- 如果你用API作为唯一的数据源,那么你最多就是复制别人数据库里的数据,不过都是些已经公布过的“黄花菜”。真正有意思的事情,是把多个数据源组合成新的形式,或者把 API 作为一种工具,从全新的视角对采集到的数据进行解释
- 虽然列表迭代速度更快, 但集合查找速度更快(确定一个对象是否在集合中).
- python的集合就是值为None的字典, 用到是hash表结构, 查询速度为O(1)
- 多种技术的融合, 多种数据的融合, 将得到更有用的信息

###Chapter5 存储数据

- 大数据存储与数据交互能力, 在新式的程序开发中已经是重中之重了.
- 存储媒体文件的2种主要方式: 只获取url链接, 或直接将源文件下载下来
- 直接引用url链接的优点:
 - 爬虫运行得更快,耗费的流量更少,因为只要链接,不需要下载文件。
 - 可以节省很多存储空间,因为只需要存储 URL 链接就可以。
 - 存储 URL 的代码更容易写,也不需要实现文件下载代码。
 - 不下载文件能够降低目标主机服务器的负载。
- 直接引用url链接的缺点:
 - 这些内嵌在网站或应用中的外站 URL 链接被称为盗链(hotlinking), 每个网站都会实施防盗链措施。
 - 因为链接文件在别人的服务器上,所以应用就要跟着别人的节奏运行了。
 - 盗链是很容易改变的。如果盗链图片放在博客上,要是被对方服务器发现,很可能被恶搞。如果 URL 链接存起来准备以后再用,可能用的时候链接已经失效了,或者是变成了完全无关的内容。
- python3的urllib.request.`urlretrieve`可以根据文件的url下载文件:

```python
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com")
bsObj = BeautifulSoup(html)
imageLocation = bsObj.find("a", {"id": "logo"}).find("img")["src"]
urlretrieve (imageLocation, "logo.jpg")
```

- csv(comma-separated values, 逗号分隔值)是存储表格数据的常用文件格式
- 网络数据采集的一个常用功能就是获取html表格并写入csv
- 除了用户定义的变量名,mysql是不区分大小写的, 习惯上mysql关键字用大写表示
- 连接与游标(connection/cursor)是数据库编程的2种模式:
 - 连接模式除了要连接数据库之外, 还要发送数据库信息, 处理回滚操作, 创建游标对象等
 - 一个连接可以创建多个游标, 一个游标跟踪一种状态信息, 比如数据库的使用状态. 游标还会包含最后一次查询执行的结果. 通过调用游标函数, 如`fetchall`获取查询结果
 - 游标与连接使用完毕之后,务必要关闭, 否则会导致连接泄漏, 会一直消耗数据库资源
- 使用`try ... finally`语句保证数据库连接与游标的关闭
- 让数据库更高效的几种方法:
 1. 给每张表都增加id字段. 通常数据库很难智能地选择主键
 2. 用智能索引, `CREATE INDEX definition ON dictionary (id, definition(16));`
 3. 选择合适的范式
- 发送Email, 通过爬虫或api获取信息, 设置条件自动发送Email! 那些订阅邮件, 肯定就是这么来的!

###Chapter6 读取文档

- 互联网的最基本特征: 作为不同类型文件的传输媒体
- 互联网不是一个html页面的集合, 它是一个信息的集合, 而html文件只是展示信息的一个框架
- 从最底层的角度看, 所有文档都是01的编码, 而任意类型的文件的唯一区别就在于,它们的01在面向用户的转换方式不同
- `utf-8`的全称: Universal Character Set - Transformation Format 8 bit
- utf-8的每个字符开头有一个标记,表示该字符用几个字节表示.一个字符最多可以是4字节, 但字节信息里还包括一部分设置信息, 因此全部32位不会都用, 最多使用21位
- utf8利用ascii的填充位让所有以"0"开头的字节表示该字符占用1个字节. 因此, 在英文字符在ascii和uft8两个编码方式下表示一样
- python默认将文本读成ascii编码格式
- utf8不能处理iso编码格式. 因此做数据采集工作时,尤其对国际网咱, 最好先看看meta标签内容, 用网站推荐的编码方式读取页面内容
- 几种读取在线文件的方法:
 1. 下载读取
 2. 从网上直接将文件读成一个字符串, 然后将其转换成一个StringIO对象, 使其具有文件的属性:

```python
dataFile = io.StringIO(data)
```

- `csv.reader`的返回对象是可迭代的, 而且由list对象构成.
- `csv.DictReader`将csv文件的每一行转换成python字典返回, 并将字段列表(标题栏)保存在dictReader.fieldnames里
- pdf的文字提取
- .docx的文字提取：
 1. 从文件读取xml, 将文档读成一个二进制对象(BytesIO), 再用zipfile解压(所有.docx文件为了节省空间都进行过压缩), 再读取解压文件, 就变成了xml

```python
from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO

wordFile = urlopen("http://pythonscraping.com/pages/AWordDocument.docx").read()
wordFile = BytesIO(wordFile)
document = ZipFile(wordFile)
xml_content = document.read("word/document.xml")
print(xml_content.decode("utf-8"))
```

##Part2 高阶数据采集

- 网站的真实故事其实都隐藏在js, 登录表单和网站反爬取措施的背后

###Chapter7 数据清洗

- 用regex移除不想要的字符, 如换行符(\n). 剔除字符的过程, 合理的先后顺序能省很多力
- 用***先以utf8格式编码,再以ascii方法解码***的方式,可以一定程度上剔除unicode字符
- 数据标准化要确保清洗后的数据在语言学或逻辑上是等价的
- python的`OrderedDict`,能解决字典无序排列的问题
- 数据标准化时,根据投入计算能力的多少,还可以再考虑大小写(python与Python),单词等价(1st与first),连字符的使用(co-ordinated与coordinated),拼写错误,语病等因素
- 对连字符的一个处理是,将其去掉或转换成其他字符,比如空格

###Chapter8 自然语言处理

####概括数据

- n-gram模型可用于词频分析, 很厉害!

####马尔可夫模型

- `马尔可夫文字生成器(markov text generator)` - 基于一种常用于分析大量随机事件的马尔可夫模型. 随机事件的特点是一个离散事件发生之后, 另一个离散事件将在前一个事件的条件下以一定概率发生
- 在马尔可夫模型描述的天气系统中,如果今天是晴天,那么明天有70%的可能是晴天,20%的可能多云,10% 的可能下雨。如果今天是下雨天,那么明天有 50% 的可能也下雨,25% 的可能是晴天,25% 的可能是多云
- 马尔可夫模型需要注意的点:
 - 任何一个节点引出的所有可能的总和必须等于 100%。无论是多么复杂的系统,必然会在下一步发生若干事件中的一个事件。
 - 只有当前节点的状态会影响下一个状态。
 - 有些节点可能比其他节点较难到达
- google的pagerank算法也是基于马尔可夫模型的, 将网站看作节点, 入站/出站链接作为节点的连线. 连接某个节点的可能性(linklihood)表示一个网站的相对关注度
- 马尔可夫文字生成器的工作原理: 对文献中的每一个单词进行有效处理, 再建立一个二维字典, 用于统计二元词组的词频. 每次以当前单词所在节点为查询表, 选择下一个节点. 随机生成一个权重, 用词频减权重, 一旦权重减为非正数, 确定该单词为下一单词. 词频高的单词使权重减小得更厉害, 因此更容易获得
- 在寻找有向图的最短路径问题中, 效果最好且最常用的方法是`广度优先搜索(breadth-first search, bfs)`

####自然语言处理

- 哪些单词使用得最频繁?哪些单词用得最少?一个单词后面跟着哪几个单词?这些单词是如何组合在一起的?
- `nltk`, 用于识别和标记英语文本中各词的词性.
- `nltk`很擅长生成一些`统计信息`,包括对一段文字的`单词数量`、`单词频率`和`单词词性`的统计
- 用nltk做统计分析一般从`Text`对象开始`

```python
from nltk import word_tokenize
from nltk import Text
tokens = word_tokenize("Here is some not very interesting text")
text = Text(tokens)
```
- `word_tokenize`函数的参数可以是任何python字符串, 其将字符串按语义分割成单词
- 文本对象可以像普通的python list那样操作, 好像它们就是一个包含文本里所有单词的list一样.
- 将文本对象放到一个`频率分布对象FreqDist`中, 可查看哪些单词是最常用的, 以及单词的频率等
- `bigrams`模块的`bigrams`函数作用于文本对象, 得到一个`bigrams(2-gram)`的生成器对象, 其也可以作为参数传入`FreqDist`, 得到频率分布对象
- 更一般的情况, 可以导入`ngrams`模块, `ngrams`函数被用来将文本对象分解成任意规模的`n-gram`序列,
- `nltk`库设计了许多不同的工具和对象来组织, 统计, 排序和度量大段文字的含义
- `nltk`默认使用`宾夕法尼亚大学`的`Penn Treebank`项目的`语料标记`部分
- `nltk`可以用它的超级大字典分析文本内容, 帮助寻找单词的含义. `nltk`的一个基本功能是识别句子中各个词的词性
- `nltk`用英语的上下文无关文法(context-free grammar)识别词性. 上下文无关文法基本上可以看成一个规则集合,用一个有序的列表确定一个词后面可以跟哪些词
- 对`nltk`进行训练, 创建一个全新的上下文无关文法规则, 比如用`Penn Treebank`词性标记手工完成语言的大部分文本的语义标记, 将结果传给`nltk`, 训练它对未标记文本的语义标记.
- 网络数据采集经常需要处理搜索的问题, 比如采集的文字的词性, 举例, ***希望采集是动词飞的fly, 而过滤掉名词苍蝇的fly***
- 自然语言中的许多歧义问题都可以用`nltk`的`pos_tag`解决, 不只是搜索目标单词或短语, 而是搜索带标记的目标单词或短语,这样可以大大提高爬虫搜索的准确率和效率

###Chapter9 穿越网页表单与登录窗口进行采集

- 利用post方法, 将信息推送到服务器进行存储与分析
- 页面表单基本上可以看成一种用户提交post请求的方式, 且这种请求方式是服务器能够理解和使用的

####Requests库

- `Requests`库是一个擅长处理复杂的http请求, cookie, header等内容的第三方库

####提交一个基本表单

- 大多数网页表单都是由一些 HTML 字段、一个提交按钮、一个在表单处理完之后跳转的“执行结果”(表单属性 action 的值)页面构成。
- 字段的名称决定了表单被确认后要被传送到服务器上的变量名称
- 表单的真实行为发生在`action`指定的页面
- HTML 表单的目的,只是帮助网站的访问者发送格式合理的请求,向服务器请求没有出现的页面
- 大多数情况下, 提交表单只需要注意:
 1. 提交数据的字段名称
 2. 表单的`action`属性, 即表单提交后网站会显示的页面

####单选按钮, 复选框和其他输入

- 无论表单的字段看起来多么复杂,仍然只有两件事是需要关注的:`字段名称`和`值`。字段名称可以通过查看源代码寻找 `name` 属性轻易获得
- `字段`的值有时会比较复杂. 如果不确定一个输入字段指定数据格式, 可**跟踪浏览器正在通过网站发出或接受的get和post请求的内容**.
- 跟踪get请求效果最好也最直接的手段是看网站的url链接, `?xxx=xxx&xxx=...`
- 复杂的`post`表单, 可查看浏览器向服务器传递的参数, 用chrome的`F12`

####提交文件和图像

- 用`requests`处理文件上传的方式与提交普通表单类似:

```python
import requests
file = {"image": open("filename", "rb")}
response = requests.post("http://...", data = file)
```

####处理登录和cookie

- 大多数新式的网站都用 `cookie` 跟踪用户是否已登录的状态信息。一旦网站验证了登录权证,它就会将它们保存在浏览器的 cookie 中,里面通常包含一个服务器生成的`令牌`、`登录有效时限`和`状态跟踪信息`。网站会把这个 cookie 当作信息验证的证据,在你浏览网站的每个页面时出示给服务器。
- `obj.cookies.method`从响应中获取`cookie`, 再通过`cookies`参数将`cookie`发送给服务器
- 使用`session`对象, 可以`持续`跟踪会话信息, 比如cookie, header, 甚至运行http协议的信息.
- 使`session`的方法就是, 创建`Session`对象, 再用`Session`对象发送请求
- 写爬虫时, 应持续关注cookie的状态, 掌握它们在可控范围内非常重要. 这样可以避免痛苦地调试和追寻网站行为异常,节省很多时间。
- 在cookie发明之前, 处理网站登录常用的方法是用`http基本接入认证(http basic access authentication)`, requests库的`auth`模块专门用来处理http认证:

```python
import requests
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth('ryan', 'password')
r = requests.post(url="http://pythonscraping.com/pages/auth/login.php", auth=auth)  # HTTPBasicAuth对象作为auth参数传递到请求
```

####其他表单问题

- 表单是网络恶意机器人(malicious bots)酷爱的网站切入点。
- 新式的网站经常在HTML 中使用很多安全措施,让表单不能被快速穿越

###Chapter10 采集 JavaScript

- JavaScript 是网络上最常用也是支持者最多的`客户端脚本语言`。它可以收集用户的跟踪数据,不需要重载页面直接提交表单,在页面嵌入多媒体文件,甚至运行网页游戏

#### JavaScript 简介

- JavaScript 是一种弱类型语言, 所有变量都用`var`关键字进行定义, 可以将函数作为变量使用
- 常用的 JavaScript 库
 1. `jQuery`:
  - 一个网站使用`jQuery`的特征是源代码里包含了`jQuery`入口.
  - jQuery 可以动态地创建 HTML 内容,只有在 JavaScript 代码执行之后才会显示。如果用传统的方法采集页面内容,就只能获得 JavaScript 代码执行之前页面上的内容
  - 这些页面还可能包含动画、用户交互内容和嵌入式媒体,这些内容对网络数据采集都是挑战。
 2. Google Analytics
  - 如果网站使用了Google Analytics,在页面底部会有类似`<!-- Google Analytics -->`的 JavaScript 代码
  - 如果一个网站使用了 Google Analytics 或其他类似的网络分析系统,而不想让网站知道在采集数据,就要确保把那些分析工具的 cookie 或者所有 cookie 都关掉。
 3. Google Map
  - 在 Google 地图上,显示一个位置最常用的方法就是用标记

```JavaScript
var marker = new google.maps.Marker({
    position: new google.maps.LatLng(-25.363882,131.044922),
    map: map,
    title: 'Some marker text'
});
```

  - 取出google.maps.LatLng()里的坐标, 生成一组经纬度坐标值, 再通过google的`地理坐标反向查询`api(https://developers.google.com/maps/documentation/javascript/examples/geocoding-reverse), 就可以将经纬度坐标组解析成格式规范的地址, 可存储或分析

####ajax和动态html

- 提交表单之后,或从服务器获取信息之后,网站的页面不需要重新刷新,那么访问的网站就在用 Ajax 技术。
- `Ajax(Asynchronous JavaScript and XML)` 其实并不是一门语言,而是用来完成网络任务的一系列技术, 网站不需要使用单独的页面请求就可以和网络服务器进行交互
- 动态 HTML(dynamic HTML,`DHTML`)也是一系列用于解决网络问题的技术集合。DHTML 是用`客户端语言`改变页面的 HTML 元素(HTML、CSS,或者二者皆被改变). 是否使用了DHTML, 关键要看有没有用 JavaScript 控制 HTML 和 CSS 元素
- 有时,***网页用一个加载页面把你引到另一个页面上,但是网页的 URL 链接在这个过程中一直没有变化。***
- 当用爬虫采集的网页内容与浏览器上显示的不同时, 是因为爬虫不能执行 JavaScript 代码, 而浏览器可以正确地执行 JavaScript .
- 用python爬取使用了`ajax`或`dhtml`的页面的2种办法:
 1. 直接从 JavaScript 代码里采集内容
 2. 用第三方库运行 JavaScript , 直接采集在浏览器中看到的页面

####Selenium

- `Selenium`是一个网络数据采集工具, 其最初是为`网站自动化测试`而开发的, 近几年,它还被广泛用于获取精确的网站快照.
- `Selenium`可以直接运行在浏览器上, 它可以让浏览器自动加载页面, 获取需要的数据, 甚至页面截屏, 或者判断网站上某些动作是否发生
- `Selenium`需要与第三方浏览器结合使用.
- `PhantomJS`可以将网站加载到内存并执行页面上的 JavaScript, 但它不会向用户展示网页的图形界面.
- 把 `Selenium` 和 `PhantomJS` 结合在一起,就可以运行一个非常强大的网络爬虫了,可以处理 `cookie`、`JavaScrip`、`header`,以及任何需要做的事情
- python的`Selenium`库是一个在`WebDriver`上调用的api, `webdriver`有点像加载网站的浏览器, 可以像`BeautifulSoup`对象一样用来查找页面元素, 与页面上的元素进行交互, 以及执行其他动作来运行爬虫
- webdriver的page_source函数返回页面的源代码字符串. 若不想要`Selenium`选择器, 则可以用返回的源代码创建`BeautifulSoup`对象.
- 页面的加载时间是不确定的, 具体依赖于服务器某一毫秒的负载情况, 以及不断变化的网速
- 解决`页面加载时间不确定`的有效方法是, 让`Selenium`不断检查某个元素是否存在, 以确定页面是否完全加载, 如果页面加载成功, 就执行后续程序.
- `WebDriverWait`与`expected_conditions`组合构成了`Selenium`的隐式等待(implicit wait).
- `隐式等待`与`显式等待`的不同之处在于,隐式等待是等 DOM 中某个状态发生后再继续运行代码(没有明确的等待时间,但是有最大等待时限,只要在时限内就可以),而显式等待明确设置了等待时间。在隐式等待中,DOM 触发的状态用expected_conditions 定义
- `Selenium`中元素被触发的期望条件有许多种, 包括
 - 弹出一个提示框
 - 一个元素被选中(比如文本框)
 - 页面的标题改变了,或者某个文字显示在页面上或者某个元素里
 - 一个元素在 DOM 中变成可见的,或者一个元素从 DOM 中消失了
- 大多数期望的条件在使用前需要指定等待的目标元素, 元素用`定位器`指定.
- `定位器`是一种抽象的查询语言,用 `By` 对象表示,可以用于不同的场合,包括创建选择器(driver.find_element(By.ID, "content"))
- 如果可以不用定位器, 就不用, 毕竟可以少导入一个模块
- `Xpath(XML Path)`是在xml文档中导航和选择元素的查询语言. `BeautifulSoup`不支持`Xpath`. 使用方法通常和css选择器一样.
- `Xpath`语法中四个重要概念:
 1. 根节点与非根节点
  - /div 选择 div 节点,只有当它是文档的根节点时
  - //div 选择文档中所有的 div 节点(包括非根节点)
 2. 通过属性选择节点
  - //@href 选择带 href 属性的所有节点
  - //a[@href='http://google.com'] 选择页面中所有指向 Google 网站的链接
 3. 通过位置选择节点
  - //a[3] 选择文档中的第三个链接
  - //table[last()] 选择文档中的最后一个表
  - //a[position() < 3] 选择文档中的前三个链接
 4. \*(星号)匹配任意字符或节点, 可以在不同条件下使用
  - //table/tr/\* 选择所有表格行 tr 标签的所有的子节点(这很适合选择 th 和 td 标签)
  - //div[@\*] 选择带任意属性的所有 div 标签
- 微软的Xpath语法页面[https://msdn.microsoft.com/en-us/enus/library/ms256471](https://msdn.microsoft.com/en-us/enus/library/ms256471)

####处理重定向

- `客户端重定向`是在服务器将页面内容发送到浏览器之**前**,由浏览器执行 JavaScript 完成的页面跳转,而不是服务器完成的跳转
- `客户端重定向`是`redirect`, 即服务器在返回的响应中告知客户端请求资源的正确url, 并设置状态码`3xx`. 客户端根据响应结果对新的url发起请求
- `服务器重定向`是`dispatch`, 指服务器在处理请求的过程中将请求先后分发(委托)给其他部件处理的过程. 服务器内部如何操作, 不能知道也不需要知道吧
- `服务器重定向`可通过python的urllib库解决
- 利用`Selenium`执行 JavaScript 代码, 解决客户端重定向问题. 关键点在于何时停止页面监控. 一种方法是: 从页面开始加载时就“监视”DOM 中的一个元素,然后重复调用这个元素直到Selenium抛出一`个StaleElementReferenceException`异常;也就是说,元素不在页面的 DOM 里了,说明这时网站已经跳转

###Chapter11 图像识别与文字处理

- 当不想让文字被爬虫采集时, 将文字做成图片放在网页上是常用的方法

####OCR(Optical Character Recognition, 光学文字识别)

- 利用`Pillow`完成图片的预处理, 让机器可以更方便地读取图片
- `Tesseract`是一个ocr库, 高精确度, 高灵活性, 可以通过训练识别出任何字体以及任何unicode字符
- `Tesseract`是一个python的命令行工具, 通过`tesseract`命令在python外运行
- `NumPy`库具有大量线性代数以及大规模科学计算的方法, 其可以用数学方法将图片表示成巨大的像素数组

####处理格式规范的文字

- 格式规范的文字的特点:
 - 使用一个标准字体(不包含手写体、草书,或者十分“花哨的”字体)
 - 虽然被复印或拍照,字体还是很清晰,没有多余的痕迹或污点
 - 排列整齐,没有歪歪斜斜的字
 - 没有超出图片范围,也没有残缺不全,或紧紧贴在图片的边缘
- 对于难于辨认的图片, 先对图片进行预处理, 可大大提高图文转换的正确率
- `Tesseract`最大的缺点是对渐变背景色的处理, 它的算法在读取文件之前自动尝试调整图片对比度
- 使用`Selenium` + `Tesseract`从网站图片中抓取文- 对于难于辨认的图片, 先对图片进行预处理, 可大大提高图文转换的正确率
- 通过给 `Tesseract` 提供大量已知的文字与图片映射集,经过训练 `Tesseract` 就可以“学会”识别同一种字体,而且可以达到极高的精确率和准确率,甚至可以忽略图片中文字的背景色和相对位置等问题。

####读取验证码与训练Tessract

- `CAPTCHA(Completely Automated Public Turing test to tell Computers and Humans Apart, 全自动区分计算机与人类的图灵测试)`, 简称验证码, 其目的是为了阻止网络访问
- 要训练`Tesseract`识别一种文字, 都需要向其提供每个字符不同形式的样本:
 1. 将大量验证码样本下载到一个目录, 样本数量由验证码的复杂程度决定.(用验证码的真实结果给每个样本文件命名)
 2. 准确地告诉tesseract一张图片中的每个字符是什么, 以及每个字符的具体位置. 这时要创建一些矩形定位文件, 一个验证码图片生成一个矩形定位文件(字符 + 包围字符的最小矩形的左下角和右上角坐标 + 图片样本的编号)(http://pp19dd.com/tesseract-ocr-chopper/ 在线转换工具)
 3. 矩形定位文件必须保存为一个`.box`的文本文件, 同样用验证码的实际结果命名
 4. 备份
 5. 用同时包含验证码图片和.box文件的目录, 创建训练文件, 即.tessdata文件

####获取验证码提交答案

- 大多数网站生成的验证码图片都具有以下属性。
 - 它们是服务器端的程序动态生成的图片。验证码图片的 src 属性可能和普通图片不太一样,但是可以和其他图片一样进行下载和处理。
 - 图片的答案存储在服务器端的数据库里。
 - 很多验证码都有时间限制,如果你太长时间没解决就会失效。虽然这对网络机器人来说不是什么问题,但是如果你想保留验证码的答案一会儿再使用,或者想通过一些方法延长验证码的有效时限,可能很难成功。
- 常用的处理方法就是,首先把验证码图片下载,清理干净,然后用 Tesseract 处理图片,最后返回符合网站要求的识别结果。

###Chapter12 避开采集陷阱

####道德规范

- 在采集那些不想被采集的网站时, 可能存在一些非常符合道德和法律规范的理由
- 大多数网络机器人一开始都只能做一些宽泛的信息和漏洞扫描

####让网络机器人看起来像人类用户

- `requests`模块除了处理网站的表单, 还是设置请求首部的利器.
- 7个被大多数浏览器用来初始化所有网络请求的请求报文首部字段:
 1. Host            : http://kissg.me
 2. Connection      : keep-alive
 3. Accept          : text/html,application/xhtml+xml,application/xml;q=0.9,image/webp
 4. User-Agent      : Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/39.0.2171.95 Safari/537.36
 5. Referrer        : https://kissg.me/
 6. Accept-Encoding : gzip,deflate,sdch
 7. Accept-Language : en-US,en
- 经典的python爬虫在使用urllib标准库时, 都会发送`Accept-Encoding=identity;User-Agent=Python-urllib/3.4`的请求头
- 虽然网站可能会对http请求首部的每个字段进行"是否具有人性"的检查, 但最重要的参数是"User-Agent"
- 在处理一些警觉性非常高的网站, 要注意经常用却很少检查的首部字段, 比如`Accept-Language`
- 请求头的不同, 可以让网站改变内容的布局, 比如`User-Agent`设置成移动设备的首部, `Accpet-Language`设置成另一种语言
- 可 以 调 用 `delete_cookie()` 、 `add_cookie()` 和 `delete_all_cookies()` 方 法 来 处 理cookie。另外,还可以保存 cookie 以备其他网络爬虫使用
- 有时候需要增加时延, 来使爬虫伪装得更像人类
- 多线程爬虫, 一个线程处理数据, 另一个加载数据(我以前想的提高爬取速度的方法大致也是这样)

####常见表单安全措施

- 在html表单中, `隐含`字段可以让字段对浏览器可见, 而对用户不可见. 随着越来越多的网站开始用 cookie 存储状态变量来管理用户状态,在找到另一个最佳用途之前,隐含字段主要用于阻止爬虫自动提交表单
- 用隐含字段阻止网络数据采集的2种方式:
 1. 使表单页面上的一个字段可以用服务器生成的随机变量表示. 解决办法就是先采集表单页面上的这个随便变量, 再与其他表单数据一并提交
 2. `蜜罐(honey pot)`, 故意设一个隐含字段, 服务器将自动忽略这些字段的真实值, 但所有填写了隐含字段的用户可能被封杀. 说白了, 就是为爬虫故意设的字段, 一般用户看不到, 也就不会填
- 如果隐含字段带有较大的随机字符串变量, 则可能网络服务器会在表单提交时检查它们. 另外还有一些检查, 用来保证当前生成的表单变量只被使用一次或是最近生成的
- `html+css`隐藏元素的方法:
 1. 通过简单css属性设置进行隐藏
 2. 隐含输入字段
 3. 设置元素的位置超出浏览器边界, 并隐藏滚动条
- `Selenium`可以获取访问页面的内容, 因此它可以区分页面上的可见与不可见元素, 通过`is_displayed()`可以判断元素在页面上是否可见. 连第3种方式隐藏的元素都能被揪出来!
- 在提交表单之前, 确认已经在表单中, 准备提交的隐含字段的值(或者让Selenium自动提交)

####问题检查表

- 首先,如果从网络服务器收到的页面是空白的,缺少信息,或其遇到他不符合预期的情况(或者不是在浏览器上看到的内容),有可能是因为网站创建页面的 JavaScript执行有问题
- 如果准备向网站提交表单或发出 POST 请求,记得检查一下页面的内容,看看想提交的每个字段是不是都已经填好,而且格式也正确。用 chrome 浏览器的网络面板(快捷键 f12 打开开发者控制台,然后点击“network”即可看到)查看发送到网站的 POST命令,确认每个参数都是正确的。
- 如果已经登录网站却不能保持登录状态,或者网站上出现了其他的“登录状态”异常,请检查 cookie。确认在加载每个页面时 cookie 都被正确调用,而且 cookie 在每次发起请求时都发送到了网站上。
- 如果在客户端遇到了 HTTP 错误,尤其是 403 禁止访问错误,这可能说明网站已经把此 IP 当作机器人了,不再接受任何请求。要么等待 IP 地址从网站黑名单里移除,要么就换个 IP 地址. 如果你确定自己并没有被封杀,那么再检查下面的内容。
 -  确认爬虫在网站上的速度不是特别快。`快速采集是一种恶习`,会对网管的服务器造成沉重的负担,还会让自己陷入违法境地,也是 IP 被网站列入黑名单的首要原因。给爬虫增加延迟,让它们在夜深人静的时候运行。切记:`匆匆忙忙写程序或收集数据都是拙劣项目管理的表现`;`应该提前做好计划,避免临阵慌乱`。
 -  还有一件必须做的事情:修改你的请求头!有些网站会封杀任何声称自己是爬虫的访问者。如果不确定请求头的值怎样才算合适,就`用浏览器的请求头`。
 -  确认没有点击或访问任何人类用户通常不能点击或接入的信息
 -  如果用了一大堆复杂的手段才接入网站,考虑联系一下网管吧,告诉他们目的。试试发邮件到 webmaster@< 域名 > 或 admin@< 域名 >,请求网管允许你使用爬虫采集数据。管理员也是人嘛!

###用爬虫测试网站

- 当研发一个技术栈较大的网络项目时,经常只对栈底(项目后期用的技术)进行一些常规测试.
- 网站通常是不同标记语言额编程语言的大杂烩. 这使网站的前端测试自动化变得困难. 比如, 为 JavaScript 部分写单元测试,但没什么用,如果 JavaScript 交互的 HTML 内容改变了,那么即使 JavaScript 可以正常地运行,也不能完成网页需要的动作

####测试简介

- 一个单元测试通常包含以下特点:
 - 每个单元测试用于测试一个组件(component). 通常一个组件的所有单元测试都集成在同一个类里
 - 每个单元测试都可以完全独立地运行, 一个单元测试需要的所有启动(setup)和卸载(teardown)都必须通过这个单元测试本身去处理. 单元测试不能对其他测试造成干扰, 而且无论按何种顺序排列, 都必须能够正常运行
 - 每个单元测试通常至少含有一个断言
 - 单元测试与生产代码是分离的. 虽然它们需要导入然后在待测试的代码中使用,但是它们一般被保留在独立的类和目录中。

####python单元测试

- python的单元测试模块`unittest`. 只要先导入模块然后继承`unittest.TestCase`类, 就可实现:
 1. 为每个单元测试的开始和结束提供`setUp`和`tearDown`函数
 2. 提供不同类型的`断言`
 3. 将所有以`test_`开头的函数当作单元测试运行, 忽略不带`test_`的函数
- `setUpClass`函数只在类的初始化阶段运行一次, `setUp`函数在每个测试启动时都运行.

##The Zen of Python
> Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than right now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!

> 优美胜于丑陋
明了胜于隐晦
简洁胜于复杂
复杂胜于混乱
扁平胜于嵌套
宽松胜于紧凑
可读性很重要
即便是特例,也不可违背这些规则
虽然现实往往不那么完美
但是不应该放过任何异常
除非你确定需要如此
如果存在多种可能,不要猜测
肯定有一种——通常也是唯一一种——最佳的解决方案
虽然这并不容易,因为你不是Python之父 1
动手比不动手要好
但不假思索就动手还不如不做
如果你的方案很难懂,那肯定不是一个好方案
如果你的方案很好懂,那肯定是一个好方案
命名空间非常有用,我们应当多加利用

##互联网简介

- 互联网是一种信息交换形式
- 当http从浏览器收到一个数据包, 数据包的内容一定被看成一个网站, 网站的结构由html构成
- 虽然html通常被看成是编程语言, 但它实际是一个标记语言, 通过标签定义文档等结构以确定各个元素
- css是配合html对网站样式进行定义的语言, 其为网站对象定义颜色, 位置, 尺寸和背景等属性

##网络数据采集的法律和道德约束

- 知识产权分3种基本类型: 商标(^TM或®), 版权(©), 专利.
- 专利用来声明内容所有权仅属于发明者
- 商标是一个单词, 词组, 符号或设计, 用来识别和区分一种商品的来源. 商标的所有权很大程度上由使用场景决定
- 只要将一件东西带到世间, 它就自动受到版权法的保护
- 版权保护只涉及创造性的作品, 不涉及统计数据或事实, 而许多爬虫采集的都是事实和统计数据. 如果数据是事实性的信息, 那么完全照搬也不违反版权法
- 如果满足下列条件, 爬虫算侵犯动产:
 1. 缺少许可. 如果网站的服务协议条款明确禁止使用爬虫
 2. 造成实际伤害.
 3. 故意而为- -
- 只有三个条件都满足, 才算侵犯动产.
- 如果网速正常, 即使一台pc也可以给许多网站造成沉重负担.
- 真的没理由去伤害别人的网站
- 可能可以在大型网站的根目录找到`robots.txt`(我真的在维基百科上找到了!)
- robots.txt 文件可以被程序轻易地解析和使用, rebots.txt 文件的语法没有标准格式。它是一种业内惯用的做法. rebots.txt 文件并不是一个强制性约束.
- robots.txt第一行非注释内容是 User-agent: ,注明具体哪些机器人需要遵守规则。后面是一组规则 Allow: 或 Disallow: ,决定是否允许机器人访问网站的该部分内容. 如果一条规则后面跟着一个与之矛盾的规则,则按后一条规则执行.
- google爬虫采集网站时, 会为网站留一个副本, 然后放在互联网上, 任何人可接入这些缓存. http://webcache.googleusercontent.com/search?q=cache:YourURL
