# hc11 · 订单区间最大重叠 + 按买 / 卖方撤单（C++20 版）

每个订单在一段时间区间内有效，问同一时刻最多有多少个订单同时有效；之后还要支持按订单整体撤单。基本做法是扫描线：把区间拆成「开始」「结束」两类事件，排序后扫一遍。撤单、在线更新和很大的坐标范围会逐步把解法推向差分表、有序 `std::map` 和线段树。C++ 版的额外考点是：比较器必须是严格弱序、时间戳接近 `LLONG_MAX` 时不能做任何加减、`std::map::operator[]` 会插入。题目分 4 个 Part，签名都在 `starter.hpp`（命名空间 `overlap`）。

## 读题前你需要知道

- **扫描线**（sweep line）：把区间变成事件，按时间扫一遍。**同一时刻先处理结束、再处理开始**，因为区间是半开的。
- **半开区间** `[start, end)`：`start` 那一刻订单已经活着，`end` 那一刻已经不活了。`[1,3)` 与 `[3,5)` 不重叠。
- **严格弱序**（strict weak ordering）：`std::sort` 的比较器要求 `comp(x, x)` 为 `false`。写成 `<=` 是未定义行为（UB），不只是结果乱。
- **有符号溢出是 UB**：时间可以接近 `LLONG_MAX`，所以只能比较，不能写 `end - start`、`end + 1`、`(a + b) / 2`。
- **差分数组**（difference array）：开始处 +1、结束处 -1，累加得到每个时刻的活跃数。
- **坐标压缩与线段树**：活跃数只在端点处变化，把端点排序去重后，值域再大也只剩下 O(n) 个格子；线段树支持区间加、区间最大。

## 公共类型（starter 已给出）

```cpp
enum class Side : unsigned char { Buy, Sell };        // 枚举类型可以装任何 unsigned char 的值

struct Peak     { int count; long long time; };       // 最大同时活跃数，以及最早达到它的时刻；从没活过是 {0, 0}
struct Interval { long long start, end; };            // 半开 [start, end)

struct Place  { long long id; Side side; long long start, end; };   // 构造函数校验：side 合法、start >= 0、end >= start
struct Cancel { long long id; long long time; };                    // 构造函数校验：time >= 0
using OrderEvent = std::variant<Place, Cancel>;       // std::visit 配 overloaded{...}，漏一个分支是编译错误
struct Report { Peak buy, sell, all; };
```

`end == start` 的 `Place` 合法（从没活过）。`Interval` 只有两个字段，Java 版「行长度不是 2」「null 行」的错误在类型里就不存在了；`start < 0` 和 `end < start` 抛 `std::invalid_argument`。

## Part 1 · 最大重叠

| 签名 | 要求 |
|---|---|
| `Peak peak(std::span<const Interval>)` | 同时活着的订单数的最大值和**最早**达到它的时刻 |
| `int max_overlap(std::span<const Interval>)` | `peak(...).count` |
| `int max_overlap_inclusive(std::span<const Interval>)` | 区间当作闭区间 `[start, end]`：`[1,3]` 与 `[3,5]` 在 3 重叠，`[5,5]` 是一个活着的点 |
| `Peak peak_events(std::span<const Interval>)` | 变体二：一个排好序的事件数组，`std::variant<Close, Open>` |
| `Peak peak_diff_map(std::span<const Interval>)` | 变体三：`std::map<long long, int>` 做差分数组，按键顺序累加 |

- 输入可以乱序、有重复；`start == end` 的空区间忽略；空输入或从没活过得 `{0, 0}`；输入不能被修改。
- O(n log n) 时间；坐标接近 `LLONG_MAX` 不能溢出。
- 提示（来自 starter）：开始和结束各排一个数组，用两个下标走；同一时刻结束在开始之前；变体二里 `Close` 是变体的第 0 个备选类型，`Open` 是第 1 个，同一时刻按备选下标排序就得到「先结束后开始」；比较器用 `<`，不用 `<=`。

### 样例

| 输入 | 结果 |
|---|---|
| `[[1,5],[2,6],[4,8]]` | `max_overlap` = 3，`peak` = `{3, 4}` |
| `[[1,3],[3,5]]` | 1，`peak` = `{1, 1}`；`max_overlap_inclusive` = 2 |
| `[[0,10],[2,3],[2,3],[5,7]]` | `peak` = `{3, 2}` |
| `[[0,1],[1,2],[2,3],[3,4]]` | 1（链式交接，任何时刻只有一个） |
| `[[2,5]]` 重复 4 次 | 4 |
| `[[5,5],[0,10],[5,5]]` | 1；闭区间版是 2 |
| `[[1,3],[1,3],[10,12],[10,12]]` | `peak` = `{2, 1}`（最大值重复出现，取最早） |
| `[[0,LLONG_MAX],[LLONG_MAX-2,LLONG_MAX],[LLONG_MAX-1,LLONG_MAX],[LLONG_MAX-5,LLONG_MAX-1]]` | `peak` = `{3, LLONG_MAX-2}`；三种实现都一样 |

C++ 专属测试：

- 「同一时刻的顺序由变体的备选下标决定」：`std::variant_alternative_t<0, SweepEvent>` 是 `Close`，`<1>` 是 `Open`（`static_assert`）。`[[1,3],[3,5],[3,4]]` 的 `peak_events` 是 `{2, 3}`。
- 「比较器必须是严格弱序」：6 万个事件只落在 3 个不同时刻，`<=` 比较器会让 `std::sort` 越界读写。
- 「闭区间在 `LLONG_MAX` 处不能算 `end + 1`」：`[[LLONG_MAX,LLONG_MAX],[0,LLONG_MAX]]` 的闭区间答案是 2，`[[0,LLONG_MAX-1],[LLONG_MAX,LLONG_MAX]]` 是 1。
- 「差分表同一个键上加的是净增量」：键 3 上有 `-1`（来自 `[1,3)`）和 `+1`（来自 `[3,5)`），净增量 0，活跃数不会到 2；`[[4,4]]` 得 `{0, 0}`。

性能测试（`perf`）：100 万个区间，2 秒内跑完 `peak`、`peak_events`、`peak_diff_map`。

## Part 2 · 买 / 卖方向 + 撤单

| 签名 | 要求 |
|---|---|
| `Report analyze(std::span<const OrderEvent>)` | 买、卖各自的峰值，以及两个方向合计的峰值。事件顺序**无所谓** |

`Place(id, side, start, end)` 的计划生命周期是 `[start, end)`；`Cancel(id, time)` 把区间截成 `[start, min(end, time))`。

- 撤单时间 `<= start`（开始前或开始的瞬间）：这张单从没活过；`>= end`：无影响。
- 同一个 `id` 多次撤单：**最早**的生效，Cancel 写在 Place 前面也行。
- 撤单的 `id` 没有对应的 `Place`，或同一个 `id` 两次 `Place`：抛 `invalid_argument`。
- 买方峰值和卖方峰值可以出现在不同时刻，`all.count` 不一定等于 `buy.count + sell.count`。

### 样例

```
Place(1,BUY, 0,10)  Place(2,BUY, 2, 8)  Place(3,SELL,3, 6)  Place(4,SELL,4,12)  Place(5,BUY, 5, 9)
Cancel(2, 6)        Cancel(4, 5)

有效区间： 1 BUY [0,10)   2 BUY [2,6)   3 SELL [3,6)   4 SELL [4,5)   5 BUY [5,9)
buy  = {3, 5}    t=5：订单 1、2、5
sell = {2, 4}    t=4：订单 3、4
all  = {4, 4}    t=4：1、2、3、4；t=5：1、2、3、5 也是 4，取最早
去掉两个 Cancel：all = {5, 5}，buy = {3, 5}，sell = {2, 4}
```

- 取消的时间点：`Place(1, BUY, 5, 10)` 配 `Cancel(1, c)`，`c` 取 0、4、5 时 `all` 是 `{0, 0}`；`c = 10` 或 99 时是 `{1, 5}`。
- 交接：`Place(1,BUY,0,10)`、`Place(2,BUY,5,8)`、`Cancel(1,5)`，买方峰值 `{1, 0}`。
- 只有卖单：`{Place(1,SELL,3,9), Place(2,SELL,4,5)}` 的报告是 `buy={0,0}, sell={2,4}, all={2,4}`。
- `Place(1, BUY, 0, LLONG_MAX)`、`Place(2, SELL, LLONG_MAX-1, LLONG_MAX)`、`Cancel(1, LLONG_MAX-1)`：买方 `{1, 0}`，卖方 `{1, LLONG_MAX-1}`，合计 `{1, 0}`。
- `Place(1, BUY, 5, 4)`、`Place(1, BUY, -1, 4)`、`Cancel(1, -1)` 在构造时就抛 `invalid_argument`。

C++ 专属测试：

- 「枚举可以装枚举值之外的数」：`Place(1, static_cast<Side>(7), 0, 1)` 抛 `invalid_argument`，否则 7 会越界下标买卖两条车道的数组。
- 「订单号可以是任何 `long long`」：`LLONG_MIN`、`-1`、`0`、`LLONG_MAX` 都是合法 id。
- 「`analyze` 接受 `vector`、`std::array` 和子 `span`」。

性能测试（`perf`）：50 万个订单加 25 万个撤单，2 秒内。

## Part 3 · 在线版

订单和撤单是一个个实时到的，不能先攒起来再排序。每来一个事件都要能马上回答：到现在为止最大重叠是多少？`t` 时刻有几张单活着？

| 签名（`class OnlineOverlap`） | 要求 |
|---|---|
| `void place(long long id, Side, long long start, long long end)` | 订单在 `start` 时刻到达，`start` 必须 >= 上一个事件的时间（相等允许）；id 重复、`end < start`、`start < 0`、非法 `side` 抛 `invalid_argument`；失败的调用不改变任何状态 |
| `bool cancel(long long id, long long time)` | 真的缩短了一张还活着的单返回 `true`；已自然结束或已撤过返回 `false`；id 不存在、`time` 倒退抛 `invalid_argument` |
| `bool apply(const OrderEvent&)` | `Place` 返回 `true`；`Cancel` 返回 `cancel` 的结果 |
| `void advance_to(long long t)` | 只推进时钟，倒退抛 `invalid_argument` |
| `now()` · `live_now()` · `live_now(Side)` | 当前时间、当前活跃数 |
| `live_at(t)` · `live_at(Side, t)` | 历史时刻 `t` 的活跃数，`0 <= t <= now()`，否则抛 `invalid_argument`（不支持预测） |
| `peak()` · `peak(Side)` · `max_so_far()` · `max_so_far(Side)` | 到现在为止的最大重叠（含当前时间戳）及最早时刻 |
| `std::size_t history_size() const` | 内部阶梯记录的条数（所有车道合计）；**读操作绝不能让它变大** |

- **关键语义**：同一时间戳内的事件视为一批。先 `place` 两张、再在同一时刻 `cancel` 其中一张，那张单的区间是空的，`max_so_far` 要**追溯修正**，不能被瞬时的 2 污染。
- 在线答案必须和「把已到事件交给 `analyze`」**逐前缀完全一致**（测试对每个前缀对拍）。
- 每个事件 O(log n)。
- 提示（来自 starter）：每条车道（买、卖、合计）一个 `std::map` 存未来的结束（计划结束时间 → 数量）、一个 `std::map` 存已确定的阶梯函数（`upper_bound` 加前一个元素回答 `live_at`）、当前活跃数、已封账的最大值；时钟越过某个时间戳时才把它的最大值封账，`peak()` 还要把当前未封账的时间戳算进去；只读路径不要用 `operator[]`。

### 样例（按到达顺序）

| 操作 | `peak()` |
|---|---|
| `place(1,BUY,0,10)` | `{1, 0}` |
| `place(2,BUY,2,8)` | `{2, 2}` |
| `place(3,SELL,3,6)` | `{3, 3}` |
| `place(4,SELL,4,12)` | `{4, 4}` |
| `place(5,BUY,5,9)` | `{5, 5}`（此刻 5 张都活着） |
| `cancel(4,5)` 返回 `true` | `{4, 4}`（追溯修正：同一时刻撤掉，5 不算数） |
| `cancel(2,6)` 返回 `true` | `{4, 4}`；`peak(BUY)` = `{3, 5}`，`peak(SELL)` = `{2, 4}`，`now()` = 6 |

此时 `t = 0..6` 的 `live_at` 依次是 `1, 1, 2, 3, 4, 4, 2`，`live_now()` 是 2，`live_at(BUY, 1)` 是 1，`live_at(SELL, 4)` 是 2。

- 同一时间戳：`place(1,BUY,5,9)`、`place(2,BUY,5,9)` 后 `max_so_far() = 2`；`cancel(1,5)` 返回 `true`，之后 `max_so_far() = 1`，`peak() = {1, 5}`。
- 到期不含右端：`place(1,SELL,0,5)`、`place(2,SELL,1,5)`、`place(3,SELL,2,6)` 后 `advance_to(4)` 仍是 3 张，`advance_to(5)` 剩 1 张；`live_at(4) = 3`、`live_at(5) = 1`；`advance_to(100)` 之后历史不变，`peak() = {3, 2}`。
- `cancel` 的返回值：`place(1,BUY,0,5)`、`place(2,BUY,1,100)`，`cancel(2,3)` 为 `true`，再 `cancel(2,4)` 为 `false`；`cancel(1,5)`（恰好计划结束时刻）和 `cancel(1,9)` 都是 `false`。
- 零长度订单：`place(1,BUY,3,3)` 之后 `live_now() = 0`，`peak() = {0, 0}`，`cancel(1,3)` 为 `false`，同一个 id 再 `place` 抛 `invalid_argument`（id 已被占用）。
- 乱序：已到 `place(1,BUY,10,20)` 后，`place(2,BUY,9,12)`、`cancel(1,9)`、`advance_to(9)`、`live_at(11)`、`live_at(-1)` 都抛 `invalid_argument`，状态不变；`place(2,SELL,10,15)` 同一时间戳合法，`peak() = {2, 10}`。
- 1000 个订单（`i` 为偶数是买）同在 50 结束：`live_now() = 1000`、`live_now(BUY) = 500`；撤掉其中两张后 `advance_to(50)`，`live_now() = 0`，`live_at(49) = 998`，`peak() = {1000, 9}`。
- 时间戳接近上限：`place(1,BUY,0,LLONG_MAX)`、`place(2,SELL,LLONG_MAX-3,LLONG_MAX-1)`，`peak() = {2, LLONG_MAX-3}`。

C++ 专属测试：

- 「读操作不让 map 变大」：对每个 `t` 调 `live_at`（三种重载）和 `peak` 之后，`history_size()` 和之前相等。
- 「`live_at` 早于第一条记录返回 0」：`place(1,BUY,5,9)` 后 `live_at(0)`、`live_at(4)` 是 0，`live_at(5)` 是 1；`const` 对象上也一样。
- 「拷贝是深拷贝」：`OnlineOverlap b = a;` 之后各改各的，互不影响，`a` 里没有的 id 在 `b` 里新增后，`a` 上撤它抛 `invalid_argument`。
- 「边读边排空到期表」：400 个时间点、每步两张订单、部分被缩短，`advance_to(1000)` 后 `live_now() = 0`，ASan 下不能留下指向已释放节点的迭代器。
- 非法 `side`（`static_cast<Side>(2)`）抛 `invalid_argument`，且 `now()` 不变，id 仍可用。

性能测试（`perf`）：60 万个 `place`，每 3 个配一次 `cancel`，每 1000 个配一次 `live_at`，2 秒内。

## Part 4 · 大坐标：坐标压缩 + 线段树

时间戳是纳秒，范围到 10^18，数组开不出来；订单可能以任意顺序加入和撤销；还要问「某个时间段内的最大重叠」。

| 签名（`class IntervalIndex`） | 要求 |
|---|---|
| `explicit IntervalIndex(std::span<const long long>)` | 先告知所有会用到的端点（任意顺序，可重复） |
| `static IntervalIndex of(std::span<const Interval>)` | 从一批区间建索引：收集端点、压缩、逐个 `add` |
| `static int max_overlap(std::span<const Interval>)` | Part 1 的答案，用压缩加线段树算，必须和扫描线一致 |
| `void add(start, end)` · `void remove(start, end)` | 加入或撤销区间 `[start, end)`；两端必须是已知端点，否则抛 `invalid_argument`；`end < start` 抛 `invalid_argument`；`start == end` 什么都不做。**失败的调用不能改动线段树** |
| `int max() const` | 全局最大重叠 |
| `int live_at(long long t) const` | `t` 时刻活着几个；`t` 在所有端点之外是 0；右端不含 |
| `int max_in(long long from, long long to) const` | `[from, to)` 内任意时刻的最大活跃数；`to < from` 抛 `invalid_argument`；`to == from` 返回 0 |
| `coordinate_count()` · `segment_count()` | 去重后的端点数、基本段数（端点数减 1，最少 0） |

- 提示（来自 starter）：排序去重后的端点是 `c[0] < ... < c[m-1]`，`[c[j], c[j+1])` 是一个基本段；`[s, e)` 覆盖第 `idx(s)` 到 `idx(e)-1` 段；二分用 `std::lower_bound` / `std::upper_bound`，只比较不做减法。
- 每次操作 O(log n)。`max()`、`live_at`、`max_in` 都是 `const`。

### 样例（单位 `u = 10^15`）

区间 `[1u,5u)`、`[2u,6u)`、`[4u,8u)`：`max() = 3`，`coordinate_count() = 6`，`segment_count() = 5`。

| 查询 | 结果 |
|---|---|
| `live_at(0)` | 0 |
| `live_at(1u)` | 1 |
| `live_at(2u + 12345)` | 2 |
| `live_at(4u)` | 3 |
| `live_at(5u)` | 2（`[1u,5u)` 在 5u 结束） |
| `live_at(8u - 1)` · `live_at(8u)` | 1 · 0 |
| `max_in(5u, 100u)` · `max_in(0, 5u)` · `max_in(0, 2u)` | 2 · 3 · 1 |

- 区间 `[10,20)`、`[15,30)`：`max_in(0,10) = 0`、`max_in(0,11) = 1`、`max_in(19,21) = 2`、`max_in(20,21) = 1`、`max_in(30,99) = 0`、`max_in(12,12) = 0`、`max_in(0,1000) = 2`。
- 端点 `{0,5,10,20,100}`：加 `[0,10)`、`[5,20)`、`[5,100)` 后 `max() = 3`；撤销 `[5,20)` 后 `max() = 2`；全部撤销后回到 0。
- 端点接近上限（同 Part 1 的第四个例子）：`max() = 3`，`live_at(LLONG_MAX) = 0`，`max_in(1, LLONG_MAX-5) = 1`。
- 空端点集、单个重复端点（`{7,7,7}` 的 `coordinate_count() = 1`，`segment_count() = 0`）都合法。
- `max_overlap([[1,3],[3,5]]) = 1`。

C++ 专属测试：

- 「查询在 `const` 对象上工作，整个范围不溢出」：`max_in(LLONG_MIN, LLONG_MAX)` 不能算 `to - from`；`live_at(LLONG_MIN)` 为 0。
- 「负坐标是普通端点」：端点 `{-5,0,5}`，`add(-5,5)`、`add(0,5)` 后 `live_at(0) = 2`，`max_in(-100,-5) = 0`。
- 「被拒绝的 `add` 不留痕迹」：`add(1,3)`、`add(3,9)`、`remove(0,9)`（3、0 不是已知端点）全部抛 `invalid_argument`，之后 `max() = 0`；起点合法也要在改树之前就检查完。
- 「树的大小在 2 的幂附近」：端点数 2、3、4、5、6、9、10 时，补出来的空叶子不能被计入，`max_in(c.back(), c.back() + 1000) = 0`。

性能测试（`perf`）：30 万个量级 10^18 的区间，加 10 万次 `max_in`，2 秒内。

## 边界清单

- tie：`[1,3)` 加 `[3,5)`；链式交接；全部相同的区间
- 空和零：空输入；`start == end`；撤单发生在开始前、开始瞬间、结束时刻、结束后
- 撤单：重复撤单；Cancel 写在 Place 前面；未知 id；同一时刻 `place` 后 `cancel`
- 方向：只有一个方向；买卖峰值时刻不同；`all` 的峰值比两者都高
- 在线：时间倒退；`live_at` 越界；很多单恰好同一时刻结束；撤单后原计划的结束要同步取消；撤单的返回值
- 大数：`LLONG_MAX` 附近的 start / end；`end - start`、`end + 1` 溢出
- 枚举：`static_cast<Side>(7)`
- 线段树：查询范围伸出所有端点之外；`to` 不含；单个端点；`remove` 之后回到原状；未知端点不留半截更新

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc11_order_interval_overlap          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc11_order_interval_overlap --tag part1
python3 tools/cpptest.py run   loop/rounds/01_video/hc11_order_interval_overlap --tag cpp      # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/01_video/hc11_order_interval_overlap                # 全部
```

编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 每个订单有数量：`+1 / -1` 换成 `+qty / -qty`，求同时在簿的最大总量。
- 买方在簿量减卖方在簿量的最大绝对值：带符号的差分，同时记最大和最小前缀和。
- 区间含端点（闭区间）或者时间是浮点：先问清楚约定。
- 最少会议室（LeetCode 253）、k 重预订（LeetCode 731 / 732）是 Part 3 和 Part 4 的原型。
