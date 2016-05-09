#BeautifulSoup Documentaion Notes

- BeautifulSoup是一个用于将数据从html或xml文档中解析出来的python库
- BeautifulSoup通过html解析器来解析html文档, 它同时支持python标准库中的html解析器和第三方的解析器. 在创建BeautifulSoup对象时, 第二个位置参数指定使用的解析器.
- html解析器对比:
 1. python's html.parser - "html.parser" - 内建, 速度一般, 文档容错能力强
 2. lxml html parser     - "lxml"        - 速度快, 文档容错能力强
 3. lxml xml parser      - "lxml-xml"|"xml" - 快, 唯一支持xml的解析器
 4. html5lib             - "html5lib"    - 最好的容错性, 以浏览器方式解析文档, 生成html5格式的文档
- 若不指定解析器, 一般默认使用`lxml`, 且会提示
- 创建一个soup对象, 可传入一个字符串, 或打开文件句柄(`soup = BeautifulSoup(open("index.html"))`). 首先, 文档将被转换为Unicode类型, html实体将被转换为unicode字符. 然后使用恰当的解析器解析文档(默认使用html解析器)
- BeautifulSoup将复杂的html文档转换成复杂的python对象数. 但用户只需要处理4类对象就可以了: `Tag`, `NavigableString`, `BeautifulSoup`, `Comment`
- `Tag`对象对应xml文档或html文档的标签元素. 一个标签最重要的特征是`名称`与`属性`.
- 每个标签都有一个名称, 可通过`.name`的方式取得. 若修改了标签名, BeautifulSoup生成的html标记也将发生改变:

```python
tag.name = "blockquote"
tag
# <blockquote class="boldest">Extremely bold</blockquote>
```

- 标签可拥有数个属性, 通过类似字典的方式获取属性`tag["id"]`. 也可用`tag.attrs`直接获得属性的字典. 可以添加, 删除, 修改属性:

```python
tag['class'] = 'verybold'
tag['id'] = 1
tag
# <blockquote class="verybold" id="1">Extremely bold</blockquote>

del tag['class']
del tag['id']
tag
# <blockquote>Extremely bold</blockquote>

tag['class']
# KeyError: 'class'
print(tag.get('class'))
# None
```

- 多值属性的值以`list`形式保存; 单值属性以`str`形式保存; 以`xml`解析文档, 不会有多值属性:

```python
xml_soup = BeautifulSoup('<p class="body strikeout"></p>', 'xml')
xml_soup.p['class']
# u'body strikeout'
```

- BeautifulSoup用`NavigableString`类来包装tag中的字符串:

```
tag.string
# u'Extremely bold'
type(tag.string)
# <class 'bs4.element.NavigableString'>
```

- 一个 NavigableString 字符串与Python中的字符串相同, 可将其装为python的字符串
- tag中包含的字符串不能编辑, 但可以用`replace_with`方法替换:

```python
tag.string.replace_with("No longer bold")
```

- 如果想在Beautiful Soup之外使用 NavigableString 对象,需要将该对象转换成普通的字符串,否则就算Beautiful Soup方法已经执行结束,该对象的输出也会带有对象的引用地址.这样会浪费内存
- `BeautifulSoup`对象本身表示一个完整的文档, 也可将其视作一个标签对象. 但由于`BeatifulSoup`实际并不与html或xml标签对应, 因此其并没有名称或属性, 但其被赋予了一个名称`[document]`, 可通过`.name`取得
- `Comment`对象是`NavigableString`的一个特殊类型.
- 导航树的方法:
 - 向下导航
  1. 通过标签名导航 - 只会匹配第一个标签
  2. 通过`.contents`获得孩子(包括标签和字符串)的list - 所有的html文档标签都是`BeautifulSoup`对象的子标签. 字符串没有`.contents`属性.
  3. 通过`.children`获得孩子的生成器
  4. 通过`.descendants`获得全部后代的生成器. `BeautifulSoup`对象只有一个直接后代, 即<html>标签, 但它拥有所有的后代
  5. 如果一个标签只有一个孩子, 且是一个`NavigableString`, 那么可通过`.string`获得该孩子
  6. 如果一个标签只有一个子标签,且该子标签有`.string`属性, 则父标签将拥有与子标签一样的`.string`属性
  7. 一个标签内部有多个孩子, 可通过`.strings`获得字符串生成器, 或者`.stripped_strings`获得不包含空白字符的字符串生成器
 - 向上导航
  1. `.parent`获得元素的父亲. 顶级标签<html>的父亲是`BeautifulSoup`对象, `BeautifulSoup`的父亲是None
  2. `.parents`获得祖辈生成器
  3. 
 - 侧向导航
  1. `.next_sibling`或`.previous_sibling`获得后一个或前一个兄弟. 若不存在, 将得到None. 兄弟必须是同一个父亲. (在html文档中, 标签可能是以换行符分隔开的, 换行符实际被认为是一个字符串, 因此其兄弟是"\n")
  2. `.next_siblings`或`.previous_siblings`获得兄弟的迭代器
 - 前后导航
  1. 


