# Scala Tutorials Tour

## Unified Types

![class hierarchy.](classhierarchy.img_assist_custom.png)

- `scala.Any` 是所有类的超类, 其两个直接子类是 `scala.AnyVal` 和 `scala.AnyRef`
- 数值类型, 引用类型
- 数值类型都是预定义的; 用户自定义的类默认是引用类型, 并且隐式拓展了 `scala.ScalaObject` 特质
- Classes from the infrastructure on which Scala do not extend scala.ScalaObject.

```scala
object UnifiedTypes extends App {
  val set = new scala.collection.mutable.LinkedHashSet[Any]
  set += "This is a string"  // add a string
  set += 732                 // add a number
  set += 'c'                 // add a character
  set += true                // add a boolean value
  set += main _              // add the main function
  val iter: Iterator[Any] = set.iterator
  while (iter.hasNext) {
    println(iter.next.toString())

  }

}
```

## Classes

- Scala 中, 类是静态模板. 圆括号内定义构造器参数
- `override` 关键字标记覆盖了预定义的内建方法
- 类通过 `new` 来实例化

## Traits

- 特质通过指定支持的方法的类型, 定义对象类型
- 特质可被部分实现, 即可以只为部分方法定义默认实现. (拓展了特质的类需要来实现为定义的方法)
- 与类不同的是, 特质没有构造参数

## Mixin Class Composition (混合类)

- Scala 允许在新的类定义中复用一个类的新成员定义
- `class Iter extends StringIterator(args(0)) with RichIterator` - StringIterator 是 `superclass`, RichIterator 被称为 `mixin`

```scala
object StringIteratorTest {

    abstract class AbsIterator {
        type T
        def hasNext: Boolean
        def next: T
    }

    trait RichIterator extends AbsIterator {
        def foreach(f: T => Unit) { while (hasNext) f(next)   }
    }

    class StringIterator(s: String) extends AbsIterator {
        type T = Char
        private var i = 0
        def hasNext = i < s.length()
        def next = { val ch = s charAt i; i += 1; ch   }
    }

    def main(args: Array[String]) {
    class Iter(s: String) extends StringIterator(s: String) with RichIterator
    val iter = new Iter("I am kissg.")
    iter foreach println
    }


}
```

## Anonymous Function Syntax

- `(参数列表) => {表达式}`
- 超轻量级的匿名函数写法举例:
    - Int => Int
    - (Int, Int) => String
    - () => String

## Higher-order Functions

- 高阶函数 - 以函数作为参数, 或返回函数作为结果
- `def apply(f: Int => String, v: Int) = f(v)`

## Nested Functions

- 举例, List 门限值过滤:

```scala
object FilterTest extends App {
  def filter(xs: List[Int], threshold: Int) = {

    def process(ys: List[Int]): List[Int] =
      if (ys.isEmpty) ys
      else if (ys.head < threshold) ys.head :: process(ys.tail)
      else process(ys.tail)

    process(xs)
  }

  println(filter(List(1, 9, 2, 8, 3, 7, 4), 5))

}
```

## Currying (柯里化)

- 举例:

```scala
/*
  以下代码偏应用了 modN 方法, 实际上只用了第一个参数.
  modN(2) 返回 Int => Boolean 的函数, 作为 filter 的第二个参数
*/

object CurryTest extends App {
  def filter(xs: List[Int], p: Int => Boolean): List[Int] =
    if (xs.isEmpty) xs
    else if (p(xs.head)) xs.head :: filter(xs.tail, p)
    else filter(xs.tail, p)

  def modN(n: Int)(x: Int) = ((x % n) == 0)
  val nums = List(1, 2, 3, 4, 5, 6, 7, 8)

  println(filter(nums, modN(2)))
  println(filter(nums, modN(3)))

}
```

- 柯里化后, 变量按定义的顺序传给函数, 即变量先传给第一个参数

## Case Classes

- 样本类是普通的类, 但是:
    - 默认不可变
    - 可分解应用于模式匹配
    - Compared by structural equality instead of by reference
    - 简洁的实例化与操作
- 实例化样本类不需要 `new` 关键字: `val emailFromJohn = Email("john.doe@mail.com", "Greetings From John!", "Hello World!")`
- 样本类的构造参数被作为公有值, 并直接访问
- 样本类, 不能直接修改字段. 正确的方法是: 使用 `copy` 方法创建一个副本, 然后替换字段: `val editedEmail = emailFromJohn.copy(title = "I am learning Scala!", body = "It's so cool!")`
- 对于每个样本类, Scala 编译器会产生一个 `equals` 方法, 实现了`结构相等` 和 `toString` 方法.
- 可以对样本类直接应用`模式匹配`

```scala
abstract class Notification
case class Email(sourceEmail: String, title: String, body: String) extends Notification
case class SMS(sourceNumber: String, message: String) extends Notification
case class VoiceRecording(contactName: String, link: String) extends Notification

def showNotification(notification: Notification): String = {
    notification match {
    case Email(email, title, _) =>
        "You got an email from " + email + " with title: " + title
    case SMS(number, message) =>
        "You got an SMS from " + number + "! Message: " + message
    case VoiceRecording(name, link) =>
        "you received a Voice Recording from " + name + "! Click the link to hear it: " + link

    }

}

val someSms = SMS("12345", "Are you there?")
val someVoiceRecording = VoiceRecording("Tom", "voicerecording.org/id/123")
println(showNotification(someSms))
println(showNotification(someVoiceRecording))
```

- 模式匹配可以匹配`值`, 也可以匹配`类型`
- 建议使用样本类来 model/group 数据, 使代码表达性更强, 可维护性越强:
    - 不可变的特性避免了应对变化的开销
    - 按值比较, 允许像原始数据一样比较实例
    - 模式匹配简化了分支逻辑, 更少的 bug, 更强的可读性
- Scala 会自动为样本类创建一个伴生对象, 包含了 `apply` 和 `unapply` 方法. 前者用来创建样本类的实例, 后者被伴生对象实现, 以使其成为提取器

## Pattern Matching

- 模式匹配可以匹配任意类型的数据, 采用 `first-match` 的机制
- 还可以对不同类型的数据进行模式匹配:

```scala
object MatchTest2 extends App {
    def matchTest(x: Any): Any = x match {
        case 1 => "one"
        case "two" => 2
        case y: Int => "scala.Int"
    }

    println(matchTest("two"))
}
```

- 通过样本类, Scala 的模式匹配对于代数类型的匹配尤其有用.
- Scala also allows the definition of patterns independently of case classes, using unapply methods in extractor objects.
- 解绑数据结构

## Singleton Objects

- 非类的函数与值, 都属于单例对象. 这些函数或值是全局的公有的
- 单例对象是定义一次性使用类的简便方法, 它不能被直接实例化
- 同 `val`, 单例对象可以被定义作为特质或类的成员, 尽管这是一个非典型用法
- 单例对象可以继承类和特质. 不带类型参数的样本类会默认创建一个同名单例对象, with a Function\* trait implemented.
- 当有类与单例对象同名, 它们互称: 伴生对象/伴生类. `必须定义在同一个源文件中`
- 类型类的实例常作为隐式值, 伴生成员被包括在相关值的默认隐式搜索中 (?)

## XML 处理

- XML 数据既可以通用数据表示, 也可以指定数据表示
- XML 数据以标签树表示
- 需要为 XML 文档定义 DTD (document type definition) 来处理 XML

## Regular Expression Patterns

## Extractor Objects

- 模式可以独立于样本类定义, 即模式 (`match` 关键字之前的) 可以是样本类, 也可以不是
- `unapply` 是 `apply` 的逆方法, 用于提取对象的构造参数
- 构造器从给定的参数列表创建一个对象, 而提取器从传递给它的对象中提取出构造该对象的参数
- 模式匹配时, 会调用 `unapply`; 对于模式匹配, `apply` 并不需要
- `unapply` 的返回类型应该是:
    - 如果只是用于测试, 返回 Boolean
    - 如果返回一个类型 T 的单值, 则返回 `Option[T]`
    - 如果返回多个值 T1, T2, ... Tn, 则返回一个 Tuple: `Option[(T1, T2, ..., Tn)]`
