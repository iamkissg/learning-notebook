# YAML 简单笔记

(内容摘自[阮一峰的 YAML 语言教程](http://www.ruanyifeng.com/blog/2016/07/yaml.html))

基本语法规则:

- 大小写敏感
- 使用缩进表示层级关系
- 缩进时不允许使用 Tab 键，只允许使用空格。
- 缩进的空格数目不重要，只要相同层级的元素左侧对齐即可
- `#` 注释

YAML 支持的数据结构:

1. `对象`: 键值对的集合，又称为映射（mapping）/ 哈希（hashes） / 字典（dictionary）
2. `数组`: 一组按次序排列的值，又称为序列（sequence） / 列表（list）
3. `纯量` (scalars): 单个的、不可再分的值

## 对象

对象的一组键值对，使用冒号结构表示: `animal: pets`

Yaml 也允许另一种写法，将所有键值对写成一个行内对象: `hash: { name: Steve, foo: bar }`

## 数组

一组连字符开头的行，构成一个数组。

```yaml
- Cat
- Dog
- Goldfish
```

行内表示的数组: `animal: [Cat, Dog]`

## 复合结构

对象和数组可以结合使用，形成复合结构。

```python
languages:
 - Ruby
 - Perl
 - Python 
websites:
 YAML: yaml.org 
 Ruby: ruby-lang.org 
 Python: python.org 
 Perl: use.perl.org 
```

## 纯量

纯量是最基本的、不可再分的值. JavaScript 的纯量:

- 字符串
- 布尔值
- 整数
- 浮点数
- Null
- 时间
- 日期

数值直接以字面量的形式表示。

布尔值用 `true` 和 `false` 表示。

null 用 `~` 表示。

时间采用 ISO8601 格式: `iso8601: 2001-12-14t21:59:43.10-05:00 `

日期采用复合 iso8601 格式的年、月、日表示。

YAML 允许使用两个感叹号，强制转换数据类型: `e: !!str 123`

## 字符串

字符串默认不使用引号表示。

如果字符串之中包含空格或特殊字符，需要放在引号之中。

单引号和双引号都可以使用，双引号不会对特殊字符转义

单引号之中如果还有单引号，必须连续使用`两个单引号转义`。

字符串可以写成多行，从第二行开始，必须有一个单空格缩进。`换行符会被转为空格`

多行字符串可以使用 `|` 保留换行符，也可以使用 `>` 折叠换行。

```yaml
this: |
  Foo
  Bar
that: >
  Foo
  Bar
```

```json
{ this: 'Foo\nBar\n', that: 'Foo Bar\n' }
```

`+` 表示保留文字块末尾的换行，`-` 表示删除字符串末尾的换行。

```yaml
s1: |
  Foo

s2: |+
  Foo


s3: |-
  Foo
```

```json
{ s1: 'Foo\n', s2: 'Foo\n\n\n', s3: 'Foo' }{ s1: 'Foo\n', s2: 'Foo\n\n\n', s3: 'Foo' }
```

字符串之中可以插入 HTML 标记:

```
message: |

  <p style="color: red">
    段落
  </p>
```

## 引用

锚点`&` 和别名 `*` ，可以用来引用。

```yaml
defaults: &defaults
  adapter:  postgres
  host:     localhost

development:
  database: myapp_development
  <<: *defaults

test:
  database: myapp_test
  <<: *defaults
```

`<<` 表示合并到当前数据

## func & regex

[JS-YAML](https://github.com/nodeca/js-yaml) 库, 提供了将 func 和 regex 转为字符串的功能. (好吧, 我不会)
