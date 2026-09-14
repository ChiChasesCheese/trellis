# od06 · Query Audit Log — record_access / accessed_in_range / unaccessed_since

**类型：** senior 电面（PS，与 LC 212 Word Search II 二合一，60 min）· **最近：** 2024-02
**置信度：** HIGH（逐字 LeetCode Discuss 帖，见文末）

## 背景
面试官原话（转述）："The system should store queries made to snowflake system. User should be
able to find columns, tables accessed in a time period. This system should also tell users what
columns, tables have not been accessed in some time 't'."——candidate 自述这轮"我提了一个设计…
问了约束、用例等"，但面试官几乎全程沉默（"did not utter a single word"）。这条一手记录明确说
这是"开放式设计题，按候选人自己的结构来评分，没有固定期望的 API"——但同一份帖子把它和 LC 212
配对，说明它确实有一个可以被写成小型可运行类骨架的核心，本题把它写成这样一个骨架，供候选人在
"沉默面试官"场景下练习"边讲边写、自己定义边界"。

## API 契约（英文签名）
```python
class QueryAuditLog:
    def record_access(self, query_id: str, ts: int, tables: set[str], columns: set[str]) -> None: ...
    def accessed_in_range(self, name: str, t_start: int, t_end: int) -> list[str]: ...
        # name 是一个 table 名或 column 名；返回在 [t_start, t_end] 闭区间内访问过它的 query_id
        # 列表，按 ts 升序排列，ts 相同则按 query_id 字典序
    def unaccessed_since(self, t: int) -> set[str]: ...
        # 返回所有"曾经被记录过、但最近一次访问时间早于 t（严格小于）"的 table/column 名字的集合
```
`tables`/`columns` 在存储和查询时统一当成"被访问的名字"处理（不区分是表名还是列名——现实中列名
可能跨表重名，本题按"名字字符串"简化，不做表限定；这是本题对开放题的一个明确简化，写在这里而不
是留给候选人现场猜）。

## 规则

### Part 1 — 记录与范围查询
`record_access(query_id, ts, tables, columns)` 记录一次查询：这次查询在时间 `ts` 访问了
`tables | columns` 里的每一个名字。同一个 `query_id` 可能被多次调用（比如重试或分批上报同一个
逻辑查询的不同阶段）——每次调用都是一条**独立的访问记录**，不去重、不覆盖。

`accessed_in_range(name, t_start, t_end)` 返回所有在 `[t_start, t_end]`（闭区间）内访问过
`name` 的 `query_id`，按 `(ts, query_id)` 升序排列；同一个 `query_id` 如果在范围内被记录了
多次（多次 `record_access` 调用都访问过 `name`），在结果里出现多次（一次访问一条记录，不去重）。
从未被访问过的 `name` 返回空列表。

### Part 2 — 时间窗效率与"多久未访问"
`unaccessed_since(t)` 返回所有"曾经被访问过、但最近一次访问的时间戳严格早于 `t`"的名字集合
（包括从系统运行以来从未在 `t` 之后被访问过的所有名字；不包括从未被访问过的名字——那些不在
"曾经被访问过"的范围内，返回的是"曾经出现但现在冷了"的名字，不是"完全不存在"的名字）。

**效率要求**：两个查询都不能是"扫描全部访问记录"的线性实现——访问记录的总条数可以远大于
`name` 的种类数。`accessed_in_range` 必须是 O(log(该 name 的记录数) + 命中数)：每个 `name`
维护一个按 `(ts, query_id)` 排序的列表，`record_access` 时 `ts` 通常非递减到达但**不保证**严格
非递减（允许乱序上报），必须用**二分插入**维持有序，而不是假设输入已排好序直接 `append`；
`accessed_in_range` 用二分查找定位 `[t_start, t_end]` 的边界后切片，不逐条扫描该 `name` 之外的
任何记录。`unaccessed_since` 只维护一份"每个 name 的最近访问时间"字典（`record_access` 时
O(1) 比较更新），查询时对这份字典（大小 = distinct name 数，通常远小于总记录数）做一次遍历——
这是本题对"避免线性扫描"的实际要求：**不扫描访问记录**，但扫描 distinct name 的数量级是可以
接受的（面试里更精巧的"按 last-access 排序的辅助结构 + 懒惰失效"是一个合理的更优追问方向，本题
主实现不要求，见下方并发追问）。

## Worked examples

**例 1（Part1，记录与范围查询）**
```
record_access("q1", 10, {"orders"}, {"orders.id"})
record_access("q2", 20, {"orders"}, set())
record_access("q3", 15, {"customers"}, set())
accessed_in_range("orders", 0, 100)
accessed_in_range("orders", 11, 100)
accessed_in_range("orders.id", 0, 100)
accessed_in_range("customers", 0, 12)
```
→
```
["q1", "q2"]
["q2"]
["q1"]
[]
```
（`accessed_in_range("orders", 0, 100)` 按 ts 升序：q1(ts=10) 先于 q2(ts=20)；
`accessed_in_range("orders", 11, 100)` 排除 ts=10 的 q1；`accessed_in_range("customers", 0, 12)`
排除 ts=15 的 q3，范围内为空。）

**例 2（Part2，`unaccessed_since`——三次 `record_access` 全部先发生，再依次查询）**
```
record_access("q1", 10, {"a"}, set())
record_access("q2", 20, {"b"}, set())
record_access("q3", 25, {"a"}, set())
unaccessed_since(15)
unaccessed_since(21)
unaccessed_since(26)
```
→
```
[]
["b"]
["a", "b"]
```
（三次 `record_access` 在任何查询**之前**就已经全部发生，所以三次 `unaccessed_since` 看到的都
是同一份完整历史：a 最近一次被访问是 `max(10, 25) = 25`（q1、q3 都访问过 a），b 最近一次是
20。`t=15`：`25 < 15` 假、`20 < 15` 假 → 两者都不算冷，`[]`。`t=21`：`25 < 21` 假、`20 < 21`
真 → 只有 b 冷了，`["b"]`。`t=26`：`25 < 26` 真、`20 < 26` 真 → a、b 都冷了，`["a", "b"]`。
`unaccessed_since` 只依据记录的 `ts` 值本身判断，与 `record_access` 调用的先后顺序无关——本例
特意把全部写入放在查询之前，避免"写入与查询交错"的时序歧义。）

## `main()` 命令流
```
RECORD <query_id> <ts> <tables_csv> <columns_csv>   -- csv 用逗号分隔，空集合用字面量 "-"
RANGE <name> <t_start> <t_end>
UNSINCE <t>
```
`RECORD` 无输出。`RANGE` 输出 `repr(list_of_query_ids)`。`UNSINCE` 输出
`repr(sorted(name_set))`（排序保证输出确定性）。

## 边界清单
- 从未记录过的 `name` 调用 `accessed_in_range` 返回 `[]`
- `unaccessed_since` 只统计"曾经被访问过"的名字；从未出现过的名字不在结果里（不是"未知就算冷"）
- 乱序上报：`record_access` 的 `ts` 不保证按调用顺序递增，`accessed_in_range` 的结果仍必须按
  `ts` 正确排序
- 同一个 `query_id` 多次访问同一个 `name`：`accessed_in_range` 里出现多次（一次记录一条），
  `unaccessed_since` 只看"最近一次"，不受重复次数影响
- `t_start > t_end` 的查询范围：返回空列表，不抛异常
- 边界时刻本身：`accessed_in_range(name, t, t)` 命中恰好在 `ts==t` 的记录（闭区间）；
  `unaccessed_since(t)` 用严格小于 `<`，`ts==t` 的记录不算"未访问"（还没到"多久没访问"的门槛）
- 10^5 次 `record_access` + 10^4 次查询，在 2s 预算内完成（二分维护有序结构，不能线性扫描）

## 并发追问
（本题来源本身没有给出显式的并发段落——这是"开放式系统设计题"的通用追问，Cross-cutting 并发
笔记里没有把这道题列入"5/10 有明确并发追问"的清单，但作为练习仍给出一个合理延伸）
1. "多个 worker 同时上报 `record_access`，怎么保证 `accessed_in_range` 不会读到"写了一半"的
   中间态？" —— 期望候选人指出每个 `name` 的有序记录列表在写入（二分插入）时需要加锁，读
   （`accessed_in_range`）可以用读写锁允许并发读、独占写。
2. "这套系统要支撑多租户（多个 Snowflake 账户共用同一套审计日志基础设施），怎么隔离？" —— 
   期望候选人提出按租户 id 分片存储（每个租户一份独立的 name->记录 索引），呼应
   `catalog/CATALOG.md` sd06 的"多租户"追问点。
3. "distinct name 的数量级如果也大到几百万，`unaccessed_since` 遍历整个字典还够用吗？怎么进一步
   优化？" —— 期望候选人提出维护一个按 last-access 排序的辅助结构（例如一棵平衡树，或一个懒惰
   失效的有序列表），把 `unaccessed_since` 降到 O(log N + 命中数)；同时能指出"按 last-access
   排序的列表 + 每次更新都插入一条新记录"这个朴素做法在"几乎每次访问都刷新 last-access"的场景下
   会退化成插入次数等于总记录数、单次插入 O(名字数) 的移位成本，整体退化到接近 O(n²)——真正的
   生产实现需要用平衡树/跳表这类支持 O(log n) 删除旧位置的结构，而不是"只插入不删除的有序列表 +
   懒惰失效"，这是本题主实现刻意回避的一个复杂度陷阱，追问时口头讲清楚即可，不要求现场实现。

## 变体
- 来源把这道题和 LC 212 Word Search II 打包在同一场 60 分钟电面里，说明 Snowflake 的高级/资深
  电面有"一道算法 + 一道开放设计"的组合模式，不是巧合。
- "存储无约束、HA/reliable 等" 是来源原文对这道题的系统设计侧扩展描述，对应 `catalog/CATALOG.md`
  sd06（Audit / Query-Event Log Service），本题只取其编码可测的核心子集。

## 来源与置信度
- https://leetcode.com/discuss/interview-question/4727339/ （2024-02-14，逐字候选人记录，与
  LC 212 Word Search II 同场）
- `catalog/raw/ood.md` #6、`catalog/CATALOG.md` Table B od06 行；置信度 **HIGH**：逐字一手记录，
  但候选人明确说明这是开放式设计题、面试官未给出固定 API——本题的具体方法签名与效率要求是本仓库
  为了让它可测试而做的**收敛**，不代表面试官原话规定了这套确切签名。

## 考什么
S09 类设计先定 API 契约（在开放题里主动收敛出可测试的边界，而不是等面试官给答案）· S06（滑窗/
时间序列查询思路，与限流器、事件流题共享）· D06 审计/治理：不可变、时间窗、多租户（系统设计侧
延伸，见 sd06）
