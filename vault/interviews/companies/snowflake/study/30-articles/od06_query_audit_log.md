# od06 · Query Audit Log：按 name 分片的有序记录，练的是"在开放题里自己收敛出可测试边界"

> [!tldr]
> - **本题的具体方法签名和效率要求是 (reconstructed)**：来源是一道"沉默面试官"的开放式设计题，候选人自述"面试官几乎全程沉默"、没有给出固定 API；本题为了可测试，收敛出下面这套具体契约，不代表面试官原话规定了它
> - 这题考的是：记录"查询访问了哪些表/列"，支持按时间范围查询访问记录、以及"哪些名字最近没被访问过"，且不能是线性扫描全部记录
> - 三步套路：先想清楚"按 name 分片存储"这个核心设计决策 → Part 1 用有序列表 + 二分维护范围查询 → Part 2 单独维护一个"最近访问时间"字典支持高效的"多久未访问"查询
> - 最值得带走的一个模式：**总记录数和 distinct key 数是两个不同量级，效率要求要按"该扫哪一个"来设计数据结构**——range 查询按 name 分片二分，"多久未访问"只扫 distinct name 数量级的字典

## 类设计先定契约
```python
class QueryAuditLog:
    def record_access(self, query_id: str, ts: int, tables: set[str], columns: set[str]) -> None: ...
    def accessed_in_range(self, name: str, t_start: int, t_end: int) -> list[str]: ...
        # [t_start, t_end] 闭区间内访问过 name 的 query_id 列表，按 (ts, query_id) 升序
    def unaccessed_since(self, t: int) -> set[str]: ...
        # 曾被访问过、但最近一次访问时间严格早于 t 的名字集合
```
**不变量（写代码前先想清楚）**：
1. 同一个 `query_id` 可能多次调用 `record_access`，每次都是独立记录，不去重、不覆盖。
2. `accessed_in_range` 必须是 `O(log(该 name 的记录数) + 命中数)`——不能扫描该 `name` 之外的任何
   记录，更不能扫描全部访问记录。
3. `record_access` 的 `ts` 不保证按调用顺序递增（允许乱序上报），但每个 `name` 的记录列表必须始终
   保持有序，用二分插入维护，不能假设"直接 append"就有序。
4. `unaccessed_since` 只维护一份"每个 name 的最近访问时间"字典，查询时只遍历这份字典（大小 =
   distinct name 数），不遍历访问记录本身。
5. `unaccessed_since(t)` 用严格小于 `<`——`ts==t` 的记录不算"未访问"。

## 1. 题目在说什么（人话版）
`record_access` 记录一次查询在某个时间点访问了哪些表和列；`accessed_in_range` 查某个表/列名在某个
时间范围内被哪些查询访问过；`unaccessed_since` 查哪些"曾经出现过"的名字最近一段时间没被访问（用于
找"冷"数据）。数据量可能很大（总记录数远大于 distinct 名字数），两个查询都不能线性扫描全部记录。

三行小例子：
```
record_access("q1", 10, {"orders"}, {})
record_access("q2", 20, {"orders"}, {})
accessed_in_range("orders", 11, 100)  -> ["q2"]   (排除ts=10的q1)
unaccessed_since(15)  -> []                        (orders最近访问是20，20<15为假)
```

## 2. 读题：把文字变成模型
- **实体**：查询（`query_id`、`ts`、访问的表/列名集合）、名字（表名或列名，统一当字符串处理）。
- **输入长什么样**：`main()` 命令流 `RECORD/RANGE/UNSINCE`。
- **输出要什么**：`RANGE` 输出 query_id 列表；`UNSINCE` 输出排序后的名字集合。
- **状态**：`dict[name, 按(ts,query_id)排序的列表]`（每个名字自己的访问历史）+
  `dict[name, 最近访问时间]`（O(1) 更新的辅助索引）。
- **一句话建模**：这是一个 **按 key 分片的时间序列存储**——range 查询是"对单个分片做二分范围查找"，
  "多久未访问"是"维护一份独立的、体量远小于总记录数的聚合索引"。

> [!note] 为什么选这个数据结构
> 如果所有记录混在一个全局列表里，`accessed_in_range` 就必须先过滤出属于这个 `name` 的记录再二分，
> 退化成线性扫描。按 `name` 分片后，每个分片自己有序，`accessed_in_range` 只需要在这一个分片内二分，
> 复杂度只跟"这个 name 自己的记录数"相关，和总记录数、其他 name 的记录数无关。`unaccessed_since`
> 如果去扫全部记录找"每个 name 的最大 ts"，会随总记录数增长；单独维护一份"name -> 最近时间"字典，
> 每次 `record_access` 只需要 O(1) 比较更新，查询只遍历 distinct name 的数量级。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **接口先行（在开放题里主动收敛）**：面试官不给固定 API 时，先把这三个方法的输入输出形状、
   排序规则、"重复算不算"、"范围边界开闭"这些歧义点自己定下来并大声说出来，再动手写——这是本题
   真正在考的能力。
2. **Part 1 最小可用**：`record_access` 对 `tables|columns` 里每个名字，把 `(ts, query_id)` 插入
   这个名字自己的列表（用 `bisect.insort` 保持有序，因为 `ts` 可能乱序到达）。`accessed_in_range`
   用两次 `bisect_left` 定位 `[t_start, t_end]` 的边界后切片。
3. **Part 2 叠加**：`record_access` 里顺带更新 `last_access[name] = max(现有值, ts)`；
   `unaccessed_since(t)` 遍历 `last_access` 字典，挑出值严格小于 `t` 的 key。
4. **收尾**：乱序上报、`t_start>t_end`、同一 query_id 多次访问同一 name、从未记录过的 name 这些边界
   过一遍；用官方例子验证排序规则（`(ts, query_id)` 升序）。

## 4. 代码怎么组织
```
QueryAuditLog.__init__               # _records: name -> 有序(ts,query_id)列表；_last_access: name -> ts
record_access(query_id, ts, tables, columns)   # 对每个名字二分插入 + O(1) 更新最近访问时间
accessed_in_range(name, t_start, t_end)         # 两次 bisect_left 定位边界后切片
unaccessed_since(t)                              # 遍历 _last_access，挑 ts<t 的 key
main(stdin, stdout)                              # 解析命令流，分发
```
两个查询方法各自只依赖自己需要的那份索引（`_records` vs `_last_access`），互不干扰——这样面试官问
"如果只要 range 查询，能不能不维护 last_access"时，可以直接指出这是两个独立的索引，各自可以单独
存在。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
class QueryAuditLog:
    def __init__(self):
        self._records = {}       # name -> 按 (ts, query_id) 排序的列表
        self._last_access = {}   # name -> 最近一次访问时间

    def record_access(self, query_id, ts, tables, columns):
        for name in tables | columns:
            bisect.insort(self._records.setdefault(name, []), (ts, query_id))  # 乱序到达，二分插入
            if ts > self._last_access.get(name, float("-inf")):
                self._last_access[name] = ts

    def accessed_in_range(self, name, t_start, t_end):
        if t_start > t_end:
            return []
        lst = self._records.get(name)
        if not lst:
            return []
        lo = bisect.bisect_left(lst, (t_start, ""))      # 空字符串比任何真实 query_id 都小，精确定位
        hi = bisect.bisect_left(lst, (t_end + 1, ""))     # 只在这个 name 的分片内二分，不扫别的记录
        return [qid for _, qid in lst[lo:hi]]

    def unaccessed_since(self, t):
        return {name for name, ts in self._last_access.items() if ts < t}   # 遍历 distinct name 数量级
```

## 6. 并发追问怎么答
- **多个 worker 并发 `record_access`，怎么保证 `accessed_in_range` 不读到"写了一半"的中间态**：
  每个 `name` 自己的有序列表在二分插入时需要加锁；读操作（`accessed_in_range`）可以用读写锁允许
  并发读、独占写，因为读写冲突只发生在同一个 `name` 上，不同 `name` 之间天然互不干扰。
- **多租户隔离怎么做**：按租户 id 分片存储——每个租户一份独立的 `name -> 记录` 索引，避免不同租户的
  查询互相扫到对方的数据，也方便按租户单独限流/清理。
- **distinct name 数量级也大到几百万，`unaccessed_since` 遍历整个字典还够吗**：可以提出维护一个
  按 last-access 排序的辅助结构（平衡树/跳表）把查询降到 `O(log N + 命中数)`；但要点明一个陷阱——
  "只插入不删除的有序列表 + 懒惰失效"在"几乎每次访问都刷新最近时间"的场景下会退化到接近 O(n²)
  （每次更新都要在列表中间插入新位置），真正的生产实现需要支持 O(log n) 删除旧位置的结构，这一点
  口头讲清楚即可，本题主实现不要求现场写出来。

## 7. 常见跑偏（方法层面，3 条）
- **假设 `ts` 按调用顺序递增，直接 `append` 而不是二分插入**：题目明确允许乱序上报，直接 append
  会破坏"每个 name 的记录列表始终有序"这个不变量，导致后续二分查找结果错误。
- **`accessed_in_range` 扫描全部记录再过滤 `name`**：即使结果是对的，也违反了效率要求——必须先按
  `name` 分片，只在这一个分片内做二分。
- **`unaccessed_since` 把"从未被访问过的名字"也算进结果**：题目明确"曾经被访问过、但最近一次访问
  早于 t"，从未出现过的名字不在"曾经被访问过"的范围内，不能返回。

## 自测清单
- 从未记录过的 name 调 `accessed_in_range` 返回 `[]`。
- `unaccessed_since` 不包含从未出现过的名字。
- 乱序上报后 `accessed_in_range` 结果仍按 `(ts, query_id)` 正确排序。
- 同一 query_id 多次访问同一 name，`accessed_in_range` 里出现多次；`unaccessed_since` 只看最近一次。
- `t_start > t_end` 返回空列表，不抛异常。
- 边界时刻：`accessed_in_range(name, t, t)` 命中 `ts==t`；`unaccessed_since(t)` 严格小于，`ts==t`
  不算冷。
- 1e5 次 `record_access` + 1e4 次查询在 2s 内完成（验证用的是二分而非线性扫描）。

## 相关题与 skills id
- skills: **S09**（类设计先定契约，在开放题里主动收敛出可测试边界）· **S06**（滑窗/时间序列查询，
  与限流器、事件流题共享）· D06（审计/治理：不可变、时间窗、多租户，系统设计侧延伸见 sd06）。
- 同族：与 Stripe 的 `ps01_transaction_stream_levels`（按用户分组 + 时间窗口）共享"按 key 分片 +
  有序扫描"的核心方法论,只是这里是按二分而不是滑窗 deque。
- 练习命令：`python3 loop/mock.py start od06`
