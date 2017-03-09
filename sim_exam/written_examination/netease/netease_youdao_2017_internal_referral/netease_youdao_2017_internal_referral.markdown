# 网易有道 2017 内推试题

## Program

- 请将下列构造函数补充完整，使得程序的运行结果是5. `p=new int(x)`

```cpp
#include<iostream>
using namespace std;
class Sample{
    public:
        Sample(int x){
            ________
        }
        ~Sample(){  # 析构函数
            if(p) delete p;
        }
        int show(){
            return *p;
        }
    private:
        int*p;
};
int main(){
    Sample S(5);
    cout<<S.showe()<<ndl;
    return 0;
}
```

- 下列程序编译时会出现错误，请根据行号选择错误位置: `1, 2, 4, 5, 6`

```cpp
#include <iostream>
using namespace std;
class A{
  int a1;
protected:
  int a2;
public:
  int a3;
};
class B: public A{
  int b1;
protected:
  int b2;
public:
  int b3;
};
class C:private B{
  int c1;
protected:
  int c2;
public:
  int c3;
};
int main(){
  B obb;
  C obc;
  cout<<obb.a1;//1  a1 是 A 私有的
  cout<<obb.a2;//2  a2 是 A 开放给派生类使用的, 客户代码不能使用
  cout<<obb.a3;//3
  cout<<obc.b1;//4  C 是私有继承于 B, 不能使用 B 的成员
  cout<<obc.b2;//5  同上
  cout<<obc.b3;//6  同上
  cout<<obc.c3;//7
  return 0;
}
```

> private 属性不能够被继承。
使用private继承，父类的protected和public属性在子类中变为private；
使用protected继承，父类的protected和public属性在子类中变为protected；
使用public继承，父类中的protected和public属性不发生改变;
private, public, protected 访问标号的访问范围：
    private：只能由1.该类中的函数、2.其友元函数访问。不能被任何其他访问，该类的对象也不能访问。
    protected：可以被1.该类中的函数、2.子类的函数、以及3.其友元函数访问。但不能被该类的对象访问。
    public：可以被1.该类中的函数、2.子类的函数、3.其友元函数访问，也可以由4.该类的对象访问。
注：友元函数包括3种：设为友元的普通的非成员函数；设为友元的其他类的成员函数；设为友元类中的所有成员函数。

## Structure

- 大小为MAX的`循环队列`中，f为当前对头元素位置，r为当前队尾元素位置(最后一个元素的位置)，则任意时刻，队列中的元素个数为:
    - `(r - f + MAX + 1) % MAX
- 设某棵二叉树的中序遍历序列为BADC，前序遍历序列为ABCD，则后序遍历该二叉树得到序列为（）.
    - BDCA

![8](8.jpg)

- 在一个10阶的B-树上，每个树根结点中所含的关键字数目最多允许为( )个，最少允许为( )个。
    - 9, 4
    - 最多 `M - 1` 个, 最少 `M / 2 - 1` 向上取整

## Network

- 以下几条路由，10.1.193.0/24,10.1.194.0/24,10.1.196.0/24,10.1.198.0/24，如果进行路由汇聚，则能覆盖这几条路由地址的是（）
    - `10.1.192.0/21`

## Others

- 关于数据解析以下说法正确的是:
    - ~~XML数据结构有且只有一个根节点，并且不能嵌套~~, XML数据结构可以有多个根节点
    - ~~JSONObjetWithData:options:error:使用文件流~~, 使用缓冲区数据来解析
    - ~~writeJSONObject:toSteam:options:error:使用缓冲区数据解析json~~, 使用流来解析
    - XML解析分为两种:SAX解析和DOM解析
- 已知两个一维模式类别的类概率密度函数为:

![3](3.png)

- 先验概率P(1)=0.6,P(2)=0.4,则样本{x1=1.35,x2=1.45,x3=1.55,x4=1.65}各属于哪一类别?
    - X4 ∈ w2
    - X3 ∈ w1
    - X2 ∈ w1
    - X1 ∈ w1
- 关于解释系统的叙述中, 正确的是:
    - 解释程序不是直接执行，而是转换成机器可识别码之后才能执行
    - ~~使用解释系统时会区分编译阶段和运行阶段~~
    - ~~目标程序可以脱离其语言环境独立执行，使用比较方便、效率较高~~, 编译程序才能脱离语言环境独立执行
    - 一般来说，建立在编译基础上的系统在执行速度要优于建立在解释执行基础上的系统
- 一磁带机有9道磁道，带长700m，带速2m/s，每个数据块1k字节，块间间隔14mm。如果数据传输率为128000字节/秒,求记录位密度为（）字节/m.
    - 数据传输率（C）= 记录位密度（D） x   线速度( V )
    - D = C / V = 128000 / 2 = 64000
