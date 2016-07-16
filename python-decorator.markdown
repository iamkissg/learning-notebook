# e-satis's answer in stackoverflow

## 装饰器基础

### Python的函数是对象

为了理解装饰器, 你必须先理解: 在Python的世界, 函数是对象. 这一点很重要. 让我们通过一个简单的例子来看看为什么:

```python
def shout(word="yes"):
    return word.capitalize()+"!"

print shout()
# 输出 : 'Yes!'

# 作为一个对象, 你可以像任何其他对象一样, 将函数赋值给一个变量

scream = shout

# 注意, 我们并没有使用括号:
# 我们没有调用函数, 我们是将"shout"函数装入到"scream"变量中
# 这意味着你可以像从"scream"调用"shout"

print scream()
# 输出 : 'Yes!'

# 不仅如此, 它还意味着你可以删除旧的名字"shout",
# 而仍然可以通过"scream"访问函数

del shout
try:
    print shout()
except NameError, e:
    print e
    # 输出: "name 'shout' is not defined"

print scream()
# 输出: 'Yes!'
```

Okay! 在脑海中保留这个概念. 我们之后会用到它.

Python函数的另一个有趣的属性是: 它们可以在另一个函数的内部被定义...

```python
def talk():

    # 你可以在运行时, 在"talk"函数内部定义一个函数
    def whisper(word="yes"):
        return word.lower()+"..."

    # ... 然后立马使用它

    print whisper()

# 当调用"talk"时, 你的每一次调用都会定义"whisper"一次,
# 再调用"whisper"
talk()
# 输出:
# "yes..."

# 但是, "whisper"在"talk"函数之外实际是不存在的

try:
    print whisper()
    except NameError, e:
        print e
        #输出 : "name 'whisper' is not defined"
        #Python的函数是对象
```

### 函数引用

还跟得上吗? 现在开始讲有趣的部分...

你已经见识过了函数是对象. 因此,

- 函数可以赋值给一个变量
- 函数可以在另一个函数中被定义

这意味着**函数可以返回(`return`)另一个函数**. 看仔细了!

```python
def getTalk(kind="shout"):

    # 我们在运行时定义函数
    def shout(word="yes"):
        return word.capitalize()+"!"

    def whisper(word="yes") :
        return word.lower()+"...";

    # 然后我们返回其中的一个
        if kind == "shout":
            # 不适用括号, 我们并不是在调用函数
            # 我们是在返回一个函数对象
            return shout
        else:
            return whisper

# 你要如何使用这洪荒巨兽呢?

# 取得函数, 并将其赋给一个变量
talk = getTalk()

# 此处, 你可以看见"talk"是一个函数对象
print talk
#输出 : <function shout at 0xb7ea817c>

# 以下对象是函数"talk"的一项返回
print talk()
#输出 : Yes!

# 你甚至可以直接使用
# And you can even use it directly if you feel wild:
print getTalk("whisper")()
#输出 : yes...
```

等等...不止如此!

如果你要`return`一个函数, 可以传入一个函数作为参数:

```python
def doSomethingBefore(func):
    print "I do something before then I call the function you gave me"
    print func()

doSomethingBefore(scream)
#输出:
#I do something before then I call the function you gave me
#Yes!
```

现在, 你已经具备了理解装饰器所需的一切知识. 如你所见, 装饰器就是"包装纸(wrapper)", 也就是说, **装饰器允许你在被装饰的函数前后执行代码**, 而不对函数本身做任何修改.

### 动手写装饰器

你最好动手写一写(装饰器):

```python
# 装饰器是函数, 它以另一个函数作为参数
def my_shiny_new_decorator(a_function_to_decorate):

    # 在装饰器的内部, 定义一个"wrapper"函数
    # wrapper函数用于包装原函数, 以在原函数前后执行代码
    def the_wrapper_around_the_original_function():

        # 在此处输入你想在调用原函数之前执行的代码
        print "Before the function runs"

        # 调用被装饰的函数(是函数调用, 需要括号)
        a_function_to_decorate()

        # 在此处输入你想在调用原函数之后执行的代码
        print "After the function runs"

    # 此处, 被装饰的函数并没有被执行
    # 返回刚刚创建的包装函数
    # 包装函数包括被装饰的函数, 在函数前后执行的代码
    return the_wrapper_around_the_original_function

# 现在, 假设你创建了一个可能用不到的函数
def a_stand_alone_function():
    print "I am a stand alone function, don't you dare modify me"

a_stand_alone_function()
#输出: I am a stand alone function, don't you dare modify me

# 然而, 你可以装饰它, 扩展它
# 只需要将它传递给一个装饰器, 装饰器将动态地将函数包装进任何你想要的代码中
# 并返回一个可用的新函数

a_stand_alone_function_decorated = my_shiny_new_decorator(a_stand_alone_function)
a_stand_alone_function_decorated()
#输出:
#Before the function runs
#I am a stand alone function, don't you dare modify me
#After the function runs
```

现在, 你可能想要在每次调用`a_stand_alone_function`时, 替代地调用`a_stand_alone_function_decorated`. 很简单, 用装饰器`my_shiny_new_decorator`返回的函数覆盖原函数`a_stand_alone_function`即可.

```python
a_stand_alone_function = my_shiny_new_decorator(a_stand_alone_function)
a_stand_alone_function()
#输出:
#Before the function runs
#I am a stand alone function, don't you dare modify me
#After the function runs

# 这就是装饰器的作用了
```

### 装饰器揭秘

用装饰器语法重现先前的例子, 是这样的:

```python
@my_shiny_new_decorator
def another_stand_alone_function(:
    print "Leave me alone"

another_stand_alone_function(
#outputs:
#Before the function runs
#Leave me alone
#After the function runs
```

是的, 就是这样, 这么简单. `@decorator`是以下形式的缩写:

```python
another_stand_alone_function = my_shiny_new_decorator(another_stand_alone_function)
```

此处所讲的装饰器是[装饰器设计模式](https://en.wikipedia.org/wiki/Decorator_pattern)的python变种. 在python中有一些经典的设计模式, 可使开发更加容易(比如迭代器(iterator)).

当然, 你可以叠加装饰器:

```python
def bread(func):
    def wrapper():
        print "</''''''\>"
        func()
        print "<\______/>"
    return wrapper

def ingredients(func):
    def wrapper():
        print "#tomatoes#"
        func()
        print "~salad~"
    return wrapper

def sandwich(food="--ham--"):
    print food

sandwich()
#输出: --ham--
sandwich = bread(ingredients(sandwich))
sandwich()
#输出:
#</''''''\>
# #tomatoes#
# --ham--
# ~salad~
#<\______/>
```

python装饰器的语法:

```python
@bread
@ingredients
def sandwich(food="--ham--"):
    print food

sandwich()
#输出:
#</''''''\>
# #tomatoes#
# --ham--
# ~salad~
#<\______/>
```

你设置装饰器的顺序很重要:

```python
@ingredients
@bread
def strange_sandwich(food="--ham--"):
    print food

strange_sandwich()
#输出:
##tomatoes#
#</''''''\>
# --ham--
#<\______/>
# ~salad~
```

---

### 现在: 针对你的问题(在python中, 如何实现串级装饰器)...
(译者注: 本文是stackoverflow上一个回答)

结论是, 如你所见, 很容易就可以实现串级装饰器:

```python
# 加粗装饰器
def makebold(fn):
    # 装饰器返回的新的函数
    def wrapper():
        # 在前后插入一些代码
        return "<b>" + fn() + "</b>"
    return wrapper

# 斜体装饰器
def makeitalic(fn):
    # 装饰器返回的新的函数
    def wrapper():
        # 在前后插入一些代码
        return "<i>" + fn() + "</i>"
    return wrapper

@makebold
@makeitalic
def say():
    return "hello"

print say()
#输出: <b><i>hello</i></b>

# 等价于
def say():
    return "hello"
say = makebold(makeitalic(say))

print say()
#输出: <b><i>hello</i></b>
```

现在, 你可以愉快地离开了(译者注: 这是作者对提问者说的). 或者接着烧脑, 看看装饰器的一些高级用法.

---

## 装饰器进阶

### 向被装饰函数传递参数

```python
# 这并不是黑魔法, 你只需要在包装过程中传入参数

def a_decorator_passing_arguments(function_to_decorate):
    def a_wrapper_accepting_arguments(arg1, arg2):
        print "I got args! Look:", arg1, arg2
        function_to_decorate(arg1, arg2)
    return a_wrapper_accepting_arguments

# 当你调用装饰器返回的函数时, 你调用了包装纸(wrapper)
# 向包装纸传递的参数将可继续传递给被装饰函数

@a_decorator_passing_arguments
def print_full_name(first_name, last_name):
    print "My name is", first_name, last_name

print_full_name("Peter", "Venkman")
# 输出:
#I got args! Look: Peter Venkman
#My name is Peter Venkman
```

### 装饰方法

python好的一点是, 方法(method)和函数(function)实际是一样的. 唯一的区别在于, 方法的第一个参数需要是当前对象(`self`)的引用.

这意味着, 你可以用同样的方式创建方法的装饰器! 不过, 别忘了`self`.

```python
def method_friendly_decorator(method_to_decorate):
    def wrapper(self, lie):
        lie = lie - 3 # 真好, 年龄更小了 :-)
        return method_to_decorate(self, lie)
    return wrapper


class Lucy(object):

    def __init__(self):
        self.age = 32

    @method_friendly_decorator
    def sayYourAge(self, lie):
        print "I am %s, what did you think?" % (self.age + lie)

l = Lucy()
l.sayYourAge(-3)
#输出: I am 26, what did you think?
```

如果要写一个通用的装饰器--可用于任何函数或方法, 而不必考虑其参数--那么, 用`*args, **kwargs`就好了:

```python
def a_decorator_passing_arbitrary_arguments(function_to_decorate):
    # 包装纸接收任意参数
    def a_wrapper_accepting_arbitrary_arguments(*args, **kwargs):
        print "Do I have args?:"
        print args
        print kwargs
        # 将得到的参数解压(unpack), 此处为*args, **kwargs
        # 如果对解压不熟悉, 可参考
        # http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/
        function_to_decorate(*args, **kwargs)
    return a_wrapper_accepting_arbitrary_arguments

@a_decorator_passing_arbitrary_arguments
def function_with_no_argument():
    print "Python is cool, no argument here."

function_with_no_argument()
#输出
#Do I have args?:
#()
#{}
#python就是这么酷, 此地无参.

@a_decorator_passing_arbitrary_arguments
def function_with_arguments(a, b, c):
    print a, b, c

function_with_arguments(1,2,3)
#输出
#Do I have args?:
#(1, 2, 3)
#{}
#1 2 3

@a_decorator_passing_arbitrary_arguments
def function_with_named_arguments(a, b, c, platypus="Why not ?"):
    print "Do %s, %s and %s like platypus? %s" %\
    (a, b, c, platypus)

function_with_named_arguments("Bill", "Linus", "Steve", platypus="Indeed!")
#输出
#Do I have args ? :
#('Bill', 'Linus', 'Steve')
#{'platypus': 'Indeed!'}
#Bill, Linus and Steve喜欢鸭嘴兽吗? 千真万确!

class Mary(object):

    def __init__(self):
        self.age = 31

    @a_decorator_passing_arbitrary_arguments
    def sayYourAge(self, lie=-3): # 现在你可以添加一个默认值
        print "I am %s, what did you think ?" % (self.age + lie)

m = Mary()
m.sayYourAge()
#输出
# Do I have args?:
#(<__main__.Mary object at 0xb7d303ac>,)
#{}
#I am 28, what did you think?
```

### 向装饰器传递参数

好吧, 现在你觉得如何向装饰器本身传递参数呢?

这有点绕, 因为装饰器必须接收一个函数作为参数. 因此, 你不能向装饰器直接传递被装饰的函数的参数.

在讲解解决方法之前, 让我们先做一个小小的回顾:

```python
# 装饰器是 普通 函数
def my_decorator(func):
    print "I am an ordinary function"
    def wrapper():
        print "I am function returned by the decorator"
        func()
    return wrapper

# 所以, 你可以不使用"@"调用它

def lazy_function():
    print "zzzzzzzz"

decorated_function = my_decorator(lazy_function)
#输出: I am an ordinary function

# 它将会输出 "I am an ordinary function", 因为这就是你所做的:
# 调用一个函. 没有一点魔法在里面

@my_decorator
def lazy_function():
    print "zzzzzzzz"

#输出: I am an ordinary function
```

上述两者完全相同, 都是调用了`my_decorator`. 所以当你`@my_decorator`, 你是在告诉Python去调用被变量`my_decorator`标记的函数.

这一点很重要! 你可以用标签直接指明装饰器, 或者不这样.

让我们再深入一点.

```python
def decorator_maker():

    print "I make decorators! I am executed only once: "+\
          "when you make me create a decorator."

    def my_decorator(func):

        print "I am a decorator! I am executed only when you decorate a function."

        def wrapped():
            print ("I am the wrapper around the decorated function. "
                  "I am called when you call the decorated function. "
                  "As the wrapper, I return the RESULT of the decorated function.")
            return func()

        print "As the decorator, I return the wrapped function."

        return wrapped

    print "As a decorator maker, I return a decorator"
    return my_decorator

# 让我们创建一个装饰器
new_decorator = decorator_maker()
# 输出:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator

# 接下来, 我们来装饰函数

def decorated_function():
    print "I am the decorated function."

decorated_function = new_decorator(decorated_function)
#输出:
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function

# 调用函数:
decorated_function()
#输出:
#I am the wrapper around the decorated function. I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.
```

这里没有什么可惊奇的.

跳过所有繁琐的中间变量, 以下与上述方法完全一样.

```python
def decorated_function():
    print "I am the decorated function."
decorated_function = decorator_maker()(decorated_function)
#输出:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function.

# 最后:
decorated_function()
#输出:
#I am the wrapper around the decorated function. I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.
```

还可以更精简一些:

```python
@decorator_maker()
def decorated_function():
    print "I am the decorated function."
#outputs:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function.

#Eventually:
decorated_function()
#outputs:
#I am the wrapper around the decorated function. I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.
```

嘿, 你看到了吗? 我们通过"`@`"语法使用了函数.

所以, 回到带参的装饰器. 如果我们可以用函数在运行时生成装饰器, 我们就能够向那个函数传递参数了, 对吧?

```python
def decorator_maker_with_arguments(decorator_arg1, decorator_arg2):

    print "I make decorators! And I accept arguments:", decorator_arg1, decorator_arg2

    def my_decorator(func):
        # 此处传递参数的能力, 得益于闭包的性质
        # 如果你不习惯闭包, 你可以假设它是ok的, 或者看一下这篇文章:
        # http://stackoverflow.com/questions/13857/can-you-explain-closures-as-they-relate-to-python
        print "I am the decorator. Somehow you passed me arguments:", decorator_arg1, decorator_arg2

        # 不要混淆了装饰器参数和函数参数!
        def wrapped(function_arg1, function_arg2) :
            print ("I am the wrapper around the decorated function.\n"
                  "I can access all the variables\n"
                  "\t- from the decorator: {0} {1}\n"
                  "\t- from the function call: {2} {3}\n"
                  "Then I can pass them to the decorated function"
                  .format(decorator_arg1, decorator_arg2,
                          function_arg1, function_arg2))
            return func(function_arg1, function_arg2)

        return wrapped

    return my_decorator

@decorator_maker_with_arguments("Leonard", "Sheldon")
def decorated_function_with_arguments(function_arg1, function_arg2):
    print ("I am the decorated function and only knows about my arguments: {0}"
           " {1}".format(function_arg1, function_arg2))

decorated_function_with_arguments("Rajesh", "Howard")
#输出:
#I make decorators! And I accept arguments: Leonard Sheldon
#I am the decorator. Somehow you passed me arguments: Leonard Sheldon
#I am the wrapper around the decorated function.
#I can access all the variables
#   - from the decorator: Leonard Sheldon
#   - from the function call: Rajesh Howard
#Then I can pass them to the decorated function
#I am the decorated function and only knows about my arguments: Rajesh Howard
```

这就是带参的装饰器了.参数也可以设置成变量:

```python
c1 = "Penny"
c2 = "Leslie"

@decorator_maker_with_arguments("Leonard", c1)
def decorated_function_with_arguments(function_arg1, function_arg2):
    print ("I am the decorated function and only knows about my arguments:"
           " {0} {1}".format(function_arg1, function_arg2))

decorated_function_with_arguments(c2, "Howard")
#输出:
#I make decorators! And I accept arguments: Leonard Penny
#I am the decorator. Somehow you passed me arguments: Leonard Penny
#I am the wrapper around the decorated function.
#I can access all the variables
#   - from the decorator: Leonard Penny
#   - from the function call: Leslie Howard
#Then I can pass them to the decorated function
#I am the decorated function and only knows about my arguments: Leslie Howard
```

如你所见, 使用该技巧, 你可以像任何(普通)函数一样向装饰器传递参数. 如果你愿意, 你甚至可以使用`*args, **kwargs`. 但是, 请记住装饰器只能被调用**1次**, 即在导入脚本的时候. 之后你就不能动态地设置参数了. 当你"import x"时, **函数已经被装饰了**, 你不能再做任何修改.

---

### 练习: 装饰装饰器

作为福利, 我将给你一个能接收任意参数的装饰器代码片段. 然后, 我们用另一个函数来创建我们的装饰器, 以接收参数.

我们对装饰器进行了包装.

如前所见, 我们是用什么包装了函数?

是的, 就是装饰器!

让我们愉快地写一个装饰器的装饰器吧:

```python
def decorator_with_args(decorator_to_enhance):
    """
    这个函数被用作一个装饰器.
    它必须装饰另一个函数, 那个函数也是一个装饰器
    它允许任何装饰器接收任意数量的参数, 这样就不用每次写(装饰器)的时候都回忆一遍.
    """

    # 使用了与上述一样的技巧传递参数
    def decorator_maker(*args, **kwargs):

        # 我们在运行时创建了一个装饰器, 它接收一个函数作为参数
        # 但它可以持有maker传来的参数
        def decorator_wrapper(func):

            # 我们返回原始装饰器的结果, 一个普通函数
            # 唯一的异错的地方在于: 装饰器必须这样才能正常工作
            return decorator_to_enhance(func, *args, **kwargs)

        return decorator_wrapper

    return decorator_maker
```

它可以像下述一样使用:

```python
# 你可以创建一个用作装饰器的函数. 再用一个装饰器来装饰它
# 不要忘了, 用法是"decorator(func, *args, **kwargs)"
@decorator_with_args
def decorated_decorator(func, *args, **kwargs):
    def wrapper(function_arg1, function_arg2):
        print "Decorated with", args, kwargs
        return func(function_arg1, function_arg2)
    return wrapper

# 现在, 你可以用刚刚创建的被装饰的装饰器来装饰函数了

@decorated_decorator(42, 404, 1024)
def decorated_function(function_arg1, function_arg2):
    print "Hello", function_arg1, function_arg2

decorated_function("Universe and", "everything")
#输出:
#Decorated with (42, 404, 1024) {}
#Hello Universe and everything

# 哇!
```

我知道, 你最近一次有这种感觉, 是听某人说了: "要理解递归, 你必须先理解递归". 现在, 对于学会了(装饰器), 你不感觉很棒码?

---

### 最佳实践: 装饰器

- 装饰器最早出现于Python2.4, 所以请确保你的代码能在2.4之后的版本上运行
- 装饰器减慢了函数调用的速度. 谨记.
- **你无法对函数去装饰**. (确实有技巧可以创建可移除的装饰器, 但没有人会使用它们.) 因此, 一旦函数被装饰了, 在整个代码中, 它都是被装饰的.
- 装饰器包装了函数, 这使得调试变得困难. (这一点在Pyhton2.5之后的版本得到缓解; 请看下面的内容)

Python2.5引入了`functools`模块, 该模块包含的`funtools.wraps()`函数, 可以将被装饰函数名称, 模块, 文档字符串(docstring)拷贝到它的包装纸中.

(有趣的事实是: `funtools.wraps()`还是一个装饰器!)

```python
# 为了调试方便, 栈回溯(stacktrace)打印函数的__name__属性
def foo():
    print "foo"

print foo.__name__
#输出: foo

# 当使用装饰器时, 就显得混乱了
def bar(func):
    def wrapper():
        print "bar"
        return func()
    return wrapper

@bar
def foo():
    print "foo"

print foo.__name__
#输出: wrapper

# "functools"`模块能解决这个问题

import functools

def bar(func):
    # 我们说"wrapper"包装了"func", 然后魔法就发生了
    @functools.wraps(func)
    def wrapper():
        print "bar"
        return func()
    return wrapper

@bar
def foo():
    print "foo"

print foo.__name__
#输出: foo
```

---

### 如何使用装饰器

**一个大问题**: 我能用装饰器做什么?

(装饰器)看上去很酷很强大, 但是用一个实际例子来说明可能会更好. 装饰器的用法很多. 经典的用法是, 拓展一个外部库函数(你无法修改它)的功能, 或者用于调试(因为它是临时的, 你并不想进行修改).

你可以用装饰器不重复地拓展多个函数, 像这样:

```python
def benchmark(func):
    """
    打印函数被执行的时间的装饰器
    """
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print func.__name__, time.clock()-t
        return res
    return wrapper


def logging(func):
    """
    记录脚本活动的装饰器
    (事实上, 它只是进行了打印, 但可以进行日志打印)
    """
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print func.__name__, args, kwargs
        return res
    return wrapper


def counter(func):
    """
    统计并打印函数被执行次数的装饰器
    """
    def wrapper(*args, **kwargs):
        wrapper.count = wrapper.count + 1
        res = func(*args, **kwargs)
        print "{0} has been used: {1}x".format(func.__name__, wrapper.count)
        return res
    wrapper.count = 0
    return wrapper

@counter
@benchmark
@logging
def reverse_string(string):
    return str(reversed(string))

print reverse_string("Able was I ere I saw Elba")
print reverse_string("A man, a plan, a canoe, pasta, heros, rajahs, a coloratura, maps, snipe, percale, macaroni, a gag, a banana bag, a tan, a tag, a banana bag again (or a camel), a crepe, pins, Spam, a rut, a Rolo, cash, a jar, sore hats, a peon, a canal: Panama!")

#输出:
#reverse_string ('Able was I ere I saw Elba',) {}
#wrapper 0.0
#wrapper has been used: 1x
#ablE was I ere I saw elbA
#reverse_string ('A man, a plan, a canoe, pasta, heros, rajahs, a coloratura, maps, snipe, percale, macaroni, a gag, a banana bag, a tan, a tag, a banana bag again (or a camel), a crepe, pins, Spam, a rut, a Rolo, cash, a jar, sore hats, a peon, a canal: Panama!',) {}
#wrapper 0.0
#wrapper has been used: 2x
#!amanaP :lanac a ,noep a ,stah eros ,raj a ,hsac ,oloR a ,tur a ,mapS ,snip ,eperc a ,)lemac a ro( niaga gab ananab a ,gat a ,nat a ,gab ananab a ,gag a ,inoracam ,elacrep ,epins ,spam ,arutaroloc a ,shajar ,soreh ,atsap ,eonac a ,nalp a ,nam A
```

当然, 装饰器的好处是, 对于几乎所有东西, 在不重写的情况, 马上可用. 我说过, 不重复(D.R.Y, Don't Repeat Yourself):

```python
@counter
@benchmark
@logging
def get_random_futurama_quote():
    from urllib import urlopen
    result = urlopen("http://subfusion.net/cgi-bin/quote.pl?quote=futurama").read()
    try:
        value = result.split("<br><b><hr><br>")[1].split("<br><br><hr>")[0]
        return value.strip()
    except:
        return "No, I'm ... doesn't!"


print get_random_futurama_quote()
print get_random_futurama_quote()

#输出:
#get_random_futurama_quote () {}
#wrapper 0.02
#wrapper has been used: 1x
#The laws of science be a harsh mistress.
#get_random_futurama_quote () {}
#wrapper 0.01
#wrapper has been used: 2x
#Curse you, merciful Poseidon!
```

Python本身提供了多个装饰器: `property`, `staticmethod`等等.

- Django用装饰器管理缓存(caching)和视图权限(view permissions).
- 内联异步函数调用的变向实现.

装饰器确实大有用途.
