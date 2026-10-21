# hc11 讲义 · 订单区间最大重叠：从「逐个时刻数」到扫描线、在线差分、坐标压缩与线段树

> 读者：会写基本 Java（类、方法、循环、`ArrayList` / `HashMap`），没学过扫描线、差分数组、线段树、坐标压缩；每个概念从零讲。

---

## 1. 这道题在问什么

交易所里每一张订单（order）有一段**生命周期**：`start` 时刻进入订单簿，`end` 时刻离开（过期或被撤）。面试官问：

* **Part 1**：任何一个时刻，簿上同时有多少张订单「活着」？这个数最大是多少（最大重叠，maximum overlap）？
* **Part 2**：订单分**买单**（BUY）和**卖单**（SELL）。分别求买、卖各自的最大重叠；另外，订单可以被**撤单**（cancel）——撤单让订单提前结束，区间被截短。
* **Part 3**：订单和撤单是**实时**一个个到来的，不能先攒起来。来一个处理一个，随时回答「到现在为止最大重叠多少」「t 时刻有几张单活着」。
* **Part 4**：时间戳是纳秒，数值高达 10¹⁸，不能开数组；订单还可以任意顺序加入和撤销，要问「某段时间内的最大重叠」。

### 手算一遍（Part 1）

三张订单：A = [1,5)，B = [2,6)，C = [4,8)。这里 `[1,5)` 的意思是：时刻 1, 2, 3, 4 活着，时刻 5 已经结束（**左闭右开**，2.1 节解释）。

```
时刻:   0  1  2  3  4  5  6  7  8
A=[1,5)    ■  ■  ■  ■
B=[2,6)       ■  ■  ■  ■
C=[4,8)             ■  ■  ■  ■
活着数:  0  1  2  2  3  2  1  1  0
```

最大重叠是 **3**，最早出现在时刻 **4**（A、B、C 同时活着）。

### 手算一遍（Part 2：买卖 + 撤单）

```
Place(1,BUY, 0,10)  Place(2,BUY, 2, 8)  Place(3,SELL,3, 6)  Place(4,SELL,4,12)  Place(5,BUY, 5, 9)
Cancel(2, 6)   Cancel(4, 5)
```

撤单把区间截成 `[start, min(end, 撤单时间))`：

| 订单 | 方向 | 计划 | 撤单 | 有效区间 |
|---|---|---|---|---|
| 1 | BUY | [0,10) | — | [0,10) |
| 2 | BUY | [2,8) | 6 | [2,6) |
| 3 | SELL | [3,6) | — | [3,6) |
| 4 | SELL | [4,12) | 5 | [4,5) |
| 5 | BUY | [5,9) | — | [5,9) |

* BUY（订单 1, 2, 5）：时刻 5 时三张都活着 → **3，在 t=5**。
* SELL（订单 3, 4）：时刻 4 时两张都活着 → **2，在 t=4**。
* 全部：时刻 4 活着的是 1, 2, 3, 4 → 4；时刻 5 活着的是 1, 2, 3, 5（订单 4 的 [4,5) 已经结束）→ 也是 4。取最早 → **4，在 t=4**。
  如果没有那两个撤单，时刻 5 有五张订单同时活着，答案是 5。**撤单让答案变了**。

注意：买方的峰值（t=5）和卖方的峰值（t=4）**不在同一时刻**，所以「全部」的峰值 4 并不等于 3 + 2 = 5。

---

## 2. 前置知识

> 复杂度记号速记：`O(n)` 表示步数随输入规模 n 线性增长；`O(log n)` 表示 n 翻倍只多一步（二分查找、平衡树、堆）；`O(n²)` 表示每一对元素都要处理一次；`O(1)` 表示与 n 无关。

### 2.1 半开区间 `[start, end)`

**是什么**：包含 `start`、不包含 `end` 的区间。数学上写 `[a, b)`。

**为什么这样约定**：订单 A 在 3 时刻结束，订单 B 在 3 时刻开始——是不是同时活着？现实里这是「交接」，不是重叠。用**闭区间**（两端都含）会把它算成重叠，用**半开区间**则自然得到「不重叠」。其他好处：
* 长度 = `end - start`；
* 相邻区间 `[0,3)`、`[3,5)` 首尾相接，不重叠、不留空；
* 空区间就是 `start == end`，不用特殊情况。

编程里几乎所有区间都是半开的：`Arrays.copyOfRange(a, from, to)`、`String.substring(begin, end)`、`for (i = lo; i < hi; i++)`。

**怎么写**：判断时刻 t 是否活着：`start <= t && t < end`。

⚠️ 面试时先问清楚：「区间两端是否包含？」`[1,3]` 和 `[3,5]` 在闭区间下重叠、在半开下不重叠，答案可以差 1。本题的 `maxOverlapInclusive` 是闭区间版本。

### 2.2 扫描线（sweep line）

**是什么**：把「区间」问题变成「事件」问题，然后沿着时间轴从左到右**扫**过去，边扫边维护一个计数器。

**为什么需要它**：重叠数只在端点处变化——区间开始时 +1，区间结束时 −1。所以没必要检查每个时刻，只需要按顺序处理 2n 个端点事件。

**它怎么工作**：对每个区间 `[s, e)`，生成两个事件 `(s, +1)` 和 `(e, -1)`；按时间排序；依次处理，计数器加上 delta，记录最大值。

```
事件:  (1,+1) (2,+1) (4,+1) (5,-1) (6,-1) (8,-1)      ← A=[1,5) B=[2,6) C=[4,8)
计数:     1      2      3      2      1      0
最大值 = 3，出现在处理 (4,+1) 之后，即时刻 4
```

**Java 里怎么写**：见 4.1 节。

### 2.3 同一时刻：先结束，再开始（tie 规则）

**是什么**：事件按时间排序时，如果两个事件**时间相同**，要规定谁先谁后。规则：**−1（结束）排在 +1（开始）前面**。

**为什么**：看 `[1,3)` 和 `[3,5)`：

```
事件: (1,+1) (3,+1) (3,-1) (5,-1)
如果同一时刻 +1 先：计数 1, 2, 1, 0  → 最大值 2  ✗（错）
如果同一时刻 -1 先：事件 (1,+1) (3,-1) (3,+1) (5,-1)  计数 1, 0, 1, 0 → 最大值 1  ✓
```

时刻 3 订单 1 已经死了（半开区间 `end` 不含），订单 2 刚出生——任何时刻只有一张活着。先处理结束，计数器在「中间状态」降下来，才不会虚高。

**怎么实现这个顺序**：把事件写成 `(time, delta)`，排序时先比 `time`，再比 `delta`：因为 −1 < +1，天然满足。
**常见的错**：只按 `time` 排序，且排序算法的平局顺序不确定（或者事件对象用了不稳定排序、或者按插入顺序平局）——结果时对时错，是这道题最经典的坑。

### 2.4 差分数组（difference array）与前缀和

**是什么**：想象一个数组 `live[t]` 表示 t 时刻活着的订单数。**差分数组** `d[t] = live[t] - live[t-1]`，它记录「每个时刻相对上一时刻的**变化**」。反过来，`live[t] = d[0] + d[1] + … + d[t]`（**前缀和**，prefix sum）。

**为什么需要它**：给一个区间 `[s, e)` 全部 +1，如果直接改 `live` 数组要改 `e - s` 个格子；用差分数组只改两个格子：`d[s] += 1`、`d[e] -= 1`。n 个区间只改 2n 个格子，最后做一遍前缀和还原。这就是扫描线的数学本质——事件列表就是**稀疏**的差分数组（只记录非零项）。

```
下标 t:    0   1   2   3   4   5   6   7   8
d[t]:      0  +1  +1   0  +1  -1  -1   0  -1      ← A=[1,5) B=[2,6) C=[4,8)
前缀和:    0   1   2   2   3   2   1   1   0       = live[t]
```

Part 3 的在线版和 Part 4 的线段树，都是在「差分数组」这个想法上做文章。

### 2.5 有序 Map：`TreeMap`

**是什么**：按键排好序的 `Map`（底层红黑树），`put / get / remove` 都是 O(log n)，并且支持「最小键」`firstEntry()`、「删除并返回最小」`pollFirstEntry()`、「≤ x 的最大键」`floorEntry(x)` 等。红黑树是自平衡二叉搜索树，旋转和染色保证树高 O(log n)；Java 21 起这些两端操作被统一进 `SequencedMap`。

**为什么需要它**：Part 3 要维护「未来哪些时刻会有订单结束」，必须能按时间顺序取最早的那个——正是 `firstEntry / pollFirstEntry`。回答「t 时刻有几张」要找「不晚于 t 的最近一次变化」——正是 `floorEntry(t)`。

```java
var expiries = new TreeMap<Long, Integer>();      // 结束时间 → 在那一刻结束的订单数
expiries.merge(10L, 1, Integer::sum);             // 记一笔
var e = expiries.firstEntry();                    // 最早的结束
expiries.pollFirstEntry();                        // 取出并删除
var f = history.floorEntry(7L);                   // ≤ 7 的最大键对应的条目（没有则 null）
```

### 2.6 sealed 事件与模式匹配

`OrderEvent` 是 `sealed interface ... permits Place, Cancel`：只有「下单」和「撤单」两种事件。`switch (e) { case Place p -> …; case Cancel(var id, var time) -> … }` 编译器检查穷尽性。

### 2.7 线段树（segment tree）与懒标记——从零推出来

这一节是 Part 4 的全部预备知识。先用最朴素的想法出发。

**问题**：有 m 个格子（初始都是 0），要支持两个操作：
* `rangeAdd(l, r, δ)`：把第 l 到第 r 个格子**都加上** δ；
* `rangeMax(l, r)`：问第 l 到第 r 个格子里的**最大值**。

**最笨的办法**：用数组，两个操作都是循环，每次 O(m)。如果有 q 次操作，总共 O(q·m)。m = 2×10⁵、q = 3×10⁵ 时是 6×10¹⁰，跑不完。

**想法 1：给区间分层，提前存好每段的答案（线段树）。** 把整个数组分成两半，每半再分成两半……直到单个格子，形成一棵二叉树。每个结点管一个区间，存「这个区间里的最大值」。

```
m = 4 个格子（下标 0..3），结点编号从 1 开始，结点 i 的孩子是 2i 和 2i+1：

                  结点1 [0..3]
               /                \
        结点2 [0..1]          结点3 [2..3]
         /       \             /       \
   结点4 [0]  结点5 [1]    结点6 [2]  结点7 [3]       ← 叶子 = 单个格子
```

* **查询** `rangeMax(l, r)`：从根开始。如果结点的区间**完全落在** [l, r] 里，直接返回它存的最大值（不用往下）；否则往有重叠的孩子递归，结果取最大。
  任何一个查询区间最多被拆成 O(log m) 个「完全落在里面」的结点（每一层最多访问 4 个结点，两个「部分重叠」继续往下、两个「完全覆盖」直接返回）。
* **点更新**（只改一个格子）：改叶子，沿路径回到根，每个结点重新取两个孩子的最大值，O(log m)。

**问题 2：区间加怎么办？** 如果区间加 `[l, r]` 要改 r−l+1 个叶子再更新祖先，又回到 O(m)。

**想法 2：懒标记（lazy propagation）——「先欠着，需要时再还」。** 如果结点的区间**完全落在**更新区间里，就不要往下走，只在这个结点上记一笔「整段还欠着 +δ」（`add[node] += δ`），同时把这个结点存的最大值也加上 δ（整段都加了 δ，最大值当然也加 δ）。孩子们暂时不知道——这笔账是「懒」的。

**经典做法（下推 push-down）**：以后有人要往这个结点**内部**走（部分重叠）时，先把它欠的账分给两个孩子（孩子的 `add` 和最大值各加上），自己清零，再往下走。

**更简单的做法：标记永久化（不下推）。** 注意到「整段加 δ」这个标记永远不会影响*相对关系*，只是平移。所以可以**永远不下推**：
* 每个结点存两个数：`add[node]` 是整个区间被整体加了多少（只在本结点生效，孩子不知道）；`mx[node]` 是这个区间内的最大值，**已经包含**本结点和所有后代的 `add`，**不包含**祖先的 `add`。
* 更新时，完全覆盖的结点：`add[node] += δ; mx[node] += δ`。部分覆盖的结点：递归孩子，然后 `mx[node] = add[node] + max(mx[左], mx[右])`。
* 查询时，完全覆盖的结点：返回 `mx[node]`。部分重叠的结点：递归孩子取最大，**最后加上本结点的 `add[node]`**（因为这笔整体平移对结点内所有格子都生效，孩子们不知道，要在这里补上）。

**手算：4 个格子，加区间 [0,2] 再加 [1,3]**（节点编号如上图，初始全 0）：

```
操作 1：rangeAdd(0, 2, +1)
  根 [0..3] 部分覆盖 → 递归
    结点2 [0..1] 完全覆盖 → add[2]=1, mx[2]=1
    结点3 [2..3] 部分覆盖 → 递归
      结点6 [2] 完全覆盖 → add[6]=1, mx[6]=1
      （结点7 不重叠）
    回到结点3：mx[3] = add[3] + max(mx[6], mx[7]) = 0 + max(1,0) = 1
  回到根：mx[1] = 0 + max(mx[2], mx[3]) = max(1,1) = 1
  此时：add = {2:1, 6:1}，mx = {1:1, 2:1, 3:1, 6:1}

操作 2：rangeAdd(1, 3, +1)
  根部分覆盖 → 递归
    结点2 [0..1] 部分覆盖 → 递归
      结点5 [1] 完全覆盖 → add[5]=1, mx[5]=1
      回到结点2：mx[2] = add[2] + max(mx[4], mx[5]) = 1 + max(0,1) = 2
    结点3 [2..3] 完全覆盖 → add[3]=1, mx[3]=1+1=2
  回到根：mx[1] = 0 + max(2, 2) = 2
  此时：add = {2:1, 3:1, 5:1, 6:1}，mx = {1:2, 2:2, 3:2, 5:1, 6:1}

查询 rangeMax(2, 2)（第 2 个格子）：
  根 → 结点3（部分重叠）→ 结点6（完全覆盖）返回 mx[6]=1
  回到结点3：1 + add[3] = 2；回到根：2 + add[1] = 2   → 答案 2 ✓（区间 [0,2] 和 [1,3] 都覆盖第 2 格）
查询 rangeMax(0, 0)：
  根 → 结点2（部分重叠）→ 结点4 返回 0；回到结点2：0 + add[2] = 1；回到根：1   → 答案 1 ✓（只有 [0,2] 覆盖第 0 格）
```

**复杂度**：每个操作每层最多访问常数个结点（≤ 4），树高 ⌈log₂ m⌉，所以 O(log m)。内存：叶子数补到 2 的幂 `size`，两个数组各 `2·size` 个 `int`。

**为什么「标记永久化」只适用于这里**：它要求操作满足「加法」+「取最大」这种*平移不改变相对大小*的性质。如果更新是「区间赋值」或者查询是「区间和」（和需要知道区间有多少个格子才能乘 δ），就需要完整的下推。

**Java 里怎么写**：见 5.4 节的 `IntervalIndex`。

### 2.8 坐标压缩（coordinate compression）

**是什么**：把很大（或很稀疏）的坐标映射成 0, 1, 2, … 的小整数下标，保持大小顺序。

**为什么需要它**：时间戳可能是 10¹⁸（纳秒），线段树需要一个数组，开不出 10¹⁸ 个格子。但 n 张订单只有 2n 个**端点**，而活跃数只在端点处变化——两个相邻端点之间的所有时刻，活跃数完全一样。所以我们只需要关心端点。

**它怎么工作**：端点排序去重得到 `c[0] < c[1] < … < c[m-1]`。相邻两个端点之间的 `[c[j], c[j+1])` 叫一个**基本段**，一共 m−1 个，每个基本段内活跃数是常数。区间 `[s, e)` 恰好覆盖基本段 `idx(s)` 到 `idx(e)-1`，其中 `idx(x)` 是 x 在 `c` 里的下标（二分查找）。

```
订单 [10,50) [20,60) [40,80)  → 端点排序去重 c = [10, 20, 40, 50, 60, 80]（m=6）
基本段:  seg0=[10,20)  seg1=[20,40)  seg2=[40,50)  seg3=[50,60)  seg4=[60,80)
[10,50) 覆盖 idx(10)=0 .. idx(50)-1=2  → seg0..seg2
[20,60) 覆盖 idx(20)=1 .. idx(60)-1=3  → seg1..seg3
[40,80) 覆盖 idx(40)=2 .. idx(80)-1=4  → seg2..seg4
每段活跃数:  1   2   3   2   1      最大 3（seg2 = [40,50)）
```

**Java 里怎么写**：`Arrays.sort`、手工去重、`Arrays.binarySearch(long[] a, long key)`：找到返回下标，没找到返回 `-(插入点) - 1`，所以「≤ x 的最大下标」是 `-i - 2`、「≥ x 的最小下标」是 `-i - 1`。

### 2.9 溢出：只比较，不运算

时间戳可能接近 `Long.MAX_VALUE`。`end - start`、`(lo + hi) / 2` 这类运算会溢出成负数。本题的原则：**时间只比较，不做运算**。线段树里下标是 `int`（压缩后的小整数），用 `(nl + nr) >>> 1` 取中点（无符号右移，即使下标很大也不会变负）。
背景：`long` 的范围是 −2⁶³ … 2⁶³−1，超出会静默回绕成相反符号的数；`Math.addExact` / `multiplyExact` 则在溢出时抛 `ArithmeticException`。

---

## 3. 从最笨的解法开始

### 3.1 逐个时刻数

```java
int best = 0;
for (long t = 0; t <= maxEnd; t++) {
    int live = 0;
    for (long[] iv : intervals) if (iv[0] <= t && t < iv[1]) live++;
    best = Math.max(best, live);
}
```

* 复杂度 O(T·n)，T 是时间轴长度。**T 是时间戳的数值范围，不是订单数！** 纳秒时间戳 T ≈ 10¹⁸，永远跑不完。
* 它仍然有用：只用小坐标做**对拍**（拿它的答案核对快解法）。

### 3.2 只检查开始时刻

重叠数只会在某个区间的 `start` 处达到新高（只有开始会让数变大），所以只检查每个 `start`：

```java
for (long[] a : intervals) {
    int live = 0;
    for (long[] b : intervals) if (b[0] <= a[0] && a[0] < b[1]) live++;
    best = Math.max(best, live);
}
```

O(n²)。n = 10⁶ 时 10¹²，几小时。比 3.1 好（和时间戳范围无关），但仍然太慢。

### 3.3 Part 3/4 的笨办法

* 在线版：每来一个事件，把到目前为止的全部订单重新交给 Part 2 的 `analyze`，O(n) 到 O(n log n) 一次，总 O(n² log n)。它仍然有用——**可以用它对每个前缀对拍在线版**。
* 大坐标：逐个时刻数不可行（T 太大）；在 n 个订单上每次查询线性扫描，q 次查询 O(q·n)。

---

## 4. 一步一步改进

### 4.1 Part 1：扫描线

**第 1 步：事件列表 + 排序**

```java
// 每个区间 [s,e) → 两个事件，用 long[]{time, delta}
var events = new long[2 * n][];
for (...) { events[2*i] = new long[]{s, +1}; events[2*i+1] = new long[]{e, -1}; }
Arrays.sort(events, Comparator.<long[]>comparingLong(x -> x[0]).thenComparingLong(x -> x[1]));  // 同一时刻 -1 在 +1 前
int live = 0, best = 0;
for (var ev : events) { live += (int) ev[1]; best = Math.max(best, live); }
```

* 复杂度 O(n log n)；正确，但每个事件一个 `long[]` 对象：2n 个小数组，缓存不友好，排序时要比较器间接比较。
* 比较器第二关键字是 `delta`（−1 < +1）。这就是 2.3 节的 tie 规则。

**第 2 步：去掉事件对象——两个已排序的数组**

观察：开始事件只有 +1，结束事件只有 −1。把所有 `start` 放进一个 `long[]` 排序，把所有 `end` 放进另一个 `long[]` 排序，然后**像归并一样**一起扫：

```java
Arrays.sort(starts); Arrays.sort(ends);
int j = 0;                                           // ends[0..j) 都已经结束
for (int i = 0; i < n; i++) {
    long s = starts[i];
    while (j < n && ends[j] <= s) j++;               // 结束时间 <= s：已经结束（半开区间，同一时刻先结束）
    int live = (i + 1) - j;                          // 已开始个数 - 已结束个数
    best = Math.max(best, live);
}
```

* 「同一时刻先结束后开始」就是 `ends[j] <= s`（`<=` 是关键；闭区间版本改成 `<`）。
* 最大值只可能出现在某个 `start` 上，所以只在 `start` 处计算。
* `Arrays.sort(long[])` 是原始类型的双轴快速排序，没有装箱、没有比较器，内存连续。100 万个区间整体 80 ms 左右。
* 同一个 `s` 重复出现（多张订单同一时刻开始）：`i` 逐个推进，`live` 逐个增大；用严格 `>` 更新最优，所以 `time` 取到最早且为同一个 `s`。

**第 3 步：最早时刻**

`if (live > best) { best = live; bestTime = s; }` ——严格 `>`，多个时刻达到最大值时保留最早的。

**第 4 步：空区间与非法输入**

* `start == end` 的区间从没活过，直接跳过（不跳过也不会错——`ends[j] <= s` 会在同一个 s 上把它立刻抵消，两种写法结果一样；跳过更清楚）。
* `end < start`、`start < 0`、行长度不是 2 → `IllegalArgumentException`。

**另一种经典解法：堆**（Meeting Rooms II）：按 start 排序，用一个最小堆存「当前活着的订单的结束时间」；来一个新订单先 `while (heap 非空 && heap.peek() <= s) heap.poll()`，再 `heap.add(e)`，堆的大小的最大值就是答案。
O(n log n)，同样正确。选择两数组的理由：没有堆的对象开销；tie 规则一眼可见；容易扩展到「按方向拆开」「带撤单」。

### 4.2 Part 2：买卖方向 + 撤单

**撤单的语义翻译**：撤单只是**修改区间**——把 `end` 改成 `min(end, cancelTime)`。所以：

1. 第一遍扫事件：`Place` 存进 `HashMap<id, Place>`（重复 id → 报错）；`Cancel` 存进 `HashMap<id, 最早撤单时间>`（`merge(id, time, Math::min)`：同一个订单撤多次，最早的生效）。
2. 检查每个撤单的 id 都有对应的 `Place`（所以事件的**顺序无所谓**：撤单写在下单前面也行，因为是先收集后处理）。
3. 对每个 `Place` 算有效区间 `[start, min(end, cancelTime))`；如果有效结束 `<= start`（撤得太早或空区间）→ 跳过。
4. 按方向分到三个「车道」（BUY、SELL、ALL），每个车道各自做 4.1 的扫描。

* 复杂度：O(n log n)（三次排序）。
* 注意 ALL 车道必须**单独扫描**，不能用 `buy.count + sell.count`（两个峰值时刻不同，2.2 节例子里 3 + 2 ≠ 4）。
* sealed 的 `OrderEvent`：`switch` 里只写 `Place` 和 `Cancel`，不写 `default`；以后新增事件类型（比如 `Amend` 改单），所有没处理的 `switch` 编译报错。

### 4.3 Part 3：在线版

**问题**：事件一个个到来。不能再「先全部读完，排序，扫描」。

**观察 1**：事件按时间顺序到达，所以「排序」已经由时间本身做完了。我们要做的是**边到边扫**。

**观察 2**：扫描线的计数器 `live` 在时刻 `now` 的值，需要知道「哪些订单已经在 now 之前结束了」。已知所有订单的计划结束时间，但它们在未来；需要一个按结束时间排序的结构，`now` 前进时把到期的取出来——有序 Map `expiries: TreeMap<结束时间, 订单数>`（2.5 节）。这其实是差分数组的**未来部分**：`d[end] -= 1`。过去部分已经被累加进 `live`，不用再存差分。

**数据结构（每个车道）**：

| 字段 | 含义 |
|---|---|
| `expiries` | `TreeMap`，结束时间 → 在这一刻结束的订单数（未来的 −1） |
| `live` | 当前（`now`）活着的订单数 |
| `history` | `TreeMap`，时间 → 该时刻的活跃数（只记录**变化点**，是个阶梯函数） |
| `committedMax` / `committedTime` | 已经「过去」的时间戳里的最大值，及其最早时刻 |

**事件处理**：

* `place(id, side, start, end)`：先 `advanceTo(start)`（时钟推进，见下），再 `live++`、`expiries[end] += 1`、`history[now] = live`。
* `cancel(id, time)`：先 `advanceTo(time)`；如果订单计划结束 `end > time`（还活着）：`live--`、`expiries[end] -= 1`（从未来的差分里撤掉）、`history[now] = live`，并把订单记录的 `end` 改成 `time`（以后再撤就发现「已经结束」→ 返回 `false`）。
* `advanceTo(t)`（`t > now`）：先「封账」当前时间戳（下面解释），然后把 `expiries` 里所有键 `<= t` 的**依次**取出（`pollFirstEntry`）：`live -= count`，并在 `history[键] = live` 记下阶梯下降。

三个车道（BUY、SELL、ALL）各一份，每个事件更新其方向车道和 ALL 车道。

**最大值的陷阱：同一时间戳内先加后撤**

考虑：`place(1,BUY,5,9)`、`place(2,BUY,5,9)`、`cancel(1,5)`，三个事件时间戳都是 5。

```
place 1 @5 : live=1
place 2 @5 : live=2          ← 如果此刻就把「最大值=2」记下来
cancel 1 @5: live=1          ← 订单 1 的有效区间是 [5,5)，空，从没活过
```

真正的答案是最大重叠 1。如果每次 `place` 后立即更新最大值，就被瞬时的 2 污染了（这个 2 在后来的事件里被撤销了）。

**解法：封账（commit）。** 一个时间戳**过去**之后（时钟前进到更大的时间）才把它的最终活跃数记入 `committedMax`；而当前时间戳的值只在查询时临时参与比较：

```java
// advance(to)：时钟从 lastTick 走到 to
if (live > committedMax) { committedMax = live; committedTime = lastTick; }   // 给过去的时间戳封账
...                                                                           // 然后折叠到期订单
// peak()
return live > committedMax ? new Peak(live, lastTick) : new Peak(committedMax, committedTime);
```

* 严格 `>`：相等时较早的（已封账的）获胜，得到「最早时刻」。
* 为什么只在时钟前进时封账就够了？两个相邻事件时间戳之间，活跃数只会**下降**（只有到期，没有新订单），所以全局最大值一定出现在某个有事件的时间戳的**最终**值上。

**走一遍 Part 2 的样例（ALL 车道）：**

| 事件 | 动作 | `live` | `expiries`（结束时间→数量） | 已封账最大值 | `peak()` |
|---|---|---|---|---|---|
| place 1 @0 [0,10) | live++ | 1 | {10:1} | (0, 0) | (1, 0) |
| place 2 @2 [2,8) | 封账 (1,0)；live++ | 2 | {8:1, 10:1} | (1, 0) | (2, 2) |
| place 3 @3 [3,6) | 封账 (2,2)；live++ | 3 | {6:1, 8:1, 10:1} | (2, 2) | (3, 3) |
| place 4 @4 [4,12) | 封账 (3,3)；live++ | 4 | {6,8,10,12 各 1} | (3, 3) | (4, 4) |
| place 5 @5 [5,9) | 封账 (4,4)；live++ | 5 | {6,8,9,10,12 各 1} | (4, 4) | (5, 5) |
| cancel 4 @5 | 同时间戳；live--，撤掉 {12} | 4 | {6,8,9,10 各 1} | (4, 4) | **(4, 4)** |
| cancel 2 @6 | 封账：live=4 不 > 4；折叠 6：live=3；撤 2：live--，撤掉 {8} | 2 | {9:1, 10:1} | (4, 4) | (4, 4) |

第 5 行 `peak()` 是 (5,5)，第 6 行同一时间戳撤单后变成 (4,4)——这正是「追溯修正」，也和 Part 2 批量版对同一批订单的答案一致（BUY 车道 (3,5)、SELL 车道 (2,4) 同理）。**可以对每个前缀都用 Part 2 的批量版对拍**，因为批量版对「已到事件」的答案在后续没有新订单的情况下就是在线版的答案。

**回答 `liveAt(t)`**：`history.floorEntry(t)`——不晚于 t 的最近一次变化点，它的值就是 t 时刻的活跃数（阶梯函数在变化点之间是常数）；没有这样的变化点 → 0。O(log n)。

**为什么不支持 `t > now`（预测）？** `t` 在未来时，活跃数 = `live` − （`expiries` 里键 ≤ t 的项的总和）。TreeMap 要遍历这些键，O(k)，没有 O(log n) 的「前缀和」操作。要做到 O(log n)，需要在有序结构上维护子树和：
* 如果能提前知道所有可能的结束时间 → 坐标压缩 + 树状数组（Fenwick）或线段树（Part 4）；
* 在线且坐标未知 → 自己写平衡树（节点上存子树和），`TreeMap` 做不到。
所以面试时可以回答：「预测查询我会拆成 O(k) 的朴素版，或者离线压缩坐标后用线段树。」

### 4.4 Part 4：坐标压缩 + 线段树

**为什么扫描线不够**：Part 1 的扫描线答「全局最大」是最优的（30 万个 10¹⁸ 量级区间，扫描线 21 ms，建线段树索引 100 ms）。线段树值得用的场景是：
1. **更新顺序任意**（订单可以先撤后加；`add` 与 `remove` 交错）——扫描线必须一次性读完；
2. **区间查询**：问「[from, to) 内的最大重叠」，扫描线每次都要重做；线段树每次 O(log n)。

**第 1 步：坐标压缩**（2.8 节）。`IntervalIndex(long[] coordinates)` 构造时排序去重得到 `coords`，基本段数 `segs = coords.length - 1`。

**第 2 步：线段树**（2.7 节）。叶子数 `size` = ≥ `segs` 的最小 2 的幂；两个数组 `mx`、`add`，长度 `2·size`。

**第 3 步：把订单区间映射到基本段**

```java
public void add(long start, long end) {
    int lo = exactIndex(start);          // 二分：start 必须是已知端点，否则 IAE
    int hi = exactIndex(end);
    if (lo == hi) return;                // 空区间
    rangeAdd(1, 0, size - 1, lo, hi - 1, +1);    // [start, end) 覆盖基本段 lo..hi-1
}
```

**第 4 步：`liveAt(t)`** = 点查询。找 `t` 所在的基本段 `j = floorIndex(t)`（≤ t 的最大端点下标）；`t` 比所有端点小，或 `j >= segs`（≥ 最右端点，右端不含）→ 0；否则 `rangeMax(j, j)`。

**第 5 步：`maxIn(from, to)`**：要覆盖 `[from, to)` 的所有基本段：
* 第一个段：`from` 所在的段 `lo = max(0, floorIndex(from))`（`from` 在最左端点之前就从第 0 段开始）；
* 最后一个段：起点 `< to` 的最后一段 `hi = min(segs-1, lowerBound(to) - 1)`（`lowerBound` = 第一个 `≥ to` 的端点下标；`to` 本身不含，所以段起点 `== to` 的不算）；
* 范围伸出所有端点之外的部分活跃数是 0，所以最终结果 `max(0, rangeMax(lo, hi))`。

**第 6 步：`remove`**：和 `add` 一样，δ = −1。调用方保证只撤销加过的。

**复杂度**：构造 O(m log m)（排序）；每次 `add / remove / liveAt / maxIn` O(log m)，m ≤ 2n。

---

## 5. 逐段讲解法

### 5.1 数据类型（`OrderIntervals.java`）

```java
public enum Side { BUY, SELL }
public record Peak(int count, long time) {}
public sealed interface OrderEvent permits Place, Cancel {}
public record Place(long id, Side side, long start, long end) implements OrderEvent {
    public Place {
        Objects.requireNonNull(side, "side");
        if (start < 0) throw new IllegalArgumentException("negative start: " + start);
        if (end < start) throw new IllegalArgumentException("end < start: " + end + " < " + start);
    }
}
public record Cancel(long id, long time) implements OrderEvent { ... }
public record Report(Peak buy, Peak sell, Peak all) {}
```

* `Peak(0, 0)` 表示「从没有订单活着」：时间域是 `t >= 0`，最大值 0 在 t = 0 就达到，所以 `(0, 0)` 是**自洽的真话**，不是特殊哨兵值。
* 紧凑构造器里做所有单个对象能判断的校验：非法的 `Place` 构造不出来，`OnlineOverlap.place` 直接 `new Place(...)` 来复用这些检查。

### 5.2 `peakOf`——扫描线的核心

```java
static Peak peakOf(long[] starts, long[] ends, int n, boolean inclusive) {
    if (n == 0) return new Peak(0, 0);
    Arrays.sort(starts, 0, n);
    Arrays.sort(ends, 0, n);
    int best = 0; long bestTime = 0; int j = 0;
    for (int i = 0; i < n; i++) {
        long s = starts[i];
        while (j < n && (inclusive ? ends[j] < s : ends[j] <= s)) j++;
        int live = (i + 1) - j;
        if (live > best) { best = live; bestTime = s; }
    }
    return new Peak(best, bestTime);
}
```

* `Arrays.sort(a, 0, n)`：只排前 n 个，因为数组可能比有效数据长（`sweep` 里分配了 `intervals.length`，空区间被跳过后 `n` 更小）。
* 两个数组各自排序，是**原地**修改——所以 `sweep` 里的数组是**拷贝**出来的，调用者的 `long[][]` 不会被动。
* 只比较、不运算：`ends[j] <= s`，时间接近 `Long.MAX_VALUE` 也安全。

### 5.3 `analyze`

```java
for (OrderEvent e : events) {
    switch (e) {
        case Place p -> { if (places.putIfAbsent(p.id(), p) != null) throw new IllegalArgumentException("duplicate order id " + p.id()); }
        case Cancel(var id, var time) -> cancelAt.merge(id, time, Math::min);
    }
}
...
Lane lane = switch (p.side()) { case BUY -> buy; case SELL -> sell; };
lane.add(p.start(), end);
all.add(p.start(), end);
```

* 第一个 `switch` 是**语句**（每个 `case` 用 `->`，没有穿透 fallthrough）；第二个是**表达式**，穷尽 `Side` 枚举，不需要 `default`——以后 `Side` 加一个值（比如 `SHORT_SELL`），这行编译失败。
* `cancelAt.merge(id, time, Math::min)`：同一个订单多次撤单，保留最早的。
* `Lane` 是私有的小容器：两个 `long[]` 加计数，预分配 `places.size()`（最多这么多条），避免 `ArrayList<Long>` 的装箱。

### 5.4 `OnlineOverlap`

```java
void advance(long to) {
    if (live > committedMax) { committedMax = live; committedTime = lastTick; }   // 封账
    Map.Entry<Long, Integer> e;
    while ((e = expiries.firstEntry()) != null && e.getKey() <= to) {
        expiries.pollFirstEntry();
        live -= e.getValue();
        history.put(e.getKey(), live);      // 阶梯在结束时间处下降
    }
    lastTick = to;
}
```

* 每个车道有自己的 `lastTick`：`OnlineOverlap.advanceTo` 在时钟前进时对**所有**车道调用 `advance`，所以它们的 `lastTick` 总是等于全局 `now`。
* `firstEntry()` / `pollFirstEntry()`：TreeMap（`NavigableMap` / Java 21 的 `SequencedMap`）从有序一端取。
* `history.put(e.getKey(), live)`：每个折叠点都记一笔，所以 `floorEntry(t)` 在到期时刻也正确。注意「同一个到期时间有多个订单」：`expiries` 的值是计数，一次折叠减去全部，`history` 只记折叠后的结果（不会记「中间状态」）。

```java
public boolean cancel(long id, long time) {
    var o = orders.get(id);
    if (o == null) throw new IllegalArgumentException("cancel of unknown order " + id);
    if (time < now) throw new IllegalArgumentException("event out of order: " + time + " < " + now);
    advanceTo(time);
    boolean effective = o.end() > time;       // start <= now == time，所以 end > time 就是还活着
    if (effective) {
        var lane = lanes.get(o.side());
        lane.cancel(o.end());  all.cancel(o.end());
        lane.stamp();          all.stamp();
        orders.put(id, new Order(id, o.side(), o.start(), time));    // 用新 record 替换：end 缩短成 time
    }
    return effective;
}
```

* **校验在改状态之前完成**：未知 id、时间倒退都先抛，之后才 `advanceTo`；失败的调用不改变任何状态。
* `Order` 是 record（不可变），撤单用「新 record 替换旧的」：既避免可变状态，又让第二次撤单自动返回 `false`（`end == 第一次撤单时间 <= 新时间`）。
* `lane.cancel(end)` 里 `expiries.compute(end, (k, c) -> c == 1 ? null : c - 1)`：计数减 1，减到 0 返回 `null` 删除这个键（避免 `TreeMap` 里留下计数 0 的垃圾键，否则 `firstEntry` 会反复折叠 0）。

```java
public boolean apply(OrderIntervals.OrderEvent e) {
    return switch (e) {
        case OrderIntervals.Place(var id, var side, var start, var end) -> { place(id, side, start, end); yield true; }
        case OrderIntervals.Cancel(var id, var time) -> cancel(id, time);
    };
}
```

`switch` **表达式**，块分支用 `yield` 返回值；记录模式 `Place(var id, var side, var start, var end)` 直接解构四个字段。

### 5.5 `IntervalIndex`

```java
private void rangeAdd(int node, int nl, int nr, int l, int r, int delta) {
    if (l <= nl && nr <= r) { add[node] += delta; mx[node] += delta; return; }     // 整段覆盖：只记在这个结点
    int mid = (nl + nr) >>> 1;
    if (l <= mid) rangeAdd(2 * node, nl, mid, l, r, delta);
    if (r > mid)  rangeAdd(2 * node + 1, mid + 1, nr, l, r, delta);
    mx[node] = add[node] + Math.max(mx[2 * node], mx[2 * node + 1]);
}

private int rangeMax(int node, int nl, int nr, int l, int r) {
    if (l <= nl && nr <= r) return mx[node];
    int mid = (nl + nr) >>> 1;
    int best = Integer.MIN_VALUE;
    if (l <= mid) best = Math.max(best, rangeMax(2 * node, nl, mid, l, r));
    if (r > mid)  best = Math.max(best, rangeMax(2 * node + 1, mid + 1, nr, l, r));
    return best + add[node];     // 本结点还欠着的整体加数，孩子不知道，在这里补上
}
```

* 参数 `(node, nl, nr)` 表示「当前结点管下标区间 [nl, nr]」；`(l, r)` 是操作区间。
* `rangeMax` 最后的 `+ add[node]` 是整个设计的**关键一行**：删掉它，整体平移的标记就丢了。同样，`rangeAdd` 末尾 `mx[node] = add[node] + …` 里的 `add[node]` 也不能少。
* 递归深度 ≤ ⌈log₂ size⌉ ≈ 20，不会栈溢出。

```java
private int floorIndex(long x) { int i = Arrays.binarySearch(coords, x); return i >= 0 ? i : -i - 2; }
private int lowerBound(long x) { int i = Arrays.binarySearch(coords, x); return i >= 0 ? i : -i - 1; }
```

`Arrays.binarySearch` 的约定：找到返回下标；没找到返回 `-(插入点) - 1`，插入点是第一个大于 `x` 的元素的下标。所以 floor（≤ x 的最大下标）是插入点 − 1 = `-i - 2`；lowerBound（≥ x 的最小下标）就是插入点 = `-i - 1`。

---

## 6. Java 21 特性小课

### record 与紧凑构造器

`Peak`、`Place`、`Cancel`、`Report`、`Order` 都是 record。旧写法：`final class` + 私有字段 + 构造器 + getter + `equals/hashCode/toString`。
本题的好处：`new Peak(3, 5)` 这样的值可以直接按字段比较；`Place` 的紧凑构造器让「`end < start` 的订单」构造不出来。**不该用**：`Lane`（要频繁修改字段）就是普通 `final class`。

### sealed + 模式匹配 switch + 记录模式

`OrderEvent permits Place, Cancel`：

```java
// 旧写法
if (e instanceof Place) { Place p = (Place) e; ... }
else if (e instanceof Cancel) { Cancel c = (Cancel) e; ... }
else { throw new IllegalStateException(); }   // 编译器不知道这里不可能到达

// 新写法
switch (e) {
    case Place p -> ...
    case Cancel(var id, var time) -> ...       // 一步完成「判断类型 + 取字段」，不需要 default
}
```

编译器能证明穷尽，所以新增事件类型时所有 `switch` 编译失败，不会漏处理。

### switch 表达式与 `yield`

`Lane lane = switch (p.side()) { case BUY -> buy; case SELL -> sell; };`：表达式、无穿透、对枚举穷尽。块分支里用 `yield true;` 返回值。旧写法需要先声明 `Lane lane;` 再在每个 `case` 里赋值加 `break`，忘 `break` 就会穿透。

### Sequenced Collections：`TreeMap` 的两端操作

`firstEntry()`、`pollFirstEntry()`、`floorEntry()`：有序 Map 的统一两端接口（Java 21 起 `NavigableMap` 同时是 `SequencedMap`）。在线版用它们实现「到期折叠」。

### 文本块与 `var`

用文本块写多行订单脚本，比一串字符串拼接可读；`var` 只用在类型显然的局部变量（`var o = new OnlineOverlap();`）。

### 未命名模式 `_`（预览）

`e instanceof OrderIntervals.Place(var id, _, var s, var en)` 用 `_` 表示「这个字段不需要」。需要 `--enable-preview`。

---

## 7. 追问预演

**问：为什么同一时刻要先处理结束再处理开始？如果区间是闭的呢？**
* 思考：半开区间下 `end` 那一刻订单已经不活；`[1,3)` 和 `[3,5)` 是交接。
* 答：半开 `[s, e)`：事件排序 −1 在 +1 前，两数组写法是 `ends[j] <= s`。闭区间 `[s, e]`：`end` 那一刻仍然活着，同一时刻先开始后结束，写法是 `ends[j] < s`。先问清楚约定。
* 说出口：「先和面试官确认端点是否包含。我默认半开，这样 `[1,3)` 与 `[3,5)` 不重叠，对应事件排序里同一时刻先结束后开始；闭区间则反过来。」

**问：能用堆解吗？和排序数组比？**
* 答：能（Meeting Rooms II）：按 start 排序，最小堆存结束时间，`while (peek <= s) poll`，堆最大尺寸即答案。O(n log n)，但有对象与堆的常数，而且按方向、撤单、「最早时刻」扩展不如两数组直接。
* 说出口：「堆也行；我用两个排序数组是因为没有分配、tie 规则一眼可见。」

**问：撤单怎么处理？撤单在下单前到达呢？**
* 答：撤单 = 把 `end` 改成 `min(end, 撤单时间)`；批量版先收集 `Place` 与 `Cancel`，再统一计算，所以到达顺序无所谓；在线版事件已经按时间排序，撤单一定在下单之后（找不到订单就是非法输入，抛异常）。撤单时间 ≤ start 则区间为空。
* 说出口：「撤单就是缩区间。批量版先收集再算，所以顺序无关；同一订单多次撤单取最早。」

**问：在线版为什么不能每来一个事件就重新排序？时间复杂度多少？**
* 答：事件已按时间到达，不需要排序；用差分数组的思想，未来的结束放进 `TreeMap`，到时取出，每个事件 O(log n)。重排是 O(n log n)/事件，总 O(n² log n)。
* 说出口：「未来的结束时间放有序 map，时钟走到哪就折叠到哪，每个事件 log n。」

**问：「到现在为止的最大重叠」在同一时间戳里先加后撤会怎样？**
* 答：见 4.3 节。必须等时间戳「过去」后才封账；当前时间戳的值在查询时临时比较。
* 说出口：「同一时刻的事件我当一批处理：最大值在时钟前进时才记入，当前这一刻只在查询时参与比较，这样同刻的撤单能追溯修正。」

**问：能不能回答「未来某时刻 t 有几张单活着」？**
* 答：见 4.3 节：`live` 减去 `expiries` 中键 ≤ t 的总和。TreeMap 遍历是 O(k)。要 O(log n)：离线压缩坐标 + Fenwick / 线段树；在线未知坐标 → 需要带子树和的平衡树（自写或 `ConcurrentSkipListMap` 做不到前缀和）。注意它只是**预测**：之后可能有撤单让结果变小，所以业务上要标明「不含未来撤单」。

**问：什么时候该用线段树，而不是扫描线？**
* 答：扫描线适合「一次性读完，求全局最大」，比线段树快（同样 30 万个区间，21 ms 对 100 ms）。线段树适合：更新顺序任意、增删交错、区间查询（`maxIn`）、需要在线反复查询。
* 说出口：「只要全局最大，我用扫描线；需要增删交错或区间查询才上线段树，并先做坐标压缩。」

**问：线段树的懒标记为什么不用下推？什么时候必须下推？**
* 答：2.7 节。标记永久化：`mx` 含本结点及子树的加数，不含祖先的；查询回溯时补上沿途的 `add`。适用于「区间加 + 区间最大/最小」。「区间赋值」「区间和」需要知道区间长度或会覆盖旧标记，必须下推。

**问：坐标压缩之后，如果事先不知道所有坐标呢？**
* 答：离线（读完所有输入）才能压缩。在线且坐标未知：用动态开点线段树（只创建被访问到的结点，内存 O(n log C)，C 是坐标范围 10¹⁸ → 深度 60），或者平衡树（自写 order-statistic 树）。
* 说出口：「动态开点：值域直接是 [0, 2⁶⁰)，只在用到时才创建结点，深度 60。」

**问：怎么处理每张订单有数量（quantity）？**
* 答：+1/−1 换成 +qty/−qty，`live` 改成 `long`（防溢出，用 `Math.addExact`）；最大值语义变成「在簿的最大总量」。

---

## 8. 常见误区

| 很多人会这样写 | 为什么错 | 正确写法 |
|---|---|---|
| 事件只按时间排序 | 同一时刻 +1/−1 的先后不确定，`[1,3)`+`[3,5)` 可能得 2 | 排序键 `(time, delta)`，−1 在前；或两数组 `ends[j] <= s` |
| 把 `end` 当作包含的 | `[1,3)` 与 `[3,5)` 被算成重叠 | 先确认端点约定；半开用 `<=`，闭区间用 `<` |
| `all.count = buy.count + sell.count` | 买卖峰值时刻不同，会虚高 | 单独扫描全部订单 |
| 在线版每次 `place` 后立刻更新最大值 | 同一时间戳内被撤的订单污染最大值 | 时钟前进时封账，当前时间戳查询时临时比较 |
| 撤单只从计数里减 1，忘了从 `expiries` 里删它原来的结束时间 | 之后到期时再减一次，计数变成负的 | 撤单同时撤掉未来的 −1 |
| `expiries` 计数减到 0 不删键 | `firstEntry` 反复折叠 0 值，history 出现无意义的点 | `compute` 里减到 0 返回 `null` |
| 撤单时间 ≥ 计划结束时间仍然「生效」 | 订单已经结束，撤单应返回 `false` | `end > time` 才生效 |
| 先改状态后校验 | 失败的调用留下半修改的状态 | 先校验（未知 id、时间倒退），再改 |
| `mid = (lo + hi) / 2` | 极大值溢出成负数 | `(lo + hi) >>> 1`；坐标只比较 |
| 线段树 `rangeMax` 不加 `add[node]` | 整体平移的标记丢了 | 回溯时 `best + add[node]` |
| 区间 `[s, e)` 映射成基本段 `idx(s)..idx(e)` | 多算了 `e` 所在的段 | `idx(s)..idx(e) - 1` |
| 压缩坐标时不去重 | 同一个端点占两个下标，出现长度为 0 的基本段 | 排序后去重 |
| 对输入数组原地排序 | 调用者的数据被改动 | 拷贝后再排 |

---

## 9. 自测题

1. 订单 `[0,4)`、`[2,6)`、`[4,8)`、`[6,10)` 的最大重叠和最早时刻是多少？如果改成闭区间 `[s, e]` 呢？
2. 事件 `(5,+1) (5,-1) (5,+1)` 按「−1 在前」排序后是什么顺序？这个时刻最终的计数（假设之前是 0）是多少？
3. 在线版：`place(1,BUY,3,10)`、`place(2,BUY,4,6)`、`cancel(1,5)`、`advanceTo(6)`。依次写出 `liveNow()`、`peak()`、`liveAt(4)`、`liveAt(5)`。
4. 坐标 `[10, 50, 20, 50, 80]` 压缩后是什么？区间 `[20, 80)` 覆盖哪几个基本段？
5. （思考）把线段树改成「区间加 + 区间**求和**」，标记永久化还能直接用吗？需要改什么？
6. （小编程）只用一个排序数组 `long[] ev`（把结束编码成负数或用别的编码），写出 Part 1 的扫描线。提示：同一时刻要结束在前。

<details><summary>答案</summary>

1. `[0,4)`、`[2,6)`、`[4,8)`、`[6,10)`：时刻 2–3 有 `[0,4)`、`[2,6)` 两张；时刻 4–5 有 `[2,6)`、`[4,8)` 两张（`[0,4)` 在 4 结束）；时刻 6–7 有 `[4,8)`、`[6,10)`。最大重叠 **2**，最早在 **t=2**。闭区间：时刻 4 有 `[0,4]`、`[2,6]`、`[4,8]` 三张 → 最大 **3**，最早 t=4。
2. 排序后：`(5,-1) (5,+1) (5,+1)`。之前是 0，先 −1 会变成 −1（说明输入本身不一致：没有对应开始的结束），再两个 +1 → 1。正常输入里每个 −1 都有在它之前的 +1。
3. `place(1,BUY,3,10)`：live=1。`place(2,BUY,4,6)`：live=2，`expiries {6:1,10:1}`。`cancel(1,5)`：时钟到 5，订单 1 的 `end=10>5` 生效，live=1，`expiries {6:1}`（撤掉 10）。`advanceTo(6)`：折叠 6，live=0。结果：`liveNow()`=0；`peak()`=(2,4)（t=4 时两张都活着）；`liveAt(4)`=2；`liveAt(5)`=1（订单 1 在 5 被撤，订单 2 还活着）。
4. 排序去重：`[10, 20, 50, 80]`（m=4，3 个基本段 `[10,20) [20,50) [50,80)`）。`[20, 80)` 覆盖 `idx(20)=1` 到 `idx(80)-1=2`，即后两个基本段。
5. 不能直接用。求和需要「区间长度 × δ」，标记要带上长度，且查询回溯时要乘以「查询与结点区间的交集大小」；常见做法仍用下推（push-down）。永久化也可以，但需要在每个结点额外记录 `sum` 与区间长度，查询时累加 `add[node] * overlapLength`。
6. 例如把开始编码成 `2*t + 1`、结束编码成 `2*t`（`t` 不能太大，否则溢出——这正是本题坐标高达 `Long.MAX_VALUE` 时这种编码不可行的原因），排序后同一时刻结束（偶数）在开始（奇数）前。这个技巧在小坐标时可用；大坐标请用两个数组或 `(time, delta)` 比较器。

</details>

---

「延伸」LeetCode 253 / 731 / 732（区间重叠家族）。
