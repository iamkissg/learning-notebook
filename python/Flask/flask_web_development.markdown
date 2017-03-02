# Flask Web 开发

## Chapter 1 & Chapter 2

- Python, 修饰器是 Python 语言的标准特性，可以使用不同的方式修改函数的行为。惯常用法是使用修饰器`把函数注册为事件的处理程序`。
- Flask，`@app.route(/user/<int:id>)` 尖括号中为 URL 的动态部分，此处，`int` 表示只匹配路由中使用 int 的动态部分。还有 `float`，`path`，其中 `path` 也是字符串，但不把斜杆视作分隔符，而当作动态片段的一部分
- Flask，Web 服务器启动后，会进入轮询，等待并处理请求（我以为是类似中断的方式呢）
- Flask，使用 *context* 让特定的变量在一个线程中全局可访问，而不干扰其他线程。（比如`request`)
- 多线程 Web 服务器会创建一个线程池，再从线程池中选择一个线程用于处理接收到的请求。

![Flask Context Global Variables](flask_context_global_variables.png)

- Flask 在分发请求之前激活（或推送）程序和请求上下文，请求处理完成后再将其删除。
- ，Flask 会在程序的 URL 映射中查找请求的 URL。`URL 映射`是 URL 和视图函数之间的对应关系。Flask 使用 `app.route` 修饰器或者非修饰器形式的 `app.add_url_rule()` 生成映射。

```python
app.url_map  # 查看 Flask 程序的 URL 映射
```

- 请求钩子 - 请求钩子函数和视图函数之间共享数据一般使用上下文全局变量 g
    - `before_first_request`：注册一个函数，在处理第一个请求之前运行。
    - `before_request`：注册一个函数，在每次请求之前运行。
    - `after_request`：注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。
    - `teardown_request`：注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。
- `重定向` 的特殊响应类型，没有页面文档，仅告诉浏览器一个新地址用以加载新页面。`return redirect("http://kissg.me")` 或 `return make_response("", 302, {"Location": "http://kissg.me"})`
- `abort` - 生成特殊的响应，用于处理错误。不会把控制权交还给调用它的函数，而是抛出异常把控制权交给 Web 服务器。

## Chapter 3

- Flask 提供的 `render_template` 函数把 Jinja2 模板引擎集成到了程序中。 `render_template` 函数的第一个参数是模板的文件名。随后的参数都是`键值对`,表示模板中变量对应的`真实值`。
- 访问数据库添加用户，生成响应并返回给浏览器。这两个过程分别称为`业务逻辑`和`表现逻辑`。
- 默认情况下，Flask 在程序文件夹中的 `templates` 子文件夹中寻找模板。
- Jinja2 使用 `{{ xx }}` 作为占位符，告诉模板引擎这个位置的值从渲染模板时使用的数据中获取
- Jinja2 能识别所有类型的变量,甚至是一些复杂的类型,例如列表、字典和对象
- 模板可以使用`过滤器`修改变量，格式如 `{{ name | capitalize }}`
- `safe` 过滤器，在渲染时不转亦。默认情况下,出于安全考虑,Jinja2 会转义所有变量。
- 除了 `if` 和 `for`，Jinja2 还支持`宏(macro)`，宏类似于 Python 代码中的函数。为了重复使用宏,可以将其保存在单独的文件中,然后在需要使用的模板中导入
- 需要在多处重复使用的模板代码片段可以写入单独的文件,再包含在所有模板中,以避免重复。另一种复用代码的方式是`模板继承`
- Bootstrap 是客户端框架,因此不会直接涉及服务器。服务器需要做的只是提供引用了 Bootstrap 层叠样 式表(CSS) 和 JavaScript 文件 的 HTML 响应, 并在 HTML、CSS 和JavaScript 代码中实例化所需组件
- 最常见的错误代码有两个:404,`客户端请求未知页面或路由`时显示;500,`有未处理的异常`时显示。
- 返回的渲染后的模板，是 `response` 的 body
- 错误处理函数也返回响应，并返回与错误对应的数字状态码
- 生成连接程序内不同路由的链接时,使用相对地址就足够了。如果要生成在浏览器之外使用的链接,则必须使用绝对地址。
- `url_for()` - 生成动态地址时, 将动态部分作为关键字参数传入；任何额外参数添加到查询字符串
- 日期本地化 - 在服务器上只使用 UTC 时间，把时间单位发送给 Web 浏览器,转换成当地时间,然后渲染

```html
{% macro render_comment(comment) %}
<li>{{ comment }}</li>
{% endmacro %}
<ul>
{% for comment in comments %}
{{ render_comment(comment) }}
{% endfor % }
</ul>
```
## Chapter 4

- `request.form` 能获取 POST 提交的表达
- 跨站请求伪造(CSRF), 恶意网站把请求发送到被攻击者已登录的其他网站时就会引发 CSRF 攻击
- `SECRET_KEY` 配置变量是通用密钥,可在 Flask 和多个第三方扩展中使用
- 使用 Flask-WTF 时,`每个 Web 表单都由一个继承自 Form 的类表示`。这个类定义表单中的一组字段,`每个字段都用对象表示`。字段对象可附属一个或多个验证函数。验证函数用来验证用户提交的输入值是否符合要求。

![Flask-WTF](flask-wtf-support.png)

- 刷新页面时浏览器会重新发送之前已经发送过的最后一个请求, 如果这个请求是一个包含表单数据的 POST 请求,刷新页面后会再次提交表单. 基于这个原因,最好别让 Web 程序把 POST 请求作为浏览器发送的最后一个请求
    - 解决方法: 将 `重定向` 作为 POST 请求的响应, 而不用常规响应. 重定向是一种特殊的响应,响应内容是 URL,而不是包含 HTML 代码的字符串。浏览器收到这种响应时,会向重定向的 URL 发起 GET 请求,显示页面的内容。由于最后一个请求是 GET 请求, 刷新命令能正常使 (`POST / Redict / GET`)
- 上述方法会带来另一个问题: 程序处理 POST 请求时,使用 form.name.data 获取用户输入的名字,可是一旦这个请求结束,数据也就丢失了。因为这个 POST 请求使用重定向处理,所以程序需要保存输入的名字,这样重定向后的请求才能获得并使用这个名字,从而构成真正的响应
- 程序可以把数据存储在用户`会话`中,在请求之间`记住`数据。用户会话是一种`私有存储`,存在于每个连接到服务器的客户端中
- 默认情况下,用户会话保存在客户端 cookie 中,使用设置的 `SECRET_KEY` 进行加密签名
- 请求完成后,有时需要让用户知道状态发生了变化, 可以用确认消息. 警告或错误提醒.
- `flask.flash()` 在发给客户端的下一个响应中显示一个消息
- 仅调用 flash() 函数不能把消息显示出来, 需要使用模板来渲染这些消息. Flask 将 `get_flashed_messages()` 函数开放给了模板, 用来获取并渲染消息

## Chapter 5

- 关系性数据库, 使用结构化查询语言
- 选择数据库框架时, 要考虑的:
    - 易用性
    - 性能
    - 可移植性
    - 框架集成度
- Flask-SQLAlchemy, 使用 URL 指定数据库
- 程序使用的数据库 URL 必须保存到 Flask 配置对象的 SQLALCHEMY_DATABASE_URI 键中

![SQLAlchemy Support](SQLAlchemy support.png)

- `relationship` 代表了关系的面向对象视角. 第一个参数表明关系的另一端是哪个 Model, 若 Model 未定义, 使用字符串指定; `backref` 参数为另一端 Model 添加一个属性, 从而定义反向关系.
- 大多数情况下, db.relationship() 都能自行找到关系中的外键,但有时却无法决定把哪一列作为外键

## Chapter 14

- `Flask-RESTful` 提供了 `Resource` 基类，它定义了对于给定的一个 URL 的一个或多个 HTTP 方法的路由
- `add_resource` 函数通过使用一个给定的 `endpoint` 将路由注册到框架上。最好显式地给出 `endpoint`
- `flask_restful.reqparse.RequestParser` 使用类似 `ArgParse`，它默认搜索 `request.values` 域，因此字段位置有时候需要设置，如字段来自 `request.json`，则添加参数 `location=json`
- `Flask-RESTful` 会自动将数据转成 JSON
- `Flask-RESTful` 的 `Resource` 类继承自 Flask 的 `MethodView` 类，可以通过定义 `decorators` 类变量添加装饰器
- `Flask-RESTful` ＋`Blueprints`:

from flask_restful import Api, Resource, url_for

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

class TodoItem(Resource):
    def get(self, id):
        return {'task': 'Say "Hello, World!"'}

api.add_resource(TodoItem, '/todos/<int:id>')
app.register_blueprint(api_bp)
```

- REST 的 6 个特征
    - C-S - 客户端与服务器之间必须有明确的界限
    - 无状态 - 客户端发出的请求中必须包含所有必要的信息。服务器不能在两次请求之间保存客户端的任何状态
    - 缓存 - 服务器发出的响应可以标记为可缓存或不可缓存，这样出于优化目的，客户端（或客户端和服务器之间的中间服务）可以使用缓存。
    - 接口统一 - 客户端访问服务器资源时使用的协议必须一致，定义良好，且已经标准化。（REST　Web　服务最常用的统一接口是　
    - 系统分层 - 在客户端和服务器之间可以按需插入代理服务器、缓存或网关，以提高性能、稳定性和
伸缩性
    - 按需代码 - 客户端可以选择从服务器上下载代码，在客户端的环境中执行。
- `资源`是 REST 架构的核心概念。URL 的内容无关紧要，只要资源 URL 只表示唯一的资源即可。表示资源集合的 URL 习惯是在末尾加一个 `/`，表示目录
- Flask 会特殊对待末端带有斜线的路由。如果客户端请求的 URL 的末端没有斜线，而唯一匹配的路由末端有斜线，Flask 会自动响应一个重定向，转向末端带斜线的 URL。反之则不会重定向
- REST 架构不要求必须为一个资源实现所有的请求方法。如果资源不支持客户端使用的请求方法，响应的状态码为 405，返回“不允许使用的方法”。Flask 会自动处理这种错误。
- 在设计良好的 REST API 中,客户端只需知道几个顶级资源的 URL,其他资源的 URL 则从响应中包含的链接上发掘
- 客户端程序和服务器上的程序是独立开发的，有时甚至由不同的人进行开发。因此，Web 服务的容错能力要比一般的 Web 程序强,而且还要保证旧版客户端能继续使用。通常的解决办法是`使用版本区分 Web 服务所处理的 URL`
- `request.json` - 获得请求中包含的 JSON 数据；`jsonify()` 将 Python 字典转为包含 JSON 的响应
- REST API 相关的路由是一个自成一体的程序子集，为了更好地组织代码，最好将路由放到独立的 Blueprint 中。
    - Flask 用 蓝图（blueprints） 的概念来在一个应用中或跨应用制作应用组件和支持通用的模式
    - 一个 Blueprint 对象与 Flask 应用对象的工作方式很像，但它确实不是一个应用，而是一个描述如何构建或扩展应用的 蓝图 。Flask uses a concept of blueprints for making application components and supporting common patterns within an application or across applications.
- 为所有客户端生成适当响应的一种方法是，在错误处理程序中根据客户端请求的格式改写响应，这种技术称为`内容协商`。
- Web 服务中使用 cookie 有点不现实,因为 Web 浏览器之外的客户端很难提供对 cookie 的支持

