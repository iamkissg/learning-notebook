# 京东2016实习生招聘笔试研发类模拟练习

# C/C++

```c
#include<stdio.h>
#include<stdlib.h>
void main()
{
　　int a = -3;
　　unsigned int b = 2;
　　long c = a + b;
　　printf("%ld\n",c);
```

- 上述 C 程序执行后, c 的输出结果是:
    - `-1`
    - `4294967295`
    - `0xFFFFFFFF`

> `无符号和有符号整数进行运算时，有符号整数会被提升为无符号整数。`
-3对应的二进制表示是0xfffffffd，和2相加表示0xffffffff。
输出结果取决于long是32位，还是64位。这个取决于编译器和机器。
long是有符号的整型。
如果是32位，0xfffffff在补码表示法（最高位是负数位）下是等于-1.
如果是64位，0xfffffff是属于long的正整数范围（负数位在第64位），等于4294967295.

## Java

```java

public class Demo{
　　float func0()
　　{
　　　　byte i=1;
　　　　return i;
　　}
　　float func1()
　　{
　　　　int i=1;
　　　　return;  // 没有返回值, 出错
　　}
　　float func2()
　　{
　　　　short i=2;
　　　　return i;
　　}
　　float func3()
　　{
　　　　long i=3;
　　　　return i;
　　}
　　float func4()
　　{
　　　　double i=4;  // 大转小, 出错
　　　　return i;
　　}
}
```

- Java 类 Demo 的方法哪些不合法:
    - `func1`
    - `func4`

> 自动转换按`从低到高`的顺序转换。不同类型数据间的优先关系如下：
低 -----------------------------------------> 高
byte,short,char-> int -> long -> float -> double

> 强制数据类型转换
强制转换的格式是在需要转型的数据前加上 “( )” ，然后在括号内加入需要转化的数据类型。有的数据经过转型运算后，精度会丢失，而有的会更加精确

```java
public class Demo{
　public static void main(String args[]){
　　　int num = 10;
　　　System.out.println(test(num));
}
public static int test(int b){
　　　try
　　　{
　　　　b += 10;
　　　　return b;
　　　}
　　　catch(RuntimeException e)
　　　{
　　　}
　　　catch(Exception e2)
　　　{
　　　}
　　　finally
　　　{
　　　　b += 10;
　　　　return b;
　　　}
　　}
}
```

- 执行上述代码, 输出为 `30`

> `return语句并不是函数的最终出口，如果有finally语句，这在return之后还会执行finally`（return的值会暂存在栈里面，等待finally执行后再返回）

> finally里面不建议放return语句，根据需要，return语句可以放在try和catch里面和函数的最后。可行的做法有四：
（1）return语句只在函数最后出现一次。
（2）return语句仅在try和catch里面都出现。
（3）return语句仅在try和函数的最后都出现。
（4）return语句仅在catch和函数的最后都出现。
注意，除此之外的其他做法都是不可行的，编译器会报错

## Front End

```html
<html>
<head>
　<script type="text/javascript">
　　function writeIt (value) { document.myfm.first_text.value=value;}
　</script>
</head>
<body bgcolor="#ffffff">
　<form name="myfm">
　　<input type="text" name="first_text">
　　<input type="text" name="second_text" onchange="writeIt(value)">
　</form>
</body>
</html>
```

- 以下分析以下代码说法正确的是:
    - ~~在页面的第二个文本框中输入内容后，当鼠标离开第二个文本框时，第一个文本框的内容不变~~
    - ~~在页面的第一个文本框中输入内容后，当鼠标离开第一个文本框时，将在第二个文本框中复制第一个文本框的内容~~
    - `在页面的第二个文本框中输入内容后，当鼠标离开第二个文本框时，将在第一个文本框中复制第二个文本框的内容`
    - `在页面的第一个文本框中输入内容后，当鼠标离开第一个文本框时，第二个文本框的内容不变`
    - `onchange` 是失去焦点且内容改变才会执行函数
    - `onblur` 只要失去焦点 就会执行函数

## Network

- 假设信道长度为1200km，其往返时间为20ms，分组长度为1200bit，发送速率为1Mb/s。若忽略处理时间和发送确认分组时间，则该信道的利用率为( )
    - `0.0566`

> 1200bit的长度，发送速度为1mb/s，则需要1.2ms
往返时间20ms，则发送一组共需要(20+1.2)ms
利用率=1.2/21.2=0.0566

## Others

```
NSTimer *myTimer = [NSTimer timerWithTimeInterval:1.0 target:self selector:@selector(doSomeThing:) userInfo:nil repeats:YES];
[myTimer fire]
```

- 对上述代码描述正确的是:
    - `没有将timer加入runloop`
    - ~~doSomeThing缺少参数~~
    - ~~忘记传递数据给userInfo~~
    - ~~myTimer对象未通过[[myTimer alloc] init]方法初始化~~

- 两个浮点向量Xi和Yi(i=1,2,…n),相加后的结果为Zi。设浮点加法运算分4段(对阶、 尾加、规格化、舍入)完成。分别计算当 n=100,m=4(段数),N=20（处理单元数）时，t=1us（每段时间）时，串行、流水和向量运算所需的时间分别是( )
    - `400us, 103us, 20us`

> T串 = m * n * t = 4 * 100 * 1 = 400 us
T流水 = (m + n - 1) * t = (4 + 100 - 1) * 1 = 103 us
T向量 = m * t * [n / N] = 4 * 1 * [100 / 20] = 20 us

- 两个浮点向量Xi和Yi(i=1,2,…n),相加后的结果为Zi。设浮点加法运算分4段(对阶、 尾加、规格化、舍入)完成。分别计算当 n=100,m=4(段数),N=20（处理单元数）时，t=1us（每段时间）时，串行、流水和向量运算所需的时间分别是( )
    - `136`

> 简单粗暴解法：就是从11个数里面选3个，有11 * 10 * 9 / 6 = 165，再看答案就可以了
