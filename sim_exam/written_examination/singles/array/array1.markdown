# 数组1

- 下列数组定义及赋值正确的是:
    - ~~int intArray[];~~, `array size missing`
    - intArray=new int[3]; intArray[1]=1; intArray[2]=2; `赋值`
    - int a[]={1, 2, 3, 4, 5};
    - int a[][]=new int[2][]; a[0]=new int[3]; a[1]=new int[3];
- 假设以行优先顺序存储三维数组A[5][6][7],其中元素A[0][0][0]的地址为1100，且每个元素占2个存储单元，则A[4][3][2]的地址是(
)
    - `1380`
    - 数组下标从 `0` 开始啊, A[4] 表示最高维前面已经过去了 0123
- A为整数数组， N为A的数组长度，请问执行以下代码，最坏情况下的时间复杂度为 `O(N^2)`, `以下代码就是`冒泡排序`

```c
void fun(int A[], int n) {                                                                       
    for (int i = n - 1; i >= 1; i--) {                                                          
        for (int j = 0; j < i; j++) {                                                            
            if (A[j] > A[j+1]) {                                                                
                int tmp = A[j + 1];                                                              
                A[j + 1] = A[j];
                A[j] = tmp;
         }
      }
   }
}
```

- 给定一个m行n列的整数矩阵（如图），每行从左到右和每列从上到下都是有序的。判断一个整数k是否在矩阵中出现的最优算法，在最坏情况下的时间复杂度是 `O(m + n)`, 前 m 次确定行, 后 n 次在行中搜索就 OK 了啊

![1_8.jpg](1_8.jpg)

```c
#define NUMA 10000000
#define NUMB 1000
int a[NUMA], b[NUMB];

void pa()
{
    int i, j;
    for(i = 0; i < NUMB; ++i)
        for(j = 0; j < NUMA; ++j)
            ++a[j];
}
void pb()
{
    int i, j;
    for(i = 0; i < NUMA; ++i)
        for(j = 0; j < NUMB; ++j)
            ++b[j];
}
```

- 上述代码, `pb 比 pa 快`, 数组 a 比数组 b 大很多，可能跨更多的页，缺页率高或者缓存命中更低，所以pb快.
    - 一般情况下，把大的循环放在里面，效率会比较高
    - 但是当如此题一样，涉及不同的内存存取时，把大的循环放在外面可以增大缓存命中率，大幅提高效率。
- 设有字母序列{Q,D,F,X,A,P,N,B,Y,M,C,W}，请写出按二路归并方法对该序列进行一趟扫描后的结果为 `DQFXAPBNMYCW`
    - 这`二路归并排序`似乎是两个两个取, 比较排序
