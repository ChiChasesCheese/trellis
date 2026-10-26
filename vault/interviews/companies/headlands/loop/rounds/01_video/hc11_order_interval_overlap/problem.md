# hc11 · 订单区间最大重叠

每个订单在一段时间区间内有效，问同一时刻最多有多少个订单同时有效。做法是扫描线（sweep line）：把每个区间拆成「开始」和「结束」两个事件，按时间排序后扫一遍，边扫边数。分数在两处：同一时刻先处理结束还是先处理开始，以及后面加上买卖方向和撤单之后，怎么把业务规则翻译成区间。Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "Each order is alive during a time interval `[start, end]`. Find the maximum number of orders alive at the same time."
> 接着会问："Is the end inclusive?" "Now every order has a side, BUY or SELL, and some orders are cancelled. Compute the max overlap per side." "What if orders arrive online?" "What if timestamps are huge?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：end 算不算在内？区间会乱序吗？时间会很大吗？ |
| 3–15 分钟 | **Part 1**：最大重叠，扫描线 |
| 15–30 分钟 | **Part 2**：按方向分开算，撤单把区间截短 |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 最大重叠（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static int maxOverlap(long[][] intervals)` |
| C++ | `int max_overlap(const std::vector<std::pair<long long, long long>>& intervals)` |

- 每行 `{start, end}`，返回同一时刻最多有多少个区间同时活着。输入可以乱序，可以有重复。
- 约定：区间是**左闭右开** `[start, end)`，`start` 那一刻订单已经活着，`end` 那一刻已经不活了。所以 `[1,3)` 和 `[3,5)` **不重叠**。
- `start == end` 的区间从没活过，忽略。没有区间时返回 0。
- `end < start`：Java 抛 `IllegalArgumentException`，C++ 抛 `std::invalid_argument`。
- 时间可以接近 `Long.MAX_VALUE`，所以只比较、不做减法。
- 例子：

| 输入 | 结果 |
|---|---|
| `[[1,5],[2,6],[4,8]]` | 3 |
| `[[1,3],[3,5]]` | 1 |
| `[[3,5],[1,3],[5,7]]` | 1 |
| `[[0,10],[2,3],[2,3],[5,7]]` | 3 |
| `[[4,4]]` | 0 |

## Part 2 · 买 / 卖方向 + 撤单（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static int[] maxOverlapBySide(List<Order> orders, Map<Integer, Long> cancelAt)`，`Order(Side side, long start, long end)` |
| C++ | `std::pair<int, int> max_overlap_by_side(const std::vector<Order>& orders, const std::map<int, long long>& cancel_at)`，`Order{Side side; long long start, end;}` |

- 每张订单有方向 `BUY` 或 `SELL`，生命周期 `[start, end)`。返回 `{买方最大重叠, 卖方最大重叠}`，两个方向分开数，不合在一起。
- `cancelAt` 把订单在列表里的下标映射到撤单时间。撤单后，订单的有效区间是 `[start, min(end, 撤单时间))`。
- 撤单时间 `<= start`：这张订单从没活过。撤单时间 `>= end`：没有影响。
- `cancelAt` 里有不存在的下标，或某张订单 `end < start`：抛 Part 1 里同样的异常。
- 思路：先把每张订单换成它的有效区间，按方向分成两组，每组调用 Part 1。
- 例子：三张买单 `[0,10)`、`[2,8)`、`[5,9)`，不撤单时在 t=5 三张同时活着，买方峰值 3；订单 1 在 t=4 撤单后变成 `[2,4)`，t=5 只剩两张，买方峰值 2。
- 例子：`BUY [0,5)`、`SELL [0,5)`、`SELL [1,3)` 返回 `{1, 2}`：买卖不合并。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 如果 end 是包含的（闭区间），算法要怎么改？
2. 排序时如果只按时间排，同一时刻 `+1` 和 `-1` 的先后不管，会出什么错？
3. 订单和撤单是实时一个个到的，要随时回答「到现在为止最大重叠是多少」，怎么做？
4. 时间戳高达 10^18，还要支持任意顺序加入、撤销区间，并问「某个时间段内的最大重叠」，怎么做？
5. 如果每张订单有数量，要求同一时刻在簿的最大总量，怎么改？
6. 如果只要全局最大重叠，为什么扫描线比线段树更好？

## 边界

- 空输入、`start == end`、全部区间相同
- `[1,3)` 与 `[3,5)` 首尾相接，以及乱序的链式交接
- 撤单时间等于 `start`、小于 `start`、大于等于 `end`
- 只有一个方向的订单；买卖两个方向的区间互相重叠
- 时间接近 `Long.MAX_VALUE`

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc11_order_interval_overlap       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc11_order_interval_overlap --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc11_order_interval_overlap       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc11_order_interval_overlap --tag part1
```
