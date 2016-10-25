# Note on Swagger

> The World's Most Popular Framework for APIs.
Swagger™ is a project used to describe and document RESTful APIs. `描述 API`
The goal of Swagger™ is to define a standard, language-agnostic interface to REST APIs which allows both humans and computers to discover and understand the capabilities of the service without access to source code, documentation, or through network traffic inspection.
Swagger is a set of rules (in other words, a specification) for a format describing REST APIs. The format is both machine-readable and human-readable. As a result, it can be used to share documentation among product managers, testers and developers, but can also be used by various tools to automate API-related processes.

## Get Started

如何用 Swagger 描述 API

- `自顶向下` - 用 [Swagger Editor](http://editor.swagger.io) 创建 Swagger 定义, 再用集成的 [Swagger Codegen](http://swagger.io/swagger-codegen/) 工具生成服务器端的实现.
- `自底向上` - 已有用于创建 Swagger 定义的 `REST API`. 手动创建定义或使用框架自动地创建定义.

利用 Swagger 定义进行 API 整合, 可用 [Swagger UI](http://petstore.swagger.io/) 的在线版探索 API, 再用 Swagger Codegen 生成客户端库

例子:

```yaml
swagger: "2.0"
info:
  version: "1.0"
  title: "Hello World API"
paths:
  /hello/{user}:
    get:
      description: Returns a greeting to the user!
      parameters:
        - name: user
          in: path
          type: string
          required: true
          description: The name of the user to greet.
      responses:
        200:
          description: Returns the greeting.
          schema:
            type: string
        400:
          description: Invalid characters in "user" were provided.
```

## Open API Specification

> The Swagger specification defines a set of files required to describe such an API. These files can then be used by the Swagger-UI project to display the API and Swagger-Codegen to generate clients in various languages.

### Definitions

##### Path Templating

Path templating 是指用花括号 ({}) 去标记一个 URL 路径的部分, 该部分是可替代的参数

##### Mime Types

Mime type 定义需要符合 [RFC 6838](https://tools.ietf.org/html/rfc6838) 规范. 如下:

```text
  text/plain; charset=utf-8
  application/json
  application/vnd.github+json
  application/vnd.github.v3+json
  application/vnd.github.v3.raw+json
  application/vnd.github.v3.text+json
  application/vnd.github.v3.html+json
  application/vnd.github.v3.full+json
  application/vnd.github.v3.diff
  application/vnd.github.v3.patch
```

##### HTTP Status Codes

HTTP Status Codes 用于指示操作的状态. 可用的代码在 [RFC 7231](https://tools.ietf.org/html/rfc7231#section-6) 和 [IANA Status Code Registry](http://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml) 有描述

### Specification

### Format

依据 Swagger 规范描述 RESTful API 的文件, 用 JSON 对象表示, 符合 JSON 标准. 也可用 YAML.

所有字段名都是大小写敏感的

有两种类型的字段: 固定字段和模式字段. 模式字段可用出现多次.

### File Structure

Swagger  File Structure

Swagger 用一个单一的文件表示 API. (用户可也按需将定义的各部分分成多个文件保存.) This is applicable for $ref fields in the specification as follows from the [JSON Schema](http://json-schema.org/) definitions.

方便起见, Swagger 规范文件以 `swagger.json` 命名

### Data Types

Swagger 规范中的原始数据类型 (Primitive Data types) 是基于 [JSON-Schema Draft 4](http://json-schema.org/latest/json-schema-core.html#anchor8) 的. 使用 [Schema Object](http://swagger.io/specification/#schemaObject) 描述的模块是 JSON Schema Draft 4 的自己

补充原始数据类型 `file` 被 [Parameter Object](http://swagger.io/specification/#parameterObject) 和 [Response Object](http://swagger.io/specification/#responseObject) 用于设置 parameter type 或 response 为文件

### Schema

#### swagger object

`swagger object` 对象是 API 规范的根文档对象.

##### Fixed Fields

##### Patterned Objects


| Field Pattern	| Type	| Description |
| :----------:  | :---: | :---------: |
| ^x-	        | Any	| Allows extensions to the Swagger Schema. The field name MUST begin with x-, for example, x-internal-id. The value can be null, a primitive, an array or an object. See [Vendor Extensions](http://swagger.io/specification/#vendorExtensions) for further details. |

#### info object

该对象提供了关于 API 的元数据. 元数据可被客户端使用, 并可用 `Swagger-UI` 展示.

#### contact object

暴露 API 的 contact info

#### license object

暴露 API 的 license info

#### paths object

为独立的终端维护相对路径, 将补充到 [basePath](http://swagger.io/specification/#swaggerBasePath) 之后构造完整的路径. 可以为空

#### path item object

描述了对单个路径的可行操作, 可为空. 路径本身会暴露给文档阅读者, 但是他们无法得知哪些操作和参数是可用的

#### operation object

描述了路径上的一个单一的 API 操作

#### external documentation object

允许引用外部文档

#### parameter object

描述了一个单一的操作参数. 一个唯一的参数由 name 和 location 两部分组成.

5 种可能的参数类型:

- path - 参数值实际是操作 URL 的部分. 不包括主机或 base path. `/items/{itemId}`, path parameter 是 `itemId`
- query - `items?id=###`, query parameter 是 `id`
- header - Custom headers that are expected as part of the request.
- body - HTTP 请求的有效负载 (payload). 因为 Form 参数也可是 payload, body 和 form 参数不能同时存在.
- form - 描述 HTTP 请求的 payload, 当 `application/x-www-form-urlencoded` 或 `multipart/form-data` 或两者同时用作 content type. 唯一的可用于发送文件的参数类型
    - application/x-www-form-urlencoded - 类似于 query 参数的格式, 但是是一个 payload. `foo=1&bar=swagger`, `foo` 和 `bar` 都是 form 参数. 通常用于简单参数的转换
    - multipart/form-data - 每个参数都是 payload 的一部分, 带 internal header. 更多的用于文件的转换

#### items object

JSON-Schema's items 对象的限制子集. 

items 必须是字符串类型, 最短长度是 2

#### responses object

操作的期望响应, 是容器. 将 HTTP response 代码映射到期望的响应.

可以为所有的 HTTP 代码设置默认的响应对象. 不会被覆盖?

响应对象必须包含至少一个响应代码, 并应该是一个成功的操作调用响应

```yaml
'200':
  description: a pet to be returned
  schema:
    $ref: '#/definitions/Pet'
default:
  description: Unexpected error
  schema:
    $ref: '#/definitions/ErrorModel'
```

- 如上, 200 是成功操作的响应, default 是其他所有操作的响应

#### response object

描述了一个 API 操作的单一响应

#### headers object

列举可用作为响应的一部分发送的头部

#### example object

为操作响应设置例子

#### header object

#### tag objects

不是每个 tag 都必须有一个 tag 对象.

允许为 [Operation Object](http://swagger.io/specification/#operationObject) 使用的单个 tag 添加元数据

#### reference object

允许引用规范中其他定义的简单对象.

Reference object 是一个 [JSON Reference](https://tools.ietf.org/html/draft-pbryan-zyp-json-ref-02), 使用 [JSON Pointer](https://tools.ietf.org/html/rfc6901) 作为值. 仅支持 [canonical dereferencing](http://json-schema.org/latest/json-schema-core.html#anchor27)

#### schema object

schema 对象允许对输入输出数据的类型进行定义, 可以是原生数据类型或数组, 也可以是对象. schema 对象是基于 [JSON SchemaSpecification Draft 4](http://json-schema.org/) 的, 使用其预定义的子集. 在该子集的顶部, 有该规范提供的拓展, 为写一个更完整的文档提供了可能

## Tools

- [Swagger Core](http://swagger.io/swagger-core/) - For generating and reading Swagger definitions
- [Swagger Codegen](http://swagger.io/swagger-codegen/) - Command-line tool for generating both client and server side code from a Swagger definition
- [Swagger UI](http://swagger.io/swagger-ui/) - Browser based UI for exploring a Swagger defined API
- [Swagger Editor](http://swagger.io/swagger-editor/) - Browser based editor for authoring Swagger definitions in YAML or JSON format
- Swagger JS
- Swagger Node
- Swagger-Socket
- Swagger Parser

### Swagger Core

A set of Java libs.

### Swagger Codegen

### Swagger UI

Swagger UI is a dependency-free collection of HTML, Javascript, and CSS assets that dynamically generate beautiful documentation and sandbox from a Swagger-compliant API.

## 通过Swagger进行API设计，与Tony Tam的一次对话

- 为 REST API 创建一个泛型的 JSON 模型, 能够反映出调用者有权限进行哪些操作
- 代码生成器的输入模型
- Swagger 的核心思想: `为 API 定义一个一致的, 可预测的模型`
- 如果没有一种简单而健壮的校验机制, 那么很容易就会写出无效的规范
- 基于规范的核心目标作出决策, 而不是尝试同时解决所有人的问题, 后者只会使项目变成一个大泥巴球. "如果将所有美丽的颜色混合在一起, 只会得到一个肮脏的颜色". 因此, 对于功能, 必须以一种干净的, 清晰的方式进行设计.
- 以简便的方式展示 API, 可试用
