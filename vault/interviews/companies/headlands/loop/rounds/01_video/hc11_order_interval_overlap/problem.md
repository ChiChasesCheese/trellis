# hc11 · 订单区间最大重叠 + 按买 / 卖方撤单

每个订单在一段时间区间内有效，问同一时刻最多有多少个订单同时有效；之后还要支持按买方或卖方整体撤单。基本做法是扫描线：把区间拆成「开始」「结束」两类事件，按时间排序后扫一遍。撤单、在线更新和很大的坐标范围会逐步把解法推向差分数组、线段树和坐标压缩。

## 读题前你需要知道

* **扫描线（sweep line）**：把「区间」变成「事件」，按时间扫一遍；以及为什么**同一时刻要先处理结束再处理开始**；
* **差分数组（difference array）**与前缀和；**有序 Map**（`TreeMap`）；
* **线段树（segment tree）**与**懒标记（lazy propagation）**，以及**坐标压缩（coordinate compression）**；
* **半开区间** `[start, end)` 的好处。

## 背景

交易系统里每张订单（order）都有一个**生命周期**：从 `start` 时刻进入订单簿，到 `end` 时刻离开（过期或成交）。我们把它建模成**左闭右开**区间 `[start, end)`：
`start` 那一刻订单已经「活着」，`end` 那一刻已经「不活了」。时间是**非负整数**（long），可以很大（纳秒时间戳，接近 `Long.MAX_VALUE`），
所以实现里**只能比较、不能做 `end - start` 或 `(a + b) / 2` 这类运算**。

## Part 一览

| Part | 入口 | 内容 |
|---|---|---|
| 1 | `OrderIntervals.maxOverlap` · `peak` · `maxOverlapInclusive` | 同时活着的订单数的最大值（以及最早出现的时刻）；扫描线 + 「先结束后开始」 |
| 2 | `OrderIntervals.analyze(List<OrderEvent>)` → `Report(buy, sell, all)` | 买、卖两个方向各自的峰值；`Cancel` 把区间截短；sealed 事件 + 模式匹配 `switch` |
| 3 | `OnlineOverlap`（`place` / `cancel` / `advanceTo` / `liveAt` / `peak` / `maxSoFar`） | 在线：订单和撤单按时间到达，随时答「到现在为止的最大重叠」和「t 时刻有几张」 |
| 4 | `IntervalIndex`（`add` / `remove` / `liveAt` / `maxIn` / `max`） | 坐标高达 10^18、更新顺序任意：坐标压缩 + 懒标记线段树 |

`Side`、`Peak`、`OrderEvent`（`Place` / `Cancel`）、`Report` 在 starter 里已给出，签名以 starter 为准，这里只写语义。

## Part 1 · 最大重叠

`maxOverlap(long[][] intervals)` → `int`：每行 `{start, end}`，返回任意时刻同时活着的订单数的最大值。`peak(...)` → `Peak(count, time)`，`time` 是**最早**达到最大值的时刻。

* 区间 `[start, end)`：`[1,3)` 与 `[3,5)` **不重叠**（时刻 3 是交接，旧单已死、新单刚生）。这就是「**同一时刻先处理结束、再处理开始**」。
* `start == end` 的空区间从没活过，忽略。输入可以乱序、有重复。从没有订单活着（含空输入）→ `Peak(0, 0)`。
* `maxOverlapInclusive`：如果区间是闭的 `[start, end]`，`[1,3]` 与 `[3,5]` 在 3 重叠，`[5,5]` 是一个点。（面试官常问「如果 end 是包含的呢」。）
* `start < 0`、`end < start`、行长度不是 2 → `IllegalArgumentException`；`null` → `NullPointerException`。
* 输入不得被修改；O(n log n) 时间；百万区间 < 2 s；坐标接近 `Long.MAX_VALUE` 不能溢出。

### 样例

```
[[1,5],[2,6],[4,8]]          → 3，最早在 t=4
[[1,3],[3,5]]                → 1     （闭区间版本 maxOverlapInclusive → 2）
[[0,10],[2,3],[2,3],[5,7]]   → 3，最早在 t=2
[]                           → 0，Peak(0, 0)
```

## Part 2 · 买 / 卖方向 + 撤单

输入是一串 `OrderEvent`（顺序**无所谓**）：

* `Place(id, side, start, end)`：计划生命周期 `[start, end)`，`side` 是 `BUY` 或 `SELL`；`end == start` 合法（从没活过）。
* `Cancel(id, time)`：`time` 时刻起这张单不再活着，**把区间截成 `[start, min(end, time))`**。

`analyze(events)` → `Report(buy, sell, all)`，三个 `Peak`：只数买单、只数卖单、两个方向合计。

* 撤单时间 `<= start`（开始前或开始的瞬间）→ 这张单从没活过；`>= end` → 无影响；
* 同一个 `id` 多次撤单：**最早**的生效；
* 撤单的 `id` 没有对应的 `Place` → `IllegalArgumentException`；同一个 `id` 两次 `Place` → `IllegalArgumentException`；
* 注意：买方峰值和卖方峰值可以出现在不同时刻，而且 `all.count` **不等于** `buy.count + sell.count`（两个峰值可能错开）。

### 样例

```
Place(1,BUY, 0,10)  Place(2,BUY, 2, 8)  Place(3,SELL,3, 6)  Place(4,SELL,4,12)  Place(5,BUY, 5, 9)
Cancel(2, 6)        Cancel(4, 5)

有效区间： 1 BUY [0,10)   2 BUY [2,6)   3 SELL [3,6)   4 SELL [4,5)   5 BUY [5,9)
buy  = Peak(3, 5)    t=5：订单 1、2、5
sell = Peak(2, 4)    t=4：订单 3、4
all  = Peak(4, 4)    t=4：1、2、3、4；t=5：1、2、3、5 也是 4，取最早
（去掉两个 Cancel：all = Peak(5, 5)）
```

## Part 3 · 在线版

「订单和撤单是一个个实时到的，不能先攒起来再排序。每来一个事件都要能马上回答：到现在为止最大重叠是多少？t 时刻有几张单活着？」

`OnlineOverlap`：

| 方法 | 含义 |
|---|---|
| `place(id, side, start, end)` | 订单在 `start` 时刻到达；`start` 必须 ≥ 上一个事件的时间（相等允许），否则 `IllegalArgumentException`；`id` 重复 → IAE |
| `cancel(id, time)` → `boolean` | `time` 时刻撤单；真的缩短了一张还活着的单 → `true`；已自然结束 / 已撤过 → `false`；`id` 不存在、`time` 倒退 → IAE |
| `apply(OrderEvent)` | 用 sealed + 模式匹配分派 |
| `advanceTo(t)` | 只推进时钟 |
| `liveNow()` · `liveAt(t)`（`0 ≤ t ≤ now`）· 带 `Side` 的重载 | 当前 / 历史某时刻的活跃数；`t > now` 是「预测」，不支持 → IAE |
| `peak()` · `maxSoFar()` · 带 `Side` 的重载 | 到现在为止的最大重叠（含当前时间戳）及最早时刻 |

* **关键语义**：同一时间戳内的事件视为一批——先 `place` 两张、再 `cancel` 其中一张（同一时刻），那张单的区间是空的，`maxSoFar` 要**追溯修正**，
  不能被瞬时的 2 污染。所以最大值要等时间戳「过去」之后才算数，当前时间戳用当前值参与比较。
* 在线答案必须与「把已到事件交给 Part 2 的 `analyze`」**逐前缀完全一致**（测试会对每个前缀对拍）。
* 每个事件 O(log n)。80 万事件 < 2 s。
* 追问：`t > now` 的预测查询为什么贵？怎么办？

## Part 4 · 大坐标：坐标压缩 + 线段树

「时间戳是纳秒，范围 10^18，数组开不出来；而且订单可能以任意顺序加入和撤销，还要问『某个时间段内的最大重叠』。」

`IntervalIndex(long[] coordinates)`：先告知所有会用到的端点（任意顺序、可重复），之后：

| 方法 | 含义 |
|---|---|
| `add(start, end)` / `remove(start, end)` | 加入 / 撤销区间 `[start, end)`，两端必须是已知端点，否则 IAE；`end < start` → IAE；`start == end` 什么都不做。`remove` 只能撤销 `add` 过的 |
| `max()` | 全局最大重叠 |
| `liveAt(t)` | `t` 时刻活着几个（`t` 在所有端点之外是 0；右端不含） |
| `maxIn(from, to)` | `[from, to)` 内任意时刻的最大活跃数；`to < from` → IAE；`to == from` → 0 |
| `of(long[][])` · `maxOverlap(long[][])` | 从一批区间建索引；用压缩 + 线段树算 Part 1，必须与扫描线一致 |

* 实现要求：坐标压缩（端点排序去重，二分查找下标）+ 区间加 / 区间最大值的线段树（懒标记）。每次操作 O(log n)。
* 坐标接近 `Long.MAX_VALUE` 不能溢出（二分、比较都不做减法）。
* 30 万个 10^18 量级的区间 + 10 万次 `maxIn` 查询 < 2 s。
* 追问核心：**如果只要全局最大，为什么扫描线更好？线段树什么时候才值得？**

## 边界清单（隐藏测试会打的）

| 类别 | 例子 |
|---|---|
| tie 规则 | `[1,3)` + `[3,5)`；链式交接；全部相同的区间 |
| 空 / 零 | 空输入；`start == end`；撤单发生在开始前 / 开始瞬间 / 结束时刻 / 结束后 |
| 撤单 | 重复撤单；撤单写在 Place 前面；未知 id；同一时刻 place 后 cancel |
| 方向 | 只有一个方向；买卖峰值时刻不同；`all` 的峰值比两者都高 |
| 在线 | 时间倒退；`liveAt` 越界；很多单恰好同一时刻结束；撤单后原计划的结束要同步取消；撤单返回值 |
| 大数 | `Long.MAX_VALUE` 附近的 start / end；`end - start` 溢出 |
| 线段树 | 范围伸出所有端点之外；`to` 不含；单个端点；`remove` 之后回到原状 |

## 相关变体

* LeetCode 253 Meeting Rooms II（最少会议室 = 最大重叠）、LeetCode 731 / 732 My Calendar II / III（在线加区间，问 k 重预订）——Part 3 / 4 的原型。
* 「每个订单有数量」：把 `+1 / -1` 换成 `+qty / -qty`，求同时在簿的最大总量。
* 「同一方向内的重叠」vs「买卖对冲」：买方在簿量 − 卖方在簿量的最大绝对值，需要带符号的差分。
* 区间含端点（闭区间）、或者时间是浮点——先问清楚约定。

## 考什么

Part 1 是 LeetCode 253 的核心，**考的是 tie 规则**：同一时刻先结束后开始。很多人排序时只按时间排，`+1` 和 `-1` 谁在前由排序稳定性决定，结果时对时错。
Part 2 看你会不会把「撤单」这个业务语义翻译成「改区间」，并且按方向拆开处理；sealed 类型让「漏处理一种事件」变成编译错误。
Part 3 的陷阱是**同一时间戳内的事件顺序**与「最大值何时才算数」。Part 4 看你能不能把线段树从零推出来，并说清楚什么时候该用它、什么时候扫描线就够了。
