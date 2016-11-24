# Scala 之初见

## Why Scala

- 表达能力
    - 函数是一等公民
    - 闭包
- 简洁
    - 类型推断
    - 函数创建的文法支持
- Java互操作性
    - 可重用Java库
    - 可重用Java工具
    - 没有性能惩罚


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
- 如果需要创建一个可以修改的字符串，使用 `String Builder` 类
- length() 方法获取字符串长度
- concat() 方法连接两个字符串，或者使用 `+`
- printf() 方法格式化字符串并输出
- format() 方法可以返回 String 对象而不是 PrintStream 对象

| 序号|  方法及描述 |
| :-: | :----:      |
| 1   | char charAt(int index) 返回指定位置的字符 |
| 2   | int compareTo(Object o) 比较字符串与对象 |
| 3   | int compareTo(String anotherString) 按字典顺序比较两个字符串 |
| 4   | int compareToIgnoreCase(String str) 按字典顺序比较两个字符串，不考虑大小写 |
| 5   | String concat(String str) 将指定字符串连接到此字符串的结尾 |
| 6   | boolean contentEquals(StringBuffer sb) 将此字符串与指定的 StringBuffer 比较。 |
| 7   | static String copyValueOf(char[] data) 返回指定数组中表示该字符序列的 String |
| 8   | static String copyValueOf(char[] data, int offset, int count) 返回指定数组中表示该字符序列的 String |
| 9   | boolean endsWith(String suffix) 测试此字符串是否以指定的后缀结束 |
| 10  | boolean equals(Object anObject) 将此字符串与指定的对象比较 |
| 11  | boolean equalsIgnoreCase(String anotherString) 将此 String 与另一个 String 比较，不考虑大小写 |
| 12  | byte getBytes() 使用平台的默认字符集将此 String 编码为 byte 序列，并将结果存储到一个新的 byte 数组中 |
| 13  | byte[] getBytes(String charsetName 使用指定的字符集将此 String 编码为 byte 序列，并将结果存储到一个新的 byte 数组中 |
14  vo| id getChars(int srcBegin, int srcEnd, char[] dst, int dstBegin) 将字符从此字符串复制到目标字符数组 |
| 15  | int hashCode() 返回此字符串的哈希码 |
| 16  | int indexOf(int ch) 返回指定字符在此字符串中第一次出现处的索引 |
| 17  | int indexOf(int ch, int fromIndex) 返返回在此字符串中第一次出现指定字符处的索引，从指定的索引开始搜索 |
| 18  | int indexOf(String str) 返回指定子字符串在此字符串中第一次出现处的索引 |
| 19  | int indexOf(String str, int fromIndex) 返回指定子字符串在此字符串中第一次出现处的索引，从指定的索引开始 |
| 20  | String intern() 返回字符串对象的规范化表示形式 |
| 21  | int lastIndexOf(int ch) 返回指定字符在此字符串中最后一次出现处的索引 |
| 22  | int lastIndexOf(int ch, int fromIndex) 返回指定字符在此字符串中最后一次出现处的索引，从指定的索引处开始进行反向搜索 |
| 23  | int lastIndexOf(String str) 返回指定子字符串在此字符串中最右边出现处的索引 |
| 24  | int lastIndexOf(String str, int fromIndex) 返回指定子字符串在此字符串中最后一次出现处的索引，从指定的索引开始反向搜索 |
| 25  | int length() 返回此字符串的长度 |
| 26  | boolean matches(String regex) 告知此字符串是否匹配给定的正则表达式 |
| 27  | boolean regionMatches(boolean ignoreCase, int toffset, String other, int ooffset, int len) 测试两个字符串区域是否相等 |
| 28  | boolean regionMatches(int toffset, String other, int ooffset, int len) 测试两个字符串区域是否相等 |
| 29  | String replace(char oldChar, char newChar) 返回一个新的字符串，它是通过用 newChar 替换此字符串中出现的所有 oldChar 得到的 |
| 30  | String replaceAll(String regex, String replacement 使用给定的 replacement 替换此字符串所有匹配给定的正则表达式的子字符串 |
| 31  | String replaceFirst(String regex, String replacement) 使用给定的 replacement 替换此字符串匹配给定的正则表达式的第一个子字符串 |
| 32  | String[] split(String regex) 根据给定正则表达式的匹配拆分此字符串 |
| 33  | String[] split(String regex, int limit) 根据匹配给定的正则表达式来拆分此字符串 |
| 34  | boolean startsWith(String prefix) 测试此字符串是否以指定的前缀开始 |
| 35  | boolean startsWith(String prefix, int toffset) 测试此字符串从指定索引开始的子字符串是否以指定前缀开始。 |
| 36  | CharSequence subSequence(int beginIndex, int endIndex) 返回一个新的字符序列，它是此序列的一个子序列 |
| 37  | String substring(int beginIndex) 返回一个新的字符串，它是此字符串的一个子字符串 |
| 38  | String substring(int beginIndex, int endIndex) 返回一个新字符串，它是此字符串的一个子字符串 |
| 39  | char[] toCharArray() 将此字符串转换为一个新的字符数组 |
| 40  | String toLowerCase() 使用默认语言环境的规则将此 String 中的所有字符都转换为小写 |
| 41  | String toLowerCase(Locale locale) 使用给定 Locale 的规则将此 String 中的所有字符都转换为小写 |
| 42  | String toString() 返回此对象本身（它已经是一个字符串！） |
| 43  | String toUpperCase() 使用默认语言环境的规则将此 String 中的所有字符都转换为大写 |
| 44  | String toUpperCase(Locale locale) 使用给定 Locale 的规则将此 String 中的所有字符都转换为大写 |
| 45  | String trim() 删除指定字符串的首尾空白符 |
| 46  | static String valueOf(primitive data type x) 返回指定类型参数的字符串表示形式)) |

## 数组

- Scala 提供的数组是用来存储固定大小的同类型元素，通过索引访问元素
- 数组声明的语法格式：`var z:Array[String] = new Array[String](3)` 或 `var z = new Array[String](3)`
- 还可以定义数组：`var z = Array("Runoob", "Baidu", "Google")`
- 多维数组：`var myMatrix = ofDim[Int](3,3)`
- 合并数组也用 `concat()` 方法，接受多个数组作为参数
- 对数组的遍历：`for (x <- array )`
- range() 方法生成一个区间范围的数组，参数同 Python 的range()

## Collection

- 不可变集合，不能被改变，但仍然可以模拟添加，移除或更新操作，这些操作都将返回一个新的集合，同时不改变原来的集合

### List

- 元素以线性方式存储，所有元素的类型都相同，`不可变`, 具有递归的表结构 （链表结构）
- 声明：List[T]
- 构造列表的基本单位：`Nil` 和 `::`

```scala
scala> var site = "Runoob" :: ("Google" :: ("Baidu" :: Nil))
site: List[String] = List(Runoob, Google, Baidu)
```

- head() - 返回首元素
- tail() - 返回一个列表，包含除了第一个元素之外的其他元素
- isEmpty() - 判空
- 可以使用 `:::` 运算符或 `List:::()` 或 `List.concat()` 方法连接列表
- List.fill() 方法 - 创建一个指定重复数量的元素列表：`val site = List.fill(3)("Google")`
- List.tabulate() - 通过给定函数来创建列表，第一个参数为元素的数量，可以是二维的，第二个参数为指定的函数，起始值为 0：`val squares = List.tabulate(6)(n => n * n)`
- List.reverse - 反转

### Set

- 无序，互异。
- 分可变和不可变的，默认情况下，使用不可变集合，引用 `scala.collection.immutable.Set`；使用可变的集合，需要引用 `scala.collection.mutable.Set` 类
- exists - 检查元素是否存在于集合中
- drop - 移除元素
- 不可变的 Set 也有添加或删除的操作，但会产生一个新的 set，不改变原来的
- 3 个基本操作：head，tail，isEmpty
- set 的连接运算符为 `++` 或使用 `set.++()`
- 最大和最小的元素 .max 和 .min
- set.& 方法或 set.intersect 方法计算两个集合的交集

### Map

- Map 也叫哈希表。
- 分可变和不可变的，默认情况下，使用不可变；使用可变的集合，需要引用 `scala.collection.mutable.Map` 类
- 声明格式：`var A :[Char, Int] = Map()` - 键为字符，值为整型
- 基本操作：keys，values，isEmpty
- Map 的合并：`++` 或 `Map.++()`。合并会移除重复的 key
- 通过 foreach 循环 Map 的 keys 和 values：

```scala
sites.keys.foreach{ i =>
                      print( "Key = " + i  )
                      println(" Value = " + sites(i) ) }
```

- Map.contains - 查看 Map 中是否存在指定的 Key

### Tuple

- 元组也是不可变的，元组可以包含不同类型的元素。元组的实际类型取决于元素的类型
- Scala 支持的元素最大长度为 22
- `t._1` 访问第一个元素，依此类推
- 使用 `Tuple.productIterator()` 方法对元素的元素进行迭代：`t.productIterator.foreach{ i =>println("Value = " + i ) }`
- `Tuple.toString` - 将所有元素组合成一个字符串
- `Tuple.swap` - 交换元组的元素

### Option

- Option 的类型用来表示一个值是可选的（有值或无值的）
- Option[T] 是一个类型为 T 的可选值的容器：如果值存在，Option[T] 就是一个 Some[T] ，如果不存在，Option[T] 就是对象 None 。

```scala
// myMap 是 Value 类型是 String 的 hash map, get() 返回一个 Option[String] 的类型
val myMap: Map[String, String] = Map("key1" -> "value")
val value1: Option[String] = myMap.get("key1")
val value2: Option[String] = myMap.get("key2")

println(value1) // Some("value1")
println(value2) // None
```

- getOrElse() - 获取元组中存在的元素或使用默认值

### Iterator

- 迭代器不是集合，是一种用于访问集合的方法
- 两个基本操作是 next 和 hasNext
- it.min 和 it.max 方法从迭代器中查找最小和最大元素
- it.size 和 it.length 查看迭代器的元素个数

## 类和对象

- 类，不占用内存；对象，占用存储空间
- 可以用 new 关键字来创建类的对象
- Scala 中的类不声明为 public，一个 Scala 源文件中可以有多个类。

### 继承

- Scala 的继承类似于 Java，但是：
    1. 重写一个非抽象方法必须使用 override 修饰符
    2. 只有主构函数才可以望基类的构造函数里写参数
    3. 在子类中重写超类的抽象方法时，不需要 override 关键字
- `extends` 关键字来表示继承
- 继承会继承父类的所有属性和方法，Scala 只允许单一继承

```scala
import java.io._

class Point(val xc: Int, val yc: Int) {
   var x: Int = xc
   var y: Int = yc
   def move(dx: Int, dy: Int) {
      x = x + dx
      y = y + dy
      println ("x 的坐标点 : " + x);
      println ("y 的坐标点 : " + y);

   }

}

class Location(override val xc: Int, override val yc: Int,
        val zc :Int) extends Point(xc, yc){
   var z: Int = zc

       def move(dx: Int, dy: Int, dz: Int) {
      x = x + dx
      y = y + dy
      z = z + dz
      println ("x 的坐标点 : " + x);
      println ("y 的坐标点 : " + y);
      println ("z 的坐标点 : " + z);

       }

}

object Test {
    def main(args: Array[String]) {
      val loc = new Location(10, 20, 15);

      // 移到一个新的位置
      loc.move(10, 10, 5);

    }
}
```

- 在 Scala 中，没有 static，但提供了单例模式的实现方法，使用 `object` 关键字
- Scala 中使用单例模式时，除了定义的类之外，还要定义一个同名的 object 对象，它和类的区别是，object 对象不能带参数。
- 当单例对象与某个类共享同一个名称时，他被称作是这个类的伴生对象：companion object。必须在同一个源文件里定义类和它的伴生对象。类被称为是这个单例对象的伴生类：companion class。`类和它的伴生对象可以互相访问其私有成员。`

## Trait(特征)

- Scala Trait 相当于 Java 的接口，实际功能更强大
- Trait 可以定义属性和方法的实现
- 一般情况下 Scala 的类只能够继承单一父类，但是如果是 Trait 的话就可以继承多个，从结果来看就是实现了多重继承。
- Trait 的定义与类相似，使用关键字 trait。特征的方法可以定义方法的实现，也可以不
- subclass 继承 Trait，可以实现未被实现的方法
- `obj.isInstanceOf[T]` - 同 Python 的 `isinstance`
- `obj.asInstanceOf[T].v` - ???

### 构造器构造顺序

- 特征也可以有构造器，由字段的初始化和其他特征体中的语句构成。这些语句在任何混入该特征的对象在构造是都会被执行。
- 构造器的执行顺序：
    - 调用超类的构造器；
    - 特征构造器在超类构造器之后、类构造器之前执行；
    - 特质由左到右被构造；
    - 每个特征当中，父特证先被构造；
    - 如果多个特征共有一个父特质，父特质不会被重复构造
    - 所有特征被构造完毕，子类被构造。
- 构造器的顺序是类的线性化的反向。
- 线性化是描述某个类型的所有超类型的一种技术规格。

## 模式匹配

- 一个模式匹配包含一系列备选项。每个备选项均开始于 `case`，包含一个模式以及一个或多个表达式，用 `=>` 隔离开模式和表达式，
- `x match {case model => exp}` 等价于 `switch(x){case model: exp}`
- 不同于 switch，模式匹配只要发现一个匹配的 case，剩下的 case 不会继续匹配
- ` case _ => exp` - 表示默认的全匹配备选项
- 使用了 case 关键字的类定义就是样例类(case classes)，是特殊的类，经过优化用于模式匹配：`case class Person(name: String, age: Int)`
- 在声明样例类时，会自动：
    - 构造器的每个参数都成为 val，除非显式被声明为 var，但是并不推荐这么做；
    - 在伴生对象中提供了 apply 方法，所以可以不使用 new 关键字就可构建对象；
    - 提供 unapply 方法使模式匹配可以工作；
    - 生成 toString、equals、hashCode 和 copy 方法，除非显示给出这些方法的定义。

## regex

- 通过 scala.util.matching 中的 Regex 类来支持正则表达式
- 用 String 类的 r() 方法构造一个 Regex 对象
- pattern.findFirstIn(str) - 查看首个匹配项
- findAllIn - 查看所有匹配项
- mkString - 连接 regex 匹配结果的字符串
- `(|)` 可以用来设置不同的模式：`val pattern = new Regex("(S|s)cala")`
- replaceAllIn, replaceAllIn - 替换首个/全部匹配项
- Scala 的 regex 继承了 Java 的语法规则
- Scala 的方法可以通过抛出异常的方法的方式来终止相关代码的运行，不必通过返回值。
- 格式：`throw new IllegalArgumentException`
- catch字句是按次序捕捉的，越具体的异常越要靠前。如果抛出的异常不在catch字句中，该异常则无法处理，会被升级到调用者处。
- 在Scala里，借用了模式匹配的思想来做异常的匹配，因此，在catch的代码里，是一系列case字句：
- finally 语句用于执行不管是正常处理还是异常发生时都需要执行的步骤

```scala
try {
         val f = new FileReader("input.txt")

} catch {
    case ex: FileNotFoundException => {
            println("Missing file exception")

             }
    case ex: IOException => {
            println("IO Exception")

             }

} finally {
         println("Exiting finally...")

}
```

## 提取器 (Extractor)

- 提取器是从传递给它的对象中提取出构造该对象的参数。(提取参数)
- Scala 提取器是一个带有unapply方法的对象。unapply方法算是apply方法的反向操作：unapply接受一个对象，然后从对象中提取值，提取的值通常是用来构造该对象的值。
- apply 方法，无需使用 new 操作就能创建对象
- 实例化一个类的时，可以带上 0 个或者多个的参数，编译器在实例化的时会调用 apply 方法。可以在类和对象中都定义 apply

## 文件 I/O

- Scala 进行文件写操作，直接用的都是 java中 的 I/O 类 （java.io.File)

```scala
import java.io._

object Test {
    def main(args: Array[String]) {
      val writer = new PrintWriter(new File("test.txt" ))

      writer.write("菜鸟教程")
      writer.close()

    }
}
```

### 从屏幕读取用户输入

- `val line = Console.readline`

### 从文件读取内容

- 使用 Source 类及伴生对象来读取文件

```scala
import scala.io.Source

object Test {
    def main(args: Array[String]) {
      println("文件内容为:" )

      Source.fromFile("test.txt" ).foreach{
         print
       }
    }
}
```
