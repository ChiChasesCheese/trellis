# pc01 · Grouped Aggregation：练的是"单遍累加"和"分块再合并"是同一个答案

> [!tldr]
> - 这题考的是：百万行数据按 id 分组求和，装不下内存时怎么办
> - 三步套路：单遍 dict 累加（能装下时的基本解）→ 按 `chunk_size` 切块、每块独立聚合 → 合并局部结果
> - 最值得带走的一个模式：**只要聚合函数满足结合律（sum/count/max 都满足），"分块算局部结果再合并"
>   和"一次性算全量"永远同一个答案**——这是 MapReduce 的骨架，单机小规模一样适用

## 1. 题目在说什么（人话版）

给一份几百万行的 CSV（或 DataFrame），每行是 `id,amount`，把同一个 `id` 的 `amount` 加起来。
数据量大到不一定能一次性放进内存的时候，怎么办？

```
输入：
A,10.50
B,5.25
A,3.75

输出（按 id 排序，两位小数）：
A,14.25
B,5.25
```

## 2. 读题：把文字变成模型

- **实体**：一条条 `(id, amount)` 记录；输出是"每个 id 的总额"。
- **输入长什么样**：一行一条记录，没有表头；`amount` 是十进制字符串，可能带负号（退款）。
- **输出要什么**：按 `id` 排序，金额两位小数字符串。
- **状态**：一个 `dict[id] -> 累计金额`。数据量大时还要多一层状态：**每一块的局部 dict**，以及
  "怎么把多个局部 dict 合并成一个"。
- **一句话建模**：这是一个**分组累加**问题；当输入太大装不下时，变成**局部聚合 + 合并**（同一个
  数学答案，只是分两步算）。

> [!note] 为什么选 dict 而不是先排序再扫描
> 候选方案："先按 id 排序，再顺序扫描找连续段求和"——正确，但多花 O(n log n) 排序时间，且流式
> 场景下数据不是天然有序的。`dict` 累加是 O(n) 单遍，而且天然支持"边读边算"，不需要先攒齐所有数据。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：`main()` 读入 → 按 part 分发 → 调用核心函数 → 排序格式化输出。先让"空实现"跑
   起来。
2. **Part 1 最小可用**：`csv.reader` 逐行解析，`totals[id] = totals.get(id, 0) + amount`；用题面
   样例自测，注意金额用 `Decimal` 不用 `float`。
3. **Part 2 叠加**：把已经读到内存的行按 `chunk_size` 切片，每片调 Part 1 的函数得到局部
   `dict`，写一个 `merge(a, b)` 函数把两个局部 dict 相加，依次合并所有片。有余力再讨论
   `ThreadPoolExecutor`/`ProcessPoolExecutor` 怎么接进去。
4. **收尾**：Part 3 把 key 换成 `(id, category)` 元组，同一个累加循环里再维护 `count` 和
   `max`；输出前排序、格式化单独一个函数处理。

## 4. 代码怎么组织

```
iter_rows(lines) -> Iterator[(id, amount)]        # 只管流式解析，用 csv 模块
group_sum_streaming(lines) -> dict[id, Decimal]    # Part 1：单遍累加
chunked_group_sum(lines, chunk_size, workers) -> dict[id, Decimal]  # Part 2：切块+合并
multi_key_aggregate(lines) -> dict[(id,cat), {...}]  # Part 3：复合键多聚合
part1/2/3(lines) -> list[str]                      # 解析 header/参数 + 调核心函数 + 格式化
_fmt_amount(d) -> str                              # 输出格式集中一处（两位小数）
main(stdin, stdout)                                # 分发
```
把"解析一行"（`iter_rows`）和"核心累加逻辑"（`group_sum_streaming`）拆开，Part 2 的
`chunked_group_sum` 才能直接复用 Part 1 的函数处理每一块，不用重写一遍解析逻辑。

## 5. 核心代码（骨架，≤ 40 行，带注释）

```python
def group_sum_streaming(lines):
    totals = {}
    for key, amount in iter_rows(lines):   # csv.reader 逐行解析
        totals[key] = totals.get(key, ZERO) + amount
    return totals

def chunked_group_sum(lines, chunk_size, workers=1):
    rows = [ln for ln in lines if ln.strip()]
    chunks = [rows[i:i+chunk_size] for i in range(0, len(rows), chunk_size)]
    if workers == 1:
        partials = [group_sum_streaming(c) for c in chunks]
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            partials = list(pool.map(group_sum_streaming, chunks))
    totals = {}
    for p in partials:
        totals = _merge_totals(totals, p)   # 结合律：合并顺序不影响结果
    return totals
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「Let me confirm: no header row, amounts are decimal strings, and I should treat this
  as money — so I'll use `Decimal`, not `float`, to avoid rounding drift.」
- 写 Part 1 时：「I'm using a dict keyed by id, since a single pass with O(1) amortized lookups
  is the natural shape for a group-by-sum, and it also means I never hold more than the running
  totals in memory.」
- 交付 Part 2 时：「Since sum is associative, chunking and re-aggregating gives the exact same
  answer as one pass — that's the property I'd assert in a test, independent of chunk size or
  worker count.」

## 7. 常见跑偏（方法层面，3 条）

- 上来就想着"用 pandas 的 groupby 一行解决"——面试官会追问"如果这台机器装不下整份 DataFrame
  呢"，不如一开始就讲清楚单遍累加的思路，pandas 只是同一模式的库实现。
- 把"分块"和"合并"焊死在一起写成一个大函数，讨论"要不要并行"时改不动——应该先把"聚合一块"和
  "合并两个局部结果"拆成独立函数。
- 用浮点数累加金额，测试里的 `x.xx5` 舍入边界或大量小数相加直接对不上。

## 8. 同族题 / 延伸

- 本 kit `pc09_price_data_store`（时间序列聚合，同一个"单遍维护状态"母题，若已建）。
- `../../snowflake/loop/rounds/03_phone_coding/pc03_recent_event_stream/`：同样是"单遍扫描 + 状态
  累加"骨架，只是保留策略换成滑动窗口。
- `../../stripe/problems/q42_loose_record_aggregation/`：同一个"按 key 分组累加"母题，换成了
  schema 不固定、字段可能缺失的记录。
- 练习命令：`python3 loop/mock.py start pc01`
