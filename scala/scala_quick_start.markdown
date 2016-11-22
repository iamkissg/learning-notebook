# Scala 之初见

- `.scala` 文件编译成 Java 字节码，因此编译的过程类似 Java：
    - 编译：`scalac HelloWorld.scala`
    - 执行：`scala HelloWorld`
- 交互式：`scala` 会启动 scala 解释器， 像 Python 一样
- 脚本 scala，以下文件命名为 `.sh`， 并可以用 shell 执行

```shell
#!/usr/bin/env scala
object HelloWorld extends App {
  println("Hello, world!")

}
HelloWorld.main(args)
```

## 基本语法

- 类名 - 对于所有的类名的第一个字母要大写：`class MyFirstScalaClass`
- 方法名称 - 所有的方法名称的第一个字母用小写:`def myMethodName()`
- 程序文件名 - 程序文件的名称应该与对象名称完全匹配。
- def main(args: Array[String]) - Scala程序从main()方法开始处理，这是每一个Scala程序的强制程序入口部分。

### 标识符

- 符号"$"在 Scala 中也看作为字母。以"$"开头的标识符为保留的 Scala 编译器产生的标志符使用
- Scala 内部实现时会使用转义的标志符，比如 `:->` 使用 `$colon$minus$greater` 来表示这个符号
- `混合标志符`由字符数字标志符后面跟着一个或多个符号组成，比如 `unary_+`
- `字面量标志符`为使用倒引号 (`\``) 定义的字符串，比如 `x`。
- 可以在倒引号之间使用任何有效的 Scala 标志符，Scala 将它们解释为一个 Scala 标志符：
    - 在 Scala 中不能使用 Thread.yield() 是因为 yield 为 Scala 中的关键字， 必须使用 Thread.`yield`()来使用这个方法。
- 用分号换行，但是可选

### 包

- Scala 使用 package 关键字定义包，在Scala将代码定义到某个包中有两种方式：
    1. 在文件头定义包名，将后续所有代码都放在该包中：`package com.kissg`
    2. `package com.kissg { ... }`，可以在一个文件中定义多个包

### 导入

```scala
import java.awt.Color
import java.awt._  // Python 的 from xxx import *

// import selector
import java.awt.{Color, Font}  // 导入 Color 和 Font
import java.util.{HashMap => JavaHashMap}  // Python 的 as
import java.util.{HashMap => _, _}  // 引入 util 包所有的成员，但 HashMap 被隐藏
```

- 默认情况下，Scala 总会引入 java.lang._ 、 scala._ 和 Predef._

## 数据类型

| 数据类型 | 描述 |
| :-----： | :--: |
| Byte    | 8位有符号补码整数。数值区间为 -128 到 127 |
| Short   | 16位有符号补码整数。数值区间为 -32768 到 32767 |
| Int | 32位有符号补码整数。数值区间为 -2147483648 到 2147483647 |
| Long    | 64位有符号补码整数。数值区间为 -9223372036854775808 到 9223372036854775807 |
| Float   | 32位IEEE754单精度浮点数 |
| Double  | 64位IEEE754单精度浮点数 |
| Char    | 16位无符号Unicode字符, 区间值为 U+0000 到 U+FFFF |
| String  | 字符序列 |
| Boolean | true或false |
| `Unit`    | 表示无值，和其他语言中 void 等同。用作不返回任何结果的方法的结果类型。Unit 只有一个实例值，写成() |
| `Null`    | null 或空引用 |
| `Nothing` | Nothing 类型在 Scala 的类层级的最低端；它是任何其他类型的子类型。 |
| `Any` | Any 是所有其他类的超类 |
| `AnyRef` | AnyRef 类是 Scala 里所有引用类 (reference class) 的基类 |

- 上述数据类型都是对象，scala 没有 java 的原生类型
- 符号字面量：`'<标识符>'`，标识符可以是任何字母或数组（不能以数字开头）。
- 符号字面量被映射成预定义类 `scala.Symbol` 的实例:

```scala
package scala
final case class Symbol private (name: String) {
    override def toString: String = "'" + name
}
```

- 多行字符串的表示同 Python，使用三个双引号
- scala.Null 和 scala.Nothincode 字符可以用一个八进制转义序列来表示，即反斜线‟\‟后跟 最多三个八进制
- 0 到 255 间的 Unicode 字符可以用一个八进制转义序列来表示，即反斜线 "\" 后跟最多三个八进制。

## 变量

- 变量是一种使用方便的占位符，用于引用计算机内存地址，变量创建后会占用一定的内存空间。基于变量的数据类型，操作系统会进行内存分配并且决定什么将被储存在保留内存中
- `var` - 声明变量
- `val` - 声明常量，不可变
- 类型在变量名之后等号之前声明。语法：`var|val variable: Type [= Initial Value]`
- 在 Scala 中声明变量和常量不一定要指明数据类型，将根据初始值自动推断。仅声明没有初始化的情况下，必须给定类型；或者说，没有指定类型的情况下，必须给出初始值。
- 常量必须给出其初始值
- 多变量声明：
    - val height, weight = (175, 65) - height 和 weight 都将被初始为 tuple
    - val (height: Int, weight: Int) = (175, 65) - height 被初始化为 175，weight 被初始化为 65

## 访问修饰符

- Scala 对象的默认访问级别都是 `public`
- Scala 的 private 限定符，在嵌套类的情况下，外层类不能访问被嵌套类的私有成员

### private

- 带有 private 标记的成员只有在包含了成员定义的类或对象内部可见，同样的规则还适用于内部类

```scala
class Outer{
    class Inner{
        private def f(){println("f")}
        class InnerMost{
            f() // 正确
        }
    }
    (new Inner).f() // 错误, 访问不在类 inner 内部
}
```

### protected

- protected 限定符，只允许保护成员在定义了该成员的类的子类中。（Java 中，用 protected 关键字修饰的成员，除了定义了该成员的类的子类可以访问，同一个包内的其他类也可以对该成员进行访问）

```scala
package p{
    class Super{
        protected def f() {println("f")}
    }

    class Sub extends Super{
        f()
    }

    class Other{
        (new Super).f() // 错误, 并没有继承自 Super
    }
}
```

### public

- public 成员可以在任何地方被访问

### 作用域保护

- 访问修饰符可以通过使用`限定词强调`: `private[x]` 或 `protected[x]`. x 指代某个所属的包、类或单例对象。
- `private[x]` - 该成员除了对 [ ... ] 中的类或 [ ... ] 中的包中的类以及它们的伴生对象可见外，对其他所有类都是 private

```scala
package bobsrocckets{
    package navigation{
        private[bobsrockets] class Navigator{
            protected[navigation] def useStarChart(){}

            class LegOfJourney{
                private[Navigator] val distance = 100
            }

            private[this] var speed = 200
        }
    }
    package launch{
        import navigation._

        object Vehicle{
            private[launch] val guide = new Navigator
        }
    }
}
```

- 类 Navigator 被标记为 private[bobsrockets] 就是说这个类对包含在 bobsrockets 包里的所有的类和对象可见。

## 运算符

- Scala 的逻辑运算符 `&&`，`||`，`!`
- 位运算符：`~`, `&`, `|`, `^`, `>>`, `<<`, `>>>` (无符号右移)
- 大多数运算从左往右计算，除了：单目运算符，条件运算符，赋值运算符
- 基本的优先级：
    - 指针最优，单目运算优于双目运算
    - 先算数运算，后移位运算，最后位运算。1 << 3 + 2 & 7 等价于 (1 << (3 + 2))&7
    - 逻辑运算最后计算

## 控制结构

### 条件分支

- `if ... else if ... else ... `

### 循环

- `while`， `do while`， `for`
- Scala 不支持 break 或 continue。
- 中断循环的方式：

```scala
import scala.util.control.Breaks._

breakable {
  for (x <- elems) {
    println(x * 2)
    if (x > 0) break
  }
}
```

## 函数

- scala，方法是类的一部分，函数是一对象，可以赋值给一个变量。在类中定义的函数就是方法。
- scala 函数名可以由特殊字符`：+, ++, ~, &,-, -- , \, /, : ` 等组成
- 函数声明格式：`def functionName ([参数列表]): [returnType]`
- 如果不写等号和函数主体，函数会被隐式声明为`抽象函数`，包含它的类型也是一个抽象类型
- 函数定义格式：

```scala
def functionName ([参数列表]) : [return type] = {
   function body
   return [expr]
}
```

- 函数没有返回值时，可以返回 `Unit`。
- 函数调用的标准格式：`functionName( 参数列表 )`
- 方法的调用：`[instance.]functionName( 参数列表 )`

### 函数传名调用 (call-by-name)

- Scala 解释器在解析函数参数时，有 2 种方式：
    1. 传值调用 (call-by-value): 先计算参数表达式的值，再应用到函数内部
    1. 传名调用 (call-by-name): 将未计算的参数表达式直接应用到函数内部
- 在进入函数内部前，传值调用方式就已经将参数表达式的值计算完毕，而传名调用是在函数内部进行参数表达式的值计算的。
- 每次使用传名调用，解释器都会计算一次表达式的值。
- 使用 `=>` 符号在变量名和变量类型之间设置传名调用

### 指定函数参数名

- 调用函数时，指定函数参数名，可以不必按照顺序向函数传递参数。（Python 的关键字参数）

### 可变参数

- scala 允许指明函数的`最后一个参数`是可以重复的，即不需要指定函数参数的个数，向函数传入可变长度参数列表
- 在参数的类型之后放一个星号来设置可变参数 （Python 的 args）

### 递归函数

- 递归函数 (函数调用自身) 在函数式编程语言中起着重要作用

### 默认参数

- 格式：`def addInt( a:Int=5, b:Int=7 )`

### 高阶函数

- 高阶函数是操作其他函数的函数。其可以使用其他函数作为参数，或使用函数作为输出结果

### 函数嵌套

- 定义在函数内的函数称为局部函数

### 匿名函数

- 匿名函数语法：`( 参数列表 ) => 函数体`
- 匿名函数可以不设置参数，也可以设置多个参数

### 偏函数

- 偏函数是一种表达式，不需要提供函数需要的所有参数，只需要提供部分，或不提供所需参数
- `def log(date: Date, message: String)` -> `val date = new Date; val logWithDateBound = log(date, _ : String)`
- 上式第二个参数使用下划线替换缺失的参数列表，并把新的函数值的索引赋给变量

### 函数柯里化 (Curring)

- 柯里化(Currying)指的是将原来接受两个参数的函数变成新的接受一个参数的函数的过程。新的函数返回一个以原有第二个参数为参数的函数
- `def add(x:Int,y:Int)=x + y` -柯里化> `def add(x:Int)(y:Int) = x + y`
- 所以 `add(1, 2)` 编程了 `add(1)(2)`
- 实现过程：add(1)(2) 实际上是依次调用两个普通函数（非柯里化函数），第一次调用使用一个参数 x，返回一个函数类型的值，第二次使用参数y调用这个函数类型的值。

```scala
def add(x:Int,y:Int)=x+y
--> def add(x:Int)=(y:Int)=>x+y  // 调用使用第一个参数 x
    val result = add(1)  // 返回一个函数类型的值
    --> (y: Int) => 1 + y  // result 的值是一个匿名函数
        --> val sum = result(2)
            --> 3
```

## 闭包

- 闭包是一个函数，返回值依赖于声明在函数外部的一个或多个变量
- 闭包通常来讲可以简单的认为是可以访问一个函数里面局部变量的另外一个函数。

```scala
var factor = 3
val multiplier = (i: Int) => i * factor
```

- 上述代码中，i 是函数的形式参数，在函数被调用时会被赋一个新值。但 factor 是一个定义在函数外面的自由变量。这样的 multiplier 就称为一个闭包，它引用了函数外面定义的变量
- 定义闭包的过程: 是将自由变量捕获而构成一个封闭的函数

## 字符串

- 在 Scala 中，字符串的类型实际上是 Java String，它本身没有 String 类。
在 Scala 中，String 是一个不可变的对象，所以该对象不可被修改。这就意味着你如果修改字符串就会产生一个新的字符串对象。
- 如果需要创建一个可以修改
