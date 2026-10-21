# LLD + 数据模型：办公室人数追踪（"某一时刻有多少人"）——教科书模式

> 题库里没有（它介于 LLD 和"小型数据库设计"之间）。来源：`../catalog/raw/forums.md` §1 与 §2 的 LC6841339（2025-06，US L4 新毕业生，**拿到 offer**）：
> "Design a system to track how many people are in the office at any given time"，追问"在某个时间戳的人数""某个区间内的最大人数"，当事人自述 "system design/database oriented"。
> 它的价值：证明 SDE I 也会被问"**小型数据模型 + 时间戳查询**"，且面试官期待你把同一个模型既写成代码又写成 SQL。
> 代码：`code/occupancy_tracker.py`（`python3 -I code/occupancy_tracker.py` 打印 `OK occupancy_tracker`；测试里用标准库 `sqlite3` 对拍 SQL 答案）。

## 1. 这道题在问什么

刷卡门禁每次产生一个事件："小李 10:00 进入""小李 12:30 离开"。要回答：
1. `current()`：现在有多少人？
2. `count_at(t)`：时刻 t 有多少人？
3. `max_in(a, b)`：区间 [a, b] 内**出现过的最大人数**是多少？

手算：事件 `a进@10, b进@20, c进@30, a出@40, d进@40, b出@50, c出@60`。
- `count_at(25)`：a、b 在里面 → 2。`count_at(45)`：b、c、d → 3。
- `max_in(0, 1000)`：峰值 = 3（30 到 60 之间）。
- `max_in(41, 100)`：区间内没有"更高"的时刻，但区间**开始时**就有 3 个人 → 答案 3（**常见错误：只看区间内的事件，漏掉区间开始时的人数**）。

## 2. 前置知识

### 2.1 事件溯源（Event Sourcing）思想：存变化，不存状态
- **是什么**：不直接存"当前人数"，存每一次进出事件；任何时刻的人数 = 把事件按时间累加。
- **为什么**：只存"当前人数"就回答不了"昨天 3 点有多少人"；事件日志既能回答历史，也能审计，且追加写很便宜。
- **怎么工作**：事件 `(ts, person, delta)`，`delta = +1/-1`。人数 = **前缀和**。

### 2.2 前缀和 + 二分查找
- 事件按时间追加 → 时间数组 `times` 有序；`counts[i]` = 处理完第 i 个事件后的人数（前缀和）。
- `count_at(t)`：`bisect_right(times, t) - 1` 找到最后一个 ≤ t 的事件下标 i，答案 `counts[i]`；没有则 0。O(log n)。
```
times : 10  20  30  40  40  50  60
delta : +1  +1  +1  -1  +1  -1  -1
counts:  1   2   3   2   3   2   1
count_at(45) → 最后一个 ≤45 的事件是下标 4 → counts[4] = 3
```

### 2.3 区间最大值查询（Range Maximum Query）
- `max_in(a,b)` = max( 区间开始时的人数 `count_at(a)`, 区间内每个事件之后的人数 )。
- 区间内的事件是 `counts` 数组里一段连续下标 `[lo, hi]`（`lo = bisect_left(times, a)`，`hi = bisect_right(times, b) - 1`）。
- 求一段的最大值有三种做法：
  1. **扫描** O(k)（k 为区间内事件数）：最简单，k 小就够；
  2. **稀疏表** O(1) 查询：静态数据最快，但追加需要重建；
  3. **线段树** O(log n) 查询、摊还 O(1)~O(log n) 追加：**动态追加**的最佳折中。参考解用迭代式线段树，容量满了翻倍重建（摊还 O(1)）。

### 2.4 同一个模型，换成 SQL
```sql
-- 某时刻人数：所有 ts <= t 的 delta 之和
SELECT COALESCE(SUM(delta), 0) FROM presence_events WHERE ts <= :t;

-- 区间最大：窗口函数求前缀和，再取区间内最大，并联合"区间开始时的人数"
WITH running AS (SELECT ts, SUM(delta) OVER (ORDER BY ts, seq) AS cnt FROM presence_events)
SELECT MAX(cnt) FROM (
  SELECT cnt FROM running WHERE ts BETWEEN :a AND :b
  UNION ALL
  SELECT COALESCE((SELECT SUM(delta) FROM presence_events WHERE ts <= :a), 0)
);
```
- `seq` 是自增主键，用来在**同一秒**内给事件定序（否则窗口函数的顺序不确定）。
- 在真实库里 `SUM(...) OVER` 每次查询是 O(n)；高频查询要**物化前缀和表**（每个事件写入时顺带记下 `cnt`），或按分钟做**分桶快照**（每分钟存当前人数 + 该分钟峰值）以便区间查询只读 O(区间分钟数) 行。

## 3. 从最笨的解法开始

```python
class Office:
    def __init__(self): self.people = set()
    def enter(self, p): self.people.add(p)
    def leave(self, p): self.people.discard(p)
    def count(self): return len(self.people)
```
**错在哪**：只能回答"现在"；"昨天 3 点"和"区间最大"完全没法回答——**状态被覆盖了，历史丢了**。再进一步的朴素版本：每个查询 `sum(e.delta for e in events if e.ts <= t)`，O(n) 每次；n = 10^6 事件时每次查询 10^6 步。

## 4. 一步一步改进

| 步 | 问题 | 想法 | 变化 | 复杂度 |
|---|---|---|---|---|
| 1 | 历史丢失 | 存事件日志而不是状态 | `events: list[Event]` | 写 O(1) |
| 2 | 每次查询 O(n) | 追加时顺便维护前缀和 `counts` | `counts[i] = counts[i-1] + delta` | 写 O(1) |
| 3 | 找时刻 t 对应哪个前缀 | 时间有序 → 二分 | `bisect_right` | `count_at` O(log n) |
| 4 | 区间最大要扫描 | 线段树维护 `counts` 的区间最大 | `_MaxTree` | `max_in` O(log n) |
| 5 | 脏数据：重复进入、没进就出、时间倒流 | 显式校验并抛具体异常；失败不改变状态 | `AlreadyInside/NotInside/OutOfOrder` | O(1) |
| 6 | 要 SQL 版 | 同模型：事件表 + 窗口前缀和 | `SQL_COUNT_AT`、`SQL_MAX_IN` | 见 2.4 |

## 5. 逐段讲参考解

- `OccupancyTracker._append`：**先校验时间不倒流，再改数组**。顺序重要：如果先改数组再校验，失败会留下脏数据。测试里 `assert t.current() == 1` 证明失败的调用没有改变状态。
- `enter/leave`：用一个 `set` 记录"谁在里面"，用来**拒绝非法序列**（已在里面又进入；不在里面却离开）。它不参与人数计算（人数来自前缀和），只是输入校验。
- 同一秒的多个事件：按**到达顺序**处理。测试里 `a出@40, d进@40` → 40 这一秒结束时人数是 3。若业务要求"同一秒内以出为先"或相反，必须在需求里问清（常见追问）。
- `max_in` 的两部分：`count_at(start)`（区间开始时已在里面的人）与 `tree.query(lo, hi)`（区间内的峰值）取最大。
- 随机对拍测试：400 个随机事件，200 次随机查询，同时对比 **暴力、线段树、SQL** 三个答案。这类"实现 vs 朴素参考实现"的对拍是最便宜、最有效的正确性证据。

## 6. 追问预演

**Q1. 事件可能乱序到达（网络延迟，刷卡机批量上传）。**
答案：有序追加的前缀和失效。方案：(1) **缓冲 + 水位线**：事件先进缓冲区，等到时间 T-Δ 之前都已到达再入账（接受 Δ 的延迟）；(2) 用 **Fenwick 树（BIT）+ 离线坐标压缩**，按时间点单点更新、前缀查询 O(log n)，允许任意顺序插入；(3) 存储层用按时间排序的表，查询时再算（SQL 版本天然支持乱序，只是查询慢）。区间最大在乱序下需要**可更新的线段树**（懒标记区间加）。

**Q2. 事件丢失（有人进了没刷出）。**
答案：每天固定时间（如凌晨）**清零对账**：把仍显示"在里面"的人强制记为离开（事件标注来源 `auto_close`）；并给"不合理的停留时长"（>16 小时）告警。数据质量问题要在模型里有位置，不要假装数据完美。

**Q3. 要回答"某个人在不在"和"某时刻都有谁在"。**
答案：维护每人的**访问区间**表 `visits(person, enter_ts, exit_ts|NULL)`；`who_is_inside_at(t)` = `WHERE enter_ts <= t AND (exit_ts IS NULL OR exit_ts > t)`，加 `(enter_ts)` 索引。事件表和访问区间表是同一事实的两种投影（见 `../sd` 的"日志为准，视图可重建"）。

**Q4. 多栋楼 / 多个门。**
答案：事件加 `building`、`door` 字段，按 `(building)` 分区；楼内人数 = 该楼事件前缀和；全公司人数 = 各楼之和（查询时汇总；或每楼维护独立的追踪器再合并）。一个人从 A 楼门离开、从 B 楼门进入属于不同楼的两个事件，不要做跨楼推断。

**Q5. 并发：多个门同时上报。**
答案：追踪器的写操作是「校验 + 追加三个数组」的复合操作，要加锁（粗锁覆盖整个 `_append`）；若吞吐极高，改成每个门一个队列、单个消费者线程按时间归并写入（单写者原则）。读（`count_at`）可以用读写锁或对不可变快照读取。

**Q6. 要做成服务，一天 1 亿次进出。**
答案：事件进分区日志（按楼分区）；消费者维护"分钟级快照表"：`(building, minute) → (期末人数, 该分钟峰值)`；区间最大 = 对分钟峰值取 max（再按小时/天做二级聚合）；原始事件落冷存储做审计。`max_in` 变成对预聚合表的区间查询，与 `../sd/problems/metrics_timeseries_store.md` 的**可合并聚合 (max)** 同一个思想。

**Q7. 如何测试？**
答案：①空状态；②区间端点（闭区间）；③区间内无事件；④同秒多事件；⑤区间开始时已有人；⑥非法序列且状态不变；⑦随机对拍。

## 7. 常见误区

1. 只存当前人数，历史丢失。
2. `max_in` 漏掉**区间开始时**的人数。
3. 闭区间/开区间不统一（`bisect_left` 与 `bisect_right` 用反）。
4. 先改状态再校验，失败后留下脏数据。
5. 用 `datetime.now()` 作为事件时间（测试不可重复；也不符合"事件时间"语义）。
6. SQL 里窗口函数没有稳定的排序键（同一秒事件顺序不定）。

## 8. 自测题

1. `count_at` 为什么用 `bisect_right`？
<details><summary>答案</summary>要找最后一个 `ts <= t` 的事件（含等于）。`bisect_right` 返回第一个 `> t` 的位置，减一即所需下标。</details>

2. 事件 `+1@10, +1@20, -1@30`，`max_in(25, 25)` 是多少？
<details><summary>答案</summary>区间内无事件，取区间开始时的人数 `count_at(25) = 2`。</details>

3. 如果要求"同一秒内先处理离开再处理进入"，数据结构上怎么保证？
<details><summary>答案</summary>写入前按 `(ts, delta)` 排序（离开 -1 在前），或在 `seq` 里体现；乱序到达的同秒事件需要缓冲。需求必须先问清。</details>

4. 稀疏表和线段树怎么选？
<details><summary>答案</summary>数据静态（离线分析）→ 稀疏表 O(1) 查询；持续追加 → 线段树。</details>

5. （senior）怎么证明 SQL 版与内存版一致？
<details><summary>答案</summary>随机事件序列同时灌入两者，对随机区间对拍（本文件的测试就是这样做的），并把边界（端点、空区间、同秒）作为固定用例。</details>
