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
 - 侧向导航
  1. `.next_sibling`或`.previous_sibling`获得后一个或前一个兄弟. 若不存在, 将得到None. 兄弟必须是同一个父亲. (在html文档中, 标签可能是以换行符分隔开的, 换行符实际被认为是一个字符串, 因此其兄弟是"\n")
  2. `.next_siblings`或`.previous_siblings`获得兄弟的迭代器
 - 前后导航
  1. `.next_element`与`.previous_element`指向下一个或前一个被解析的对象, 可能是兄弟, 可能是父子
  2. `.next_elements`与`.previous_elements`获得往后或往前的对象生成器
- 搜索树, 最长用的方法:`find()`与`findAll()`
 - 可以传入`find`或`findAll`作为过滤器的可以是:
  1. 字符串
  2. regex
  3. list
  4. `True` - 将匹配它能匹配的一切
  5. 函数 - 必须以一个文档元素作为唯一参数, 并返回布尔值
 - `findAll(name, attrs, recursive, string, limit, **kw)` - 浏览一个标签的所有后代, 并获取匹配过滤器的所有后代
  1. `name` - 标签名, 可以是字符串, regex, list, 函数, `True`
  2. `**kw` - 除了`name`, `attrs`等位置参数, 其他使用关键字参数传入的参数都将被视作标签的属性. 参数值可以是str, regex, list, func, True
  3. `class`是python关键字, 当要以css的class作为检索时, 要使用`class_`, 其值可以是str, regex, func, True
  4. 对于具有多个值的属性, 匹配任意一个即可匹配到它;
  5. `string` - 用于检索字符串, 可与其他参数联合使用找到需要的标签. 将在所有标签的`.string`查询参数指定的`string`
  6. `limit` - `findAll`默认返回所有标签或字符串, 可用`limit`参数限制返回结果的数量, 将在匹配到相应数量的结果之后停止搜索
  7. `recursive` - 默认搜索所有后代, 即`recursive`的默认值是`True`, 可设为False, 从而只对标签的直接后代进行搜索
  8. 可以通过字典的方式指定标签的属性
 - `find(name, attrs, recursive, string, **kw)`
  1. 无论如何, `findAll`都将遍历整个文档, 但当文档中只存在一个特定的标签, 遍历将浪费很多时间
  2. `find`与`findAll(limit=1)`类似, 但前者直接返回搜索结果, 后者返回list, 虽然这个list只有一个值
  3. `findAll`匹配不到时, 返回`空list`, `find`则返回None
 - `find_parents`与`find_parent`
  1. `find`与`findAll`都是向下搜索的, 而`find_parent`与`find_parents`则是向上搜索
 - `find_next_siblings`与`find_next_sibling`使用`.next_siblings`迭代剩余的兄弟节点
 - `find_previous_siblings`与`find_previous_sibling`使用`.previous_siblings`迭代之前的兄弟节点
 - `find_all_next()`与`find_next()`使用`.next_elements`进行迭代
 - `find_all_previous()`与`find_previous()`使用`.previous_elements`进行迭代
- CSS 选择器
 - 使用标签对象或`BeautifulSoup`对象的的`.select()`方法, 达到css选择器的效果(好吧, 我基本不会)
- 更新树
 - 可通过`tag.name`或`tag["xxx"]`的方式轻松地修改标签名与属性
 - 通过`tag.string`可修改标签的内容, 但如果标签包含其他标签, 这些内容全都会被替换掉
 - `tag.append()` - 追加内容, 可以是str, NaviagleString, Comment, 或`new_tag`对象
 - `tag.insert()` - 与append类似, 除了插入位置可自定义
 - `insert_before`与`insert_after` - 在当前标签之前或之后插入str或标签
 - `clear` - 清除标签的内容
 - `.extract`将指定标签或str从树中解压出来, 返回并删除, 有点像pop
 - `.decompose`从树中删除标签或str, 完全地毁尸灭迹
 - `replace_with`用新的tag或str替换树中原来的tag或str
 - `.wrap`将元素打包进指定的标签
 - `.unwrap`将指定元素从速从标签中移除
