## python元类速记

- 类是一组用来描述如何生成一个对象的代码段.在python中,类同样是一个对象
- 只要使用关键字`class`,python解释器就在执行的时候创建一个对象.这个对象(类)自身拥有创建对象(类实例)的能力.
- 由于类的本质仍然是一个对象,于是可以像操作普通对象一样:
 1. 将它赋值给一个变量
 2. 可以拷贝它
 3. 可以为它增加属性
 4. 可以将它作为函数参数进行传递

- `type`函数,除了用于获取对象的类型,还可以动态地创建类.它接受一个类的描述作为参数,返回一个类(何为动态,请看这里)[http://www.cnblogs.com/cavingdeep/archive/2005/08/03/206374.html]

```python
type(类名, 父类的元组(针对继承的情况,可以为空,), 包含属性的字典(名称和值))

# 以下两种创建类的方法等效

# 1
class Foo(object):
    bar = True
    def echo_bar(self):
        print(self.bar)

#2
def echo_bar(self):
    print(self.bar)
Foo = type("Foo", (,), {"bar" : True, "echo_bar" : echo_bar})
```

- `type`实际是一个元类,它就是python在背后创建所有类的元类.`str`是用来创建字符串对象的类,`int`是用来创建整数对象的类,而`type`就是用来创建类对象的类

```python
>>> age = 35
>>> age.__class__
<type 'int'>
>>> name = 'bob'
>>> name.__class__
<type 'str'>
>>> def foo(): pass
>>>foo.__class__
<type 'function'>
>>> class Bar(object): pass
> b = Bar()
>>> b.__class__
<class '__main__.Bar'>
>>> age.__class__.__class__
<type 'type'>
>>> foo.__class__.__class__
<type 'type'>
>>> b.__class__.__class__
<type 'type'>
```

```python
class Foo(object):
    __metaclass__ = something
    [...]
```

- 当python解释器执行到`class Foo(object)`时,在内存中创建`Foo`类对象之前,将首先查看类定义中是否有`__metaclass__`属性.若存在`__metaclass__`,则用其来创建类`Foo`,否则将使用内建的`type`来创建


```python
class Foo(Bar):
    pass
```

- 此处,Python解释器也将首先在`Foo`的定义内查找`__metaclass__`.若没有找到`__metaclass__`,则一级级往上,在其父类中继续寻找`__metaclass__`属性.若还是没找到`__metaclass__`,则在模块层次寻找`__metaclass__`.若还是没找到,则使用内置的`type`来创建该类对象

- `__metaclass__`存放的就是用来创建类的东西,比如`type`,或者任何`type`的子类,或者使用`type`的东西

- 元类的主要目的是为了当创建类时能自动地改变类.常用于编写api

- `__new__`方法在`__init__`方法之前被调用,它是用来创建对象并返回之的方法.`__init__`方法只是用传入的参数来初始化对象.

- 类方法的第一个参数总是表示当前的实例

```python
class aMetaclass(type):
  def __new__(cls, name, bases, attrs):
    ...
    return type.__new__(cls, name, bases, attrs)
    # cls: class object
    # name: class name
    # bases: father class tuple
    # attrs: attribute & method dict
```

- 元类的用途:
 1. 拦截类的创建
 2. 修改类
 3. 返回修改之后的类

- python中一切都是对象,要么是类的实例,要么是元类额实例,除了`type`.`type`实际上是它自己的元类.

