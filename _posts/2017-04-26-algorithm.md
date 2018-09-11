---
layout: post
title: 算法导论
description: "算法导论"
tags: [algorithm]
modified:   2017-04-26 10:18:38 +0800
share: false
comments: false
mathjax: false
image:
  
---

## 分治策略

### 代入法求递归式

1. 猜测解的形式为$O(f(n))$
2. 用数学归纳法求出解中的常数,并证明解是正确的

    * 首先证明初始条件是不是满足的,可能假定的边界,如$n=1$并不成立.但其实只要某个有限数$n_0$即可.其中初始边界$T(0)$即不存在子问题,为0
    * 假设某个更小规模$T'(n)$如$T(n/2)$成立,递归证明$T(n)$也是满足的:恰当选择常数$c>0$,可有$T(n)\le cf(n)$

#### 例子

$T(n)=T(\lceil n/2\rceil) + 1$

1. 猜测解为$O(lgn)$
2. 有常数项1,在猜测中减去低阶项,假设$T(n)\le c lg(n-2)$
3. 把小规模的$T(\lceil n/2\rceil)$假设代入证明$T(n)$
    $T(n)\le clg(\lceil n/2\rceil - 2) + 1 \le clg(n/2 +1-2) + 1 \le clg((n-2)/2) + 1 \le  clg(n-2) - clg2 + 1 \le clg(n-2)$

### 递归树求解递归式

1. 递归树的高度为$log_bn$
2. $n^{log_ba}$个叶结点
### 主方法求解递归式

#### 主定理
令$a\ge1$和$b>1$是常数,$f(n)$是一个函数,$T(n)$是定义在非负整数上的递归式:
$$T(n)=aT(n/b)+f(n)$$

1. 若对某个常数$\epsilon>0$有$f(n)=O(n^{log_ba-\epsilon})$,则$T(n)=\Theta(n^{log_ba})$
2. 若$f(n)=O(n^{log_ba})$,则$T(n)=\Theta(n^{log_ba}lgn)$
3. 若对某个常数$\epsilon>0$有$f(n)=\Omega(n^{log_ba+\epsilon})$,且对某个常数$c>1$和所有足够大的$n$有$aT(n/b)\le cf(n)$,则$T(n)=\Theta(f(n))$

#### 例子

1. $T(n)=2T(n/4)+1$

    $f(n)=n^0=O(n^{1/2-\epsilon})=O(n^{log_42-\epsilon})$,所以$T(n)=\Theta (\sqrt{n})$

2. $T(n)=2T(n/4)+\sqrt{n}$

    $f(n)=\Theta(\sqrt{n})=\Theta(n^{log_ba})$,所以$T(n)=\Theta (\sqrt{n}lgn)$

3. $T(n)=2T(n/4)+n^2$

    $f(n)=n^2=\Omega(n^{1/2+\epsilon})$,并且存在$c=1/8$,有$2f(n/4)=\frac{1}{8}n^2\le cn^2$


## 图算法

### 广度优先搜索

从源结点开始,把源结点加入到顶点队列中.之后从队列中取出第一个顶点,并扫描该结点的邻接链表,并把未被发现的结点加入到顶点队列中,以此往复直到遍历到所有结点

``` javascript
bfs(adj, s) {
    adj.forEach(value => {
       value.color = 'white';
       value.d = Number.POSITIVE_INFINITY;
       value.pai = null;
    });

    adj[s].color = 'gray';
    adj[s].d = 0;
    adj[s].pai = null;

    let queue = new Array();
    queue.push(adj[s]);

    while (queue.length != 0) {
        let u = queue.shift();
        let index = adj.indexOf(u);

        u.forEach(value => {
            let v = adj[value.vertex];
            if (v.color == 'white') {
                v.color = 'gray';
                v.d = u.d + 1;
                v.pai = index;

                queue.push(v);
            }
        });

        u.color = 'black';
    }
}
```

其中顶点的d属性即为**最短路径距离** ,通过前置顶点pai即可获取**最短路径**

### 深度优先搜索

深度优先搜索总是从最近发现的结点的出发边搜索,直到所有边都被发现,才会回溯到前驱结点继续搜索,会持续到从源结点可以达到的所有结点均被发现.之后会从未被发现的其他结点继续改过程

``` javascript
dfs(adj) {
    adj.forEach(value => {
        value.color = 'white';
        value.pai = null;
    });

    this.time = 0;

    adj.forEach(value => {
        if (value.color == 'white') {
            this.dfs_visit(value);
        }
    })
}

dfs_visit(adj, u) {
    this.time++;

    u.d = this.time;
    u.color = 'gray';
    let index = adj.indexOf(u);

    u.forEach(value => {
        let v = adj[value.vertex];

        if (v.color == 'white') {
            v.pai = index;
            this.dfs_visit(v);
        }
    });

    u.color = 'black';
    this.time++;
    u.f = this.time;
}
```
### 拓扑排序

**拓扑排序**是有向无环图$G$中所有结点一种线性次序,其次序是经过深度遍历后每个结点结束时间的倒序

### 强连通分量

1. 对原图$G$做一次深度优先搜索
2. 创建原图的转置$G^T$
3. 对$G^T$做一次深度优先搜索,但是主过程中按照第一次深度优先搜索中的完成时间降序搜索
4. 每一颗深度优先树即是一个强连通分量

### 最小生成树

有一个连通无向图$G=(V,E)$,找到一个无环子集$T\subseteq E$,能够将所有结点连接,又具有最小的权重,即为**最小生成树**

#### Kruskal算法

每次寻找一条权重最小的安全边加入到连接森林中,安全边即为其两个节点不属于同一颗树,不会造成回路,直到连接了所有的结点即形成了一颗最小生成树

#### Prim算法

从任意一个根结点逐步长大为覆盖所有结点的树,每次从与连接树连接的边中选择一个最小权重安全边,直至连接所有结点

### 单源最短路径

#### 松弛
尝试对$s$到$v$的最短路径进行改善.测试的方法为:结点$u$的d属性加上$u$与$v$之间边的权重如果小于$v$的d属性,则改变结点$v$的d属性与前驱结点

``` javascript
relax(u, v) {
        let uVertex = this.adj[u];
        let vVertex = this.adj[v];

        let w = Number.POSITIVE_INFINITY;
        for (let i = 0;i < uVertex.length;i++) {
            if (uVertex[i].vertex == v) {
                w = uVertex[i].w;
            }
        }
        if (vVertex.d > uVertex.d + w) {
            vVertex.d = uVertex.d + w;
            vVertex.pai = u;
        }
    }
```

#### Bellman-Ford算法

该算法可以解决一般的单源路径问题,边的权值可以为负,可以是环图,但是不含权重为负的环路
该算法对每条边进行$|V|-1$次的松弛操作,既可以得到最短路径

#### 有向无环图的单源最短路径

1. 拓扑排序
2. 按照拓扑排序的顺序遍历顶点$u$
3. 遍历$u$的邻接链表中顶点$v$,对$(u,v)$做松弛操作

#### dijkstra算法

初始源结点$s$的d属性为0,其他结点d属性为$\infty$,首先由最小优先队列$Q$保存保存所有的结点,关键值为d值.
1. 从Q中取出最小d值顶点$u$
2. 遍历$u$的邻接链表中顶点$v$,对$(u,v)$做松弛操作
3. 直到$Q$为空


``` javascript
dijstra(s) {
    this.initialSingleSource(s);

    let heap = new minHeap(this.adj);

    while (!heap.isEmpty()) {
        let u = heap.heapExtractMin();

        this.adj[u.index].forEach(v => {
            this.relax(u.index, v.vertex);
        })
    }
}
```

## 最大流

#### 残存网络
首先定义**残存容量**$c_f(u,v)$

$$c_f(u,v)=\left\{
\begin{array}{lcl}
c(u,v) - f(u,v) &       & if(u,v)\in E \\
f(v,u) &       & if(v,u)\in E \\
0 &       & others
\end{array}
\right.
$$

给定一个流网络$G=(V,E)$和一个流$f$,则由$f$有道的图$G$的**残存网络**为$G_f=(V,E_f)$,其中

$$E_f=\{ (u,v)\in V \times V:c_f(u,v)>0\}$$


也就是残存网络$E_f$的边要不是原有的边,要不就是原有边的反向边,并且残存容量必须大于0.

残存网络的生成过程:**所有原有边的容量减去流量得到残存容量,如果该残存容量不为0,则在残存网络中含有该边,其容量为残存容量;如果原有边的流量不为0,则在残存网络中含有该边的反向边,容量为原有边的流量**

#### 增广路径

增广路径$p$是残存网络$G_f$中一条从源结点$s$到汇点$t$的简单路径.能在一条增广路径$p$上为每条边增加流量的最大值为路径$p$的**残存容量**:

$$c_f(p)=min\{c_f(u,v):(u,v)\in p\}$$

#### 流网络的切割

切割$(S,T)$的容量是:
$$c(S,T)=\sum_{u\in S}\sum_{v\in T}c(u,v)$$

#### 最大流最小切割定理

下面的条件是等价的

1. $f$是$G$的最大流
2. 残存网络$G_f$不包括任何增广路径
3. $|f|=c(S,T)$,其中$(S,T)$是流网络$G$的某个切割

$$1\Rightarrow2\Rightarrow3$$

#### For-Fulkerson方法

1. 流$f$初始化为0
2. 生成残存网络$G_f$
3. 在残存网络中寻找一条增广路径$p$,可以通过广度优先遍历寻找
4. 在增广路径$p$中的最小容量作为残存容量,在路径$p$使用残存容量对流$f$进行增加
5. 循环步骤2~4,直到不再存在增广路径,流$f$即为最大流


``` javascript
fordFulkerson(s, t) {
    // 初始化流
    this.adj.forEach((u, i) => {
        u.forEach(v => {
            v.f = 0;
        });
    });

    // 生成残存网络
    let residual = this.residualNetwork();
    // 广度优先遍历寻找增广路经
    this.bfs(residual, s);

    while (residual[t].pai != null) {
        let path = this.getPath(residual, s, t); //增广路经
        let min = Number.POSITIVE_INFINITY;

        // 寻找路径上的最小容量作为残存容量
        for (let i = 0;i < path.length - 1;i++) {
            let u = residual[path[i]];

            for (let j = 0;j < u.length;j++) {
                if (u[j].vertex == path[i + 1]) {
                    min = min < u[j].c ? min : u[j].c;
                }
            }
        }

        // 使用残存容量对流进行增加
        for (let i = 0;i < path.length - 1;i++) {
            let isOriginEdge = this.adj[path[i]].some((v) => v.vertex == path[i + 1]);

            if (isOriginEdge) {
                let u = this.adj[path[i]];
                let [v] = u.filter(v => v.vertex == path[i + 1]);
                v.f += min;
            } else {
                let v = this.adj[path[i + 1]];
                let [u] = v.filter(v => v.vertex == path[i]);
                u.f -= min;
            }
        }

        residual = this.residualNetwork();
        this.bfs(residual, s);
    }
}
```

#### 最大二分匹配

##### 基本概念
1. 在一个**二分图**中,节点结合课划分为$V=L\bigcup R$,其中$L$和$R$是不相交的,所有的边都横跨$L$和$R$
2. 一个**匹配**是边的一个子集$M\subseteq E$,使得对于所有的结点$v$,$M$中最多有一条边与结点$v$相连
3. **最大匹配**是最大基数的匹配

##### 寻找最大二分匹配

可以把二分图构造成一个流网络$G'$,新增加源结点$s$和汇点$t$,源结点$s$连接所有的$L$中的顶点,所有的$R$中的顶点连接汇点$t$,其中所有边的容量均为单位容量

二分图$G$的一个最大匹配$M$的基数等于对应流网络$G'$的某一个最大流$f$的值

## 多线程算法

### 基本概念
1. nested parallelism(嵌套并行)
2. parallel loops(并行循环)
3. spawn(并行关键字)
4. sync(并行关键字)
5. work(工作量)
6. span(持续时间)
7. speedup(加速比:$T_1/P$)
8. parallelism(并行度:$T_1/T_\infty $)
9. slackness(松弛度:$T_1/(PT_\infty)$)
10. complete step(完全步)
11. determinacy race(确定性竞争)

### 嵌套并行

**spawn** 和 **sync** 关键字的使用就出现了嵌套并行. **spawn** 后派生的子过程可以与父进程并行进行, 执行 **sync** 同步语句时.则需要等待所有的子进程计算完成

### 多线程执行的模型
多线程计算过程可以看成一个有向无环图

**工作量** 是指在一个处理器上执行整个计算的总时间,是在图上每个链消耗时间的总和,如果每个链消耗单位时间,则工作量为途中顶点数.

**持续时间** 是指沿着图中任一路径的最长执行时间,是图中的关键路径路径中的顶点数

$T_P$表示一个算法在$P$个处理器上的运行时间,$T_1$表示总工作量,则**工作量定律**为:
$$T_P\ge T_1/P$$
**持续时间定律**为:
$$T_P\ge T_\infty$$

**加速比**表明在$P$个处理器上计算比在1个处理器上快多少倍:
$$T_1/P$$

**并行度**
$$T_1/T_\infty $$

**松弛度**
$$T_1/(PT_\infty)$$


**贪心调度器**在每个时间布内尽可能地分配更多的链到处理器上,其执行多线程计算的运行时间为:
$$T_P\le T_1/P + T_\infty$$

### 并行循环

**parallel for** 关键字表示各自循环的每个迭代都可以并发执行,就出行了并行循环

如果两个逻辑上并行指令访问存储器同一个位置,且其中有指令执行写操作,就会发生**确定性竞争**
