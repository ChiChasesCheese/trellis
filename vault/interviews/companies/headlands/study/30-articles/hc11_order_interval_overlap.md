# hc11 讲义 · 订单区间最大重叠：从「逐个时刻数」到扫描线、在线差分、坐标压缩与线段树

> 读者：会写基本 Java（类、方法、循环、`ArrayList` / `HashMap`），没学过扫描线、差分数组、线段树、坐标压缩；每个概念从零讲。

---

## 1. 问题是什么

每张订单（order）有**生命周期**：`start` 进入订单簿，`end` 离开（过期或被撤）。

* **Part 1**：同时「活着」的订单最多多少张（最大重叠，maximum overlap）？
* **Part 2**：分**买单**（BUY）和**卖单**（SELL）各求最大重叠；订单可**撤单**（cancel），区间被截短。
* **Part 3**：订单和撤单**实时**一个个到来，随时回答「到现在最大重叠多少」「t 时刻有几张单活着」。
* **Part 4**：时间戳是纳秒（高达 10¹⁸），不能开数组；订单可任意顺序加入和撤销，问「某段时间内的最大重叠」。

### 手算一遍（Part 1）

A = [1,5)，B = [2,6)，C = [4,8)；`[1,5)` 指时刻 1–4 活着，5 已结束（**左闭右开**，2.1）。

```
时刻:   0  1  2  3  4  5  6  7  8
A=[1,5)    ■  ■  ■  ■
B=[2,6)       ■  ■  ■  ■
C=[4,8)             ■  ■  ■  ■
活着数:  0  1  2  2  3  2  1  1  0
```

最大重叠 **3**，最早在时刻 **4**（A、B、C 同时活着）。

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

* BUY（1, 2, 5）：时刻 5 三张都活着 → **3，t=5**。
* SELL（3, 4）：时刻 4 两张都活着 → **2，t=4**。
* 全部：时刻 4 是订单 1, 2, 3, 4 → 4；时刻 5 是 1, 2, 3, 5 → 也是 4。取最早 → **4，t=4**。没有撤单时刻 5 有五张，**撤单改变了答案**。买方峰值（t=5）和卖方峰值（t=4）**不同时刻**，所以「全部」的 4 不等于 3 + 2。

---

## 2. 前置知识

> 复杂度速记：`O(n)` 线性；`O(log n)` n 翻倍只多一步；`O(n²)` 每对都处理；`O(1)` 与 n 无关。

### 2.1 半开区间 `[start, end)`

包含 `start`、不含 `end`。A 在 3 结束、B 在 3 开始是「交接」不是重叠；闭区间会算重叠，半开自然得「不重叠」。其他好处：长度 = `end - start`；`[0,3)`、`[3,5)` 首尾相接不重叠不留空；空区间就是 `start == end`。编程里几乎所有区间都半开（`Arrays.copyOfRange`、`String.substring`、`for (i = lo; i < hi; i++)`）。

t 是否活着：`start <= t && t < end`。⚠️ 面试先问「两端是否包含？」：`[1,3]` 和 `[3,5]` 闭区间下重叠、半开下不重叠，答案可差 1。这里 `maxOverlapInclusive` 是闭区间版本。

### 2.2 扫描线（sweep line）

把「区间」变成「事件」，沿时间轴**扫**，边扫边维护计数器。重叠数只在端点变化（开始 +1，结束 −1），只需按序处理 2n 个端点事件：每个区间 `[s, e)` 生成 `(s, +1)` 和 `(e, -1)`，按时间排序，依次加 delta 并记录最大值。

```
事件:  (1,+1) (2,+1) (4,+1) (5,-1) (6,-1) (8,-1)      ← A=[1,5) B=[2,6) C=[4,8)
计数:     1      2      3      2      1      0
最大值 = 3，出现在处理 (4,+1) 之后，即时刻 4
```

### 2.3 同一时刻：先结束，再开始（tie 规则）

时间相同时规定：**−1（结束）排在 +1（开始）前面**。看 `[1,3)` 和 `[3,5)`：

```
事件: (1,+1) (3,+1) (3,-1) (5,-1)
如果同一时刻 +1 先：计数 1, 2, 1, 0  → 最大值 2  ✗（错）
如果同一时刻 -1 先：事件 (1,+1) (3,-1) (3,+1) (5,-1)  计数 1, 0, 1, 0 → 最大值 1  ✓
```

时刻 3 订单 1 已死（`end` 不含），订单 2 刚出生，任何时刻只有一张活着；先处理结束计数器才不会在「中间状态」虚高。实现：事件 `(time, delta)` 先比 `time` 再比 `delta`，−1 < +1 天然满足。**经典坑**：只按 `time` 排序，平局顺序不确定——结果时对时错。

### 2.4 差分数组（difference array）与前缀和

`live[t]` 是 t 时刻活着的订单数。**差分数组** `d[t] = live[t] - live[t-1]` 记录「相对上一时刻的**变化**」，`live[t] = d[0] + … + d[t]`（**前缀和**）。给区间 `[s, e)` 全部 +1，直接改 `live` 要改 `e - s` 格，差分只改两格：`d[s] += 1`、`d[e] -= 1`；n 个区间 2n 格，最后一遍前缀和还原。扫描线的本质就是这个——事件列表是**稀疏**差分数组（只记非零项）。

```
下标 t:    0   1   2   3   4   5   6   7   8
d[t]:      0  +1  +1   0  +1  -1  -1   0  -1      ← A=[1,5) B=[2,6) C=[4,8)
前缀和:    0   1   2   2   3   2   1   1   0       = live[t]
```

### 2.5 有序 Map：`TreeMap`

按键排序的 `Map`（红黑树，自平衡二叉搜索树），`put / get / remove` 都 O(log n)，支持 `firstEntry()`、`pollFirstEntry()`（删除并返回最小）、`floorEntry(x)`（≤ x 的最大键）。Part 3 用 `firstEntry / pollFirstEntry` 按时间取最早到期的订单，用 `floorEntry(t)` 找「不晚于 t 的最近一次变化」。

```java
var expiries = new TreeMap<Long, Integer>();      // 结束时间 → 在那一刻结束的订单数
expiries.merge(10L, 1, Integer::sum);             // 记一笔
var e = expiries.firstEntry();                    // 最早的结束
expiries.pollFirstEntry();                        // 取出并删除
var f = history.floorEntry(7L);                   // ≤ 7 的最大键对应的条目（没有则 null）
```

### 2.6 sealed 事件与模式匹配

`OrderEvent` 是 `sealed interface ... permits Place, Cancel`。`switch (e) { case Place p -> …; case Cancel(var id, var time) -> … }` 由编译器检查穷尽。

### 2.7 线段树（segment tree）与懒标记——从零推出来

**问题**：m 个格子（初始 0），支持 `rangeAdd(l, r, δ)`（第 l 到 r 个格子都加 δ）和 `rangeMax(l, r)`（区间最大值）。

**最笨**：数组循环，q 次共 O(q·m)；m = 2×10⁵、q = 3×10⁵ 是 6×10¹⁰。**想法 1：分层存每段答案。** 整个数组分两半，每半再分……直到单个格子，形成二叉树，每个结点管一个区间，存「该区间最大值」。

```
m = 4 个格子（下标 0..3），结点编号从 1 开始，结点 i 的孩子是 2i 和 2i+1：

                  结点1 [0..3]
               /                \
        结点2 [0..1]          结点3 [2..3]
         /       \             /       \
   结点4 [0]  结点5 [1]    结点6 [2]  结点7 [3]       ← 叶子 = 单个格子
```

* **查询** `rangeMax(l, r)`：从根开始，结点区间**完全落在** [l, r] 里就直接返回它的最大值，否则往有重叠的孩子递归取最大。一个查询最多被拆成 O(log m) 个「完全落在里面」的结点（每层最多访问 4 个）。
* **点更新**：改叶子，沿路径回根，每个结点重新取两孩子最大值，O(log m)。

**问题 2：区间加？** 改 r−l+1 个叶子再更新祖先，又回到 O(m)。**想法 2：懒标记（lazy propagation）——「先欠着，需要时再还」。** 结点区间**完全落在**更新区间里时不往下走，只记一笔 `add[node] += δ`，同时把它的最大值也加 δ；孩子暂时不知道。**经典做法（下推 push-down）**：以后要往该结点**内部**走时，先把欠的账分给两个孩子，自己清零。

**更简单：标记永久化（不下推）。** 「整段加 δ」只是平移，不影响*相对关系*，所以**永远不下推**：
* 每结点两个数：`add[node]` 是整个区间被整体加了多少（只在本结点生效）；`mx[node]` 是区间最大值，**已含**本结点和后代的 `add`，**不含**祖先的。
* 更新：完全覆盖的结点 `add[node] += δ; mx[node] += δ`；部分覆盖的递归孩子，再 `mx[node] = add[node] + max(mx[左], mx[右])`。
* 查询：完全覆盖的返回 `mx[node]`；部分重叠的递归孩子取最大，**最后加上本结点 `add[node]`**（这笔平移对结点内所有格子生效，孩子不知道，要在这里补）。

**手算：4 个格子，加区间 [0,2] 再加 [1,3]**（初始全 0）：

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

每操作每层最多访问常数个结点，树高 ⌈log₂ m⌉，O(log m)；叶子数补到 2 的幂 `size`，两个数组各 `2·size` 个 `int`。**永久化只适用于「加法 + 取最大」这类平移不改相对大小的情形**；「区间赋值」或「区间和」（需区间长度才能乘 δ）要完整下推。

### 2.8 坐标压缩（coordinate compression）

把很大或稀疏的坐标映射成保持大小顺序的小整数下标。时间戳可能 10¹⁸，线段树开不出数组；但 n 张订单只有 2n 个**端点**，活跃数只在端点变化，相邻端点之间所有时刻活跃数相同，只关心端点。

端点排序去重得 `c[0] < … < c[m-1]`；相邻两端点之间 `[c[j], c[j+1])` 是**基本段**，共 m−1 个，每段活跃数为常数。`[s, e)` 恰好覆盖基本段 `idx(s)` 到 `idx(e)-1`（`idx(x)` 是 x 在 `c` 里的下标，二分查找）。

```
订单 [10,50) [20,60) [40,80)  → 端点排序去重 c = [10, 20, 40, 50, 60, 80]（m=6）
基本段:  seg0=[10,20)  seg1=[20,40)  seg2=[40,50)  seg3=[50,60)  seg4=[60,80)
[10,50) 覆盖 idx(10)=0 .. idx(50)-1=2  → seg0..seg2
[20,60) 覆盖 idx(20)=1 .. idx(60)-1=3  → seg1..seg3
[40,80) 覆盖 idx(40)=2 .. idx(80)-1=4  → seg2..seg4
每段活跃数:  1   2   3   2   1      最大 3（seg2 = [40,50)）
```

Java：`Arrays.sort`、手工去重、`Arrays.binarySearch`（找到返回下标，没找到返回 `-(插入点) - 1`，所以「≤ x 的最大下标」是 `-i - 2`，「≥ x 的最小下标」是 `-i - 1`）。

### 2.9 溢出：只比较，不运算

时间戳可能接近 `Long.MAX_VALUE`，`end - start`、`(lo + hi) / 2` 会静默溢出成负数（`Math.addExact` 则抛 `ArithmeticException`）。原则：**时间只比较，不做运算**。线段树下标是压缩后的小 `int`，用 `(nl + nr) >>> 1` 取中点。

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

O(T·n)，**T 是时间戳的数值范围，不是订单数**；纳秒时间戳 T ≈ 10¹⁸，永远跑不完。仍可在小坐标上做**对拍**。

### 3.2 只检查开始时刻

重叠数只会在某个区间的 `start` 处达到新高，所以只检查每个 `start`：

```java
for (long[] a : intervals) {
    int live = 0;
    for (long[] b : intervals) if (b[0] <= a[0] && a[0] < b[1]) live++;
    best = Math.max(best, live);
}
```

O(n²)，n = 10⁶ 时几小时。与时间戳范围无关，但仍太慢。

### 3.3 Part 3/4 的笨办法

在线版：每来一个事件把全部订单重新交给 Part 2 的 `analyze`，总 O(n² log n)，但可**对每个前缀对拍在线版**。大坐标：每次查询线性扫描 O(q·n)。

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

O(n log n)，正确，但每个事件一个 `long[]`：2n 个小数组，缓存不友好，排序要比较器间接比较。比较器第二关键字是 `delta`（−1 < +1），即 2.3 的 tie 规则。

**第 2 步：去掉事件对象——两个已排序数组**

开始事件只有 +1，结束事件只有 −1。所有 `start` 放一个 `long[]` 排序，所有 `end` 放另一个排序，**像归并一样**一起扫：

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

* 「同一时刻先结束后开始」就是 `ends[j] <= s`（闭区间改成 `<`）。最大值只可能出现在某个 `start` 上，所以只在 `start` 处计算。
* `Arrays.sort(long[])` 是原始类型双轴快排，无装箱无比较器，100 万个区间约 80 ms。同一个 `s` 重复时 `live` 逐个增大，严格 `>` 更新最优。

**第 3 步：最早时刻**：`if (live > best) { best = live; bestTime = s; }`——严格 `>` 保留最早。

**第 4 步：空区间与非法输入**：`start == end` 从没活过，直接跳过（不跳也不错，更清楚）；`end < start`、`start < 0`、行长度不是 2 → `IllegalArgumentException`。

**另一种经典解法：堆**（Meeting Rooms II）：按 start 排序，最小堆存活着订单的结束时间；来新订单先 `while (heap.peek() <= s) heap.poll()` 再 `heap.add(e)`，堆大小的最大值是答案。O(n log n) 同样正确。选两数组因为：无堆对象开销、tie 规则一眼可见、易扩展到「按方向」「带撤单」。

### 4.2 Part 2：买卖方向 + 撤单

撤单只是**修改区间**：`end` 改成 `min(end, cancelTime)`。

1. 第一遍扫事件：`Place` 存进 `HashMap<id, Place>`（重复 id 报错）；`Cancel` 存进 `HashMap<id, 最早撤单时间>`（`merge(id, time, Math::min)`）。
2. 检查每个撤单 id 都有对应 `Place`（先收集后处理，**顺序无所谓**）。
3. 每个 `Place` 的有效区间 `[start, min(end, cancelTime))`；有效结束 `<= start` → 跳过。
4. 按方向分到三个「车道」（BUY、SELL、ALL），各自做 4.1 的扫描。

O(n log n)。ALL 车道必须**单独扫描**，不能用 `buy.count + sell.count`（峰值时刻不同，1 节例子 3 + 2 ≠ 4）。`OrderEvent` 是 sealed，`switch` 不写 `default`，新增 `Amend` 时所有没处理的 `switch` 编译报错。

### 4.3 Part 3：在线版

事件一个个到来，不能先读完再排序扫描。事件按时间到达，「排序」已由时间本身做完，要**边到边扫**。`live` 在时刻 `now` 的值需要知道「哪些订单已在 now 之前结束」：订单的计划结束时间在未来，用按结束时间排序的 `expiries: TreeMap<结束时间, 订单数>`（2.5），`now` 前进时把到期的取出来。这其实是差分数组的**未来部分** `d[end] -= 1`；过去部分已累加进 `live`。

**数据结构（每个车道）**：

| 字段 | 含义 |
|---|---|
| `expiries` | `TreeMap`，结束时间 → 在这一刻结束的订单数（未来的 −1） |
| `live` | 当前（`now`）活着的订单数 |
| `history` | `TreeMap`，时间 → 该时刻的活跃数（只记录**变化点**，阶梯函数） |
| `committedMax` / `committedTime` | 已经「过去」的时间戳里的最大值及其最早时刻 |

**事件处理**：

* `place(id, side, start, end)`：先 `advanceTo(start)`，再 `live++`、`expiries[end] += 1`、`history[now] = live`。
* `cancel(id, time)`：先 `advanceTo(time)`；若 `end > time`（还活着）：`live--`、`expiries[end] -= 1`（从未来差分里撤掉）、`history[now] = live`，并把订单的 `end` 改成 `time`（再撤就发现「已结束」→ 返回 `false`）。
* `advanceTo(t)`（`t > now`）：先「封账」当前时间戳（下文），再把 `expiries` 里所有键 `<= t` 的**依次** `pollFirstEntry`：`live -= count`，`history[键] = live`。

三个车道各一份，每个事件更新其方向车道和 ALL 车道。

**陷阱：同一时间戳内先加后撤**。`place(1,BUY,5,9)`、`place(2,BUY,5,9)`、`cancel(1,5)`，时间戳都是 5：

```
place 1 @5 : live=1
place 2 @5 : live=2          ← 如果此刻就把「最大值=2」记下来
cancel 1 @5: live=1          ← 订单 1 的有效区间是 [5,5)，空，从没活过
```

真正答案是最大重叠 1；若每次 `place` 后立即更新最大值，就被瞬时的 2 污染。**解法：封账（commit）。** 一个时间戳**过去**之后（时钟前进到更大时间）才把它的最终活跃数记入 `committedMax`；当前时间戳的值只在查询时临时参与比较：

```java
// advance(to)：时钟从 lastTick 走到 to
if (live > committedMax) { committedMax = live; committedTime = lastTick; }   // 给过去的时间戳封账
...                                                                           // 然后折叠到期订单
// peak()
return live > committedMax ? new Peak(live, lastTick) : new Peak(committedMax, committedTime);
```

严格 `>`：相等时较早（已封账）的获胜。只在时钟前进时封账就够：两个相邻事件时间戳之间活跃数只会**下降**（只有到期），所以全局最大值一定出现在某个有事件的时间戳的**最终**值上。

**走一遍 Part 2 样例（ALL 车道）：**

| 事件 | 动作 | `live` | `expiries`（结束时间→数量） | 已封账最大值 | `peak()` |
|---|---|---|---|---|---|
| place 1 @0 [0,10) | live++ | 1 | {10:1} | (0, 0) | (1, 0) |
| place 2 @2 [2,8) | 封账 (1,0)；live++ | 2 | {8:1, 10:1} | (1, 0) | (2, 2) |
| place 3 @3 [3,6) | 封账 (2,2)；live++ | 3 | {6:1, 8:1, 10:1} | (2, 2) | (3, 3) |
| place 4 @4 [4,12) | 封账 (3,3)；live++ | 4 | {6,8,10,12 各 1} | (3, 3) | (4, 4) |
| place 5 @5 [5,9) | 封账 (4,4)；live++ | 5 | {6,8,9,10,12 各 1} | (4, 4) | (5, 5) |
| cancel 4 @5 | 同时间戳；live--，撤掉 {12} | 4 | {6,8,9,10 各 1} | (4, 4) | **(4, 4)** |
| cancel 2 @6 | 封账：live=4 不 > 4；折叠 6：live=3；撤 2：live--，撤掉 {8} | 2 | {9:1, 10:1} | (4, 4) | (4, 4) |

第 5 行 `peak()` 是 (5,5)，第 6 行同一时间戳撤单后变 (4,4)——「追溯修正」，与 Part 2 批量版一致。**可对每个前缀用批量版对拍。**

**`liveAt(t)`**：`history.floorEntry(t)`——不晚于 t 的最近变化点，其值就是 t 时刻活跃数（阶梯函数）；无这样的点 → 0。O(log n)。

**为何不支持 `t > now`（预测）？** 活跃数 = `live` −（`expiries` 里键 ≤ t 的项之和），TreeMap 遍历这些键 O(k)，没有 O(log n) 前缀和。要 O(log n)：提前知道所有结束时间 → 坐标压缩 + Fenwick/线段树（Part 4）；在线且坐标未知 → 自写带子树和的平衡树。面试可答「O(k) 朴素版，或离线压缩坐标后线段树」。

### 4.4 Part 4：坐标压缩 + 线段树

扫描线答「全局最大」是最优的（30 万个 10¹⁸ 量级区间，扫描线 21 ms，建线段树索引 100 ms）。线段树值得用于：1. **更新顺序任意**（先撤后加、`add` 与 `remove` 交错），扫描线必须一次读完；2. **区间查询**「[from, to) 内最大重叠」，线段树 O(log n)。

**第 1 步：坐标压缩**（2.8）：`IntervalIndex(long[] coordinates)` 排序去重得 `coords`，基本段数 `segs = coords.length - 1`。**第 2 步：线段树**（2.7）：叶子数 `size` = ≥ `segs` 的最小 2 的幂；两个数组 `mx`、`add`，长度 `2·size`。**第 3 步：订单区间映射到基本段**

```java
public void add(long start, long end) {
    int lo = exactIndex(start);          // 二分：start 必须是已知端点，否则 IAE
    int hi = exactIndex(end);
    if (lo == hi) return;                // 空区间
    rangeAdd(1, 0, size - 1, lo, hi - 1, +1);    // [start, end) 覆盖基本段 lo..hi-1
}
```

**第 4 步：`liveAt(t)`** = 点查询：`j = floorIndex(t)`；`t` 比所有端点小或 `j >= segs`（≥ 最右端点，右端不含）→ 0；否则 `rangeMax(j, j)`。
**第 5 步：`maxIn(from, to)`**：第一个段 `lo = max(0, floorIndex(from))`；最后一个段（起点 `< to`）`hi = min(segs-1, lowerBound(to) - 1)`（`lowerBound` = 第一个 `≥ to` 的端点下标）；伸出端点之外的部分活跃数为 0，结果 `max(0, rangeMax(lo, hi))`。
**第 6 步：`remove`**：与 `add` 一样，δ = −1（调用方保证只撤销加过的）。

构造 O(m log m)；每次 `add / remove / liveAt / maxIn` O(log m)，m ≤ 2n。

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

* `Peak(0, 0)` 表示「从没有订单活着」：时间域 `t >= 0`，最大值 0 在 t = 0 就达到，是**自洽的真话**而非哨兵值。
* 紧凑构造器做单对象校验：非法 `Place` 构造不出来，`OnlineOverlap.place` 直接 `new Place(...)` 复用。

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

* `Arrays.sort(a, 0, n)` 只排前 n 个（数组可能比有效数据长，空区间跳过后 `n` 更小）；排序**原地**，所以 `sweep` 里是**拷贝**，不动调用者的 `long[][]`。
* 只比较不运算：`ends[j] <= s`，时间接近 `Long.MAX_VALUE` 也安全。

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

* 第一个 `switch` 是**语句**，第二个是**表达式**，穷尽 `Side` 枚举不需 `default`——`Side` 加值时这行编译失败。
* `Lane` 是私有小容器：两个 `long[]` 加计数，预分配 `places.size()`，避免 `ArrayList<Long>` 装箱。

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

* 时钟前进时 `OnlineOverlap.advanceTo` 对**所有**车道调用 `advance`，所以各车道 `lastTick` 总等于全局 `now`。
* `history.put(e.getKey(), live)`：每个折叠点都记一笔，`floorEntry(t)` 在到期时刻也正确。同一到期时间有多个订单时，`expiries` 的值是计数，一次折叠减去全部，`history` 只记折叠后的结果。

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

* **校验在改状态之前**：未知 id、时间倒退先抛，之后才 `advanceTo`，失败的调用不改变任何状态。
* `Order` 是不可变 record，撤单用「新 record 替换旧的」，第二次撤单自动返回 `false`（`end == 第一次撤单时间 <= 新时间`）。
* `expiries.compute(end, (k, c) -> c == 1 ? null : c - 1)`：计数减到 0 返回 `null` 删除该键，否则 `firstEntry` 会反复折叠 0。

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

* `(node, nl, nr)` 表示「当前结点管下标区间 [nl, nr]」，`(l, r)` 是操作区间。
* `rangeMax` 最后的 `+ add[node]` 是**关键一行**，删掉整体平移的标记就丢了；`rangeAdd` 末尾 `mx[node] = add[node] + …` 里的 `add[node]` 也不能少。递归深度 ≤ ⌈log₂ size⌉ ≈ 20。

```java
private int floorIndex(long x) { int i = Arrays.binarySearch(coords, x); return i >= 0 ? i : -i - 2; }
private int lowerBound(long x) { int i = Arrays.binarySearch(coords, x); return i >= 0 ? i : -i - 1; }
```

`binarySearch` 没找到时返回 `-(插入点) - 1`（插入点 = 第一个大于 `x` 的元素下标），所以 floor 是插入点 − 1 = `-i - 2`，lowerBound 是插入点 = `-i - 1`。

---

## 6. Java 21 特性小课

### record 与紧凑构造器

`Peak`、`Place`、`Cancel`、`Report`、`Order` 都是 record（旧写法：`final class` + 字段 + 构造器 + getter + `equals/hashCode/toString`）：`new Peak(3, 5)` 可直接按字段比较，`Place` 的紧凑构造器让「`end < start`」构造不出来。**不该用**：`Lane`（频繁改字段）是普通类。

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

编译器能证明穷尽，新增事件类型时所有 `switch` 编译失败，不会漏处理。

### switch 表达式与 `yield`

`Lane lane = switch (p.side()) { case BUY -> buy; case SELL -> sell; };`：表达式、无穿透、对枚举穷尽；块分支里 `yield true;`。旧写法要先声明 `Lane lane;` 再每个 `case` 赋值加 `break`，忘 `break` 就穿透。

### Sequenced Collections、文本块、`var`、`_`

`firstEntry()`、`pollFirstEntry()`、`floorEntry()` 是有序 Map 的统一两端接口（Java 21 起 `NavigableMap` 同时是 `SequencedMap`）。文本块写多行订单脚本更可读；`var` 只用在类型显然处。`e instanceof OrderIntervals.Place(var id, _, var s, var en)` 的 `_` 表示不需要该字段，需 `--enable-preview`。

---

## 7. 追问预演

**问：为什么同一时刻先处理结束再处理开始？闭区间呢？**
* 半开区间下 `end` 那一刻订单已不活，`[1,3)` 与 `[3,5)` 是交接。半开 `[s, e)`：事件排序 −1 在 +1 前，两数组写法 `ends[j] <= s`；闭区间 `[s, e]`：`end` 那一刻仍活着，同一时刻先开始后结束，写法 `ends[j] < s`。先问清约定。
* 说出口：「先确认端点是否包含。我默认半开，`[1,3)` 与 `[3,5)` 不重叠，对应同一时刻先结束后开始；闭区间反过来。」

**问：能用堆解吗？和排序数组比？**
* 能（Meeting Rooms II），O(n log n)，但有对象和堆的常数，扩展到按方向、撤单、「最早时刻」不如两数组直接。

**问：撤单怎么处理？撤单在下单前到达呢？**
* 撤单 = `end` 改成 `min(end, 撤单时间)`；批量版先收集再算，到达顺序无所谓；在线版事件已按时间排序，撤单必在下单之后（找不到订单是非法输入）。撤单时间 ≤ start 则区间为空；同一订单多次撤单取最早。

**问：在线版为什么不能每来一个事件就重新排序？复杂度？**
* 事件已按时间到达；未来的结束放进 `TreeMap`，到时取出，每个事件 O(log n)。重排是 O(n log n)/事件，总 O(n² log n)。

**问：「到现在为止的最大重叠」在同一时间戳内先加后撤会怎样？**
* 4.3：必须等时间戳「过去」后才封账；当前时间戳的值在查询时临时比较，同刻撤单就能追溯修正。

**问：能回答「未来某时刻 t 有几张单活着」吗？**
* 4.3：`live` 减去 `expiries` 中键 ≤ t 的总和，TreeMap 遍历 O(k)。要 O(log n)：离线压缩坐标 + Fenwick / 线段树；在线未知坐标 → 带子树和的平衡树。它只是**预测**：之后撤单可能让结果变小，业务上要标明「不含未来撤单」。

**问：什么时候用线段树而不是扫描线？**
* 扫描线适合「一次读完求全局最大」，更快（30 万区间，21 ms 对 100 ms）；线段树适合更新顺序任意、增删交错、区间查询（`maxIn`）、在线反复查询。

**问：线段树的懒标记为什么不用下推？什么时候必须下推？**
* 2.7：`mx` 含本结点及子树的加数、不含祖先的，查询回溯时补上沿途的 `add`。适用于「区间加 + 区间最大/最小」；「区间赋值」「区间和」需要区间长度或会覆盖旧标记，必须下推。

**问：坐标压缩时事先不知道所有坐标呢？**
* 离线（读完所有输入）才能压缩。在线且坐标未知：动态开点线段树（值域直接 [0, 2⁶⁰)，只在用到时建结点，内存 O(n log C)，深度 60），或自写 order-statistic 平衡树。

**问：每张订单有数量（quantity）？**
* +1/−1 换成 +qty/−qty，`live` 改 `long`（`Math.addExact` 防溢出）；最大值语义变成「在簿最大总量」。

---

## 8. 常见误区

| 很多人会这样写 | 为什么错 | 正确写法 |
|---|---|---|
| 事件只按时间排序 | 同一时刻 +1/−1 先后不确定，`[1,3)`+`[3,5)` 可能得 2 | 排序键 `(time, delta)`，−1 在前；或两数组 `ends[j] <= s` |
| 把 `end` 当包含的 | `[1,3)` 与 `[3,5)` 被算成重叠 | 先确认约定；半开用 `<=`，闭区间用 `<` |
| `all.count = buy.count + sell.count` | 买卖峰值时刻不同，虚高 | 单独扫描全部订单 |
| 在线版每次 `place` 后立刻更新最大值 | 同一时间戳内被撤的订单污染最大值 | 时钟前进时封账，当前时间戳查询时临时比较 |
| 撤单只从计数减 1，忘了从 `expiries` 删原结束时间 | 到期时再减一次，计数变负 | 撤单同时撤掉未来的 −1 |
| `expiries` 计数减到 0 不删键 | `firstEntry` 反复折叠 0，history 出现无意义的点 | `compute` 里减到 0 返回 `null` |
| 撤单时间 ≥ 计划结束时间仍「生效」 | 订单已结束，撤单应返回 `false` | `end > time` 才生效 |
| 先改状态后校验 | 失败的调用留下半修改的状态 | 先校验，再改 |
| `mid = (lo + hi) / 2` | 极大值溢出成负数 | `(lo + hi) >>> 1`；坐标只比较 |
| 线段树 `rangeMax` 不加 `add[node]` | 整体平移的标记丢了 | 回溯时 `best + add[node]` |
| 区间 `[s, e)` 映射成基本段 `idx(s)..idx(e)` | 多算 `e` 所在的段 | `idx(s)..idx(e) - 1` |
| 压缩坐标不去重 | 同一端点占两个下标，出现长度 0 的基本段 | 排序后去重 |
| 对输入数组原地排序 | 调用者的数据被改动 | 拷贝后再排 |

---

## 9. 自测题

1. 订单 `[0,4)`、`[2,6)`、`[4,8)`、`[6,10)` 的最大重叠和最早时刻？改成闭区间 `[s, e]` 呢？
2. 事件 `(5,+1) (5,-1) (5,+1)` 按「−1 在前」排序后是什么顺序？这个时刻最终计数（之前为 0）是多少？
3. 在线版：`place(1,BUY,3,10)`、`place(2,BUY,4,6)`、`cancel(1,5)`、`advanceTo(6)`。依次写出 `liveNow()`、`peak()`、`liveAt(4)`、`liveAt(5)`。
4. 坐标 `[10, 50, 20, 50, 80]` 压缩后是什么？区间 `[20, 80)` 覆盖哪几个基本段？
5. （思考）线段树改成「区间加 + 区间**求和**」，标记永久化还能直接用吗？需要改什么？
6. （小编程）只用一个排序数组 `long[] ev`（把结束编码成负数或别的编码），写 Part 1 扫描线。提示：同一时刻结束在前。

<details><summary>答案</summary>

1. 时刻 2–3 有 `[0,4)`、`[2,6)` 两张；4–5 有 `[2,6)`、`[4,8)` 两张（`[0,4)` 在 4 结束）；6–7 有 `[4,8)`、`[6,10)`。最大重叠 **2**，最早 **t=2**。闭区间：时刻 4 有 `[0,4]`、`[2,6]`、`[4,8]` 三张 → 最大 **3**，最早 t=4。
2. 排序后 `(5,-1) (5,+1) (5,+1)`。之前是 0，先 −1 变 −1（说明输入不一致：结束没有对应开始），再两个 +1 → 1。正常输入里每个 −1 都有在它之前的 +1。
3. `place(1)`：live=1。`place(2)`：live=2，`expiries {6:1,10:1}`。`cancel(1,5)`：时钟到 5，订单 1 的 `end=10>5` 生效，live=1，`expiries {6:1}`。`advanceTo(6)`：折叠 6，live=0。结果：`liveNow()`=0；`peak()`=(2,4)；`liveAt(4)`=2；`liveAt(5)`=1（订单 1 在 5 被撤，订单 2 还活着）。
4. 排序去重 `[10, 20, 50, 80]`（3 个基本段 `[10,20) [20,50) [50,80)`）。`[20, 80)` 覆盖 `idx(20)=1` 到 `idx(80)-1=2`，即后两段。
5. 不能直接用。求和需要「区间长度 × δ」，标记要带长度，查询回溯时要乘「查询与结点区间的交集大小」；常见做法仍用下推。永久化也可以，但每个结点要额外记 `sum` 与区间长度，查询时累加 `add[node] * overlapLength`。
6. 例如开始编码成 `2*t + 1`、结束编码成 `2*t`，排序后同一时刻结束（偶数）在开始（奇数）前。`t` 太大会溢出——坐标高达 `Long.MAX_VALUE` 时这种编码不可行，小坐标可用；大坐标用两个数组或 `(time, delta)` 比较器。

</details>

---

## 延伸阅读

* LeetCode 253 / 731 / 732（区间重叠家族）。
