---
layout: post
title: 线性代数学习笔记
description: "线性代数学习笔记"
tags: [math]
modified:   2017-11-19 14:37:14 +0800
share: false
comments: false
image:
  
---

对MIT的线性代数课程的学习与总结。

<!--more-->

## 零.线代名词

| 英文 | 中文     |
| :------------- | :------------- |
| linear combinations       | 线性组合      |
| linear equations   | 线性方程组   |
| coefficient matrix   | 系数矩阵   |
| plane   | 平面   |
| identity matrix  | 单位矩阵   |
| row echelon matrix   | 行阶梯矩阵   |
| upper triangular system   | 上三角矩阵  |
| Gauss elimination   | 高斯消元法   |
| augmented matrix   | 增广矩阵   |
| back substritution   | 回代   |
| elementary matrix    | 初等矩阵   |
| permutation   | 置换  |
| transpose   | 转置   |
| pivot variables   | 主变量  |
| free variables   | 自由变量   |
| inverse   | 逆   |
| singular   | 奇异   |
| symmetric   | 对称   |
| independence   | 线性相关性   |


## 一.方程组几何解释

### （一）对线性方程组的理解

方程组可以通过表示为矩阵形式

比如，对于方程组(为了便于取图，使用了书上的例子)：

$$\left\{
\begin{array}{l}
x-2y=1 \\
3x+2y=11
\end{array}
\right.
$$

可以通过$Ax=b$来表示：

$$\begin{bmatrix}
1 & -2\\
3 & 2
\end{bmatrix}
\begin{bmatrix}
x\\
y
\end{bmatrix}=
\begin{bmatrix}
1\\
11
\end{bmatrix}
$$

其中$A$为系数矩阵，$x$为未知数向量，$b$为右侧向量

#### 1.行图像

这是我们所熟悉的理解方式：每个方程表示为一个图像

![行图像](http://7xl20x.com1.z0.glb.clouddn.com/2.1%E8%A1%8C%E5%9B%BE%E5%83%8F.png)

交点$(3,1)$是方程的解

#### 2.列图像

把方程组放在一起考虑，关注系数矩阵的列向量

$$x\begin{bmatrix}
1 \\
3
\end{bmatrix}
+y\begin{bmatrix}
-2\\
2
\end{bmatrix}=
\begin{bmatrix}
1\\
11
\end{bmatrix}
$$

找到正确的列向量线性组合（x,y的值），结果为右侧向量，就可以得到解了

![列图像](http://7xl20x.com1.z0.glb.clouddn.com/2.2%E5%88%97%E5%9B%BE%E5%83%8F.png)

通过右侧向量，可以分别获得列向量的倍数，得到方程的解$(3,1)$


把思维扩展到3维度甚至更高，也是有相同的理解方式。三维的行图像就是平面的交点，不过更高维度的行图像就难以理解想象了，这可以体现出列向量的思想更便于理解。

### （二）矩阵与向量相乘的方法

以二阶矩阵并右乘向量$Ax=b$为例
$$\begin{bmatrix}
2 & 5 \\
1 & 3
\end{bmatrix}
\begin{bmatrix}
x_1\\
x_2
\end{bmatrix}=
\begin{bmatrix}
12\\
7
\end{bmatrix}
$$
$$x=\begin{bmatrix}
1\\
2
\end{bmatrix}$$


1. 点乘的方式。也就是最为熟知与常用的每一行与向量的点乘，得到结果

$$Ax=\begin{bmatrix}
(row1)\cdot x \\
(row2)\cdot x
\end{bmatrix}=
\begin{bmatrix}
2\times1+5\times2 \\
1\times1+3\times2
\end{bmatrix}
$$

2. 更为推荐的方式，结果是各个列向量的线性组合，同理如果是左乘行向量则为各个行向量的线性组合

$$Ax=x_1(column1)+x_2(column2)=
1\begin{bmatrix}
2\\
1
\end{bmatrix}+
2\begin{bmatrix}
5\\
3
\end{bmatrix}
$$

## 二. 矩阵消元（elimination）

### （一）消元过程

消元法：通过矩阵变换(把主元下方的元素消为0)把左侧系数矩阵$A$消元为上三角矩阵$U$，变换过程中在$A$中加入$b$列向量，构成增广矩阵，目的是使$b$随着$A$变换而变换。最后进行回代得到方程的解，也就是先求出最下面行未知数的解，逐行的代入上一行求得所有未知数的解。

以下方方程组为例，描述高斯消元的过程

$$\left\{
\begin{array}{l}
x+2y+z=2 \\
3x+8y+z=12 \\
4y+z=2
\end{array}
\right.
$$

1.构成增广矩阵

$$\left[
\begin{array}{ccc|c}
1 & 2 & 1 & 2\\
3 & 8 & 1 & 12 \\
0 & 4 & 1 & 2
\end{array}
\right]
$$

2.利用第一个主元$1$，把下方元素消为0，即$row2=row2 - 3\times row3$

$$\Rightarrow\left[
\begin{array}{ccc|c}
1 & 2 & 1 & 2\\
0 & 2 & -2 & 6 \\
0 & 4 & 1 & 2
\end{array}
\right]
$$

3.同理继续做相同的处理，直到最后一个主元。当主元位置为0时，通过行交换，将主元位置变为非0

$$\Rightarrow\left[
\begin{array}{ccc|c}
1 & 2 & 1 & 2\\
0 & 2 & -2 & 6 \\
0 & 0 & 5 & -10
\end{array}
\right]
$$

4.回代求解

$$\left\{
\begin{array}{l}
x+2y+z=2 \\
2y-2z=6 \\
5z=-10
\end{array}
\right.
\Rightarrow
\left\{
\begin{array}{l}
x=2 \\
y=1 \\
z=-2
\end{array}
\right.
$$

### （二）引入消元矩阵

像上一节提到的，更好的理解矩阵乘法（矩阵乘向量）的方式应该为矩阵的行向量或者列向量的线性组合。扩展到矩阵乘矩阵也是同理的，比如

$$\begin{bmatrix}
1 & 2 & 7 \\
1 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
1 & 2 & 1\\
3 & 8 & 1\\
0 & 4 & 1
\end{bmatrix}
=\begin{bmatrix}
1\times[1~2~1]+
2\times[3~8~1]+
7\times[0~4~1] \\
1\times[1~2~1]+
0\times[3~8~1]+
1\times[0~4~1]
\end{bmatrix}
$$

这样上述的消元过程就可以通过左乘一些消元矩阵（初等矩阵）来进行消元过程，消元过程中应该始终用线性组合的方式进行思考

1.$E_{21}A$
$$
\begin{bmatrix}
1 & 0 & 0\\
-3 & 1 & 0 \\
0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
1 & 2 & 1\\
3 & 8 & 1 \\
0 & 4 & 1
\end{bmatrix}
=\begin{bmatrix}
1 & 2 & 1\\
0 & 2 & -2 \\
0 & 4 & 1
\end{bmatrix}
$$

2.$E_{32}(E_{21}A)=U$
$$
\begin{bmatrix}
1 & 0 & 0\\
0 & 1 & 0 \\
0 & -2 & 1
\end{bmatrix}
\begin{bmatrix}
1 & 2 & 1\\
0 & 2 & -2 \\
0 & 4 & 1
\end{bmatrix}
=\begin{bmatrix}
1 & 2 & 1\\
0 & 2 & -2 \\
0 & 0 & 5
\end{bmatrix}
$$

### （三）矩阵置换

消元过程中可能会出现主元位置为0的情况，这样就需要从下方的行找到非0元素进行行置换，依然利用行向量的线性组合来理解矩阵相乘可以轻松的写出置换矩阵

$$
\begin{bmatrix}
0 & 1\\
1 & 0
\end{bmatrix}
\begin{bmatrix}
a & b\\
c & d
\end{bmatrix}
=\begin{bmatrix}
c & d\\
a & b
\end{bmatrix}
$$

当然如果想置换列的话就右乘置换矩阵

## 三.矩阵乘法与逆

### （一）矩阵乘法

$A(m\times n)\cdot B(n\times p)=C(m\times p)$

#### 1.常规的行列点乘法

$$c_{ij}=A_{row_i}\cdot B_{column_j}=\sum_{k=1}^{n}a_{ik}b_{kj}$$

#### 2.列方法，考虑A的列向量的线性组合

直接求出整列

$$c_{j}=A\cdot B_{column_j}=\sum_{k=1}^{n}b_{kj}A_{column_k}$$

#### 3.行方法，考虑B的行向量的线性组合

直接求出整行

$$c_{i}=A_{row_i}\cdot B=\sum_{k=1}^{n}a_{ik}B_{row_k}$$

#### 4.A各列与B相应的行乘积之和

多个$m\times 1$和$1 \times p$向量相乘之和

$$C=\sum_{k=1}^{n}A_{column_k}B_{row_k}$$

#### 5.分块乘法

可以通过分块简化计算,因为KaTex还没有支持`\hline`，这里通过图片举例

![](http://7xl20x.com1.z0.glb.clouddn.com/2.3block-multiplication.png)

### （二）逆矩阵

#### 1.定义

> 如果矩阵$A$是可逆的，则存在$A^{-1}$，使
> $$A^{-1}A=I ~ and ~AA{-1}=I$$

方阵的左逆是等于右逆的

#### 2.不可逆矩阵，奇异矩阵

教授在这里提到了几种不可逆矩阵的情况，而非完整的逆矩阵判断方法

$$A=\begin{bmatrix}
1 & 3\\
2 & 6
\end{bmatrix}$$

1. 按照列向量线性组合的去思考，如果$A$可逆，使$AA{-1}=I$，则$A$的列向量线性组合应该存在$\begin{bmatrix}1\\0\end{bmatrix}$和$\begin{bmatrix}0\\1\end{bmatrix}$，可见$A$不可逆
2. 如果可以找到非0向量x，使$Ax=0$成立，即$A$的列向量线性组合可以得到$0$向量。若$A$可逆，则存在$A^{-1}Ax=0\Rightarrow Ix=0\Rightarrow x=0$，可见$A$不可逆

#### 3.求逆矩阵

这里求逆矩阵的方法与本科所学的一致，思想上可以把求逆理解为求方程组

$$AA^{-1}=\begin{bmatrix}
1 & 3\\
2 & 7
\end{bmatrix}
\begin{bmatrix}
a & c\\
b & d
\end{bmatrix}=
\begin{bmatrix}
1 & 0\\
0 & 1
\end{bmatrix}$$

理解为求两个方程组

$$\begin{bmatrix}
1 & 3\\
2 & 7
\end{bmatrix}
\begin{bmatrix}
a\\
b
\end{bmatrix}=
\begin{bmatrix}
1\\
0
\end{bmatrix}$$
$$\begin{bmatrix}
1 & 3\\
2 & 7
\end{bmatrix}
\begin{bmatrix}
c\\
d
\end{bmatrix}=
\begin{bmatrix}
0\\
1
\end{bmatrix}$$

高斯-若尔当消元可以同时处理多个左侧相同的方程组，把右侧向量同时放入构成增广矩阵即可

1. 构成增广矩阵

$$\begin{bmatrix}
A & I
\end{bmatrix}=\left[
\begin{array}{ll|ll}
1 & 2 & 1 & 0\\
3 & 7 & 0 & 1
\end{array}
\right]
$$

2. 进行消元

$$\Rightarrow \left[
\begin{array}{ll|ll}
1 & 2 & 1 & 0\\
0 & 1 & -3 & 1
\end{array}
\right]
$$

3. 进一步消元，并根据解得到了$A^{-1}$

$$\Rightarrow \left[
\begin{array}{cc|cc}
1 & 0 & 7 & -2\\
0 & 1 & -3 & 1
\end{array}
\right]=\begin{bmatrix}
I & A^{-1}
\end{bmatrix}
$$

直观的计算方法为：加入单位矩阵构成增广矩阵，进行消元操作直到左侧为单位矩阵，则右侧即为逆矩阵。也就是说整个过程的最终消元矩阵$E$即为逆矩阵

#### 4.逆矩阵的性质

1. $(AB)^{-1}=B^{-1}A^{-1}$
2. $(A^{-1})^T=(A^T)^{-1}$

## 四.$A\text的LU\text{分解}$

先考虑不需要行置换并且可逆的情况，以二阶矩阵为例

$$A=\begin{bmatrix}
2 & 1\\
8 & 7
\end{bmatrix}
$$

通过消元矩阵对$A$进行消元得到$U$

$$E_{21}A=\begin{bmatrix}
1 & 0\\
-4 & 1
\end{bmatrix}
\begin{bmatrix}
2 & 1\\
8 & 7
\end{bmatrix}=
\begin{bmatrix}
2 & 1\\
0 & 3
\end{bmatrix}=U
$$

在这个例子里要想得到$L$其实很简单，只要对$U$进行相反的操作就可以得到$A$，即$L$就是$E$的逆矩阵，而初等矩阵的逆也是非常容易看出来的，把所操作的行的符号置反即可。也就是如果在第二行上加上四倍第一行，而逆矩阵就是第二行减去四倍第一行。

$$A=
\begin{bmatrix}
2 & 1\\
8 & 7
\end{bmatrix}=\begin{bmatrix}
1 & 0\\
4 & 1
\end{bmatrix}
\begin{bmatrix}
2 & 1\\
0 & 3
\end{bmatrix}=LU
$$

$A=LU$是最基础的矩阵分解。$L$是下三角矩阵，对角线都是1，$U$是上三角矩阵，对角线则为主元。

有的时候也会把主元提出来，得到

$$A=
\begin{bmatrix}
2 & 1\\
8 & 7
\end{bmatrix}=\begin{bmatrix}
1 & 0\\
4 & 1
\end{bmatrix}
\begin{bmatrix}
2 & 0\\
0 & 3
\end{bmatrix}
\begin{bmatrix}
1 & 1/2\\
0 & 1
\end{bmatrix}=LDU
$$

当扩展到更高维度的时候，求$L$的方式是一致的，以相反的顺序把$A$的消元矩阵的逆相乘就可以得到$L$

$$E_{32}E_{31}E_{21}A=U$$
$$A=E_{21}^{-1}E_{31}^{-1}E_{32}^{-1}U=LU$$

那为什么要用这种方法计算，而不是直接算出总的消元矩阵再求逆呢？以以下的消元矩阵为例

$$E_{32}E_{21}=
\begin{bmatrix}
1 & 0 & 0\\
0 & 1 & 0\\
0 & -5 & 1
\end{bmatrix}
\begin{bmatrix}
1 & 0 & 0\\
-2 & 1 & 0\\
0 & 0 & 1
\end{bmatrix}
=\begin{bmatrix}
1 & 0 & 0\\
-2 & 1 & 0\\
10 & -5 & 1
\end{bmatrix}
$$

可以发现一个很不和谐的10，这是因为第二次消元过程中使用了第二行，第一次消元时修改了第二行，从而影响到了第三行

但如果反向并用逆矩阵相乘，则会得到

$$E_{21}^{-1}E_{32}^{-1}=
\begin{bmatrix}
1 & 0 & 0\\
2 & 1 & 0\\
0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
1 & 0 & 0\\
0 & 1 & 0\\
0 & 5 & 1
\end{bmatrix}
=\begin{bmatrix}
1 & 0 & 0\\
2 & 1 & 0\\
0 & 5 & 1
\end{bmatrix}
$$

这样的形式就很完美，因为反向相乘的话每次使用的行在之前都没改变，不会互相影响，也就是如果不存在行置换的情况，只需要把每个消元乘数填充到最后的矩阵中即可得到$L$

## 五.转置-置换-向量空间R

### （一）置换

#### 1.置换矩阵群

三维下的所有置换矩阵构成了一个置换矩阵群

$$
\begin{bmatrix}
1 & 0 & 0\\
0 & 1 & 0\\
0 & 0 & 1
\end{bmatrix}
~ ~\begin{bmatrix}
0 & 1 & 0\\
1 & 0 & 0\\
0 & 0 & 1
\end{bmatrix}
~ ~\begin{bmatrix}
0 & 0 & 1\\
0 & 1 & 0\\
1 & 0 & 0
\end{bmatrix}
$$
$$
\begin{bmatrix}
1 & 0 & 0\\
0 & 0 & 1\\
0 & 1 & 0
\end{bmatrix}
~ ~\begin{bmatrix}
0 & 1 & 0\\
0 & 0 & 1\\
1 & 0 & 0
\end{bmatrix}
~ ~\begin{bmatrix}
0 & 0 & 1\\
1 & 0 & 0\\
0 & 1 & 0
\end{bmatrix}
$$

1. 置换矩阵两两相乘仍在该群中
2. 置换矩阵取逆仍在该群中

#### 2.$PA=LU$

在考虑行置换的情况下，上节的分解式可以表示为
$$PA=LU$$

#### 3.性质

1. n阶矩阵共有$n!$个置换矩阵
2. 所有置换矩阵都可逆，并且$P^{-1}=P^T$
3. $PP^T=I$


### （二）转置

1. 转置即把一个矩阵行列互换

$$A_{ij}^T=A_{ji}$$

2. 如果一个矩阵的转置等于其本身，则该矩阵为对称矩阵，即

$$A^T=A$$

3. $R^TR$总是对称矩阵，可证

$$(R^TR)^T=R^T(R^T)^T=R^TR$$


### （三）向量空间

#### 1.向量空间

空间$R^n$包含所有的n维列向量$v$，对于线性运算是封闭的

#### 2.子空间

取某向量空间的部分空间，且这部分对于线性运算（加法和乘法）封闭，则该空间为某向量空间的子空间。因为乘数可以为0，所以子空间一定包含零元。

eg:

1. $R^2$的子空间
    * 穿过原点的直线
    * 原点
    * $R^2$
2. $R^3$的子空间
    * 穿过原点的直线
    * 穿过原点的平面
    * 原点
    * $R^3$


多个子空间的并集不一定还是子空间，多个子空间的交集还是子空间

## 六.列空间和零空间

以以下矩阵为例

$$A(m \times n)x=
\begin{bmatrix}
1 & 1 & 2\\
2 & 1 & 3\\
3 & 1 & 4\\
4 & 1 & 5
\end{bmatrix}
\begin{bmatrix}
x_1\\
x_2\\
x_3
\end{bmatrix}
$$

### （一）矩阵列空间

矩阵$A$的列空间$C(A)$是$R^4(m=4)$的子空间，为矩阵各个列向量的所有线性组合

可以利用矩阵列空间来求当$b$取什么时$Ax=b$有解，只有当$b$是列向量的线性组合时，才会存在解。也就是当且仅当$b \in C(A)$时，$Ax=b$有解

### （二）矩阵零空间

矩阵$A$的零空间$N(A)$是指满足$Ax=0$的所有解的集合，$x$有三个分量，是$R^3(n=3)$的子空间

本例可以比较容易的得到解

$$x=c
\begin{bmatrix}
1\\
1\\
-1
\end{bmatrix}
$$

可见矩阵$A$的零空间是三维空间中过原点的一条直线

那$Ax=b(b \not=0)$的所有解的集合是向量空间吗？答案是否定的，因为**缺少0向量**
