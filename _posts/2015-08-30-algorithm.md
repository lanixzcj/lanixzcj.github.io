---
layout: post
title: "排序和查找算法总结"
modified: 2015-08-30 19:43:24 +0800
tags: [algorithm, sort, find]
image:
  feature: 
  credit: 
  creditlink: 
comments: false
share: false
---

## 基本概念

### 时间复杂度

<!--more-->

一个算法中的语句执行次数称为语句频度或时间频度，记为$T(n)$。若有某个辅助函数$f(n)$，使得当n趋近于无穷大时，$\frac{T(n)}{f(n)}$的极限值为不等于零的常数，则称$f(n)$是$T(n)$的同数量级函数。记作$T(n)=O(f(n))$,称$O(f(n))$为算法的渐进时间复杂度，简称时间复杂度。基本上$f(n)$为$T(n)$的最高阶项部分。

<!--more-->

### 空间复杂度

类似于时间复杂度，空间复杂度是对一个算法在运行过程中临时占用存储空间大小的量度，记做$S(n)=O(f(n))$。 

## 排序算法

TC：时间复杂度；SC：空间复杂度。

| 排序方式 |TC平均情况|TC最差情况|TC最好情况| SC | 稳定性 |
|:--------:|:--------:|:--------:|:--------:|:--:|:------:|
|插入排序  |$O(n\^2)$|$O(n\^2)$|$O(n)$|$O(1)$|稳定     | 
|希尔排序  |$O(n\^{1.3})$||$O(n\^s) \\\\1< s <2$|$O(1)$|不稳定     |
|冒泡排序  |$O(n\^2)$|$O(n\^2)$|$O(n)$|$O(1)$|稳定     |
|快速排序  |$O(n\log_{2}n)$|$O(n\^2)$|$O(n\log_{2}n)$|$O(\log_{2}n)$|不稳定     |
|选择排序  |$O(n\^2)$|$O(n\^2)$|$O(n\^2)$|$O(1)$|不稳定     |
|堆排序  |$O(n\log_{2}n)$|$O(n\log_{2}n)$|$O(n\log_{2}n)$|$O(1)$|不稳定     |
|归并排序  |$O(n\log_{2}n)$|$O(n\log_{2}n)$|$O(n\log_{2}n)$|$O(n)$|稳定     |
|基数排序  |$O(d(n+r))$|$O(d(n+r))$|$O(d(n+r))$|$O(r)$|稳定     |

### 插入排序

思想：

将一个记录插入到已排序好的有序表中，从而得到一个新，记录数增1的有序表。即：先将序列的第1个记录看成是一个有序的子序列，然后从第2个记录逐个进行插入，直至整个序列有序为止。

实现：

``` c++
void InsertSort(int a[], int n) {  
    for(int i = 1;i < n;i++){  
        int j = i - 1;   
        int x = a[i];        //复制为哨兵，即存储待排序元素  
        while(j >= 0 && x < a[j]){  //查找在有序表的插入位置  
            a[j + 1] = a[j];  
            j--;         //元素后移  
        }  
        a[j + 1] = x;      //插入到正确位置   
    }  
}  
```

### 希尔排序

思想：

一种分组插入排序,先将整个待排序的记录序列分割成为若干子序列分别进行直接插入排序，待整个序列中的记录“基本有序”时，再对全体记录进行依次直接插入排序。先将要排序的一组记录按某个增量d分成若干组子序列，每组中记录的下标相差d.对每组中全部元素进行直接插入排序，然后再用一个较小的增量（d/2）对它进行分组，在每组中再进行直接插入排序。继续不断缩小增量直至为1，最后使用直接插入排序完成排序。

### 冒泡排序

思想：

在要排序的一组数中，对当前还未排好序的范围内的全部数，自上而下对相邻的两个数依次进行比较和调整，即顺序错误则交换两个数。

实现：

``` c++
void bubbleSort(int a[], int n) {  
    for(int i = 0 ; i < n - 1; ++i) {  
        for(int j = 0; j < n-i-1; ++j) {  
            if(a[j] > a[j + 1]) {  
                int tmp = a[j]; 
                a[j] = a[j + 1];  
                a[j + 1] = tmp;  
            }  
        }  
    }  
}  
```

### 快速排序

思想：

1. 选择一个基准元素,通常选择第一个元素或者最后一个元素,
2. 通过一趟排序讲待排序的记录分割成独立的两部分，其中一部分记录的元素值均比基准元素值小。另一部分记录的 元素值比基准值大。
3. 此时基准元素在其排好序后的正确位置
4. 然后分别对这两部分记录用同样的方法继续进行排序，直到整个序列有序。

实现：

``` c++
void swap(int *a, int *b) {  
    int tmp = *a;  
    *a = *b;  
    *b = tmp;  
}  

int partition(int a[], int low, int high) {  
    int privotKey = a[low];                             //基准元素  
    while(low < high){                                   //从表的两端交替地向中间扫描  
        while(low < high  && a[high] >= privotKey) --high;  //从high 所指位置向前搜索，至多到low+1 位置。将比基准元素小的交换到低端  
        swap(&a[low], &a[high]);  
        while(low < high  && a[low] <= privotKey ) ++low;  
        swap(&a[low], &a[high]);  
    }  
      
    return low;  
}  

void quickSort(int a[], int low, int high) {  
    if(low < high){  
        int privotLoc = partition(a,  low,  high);  //将表一分为二  
        quickSort(a,  low,  privotLoc -1);          //递归对低子表递归排序  
        quickSort(a,   privotLoc + 1, high);        //递归对高子表递归排序  
    }  
} 
```

### 选择排序

思想：

在要排序的一组数中，选出最小（或者最大）的一个数与第1个位置的数交换；然后在剩下的数当中再找最小（或者最大）的与第2个位置的数交换，依次类推，直到第n-1个元素（倒数第二个数）和第n个元素（最后一个数）比较为止。

实现：

``` c++
void selectSort(int a[], int n) {  
    int min, tmp;  
    for(int i = 0; i< n; ++i) {
        min = i;  
        for(int j = i + 1 ;j < n;++j) {  
            if(a[min] > a[j]) min = j;  
        }  
 
        tmp = a[i];  a[i] = a[min]; a[min] = tmp; //最小元素与第i位置元素互换   
    }  
}
```

### 堆排序

思想：

利用完全二叉树中双亲节点和孩子节点之间的内在关系，在当前无序区中选择关键字最大(或者最小)的记录。初始时把要排序的n个数的序列看作是一棵顺序存储的二叉树（一维数组存储二叉树），调整它们的存储序，使之成为一个堆，将堆顶元素输出，得到n 个元素中最小(或最大)的元素，这时堆的根节点的数最小（或者最大）。然后对前面(n-1)个元素重新调整使之成为堆，输出堆顶元素，得到n 个元素中次小(或次大)的元素。

1. 将n 个待排序的数建成堆；
2. 输出堆顶元素后，调整剩余n-1 个元素，使其成为一个新堆。

实现：

``` c++
/** 
 * 已知H[s…m]除了H[s] 外均满足堆的定义 
 * 调整H[s],使其成为大顶堆.即将对第s个结点为根的子树筛选,  
 * 
 * @param H是待调整的堆数组 
 * @param s是待调整的数组元素的位置 
 * @param length是数组的长度 
 * 
 */  
void HeapAdjust(int H[],int s, int length) {  
    int tmp  = H[s];  
    int child = 2*s+1; //左孩子结点的位置。(i+1 为当前调整结点的右孩子结点的位置)  
    while (child < length) {  
        if(child+1 <length && H[child]<H[child+1]) { // 如果右孩子大于左孩子(找到比当前待调整结点大的孩子结点)  
            ++child ;  
        }  
        if(H[s]<H[child]) {  // 如果较大的子结点大于父结点  
            H[s] = H[child]; // 那么把较大的子结点往上移动，替换它的父结点  
            s = child;       // 重新设置s ,即待调整的下一个结点的位置  
            child = 2*s+1;  
        }  else {            // 如果当前待调整结点大于它的左右孩子，则不需要调整，直接退出  
             break;  
        }  
        H[s] = tmp;         // 当前待调整的结点放到比其大的孩子结点位置上  
    }  
}  
  
  
/** 
 * 初始堆进行调整 
 * 将H[0..length-1]建成堆 
 * 调整完之后第一个元素是序列的最小的元素 
 */  
void BuildingHeap(int H[], int length) {   
    //最后一个有孩子的节点的位置 i=  (length -1) / 2  
    for (int i = (length -1) / 2 ; i >= 0; --i)  
        HeapAdjust(H,i,length);  
}  
/** 
 * 堆排序算法 
 */  
void HeapSort(int H[],int length) {  
    //初始堆  
    BuildingHeap(H, length);  
    //从最后一个元素开始对序列进行调整  
    for (int i = length - 1; i > 0; --i) {  
        //交换堆顶元素H[0]和堆中最后一个元素  
        int temp = H[i]; H[i] = H[0]; H[0] = temp;  
        //每次交换堆顶元素和堆中最后一个元素之后，都要对堆进行调整  
        HeapAdjust(H,0,i);  
    }  
}  
```

### 归并排序

思想：

归并排序法是将两个（或两个以上）有序表合并成一个新的有序表，即把待排序序列分为若干个子序列，每个子序列是有序的。然后再把有序子序列合并为整体有序序列。

实现：

``` c++
void Merge(int sourceArr[],int tempArr[],int startIndex,int midIndex,int endIndex) {
    int i = startIndex,j=midIndex+1,k = startIndex;
    while(i!=midIndex+1 && j!=endIndex+1) {
        if(sourceArr[i]<sourceArr[j])
            tempArr[k++] = sourceArr[i++];
        else
            tempArr[k++] = sourceArr[j++];
    }
    while(i!=midIndex+1)
        tempArr[k++] = sourceArr[i++];
    while(j!=endIndex+1)
        tempArr[k++] = sourceArr[j++];
    for(i=startIndex;i<=endIndex;i++)
        sourceArr[i] = tempArr[i];
}
 
//内部使用递归
void MergeSort(int sourceArr[],int tempArr[],int startIndex,int endIndex) {
    int midIndex;
    if(startIndex<endIndex) {
        midIndex=(startIndex+endIndex)/2;
        MergeSort(sourceArr,tempArr,startIndex,midIndex);
        MergeSort(sourceArr,tempArr,midIndex+1,endIndex);
        Merge(sourceArr,tempArr,startIndex,midIndex,endIndex);
    }
}
```

### 基数排序

思想：

最高位优先(Most Significant Digit first)法，简称MSD法：先按k1排序分组，同一组中记录，关键码k1相等，再对各组按k2排序分成子组，之后，对后面的关键码继续这样的排序分组，直到按最次位关键码kd对各子组排序后。再将各组连接起来，便得到一个有序序列。

最低位优先(Least Significant Digit first)法，简称LSD法：先从kd开始排序，再对kd-1进行排序，依次重复，直到对k1排序后便得到一个有序序列。

LSD的过程就是先按最低位分组再重新串连起来，再按倒数第二位分组，直到最高位分组完毕并串连。

实现：

``` c++
int maxbit(int data[], int n) {//辅助函数，求数据的最大位数
    int d = 1; //保存最大的位数
    int p = 10;
    for(int i = 0; i < n; ++i) {
        while(data[i] >= p) {
            p *= 10;
            ++d;
        }
    }
    return d;
}
void radixsort(int data[], int n) { //基数排序
    int d = maxbit(data, n);
    int *tmp = new int[n];
    int *count = new int[10]; //计数器
    int i, j, k;
    int radix = 1;
    for(i = 1; i <= d; i++) {//进行d次排序
        for(j = 0; j < 10; j++)
            count[j] = 0; //每次分配前清空计数器
        for(j = 0; j < n; j++) {
            k = (data[j] / radix) % 10; //统计每个桶中的记录数
            count[k]++;
        }
        for(j = 1; j < 10; j++)
            count[j] = count[j - 1] + count[j]; //将tmp中的位置依次分配给每个桶
        for(j = n - 1; j >= 0; j--) {//将所有桶中记录依次收集到tmp中
            k = (data[j] / radix) % 10;
            tmp[count[k] - 1] = data[j];
            count[k]--;
        }
        for(j = 0; j < n; j++) //将临时数组的内容复制到data中
            data[j] = tmp[j];
        radix = radix * 10;
    }
    delete[]tmp;
    delete[]count;
}
```

### 使用策略

影响排序的因素有很多，平均时间复杂度低的算法并不一定就是最优的。相反，有时平均时间复杂度高的算法可能更适合某些特殊情况。同时，选择算法时还得考虑它的可读性，以利于软件的维护。一般而言，需要考虑的因素有以下四点：

* 待排序的记录数目n的大小；
* 记录本身数据量的大小，也就是记录中除关键字外的其他信息量的大小；
* 关键字的结构及其分布情况；
* 对排序稳定性的要求。

设待排序元素的个数为n。

1. 当n较大，则应采用时间复杂度为$O(n\log_{2}n)$的排序方法：快速排序、堆排序或归并排序序：
    * 快速排序：是目前基于比较的内部排序中被认为是最好的方法，当待排序的关键字是随机分布时，快速排序的平均时间最短；
    * 堆排序：如果内存空间允许且要求稳定性的；
    * 归并排序：它有一定数量的数据移动，所以我们可能过与插入排序组合，先获得一定长度的序列，然后再合并，在效率上将有所提高。
2. 当n较大，内存空间允许，且要求稳定性：归并排序。
3. 当n较小，可采用直接插入或直接选择排序：
    * 直接插入排序：当元素分布有序，直接插入排序将大大减少比较次数和移动记录的次数；
    * 直接选择排序：元素分布有序，如果不要求稳定性，选择直接选择排序
4. 一般不使用或不直接使用传统的冒泡排序。
5. 基数排序，它是一种稳定的排序算法，但有一定的局限性：
    * 关键字可分解；
    * 记录的关键字位数较少，如果密集更好；
    * 如果是数字时，最好是无符号的，否则将增加相应的映射复杂度，可先将其正负分开排序。

## 查找算法

| 查找方式 | 时间复杂度 |
|:--------:|:----------:|
|顺序查找  |$O(n)$      |
|二分查找  |$O(\log_{2}n)$|
|分块查找  ||$O(n\^2)$  |
|哈希查找  |$O(1)$      |
|B树查找   |$O(\log_{2}n)$|

### 顺序查找

思想：

按顺序比较每个元素，直到找到关键字为止。

### 二分查找

思想：

待查找记录序列为有序序列。查找过程从数组的中间元素开始，如果中间元素正好是要查找的元素，则搜素过程结束；如果某一特定元素大于或者小于中间元素，则在数组大于或小于中间元素的那一半中查找，而且跟开始一样从中间元素开始比较。

实现：

``` c++
int halfSearch(int a[], int n, int key) {
    int left = 0;
    int right = n - 1;
    int mid;
    
    while (left <= right) {
        mid = (left + right) / 2;
        if (key == a[mid]) {
            return mid;
        } else if (key < a[mid]) {
            right = mid - 1;
        } else {
            left = mid + 1;
        }
    } 
    
    return -1;
} 
```

### 分块查找

思想：

将n个数据元素"按块有序"划分为m块（m ≤ n）。每一块中的结点不必有序，但块与块之间必须"按块有序"；即第1块中任一元素的关键字都必须小于第2块中任一元素的关键字；而第2块中任一元素又都必须小于第3块中的任一元素，以此类推。然后使用二分查找及顺序查找。

### 哈希查找

思想：

先创建哈希表(散列表)，根据键值方式(Key value)进行查找，通过散列函数，定位数据元素。

### B树查找

思想：

先创建二叉排序树：

1. 若它的左子树不空，则左子树上所有结点的值均小于它的根结点的值；
2. 若它的右子树不空，则右子树上所有结点的值均大于它的根结点的值；
3. 它的左、右子树也分别为二叉排序树。

在二叉查找树b中查找x的过程为：

1. 若b是空树，则搜索失败，否则：
2. 若x等于b的根节点的数据域之值，则查找成功；否则：
3. 若x小于b的根节点的数据域之值，则搜索左子树；否则：
4. 查找右子树。

