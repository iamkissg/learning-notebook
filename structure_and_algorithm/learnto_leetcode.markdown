#### Power of two

(学习自 [CSDN 博客](http://blog.csdn.net/x_i_y_u_e/article/details/50507281)

- $2^n$: 首位是 1, 其余全为 0; $2^n - 1$: 比 $2^n$ 少一位, 每位上都是 1.
- 因此 若 n 为 2 的幂, 则$2^n & (2^n - 1) == 0$

```c
bool isPowerOfTwo(int n){
    return n > 0 ? (n & (n - 1)) == 0 : 0;
}
```

#### Power of Three

- 数学方法(低效)

```c
#include <math.h>

bool isPowerOfThree(int n){
    double logAns = log10(n) / log10(3);
    return (logAns - (int)(logAns) == 0) ? true : false;
}
```

- 若 $n$ 是 3 的幂, 则其所有约数也都是 3 的幂. 因此, 3 的幂一定是能取到的最大的 3 的幂的约数. 一般, C 语言 int 的最大值是 $2^31 - 1 = 2147483647$, 能取到的最大的 3 的幂是 1162261467.

```c
bool isPowerOfThree(int n){
    return n > 0 ? !(1162261467 % n) : 0;
}
```

#### Power of four

(学习自 [CSDN 博客](http://blog.csdn.net/x_i_y_u_e/article/details/50507281)

- 4 的幂首先是 2 的幂, 且二进制表示时, 后面跟随偶数个零, 即 4 的幂唯一的 1 在奇数位上
- 因此, 先判断数是否 2 的幂, 再判断 1 是否在奇数位上, 位与上 `0x55555555` (最大的奇数位上全为 1 的 int)

```c
bool isPowerOfFour(int num){

    return (num & (num - 1)) == 0 && (num & 0x55555555) != 0;
}
```

#### Number of 1 Bits

- 位移法, 不管多少个 1, 都循环 31 次

```c
int hammingWeight(uint32_t n) {
    char sum = 0;
    char i = 0;
    for (; i < 32; i++){
        sum += (n >> i) & 1;
    }
    return sum;
}
```

(学习自 [CSDN](http://blog.csdn.net/zzc8265020/article/details/46524199)

- $n - 1$ 之后, 最低位的 1 变为 0, 其后所有 0 变成 1.
- 因此, $n$ 位与上 $n - 1$, $n$ 最低位的 1 被消除. 1 不多的时候, 递减速度特别快. 1 多的时候, 效果一般.

```c
int hammingWeight(uint32_t n){
    char count = 0;
    while(n){
        n = n & (n - 1);
        count++;
    }
    return count;
}
```

#### Reverse String

- 如果 `strrev()` 函数可以使用, 可以简单地:

```c
#include <string.h>

char* reverseString(char* s){
    return strrev(s);
}
```

- 但是 Linux 下, `<string.h>` 不包括 `strrev()` 函数, 替代的方法是:

```c
#include <string.h>
char *strrev(char *str){
    char *p1, *p2;

    if (! str || ! *str)
        return str;
    for (p1 = str, p2 = str + strlen(str) - 1; p2 > p1; ++p1, --p2){
        *p1 ^= *p2;  // 采用异或, 就不需要借助第三个变量了
        *p2 ^= *p1;
        *p1 ^= *p2;
    }
    return str;
}
```

[CSDN 博客](http://blog.csdn.net/turingo/article/details/8124432) 提供的不使用 `strlen` 的思路 (效率更高):

```c
char* reverseString(char *s){
    char* h = s;
    char* t = s;
    char ch;

    while(*t++){};
    t--;
    t--;

    while(h<t){
        ch = *h;
        *h++ = *t;
        *t-- = ch;
    }
    return s;
}
```
