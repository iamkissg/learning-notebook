- jinja2是一个现代的,设计者友好的python模板语言.
- 特性:
 - 沙箱中执行
 - 强大的 HTML 自动转义系统保护系统免受 XSS
 - 模板继承
 - 及时编译最优的 python 代码
 - 可选提前编译模板的时间
 - 易于调试。异常的行数直接指向模板中的对应行。
 - 可配置的语法
- 基本API调用,通过`Template`创建模板,并用`render`来渲染.(如果模板不是从字符串加载的,而是文件系统或别的数据源,不推荐这种方式)
- `render`方法在有字典或关键字参数时调用扩充模板,字典或关键字参数被传递到模板
- Jinja2 使用一个名为`Environment`的中心对象。这个类的实例用于存储配置、全局对象，并用于从文件系统或其它位置加载模板
- 即使通过:class:Template 类的构造函数用字符串创建模板，也会自动创建一个环境，尽管是共享的
- loader(加载器)负责从application路径下的templates文件夹中寻找模板,可使用多个加载器.
- 不适用加载器,还可以手动加载模板

```python
template env.get_template("xxx.html")
```

- 使用模板加载器,使得模板继承成为可能
- jinja2内部使用unicode,所幸python3中字符串默认就是unicode
- 

```python
class jinja2.Environment([options])
'''The core component of Jinja is the Environment. It contains important shared variables like configuration, filters, tests, globals and others. Instances of this class may be modified if they are not shared and if no template was loaded so far. Modifications on environments after the first template was loaded will lead to surprising effects and undefined behavior.'''
```

- 如果模板通过 Template 构造函数创建，会自动创建一个环境。这些环境被创建为共享的环境，这意味着多个模板拥有相同的匿名环境
- `Template`类代表一个编译好的模板,通常情况下由`Environment`生成模板对象,也可以通过构造函数创建,如上所述.
- 模板是不可变的
- `jinja2.environment.TemplateStream`,一个模板流像python的生成器,但能一次缓冲多个元素.
- `jinja2.Undefined`,默认的未定义类型,能被打印以及迭代,但任何其他访问都会引发异常
- `DebugUndefined`类,打印时输出debug信息
- `StrictUndefined`不允许打印与迭代,只能checking if it's defined using the defined test
- `Undefined`对象通过重载特殊的`__underscore__`方法实现.默认的`Undefined`类实现`__unicode__`而返回一个空字符串,但`__int__`和其他会始终抛出异常.(因此可自定义`__underscore__`方法来改变返回值)
- `jinja2.runtime.Context`包含了模板的变量.它储存传入模板的值,以及模板输出的名.它是不可变类型
- 加载器,负责从诸如文件系统的资源加载模板,环境会把编译的模板保持在内存中.
- 所有加载器都是`BaseLoader`的子类,通过覆盖`get_template`方法实现自定义的加载机制.
- `get_source(environment, template)`: get the template source, filename and reload helper for a template. Return a tuple in the form(source, filename, uptodate). The source part must be the source of the template as unicode or a ascii bytestring. The filename should be the name of the file on the filesystem if it was loaded from there. If uptodate returns False, the template will be reloaded
- `load(environment, name, globals=None)`: load a template. The method looks up the template in the cache or loads one by calling `get_source()`
- jinja2内置的加载器如下:
 1. FileSystemLoader(searchpath, encoding="utf-8"): loads templates from the file system
 2. PackageLoader(package_name, package_path="templates", encoding="utf-8"): loads templates from python eggs or packages
 3. Dictloader(mapping): loads a template from a python dict.It's passed a dict of unicode strings bound to template name
 4. Functionloader(load_func): the function becomes the name of the template passed
 5. PrefixLoader(mapping, delimiter='/'):
 6. ChoiceLoader(loaders): if a template could not be found by one the next one is tried
 7. ModuleLoader(path): loads templates from precompiled templates
- `BytecodeCache`: 字节码缓存,使得在首次使用时把生成的字节码存储到文件系统或其他位置来避免处理模板.当一次性编译大量模板拖慢应用时尤其有用.
- 使用字节码缓存时,将它实例化传给`Environment`
- `jinja2.bccache.Bucket(environment, key, checksum)`: Buckets are used to store the bytecode for one template. 它由字节码缓存创建并初始化,并被传递给一个加载函数
- 内建的字节码缓存:
 1. `FileSystemBytecodeCache`: 将字节码缓存存储到文件系统,
 2. `MemcacheBytecodeCache`: 将字节码缓存存储到内存中
 3. `MinimalClientInterface`:
- 自定义过滤器: 常规的python函数,过滤器左边作为第一个参数,其余的参数作为额外的参数或关键参数传递到过滤器(基本不懂)
- 元api返回一些关于抽象语法树的信息，这些信息能帮助应用实现更多的高级模块概念.所有的元api函数操作一个`Environment.parse()`方法返回抽象语法树
- sandbox(沙箱): 用于为不信任的代码求值. 访问不安全的属性和方法是被禁止的.
- `jiaja2.sandbox.SandboxedEnvironment`: 一个沙箱包裹的环境,与常规的环境一样地工作,但它会告诉编译器去生成沙箱代码
- `jinja2.sanbox.ImmutableSandboxedEnvironment`: 像沙箱环境一般工作,但使用函数`modifies_known_mutable()`禁止了对内建可变对象的修改,如list,set,dict等.
- `jinja2.sandbox.unsafe()`作为装饰器,将函数或方法标记为不安全的
- jinja2沙箱并没有彻底解决安全问题.对于web应用,用户可能用任意的html来创建模板,保证他们不通过 JavaScript 或其他方法来互相损害是至关重要的.
- 沙箱的好坏取决于配置,强烈建议只向模板传递非共享资源,并且使用某种属性白名单
- 模板会抛出运行时或编译器错误
- 为了性能最大化,jinja2会让运算符直接调用类型特定的回调用法.这意味着,通过重载`Environment.call`来拦截是不可能的.为了拦截运算符,需要覆盖`SandboxedEnvironment.intercepted_binops`属性.当需要拦截的运算符被添加到该集合,jinja2会生成调用`SandboxedEnvironment.call_binop()`函数的字节码

