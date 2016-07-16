#Text Processing Services

##6.2 re

###6.2.1 Syntax

- regex使用反斜杆(`\`)指示特殊形式或转义
- 使用python的`raw string`, 从而避免繁琐的转义. `r"\n"`是两个字符的字符串, `"\n"`是一个换行符的字符串. 通常使用`raw string`
- regex可以`级联`生成新regex, 即A, B都是regex, 那么AB也是一个regex. 换言之, p匹配A, q匹配B, pq将匹配AB. 当A或B中包含低优先级的操作时, `regex级联`将失败, 包括A与B之间存在边界条件, 或编号好的组
- regex特殊字符:
 - `.` - 默认匹配除换行符以外的所有字符(即匹配任意字符, 直到信号). 使用`DOTALL`标志, 连换行符都能匹配
 - `^` - 匹配字符串的头.
 - `$` - 匹配字符串的尾
 - `*` - 重复前面的 regex 0次或任意多次
 - `+` - 重复前面的 regex 至少1次
 - `?` - 匹配前面的 regex 0次或1次
 - `*?`, `+?`, `??` - lazy匹配模式, 即尽量少的匹配到
 - `{m}` - 精确地重复m次
 - `{m, n}` - 重复m-n次(含m, n). 省略m, 则最少匹配0次, 省略n, 则最多匹配无穷次
 - `{m, n}?` - lazy模式, `a{3, 5}`优先匹配5个a, `a{3, 5}`优先匹配3个a
 - `\` - 转义, 虽然使用python的`raw string`避免了python的特殊字符, 但regex使用的特殊字符(如`*`), 还需要转义
 - `[]` - 定义一个字符集. 特殊字符(如`+`)在其中将被当作普通字符(看来它的优先级还是高啊). `]`仍需转义, 否则就提早结束啦. 字符集以`^`开头, 相当于创建了一个非集, 即匹配任何不在该字符集中的字符
 - `|` - 或, 匹配左边的regex或右边的, 当A被匹配到了, B会被短路.
 - `(...)` - 匹配括号中的regex, 每个被匹配到的字符串都被编排成一个组, 匹配结束后可获得组的内容
 - `(?...)` - *?*之后的第一个字符用于`表义`, 表示后续字符的语义
 - `(?P<name>...)` 为分组命名
 - ...
 - `\number` - 重复前面一个组(group)的内容number次. 如`(.+) \1`将匹配`he he`
 - `\A` - 仅匹配字符串的开始(纳尼)
 - `\b` - 匹配单词前后的`empty string`, 可以是空串, 也可以是任何非字母或下划线的字符
 - `\B` - 匹配单词内部的`empty string`\\
 (以上2个真心不太懂)
 - `\d` - 匹配十进制数字, `[0-9]`
 - `\D` - 匹配任意非十进制数字的字符, `[^0-9]`
 - `\s` - 匹配空白字符, `[ \t\n\r\f\v]`
 - `\S` - 匹配任意非空白字符
 - `\w` - 匹配单词字符, `[A-Za-z0-9_]`
 - `\W` - 匹配任意非单词字符
 - `\Z` - 匹配字符串的尾, 与`\A`相对应?
- 大多数python字符串支持的标准特殊字符, regex解析器都接受:

```text
\a      \b      \f      \n
\r      \t      \u      \U
\v      \x      \\
```

###6.2.2 Module Contents

- re.compile(pattern, flags=0) - 编译regex pattern, 得到一个regex 对象, 其自带`match`与`search`方法. flags 如下所示:
 - re.A
 - re.ASCII - 使`\w`, `\W`, `\b`, `\B`, `\d`, `\D`, `\s`和`\S`工作在ASCII模式下
 - re.DEBUG - 显示编译表达式的debug信息
 - re.I
 - re.IGNORECASE - 忽略大小写, [A-Z]将可以匹配小写字母
 - re.L
 - re.LOCALE - 使`\w`, `\W`, `\b`, `\B`, `\s`和`\S`工作在当前作用域的编码格式下
 - re.M
 - re.MULTILINE - `^`, `$`除了原义外, 还能匹配每行的首尾
 - re.S
 - re.DOTALL - `.`可以匹配任意字符包括新行
 - re.X
 - re.VERBOSE - 该标志允许书写可读性更强的regex, 可多行书写, 忽略空格, 可添加注释. 如:

```python
a = re.compile(r"""\d +  # the integral part
                   \.    # the decimal point
                   \d *  # some fractional digits""", re.X)
```

- re.search(pattern, string, flags=0) - 扫描字符串, 将所有子串都尝试与regex进行匹配,匹配到则立即返回一个`match object`, 匹配不到则返回`None`
- re.match(pattern, string, flags=0) - 只从字符串的开始与regex进行匹配, 成功则返回`match object`, 否则返回`None`
- re.fullmatch(pattern, string, flags=0) - 只有在字符串完全匹配regex, 才返回`match object`
- re.split(pattern, string, maxsplit=0, flags=0) - 用regex匹配到的子串分割字符串. 若`pattern`中使用了分组(group), 则得到的全部分组也将作为返回列表的一部分被返回. `maxsplit`参数用于指定最大分割次数, 若前面的分割已经达到了`maxsplit`的值, 字符串剩余部分将被最后一个元素

```python
> re.split('\W+', 'Words, words, words.')
['Words', 'words', 'words', '']
> re.split('(\W+)', 'Words, words, words.')
['Words', ', ', 'words', ', ', 'words', '.', '']
> re.split('\W+', 'Words, words, words.', 1)
['Words', 'words, words.']
> re.split('[a-f]+', '0a3B9', flags=re.IGNORECASE)
['0', '3', '9']
```

- re.findall(pattern, string, flags=0) - 以list的形式返回字符串中所有不重叠的匹配项. 所谓不重叠, 即`re.findall('ab+', "abbbb")`只能匹配`abbbb`, 不能再匹配`ab`或`abb`或`abbb`. 按从左到右的顺序扫描字符串, 并按匹配的先后顺序返回. 若`pattern`使用了分组(group), 则返回一个元组的列表
- re.finditer(pattern, string, flags=0) - 与findall类似, 只是返回一个`match object`的生成器
- re.sub(pattern, repl, string, count=0, flags=0) - 用`repl`替换`str`中被匹配到的字符串, 并返回. 若没有匹配到, 则字符串原样返回. `repl`可以是字符串, 也可以是函数. 当`repl`是字符串时, 与`\`搭配的特殊字符将被执行. 若为函数, 则需要以一个`match object`作为对象, 并返回一个替换的字符串:

```python
>>> def dashrepl(matchobj):
...     if matchobj.group(0) == '-' : return ' '
...     else: return '-'
>>> re.sub('-{1,2}', dashrepl, 'pro----gram-files')
pro--gram files'
```

- re.sub(pattern, repl, string, count=0, flags=0)中的`count`表示最大替换次数. 若未指定或为0, 则替换全部匹配到的字符串
- re.subn(pattern, repl, string, count=0, flags=0) - 与re.sub功能相同, 但返回一个新串与替换次数的tuple`(new_string, number_of_subs_made)
- re.escape(string) - 对所有ASCII字母, 数字和下划线的字符进行转义, 返回一个转义后的字符串
- re.purge - 清楚regex缓存, 不知道什么意思
- re.error(msg, pattern=None, pos=None) - 当作为regex不合法时, 抛出此异常.

###6.2.3 regex Objects

- 编译regex, 将得到regex对象.
- regex.search(string[, pos[, endpos]]) - 与re.search类似. `string`表示待搜索的字符串.`pos`指定搜索的起点, 默认是字符串的开始; `endpos`搜索的结束位置
- regex.match(string[, pos[, endpos]]) - 与re.match类似, 另外的参数与regex.search一样
- regex.fullmatch(string[, pos[, endpos]]) - 与re.fullmatch类似, 另外的参数与regex.search一样
- regex.split(string, maxsplit=0) - 与re.split一样
- regex.findall(string[, pos[, endpos]]) - 同上(与re.xx类似, 可选参数与上述一样
)
- regex.finditer(string[, pos[, endpos]]) - 同上
- regex.sub(repl, string, count=0) - 与re.sub一样
- regex.subn(repl, string, count=0) - 与re.subn一样
- regex.flags - 在编译时指定
- regex.groups - pattern中的分组数量, 由此可得到`regex.findall`返回的list中每个元素的中的组数
- regex.groupindex - A dictionary mapping any symbolic group names defined by (?P<id>) to group numbers. 即一般为空
- regex.pattern - 显然而建, 返回regex

###6.2.4 Match Object

- `match`对象总是带有一个布尔值, 因此可以简单地将match对象作为判断表达式
- match.expand(template) - 对一个模板字符串进行特殊字符转换, 返回结果字符串
- match.group([group1, ...]) - 返回匹配到的分组结果. 如果是单参数的, 返回单个字符串; 若参数为多个,则返回一个tuple. 不指定参数, `group1`默认是0, 返回完成的匹配结果, 否则返回对应的分组, 因为0已经被使用, 因此分组的索引从1开始. 若一个分组匹配了多次, 只有最后一次匹配结果是可访问的:

```python
>>> m = re.match(r"(..)+", "a1b2c3")  # Matches 3 times.
>>> m.group(1)                        # Returns only the last match.
'c3'
```

- match.groups(default=None) - 返回包含所有分组的tuple. default用于在没有匹配到选项时, 作为返回值, 默认是`None`
- match.groupdict(default=None) - 返回命名分组的字典, key即为分组名称. default用法同上
- match.start([group]) & match.end([group]) - 返回`group`匹配到的子串的首(尾)字符在整个`match.string`中的索引. `group`默认是0, 即整个字符串. 若分组存在, 但并没有匹配到任何字符串, 将返回-1.
- match.span([group]) - 返回一个二元元组`(m.start(group), m.end(group))`, 即分组的子串的在整个`match.string`中索引的起止.
- match.pos - 即用于regex对象的`search`, `match`方法的pos
- match.endpos - 同上
- match.lastindex - 最后一个分组的索引
- match.lastgroup - 最后一个分组的名称, 若未指定名称, 则为None
- match.re - 得到该`match`对象使用的regex
- match.string - 得到该`match`对象的string

###6.2.5 Examples

- `.*(.).*\1` - 检查字符串中出现的一对字符(重复1次)
- 模拟`C`语言的`scanf`函数:

```text
scanf   regex
%c      .
%5c     .{5}
%d      [-+]?\d+
%e,     %E, %f, %g  [-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?
%i      [-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)
%o      [-+]?[0-7]+
%s      \S+
%u      \d+
%x, %X  [-+]?(0[xX])?[\dA-Fa-f]+
```

- 因此对于`/usr/sbin/sendmail - 0 errors, 4 warnings`的解析可以是:\\
`%s - %d errors, %d warnings` - > `(\S+) - (\d+) errors, (\d+) warnings`
- search vs match
 - match只检查字符串的头
 - search扫描整个字符串
 - 在regex中使用`^`, 限制search从头匹配
 - 多行模式下, `match`只能匹配字符串的开始, 对`search`使用`^`能匹配每一行的开始
- `sub`函数的`repl`可以是一个函数, 但这个函数只能接收`match`对象作为唯一参数, 并返回替换后的string

```python
>>> def repl(m):
...     inner_word = list(m.group(2))
...     random.shuffle(inner_word)
...     return m.group(1) + "".join(inner_word) + m.group(3)
>>> text = "Professor Abdolmalek, please report your absences promptly."
>>> re.sub(r"(\w)(\w+)(\w)", repl, text)
'Poefsrosr Aealmlobdk, pslaee reorpt your abnseces plmrptoy.'
>>> re.sub(r"(\w)(\w+)(\w)", repl, text)
'Pofsroser Aodlambelk, plasee reoprt yuor asnebces potlmrpy.'
```

```python
>>> def dashrepl(matchobj):
...     if matchobj.group(0) == '-': return ' '
...     else: return '-'
>>> re.sub('-{1,2}', dashrepl, 'pro----gram-files')
'pro--gram files'
```

- 与`search`不同, `findall`匹配给定字符串中所有regex, 并返回一个list
- 与`findall`不同, `finditer`返回一个`match`对象的迭代器, 由于每个元素都是一个`match`对象, 因此包含的信息会比简单的string更多
- `raw string`能是regex更清晰, 不用太多的`\`转义
- 自制分词器:

```python
import collections
import re

Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])

def tokenize(code):
    keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
    token_specification = [
        ('NUMBER',  r'\d+(\.\d*)?'),  # Integer or decimal number
        ('ASSIGN',  r':='),           # Assignment operator
        ('END',     r';'),            # Statement terminator
        ('ID',      r'[A-Za-z]+'),    # Identifiers
        ('OP',      r'[+\-*/]'),      # Arithmetic operators
        ('NEWLINE', r'\n'),           # Line endings
        ('SKIP',    r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH',r'.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            raise RuntimeError('%r unexpected on line %d' % (value, line_num))
        else:
            if kind == 'ID' and value in keywords:
                kind = value
            column = mo.start() - line_start
            yield Token(kind, value, line_num, column)

statements = '''
    IF quantity THEN
        total := total + price * quantity;
        tax := price * 0.05;
    ENDIF;
'''

for token in tokenize(statements):
    print(token)
```
