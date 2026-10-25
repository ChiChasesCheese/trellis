# hc11 · 思路与追问（C++20 版）

最大重叠是 LeetCode 253 的核心，十分钟能写完；分数在追问里：同一时刻先结束还是先开始、闭区间怎么办、撤单怎么翻译成「改区间」、实时到达时最大值何时才算数、坐标到 10^18 时怎么办。C++ 版再加一层：比较器必须是严格弱序，时间戳接近 `LLONG_MAX` 时不能做加减，`std::map::operator[]` 读一下就会插入。下面按 Part 写怎么写、面试官在探什么、该说出口的话。详细推导和可运行的示例在讲义 [[hc11_order_interval_overlap_cpp]]。

## 30 秒版本

- **Part 1**：开始和结束各排一个数组，双指针扫；同一时刻**先结束后开始**（半开区间）；闭区间只把 `ends[j] <= s` 换成 `ends[j] < s`。
- **UB 三件事**：比较器用 `<` 不用 `<=`；不写 `end + 1`、`end - start`；枚举 `Side` 要校验，`static_cast<Side>(7)` 是合法值。
- **Part 2**：撤单就是 `end = min(end, 最早的撤单时间)`；`end <= start` 的单从没活过；买、卖、合计各算一次。
- **Part 3**：每条车道两张 `std::map`（未来的结束、已确定的阶梯）；同一时间戳是一批，时钟越过它才封账最大值；只读路径用 `upper_bound`，不用 `operator[]`。
- **Part 4**：坐标压缩加线段树，用永久化标记，查询是 `const`；二分只比较；全局最大用扫描线就够。

## Part 1 · 最大重叠

**写法**

```cpp
std::sort(starts.begin(), starts.end());
std::sort(ends.begin(), ends.end());
for (size_t i = 0, j = 0; i < starts.size(); ++i) {
    while (j < ends.size() && ends[j] <= starts[i]) ++j;    // 闭区间：ends[j] < starts[i]
    int live = int(i + 1 - j);
    if (live > best) { best = live; best_time = starts[i]; }   // 严格大于：同样的最大值保留最早的时刻
}
```

最大值只可能出现在某个开始的时刻，所以只在开始处更新。`start == end` 的空区间在收集阶段就丢掉。另外两种写法：`peak_events` 排一个 `std::variant<Close, Open>` 的数组，按（时间，备选下标）排序，`Close` 是第 0 个备选，所以同一时刻结束在开始之前；`peak_diff_map` 用 `std::map<long long, int>`，开始处 `+1`、结束处 `-1`，按键累加。

**面试官在探什么**

1. **同一时刻的顺序**：`[1,3)` 与 `[3,5)` 在 3 是交接，不是重叠。只按时间排序时，`+1` 和 `-1` 谁在前由排序细节决定，会时对时错。差分表按键累加的是同一个键上的净增量，所以规则自动成立。
2. **比较器是严格弱序**：`comp(x, x)` 必须为 `false`。`<=` 在大量相等值时会让 `std::sort` 越界读写，是 UB，不是「结果有点乱」。
3. **闭区间**：不要转成 `[s, e + 1)`，`e = LLONG_MAX` 时 `e + 1` 是有符号溢出；只把比较条件从 `<=` 换成 `<`，不做任何运算。
4. **大时间戳**：不写 `end - start`，不写 `(a + b) / 2`，只比较。
5. **取最早时刻**：用严格 `>` 更新，不用 `>=`。
6. **`std::map` 版为什么慢**：节点分散、每个键一次堆分配；排序加双指针是连续内存，快得多。它的好处是代码短、tie 规则自动对。
7. **输入不能被修改**：`span<const Interval>`，把起止点拷到自己的数组里排序。

**该说出口的话**：「区间是半开的，同一时刻先处理结束再处理开始；我把开始和结束各排一遍，双指针扫，比较器用严格小于，全程只比较，不做加减。」

## Part 2 · 买 / 卖方向 + 撤单

**写法**：先遍历一遍事件，用 `std::visit(overloaded{...})` 分派：`Place` 放进 `unordered_map<id, Place>`（重复 id 抛 `invalid_argument`），`Cancel` 记下每个 id 最早的撤单时间。然后检查每个撤单都有对应的 `Place`。最后对每张单算有效结束 `end = min(p.end, cancel)`，`end <= start` 的跳过，按 `side` 放进买、卖、合计三组起止数组，各调一次 Part 1 的核心。

**面试官在探什么**

1. **撤单翻译成改区间**：`[start, min(end, time))`；撤单时间 `<= start` 等于从没活过，`>= end` 无影响；多次撤单取最早，Cancel 写在 Place 前面也行，所以要先收集再算，不能边读边算。
2. **三个峰值互相独立**：买方峰值和卖方峰值可以在不同时刻，`all.count` 不等于两者之和。样例里买方 `{3, 5}`、卖方 `{2, 4}`、合计 `{4, 4}`。
3. **穷尽分派**：`std::visit` 漏一个备选类型是编译错误，Java 的 sealed 加 switch 是同一个意思。
4. **枚举越界**：`enum class Side` 可以装 `static_cast<Side>(7)`，拿它当数组下标会越界。构造函数里校验，抛 `invalid_argument`。
5. **id 的范围**：`long long` 的任何值都合法，包括 `LLONG_MIN` 和负数，用哈希表而不是数组。

**该说出口的话**：「撤单就是把结束时间取 min；先把每个 id 最早的撤单收集起来，再算有效区间，买、卖、合计各跑一次扫描线。」

## Part 3 · 在线版

**写法**：每条车道（买、卖、合计）一个 `Lane`：

| 成员 | 含义 |
|---|---|
| `expiries : map<end, count>` | 未来的差分：在某个计划结束时间结束的订单数，`begin()` 是最近的结束 |
| `history : map<time, live>` | 已确定的阶梯函数：从 `time` 起活跃数是 `live` |
| `live`、`committed_max/time` | 当前活跃数；已封账的最大值及最早时刻 |

`place` 先校验、再 `advance_to(start)`，然后给三条车道里相关的两条登记结束并记一个阶梯。`advance_to` 先把离开的时间戳的 `live` 并进 `committed_max`，再把 `expiries` 里到期的取出来折进 `live`：

```cpp
auto node = expiries.extract(expiries.begin());     // 摘下最近的结束，节点随后销毁
live -= node.mapped();
history.insert_or_assign(node.key(), live);
```

`live_at(t)` 是 `upper_bound(t)` 的前一个元素，在第一条记录之前返回 0。

**面试官在探什么**

1. **同一时间戳是一批**：先 `place` 两张、同一时刻 `cancel` 一张，被撤的那张区间为空，瞬时的 2 不能算最大值。所以最大值只在时钟离开这个时间戳时封账；`peak()` 把当前还没封账的时间戳也当候选，相等时已封账的（更早的）赢。
2. **读路径不能 `operator[]`**：`std::map::operator[]` 在键不存在时插入默认值，读一下就让 map 变大，还编造一条「活跃数为 0」的记录。读用 `find` 或 `upper_bound`，函数标 `const`，编译器会拦住你。测试用 `history_size()` 检查。
3. **`prev(begin())` 是 UB**：`upper_bound(t) == begin()` 说明 `t` 在第一条记录之前，必须先判断。
4. **复杂度**：每个订单的结束最多被折进 `live` 一次，`map` 的插入、删除、查找各 O(log n)，所以每个事件 O(log n)。
5. **`cancel` 的返回值**：`o.end > time` 才算真的缩短了一张还活着的单；之后把 `o.end` 改成 `time`，第二次撤单或计划结束就会看到「已结束」。同时要从 `expiries` 里把原来的计划结束扣掉一个。
6. **拷贝**：`OnlineOverlap` 全是值成员，默认拷贝就是深拷贝，两份互不影响。
7. **预测查询为什么不支持**：`t > now` 以后可能还有撤单，答案不确定；要精确，就要把已知订单的计划结束和未来的撤单分开建模，或者每次重建。
8. **失败的调用不改状态**：先校验、再改；时间倒退、重复 id、非法 `side` 都在改动之前抛出。

**该说出口的话**：「事件按时间到达，过去的差分已经累加成确定的活跃数，只有计划结束需要等；同一时间戳是一批，最大值等时钟越过它再封账；读路径只用 `upper_bound`。」

## Part 4 · 大坐标：坐标压缩 + 线段树

**写法**：构造时把端点排序去重成 `c[0] < ... < c[m-1]`，相邻两个端点之间是一个基本段，每段内活跃数是常数。`[s, e)` 覆盖第 `idx(s)` 到 `idx(e)-1` 段，`idx` 用 `std::lower_bound` 求，并且要求命中（否则抛 `invalid_argument`）。线段树用两个 `std::vector<int>`，堆布局，叶子数补到 2 的幂：

```cpp
if (l <= nl && nr <= r) { add_[n] += delta; mx_[n] += delta; return; }       // 完整覆盖：只打标记
...
mx_[n] = add_[n] + std::max(mx_[2*n], mx_[2*n+1]);                           // 回溯重算
// 查询：return best + add_[n];   经过的结点的标记在回溯时累加，不下推
```

**面试官在探什么**

1. **为什么压缩坐标有效**：活跃数只在端点处变化，值域 10^18 变成最多 2n 个格子。
2. **永久化标记**：标记不下推，查询只读不写，所以 `max()`、`live_at`、`max_in` 都是 `const`，并发读也安全；代价是查询要累加路径上的 `add`。
3. **二分只比较**：`lower_bound` 和 `upper_bound` 不做减法，接近 `LLONG_MAX` 不会溢出；`max_in(LLONG_MIN, LLONG_MAX)` 也不能算 `to - from`。
4. **先校验再改树**：`add(1, 3)` 的起点合法、终点未知，必须在改树之前就两个端点都检查完，否则抛了异常树却被改过。
5. **补出来的叶子**：端点数不是 2 的幂时有空叶子，空叶子的值是 0，不能被计入查询；`max_in` 的区间还要夹到真实的基本段范围里，伸出去的部分算 0。
6. **什么时候才值得线段树**：要任意顺序增删、问区间最大；只要全局最大，排序加扫描线更简单更快。
7. **半开语义**：`live_at(t)` 在右端点上不含；`max_in(from, to)` 的 `to` 不含；`to == from` 返回 0。

**该说出口的话**：「活跃数只在端点处变，我先压缩坐标，再用区间加、区间最大的线段树，标记永久化，查询不改树；二分只比较，所以 10^18 也不会溢出。」

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 输入 | `long[][]`，检查 `length == 2`、`null` | `span<const Interval>`，两个字段，没有 null |
| 事件类型 | `sealed interface` + `switch` 模式匹配 | `std::variant` + `std::visit(overloaded{...})`，编译期穷尽 |
| 枚举 | `enum Side` 只有两个值 | `enum class Side` 可以装别的值，入口要校验 |
| 排序 | `Arrays.sort`，比较器写错多半是结果不对 | `std::sort`，`<=` 比较器是 UB |
| 有序 map | `TreeMap.firstEntry()` / `floorEntry()` / `compute` | `begin()` / `upper_bound` 加 `prev` / `find` 加 `erase`；`operator[]` 会插入 |
| 溢出 | `int`、`long` 静默回绕 | 有符号溢出是 UB，`end + 1`、`end - start` 都不能写 |
| 拷贝 | 引用语义，拷贝要自己写 | 值成员，默认拷贝是深拷贝 |
| 线段树标记 | 懒标记永久化，不下推 | 同样永久化，并且查询是 `const`，由编译器保证不改树 |
