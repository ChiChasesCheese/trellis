# pc01 · Grouped Aggregation — 单遍 dict 累加 → 分块聚合再合并 → 多键多聚合

> Millennium LEaD 第一轮（45 min：15 min 背景 + 30 min 实时编码，Webex + HackerRank）。Part 1、Part 2
> 是一手报道的原题机制；Part 3 **(reconstructed)**。面试官允许查语法（不是纯记忆考核）。

## 背景

2025-12 一位 Quant Developer-Python 候选人（Round 3）在 LeetCode Discuss 报道："given a
dataframe or csv with millions of records, group by a common identifier and find aggregated
sums… solved by chunking and re-aggregating"。这不是一道"背 pandas API"的题：面试官想看的是候选人
知不知道**百万行数据不一定能一次性放进内存/一个 DataFrame**，于是先给出单遍 dict 累加的基本解，
再被引导到"分块处理、每块独立聚合、再合并局部结果"这个模式——这正是 MapReduce 的"map → 局部
reduce → 合并"骨架，只是规模小到单机就能做。

## API 契约（英文签名）

```python
def group_sum_streaming(lines: Iterable[str]) -> dict[str, Decimal]
def chunked_group_sum(lines: Sequence[str], chunk_size: int, workers: int = 1) -> dict[str, Decimal]
def multi_key_aggregate(lines: Iterable[str]) -> dict[tuple[str, str], dict[str, object]]
```
输入行是不带表头的 CSV 数据行。`group_sum_streaming` / `chunked_group_sum` 的每行是
`id,amount`；`multi_key_aggregate` 的每行是 `id,category,amount`。`amount` 是十进制字符串（可
带负号，两位小数或更多），内部一律用 `decimal.Decimal` 累加并四舍五入（`ROUND_HALF_UP`）到 2
位，不用浮点数。字段数不对、`id`/`category` 为空、`amount` 不是合法数字 → `ValueError`。
`chunk_size <= 0` 或 `workers <= 0` → `ValueError`。

## 规则

### Part 1 — 单遍纯 Python 流式 group-sum（一手原题的基本解）

用 `csv` 模块逐行解析，`dict` 按 `id` 累加 `amount`。一次遍历，除了结果字典本身，不额外持有一个
随行数会增长的容器。

### Part 2 — 分块 → 每块聚合 → 合并（一手原追问："chunking and re-aggregating"）

把行序列按 `chunk_size` 切块，每块独立跑 Part 1 的逻辑得到一个局部 dict，再把所有局部 dict 合并
成总表。`workers > 1` 时用 `concurrent.futures.ThreadPoolExecutor` 把"每块聚合"这一步分发出去。
因为 `sum` 满足结合律，局部字典按任意顺序合并结果都一样——**这个确定性（与 `chunk_size`、
`workers` 无关）就是本题的核心断言**，不是"跑得更快"。

### Part 3 — 多键分组 + 多聚合 **(reconstructed)**

按 `(id, category)` 复合键分组，同一遍里累计三个聚合：`sum`、`count`、`max`。输出按
`(id, category)` 字典序排序。

## Worked examples（全部由 `solution.py` 实际运行得出，不手算）

**例 1（Part 1）**
```python
lines = ["A,10.50", "B,5.25", "A,3.75", "C,100", "B,0.75"]
part1(lines)
```
→ `['A,14.25', 'B,6.00', 'C,100.00']`

**例 2（Part 2，同一批数据、`CHUNK_SIZE 2` 切成 3 块，结果与例 1 完全一致）**
```python
lines = ["CHUNK_SIZE 2", "A,10.50", "B,5.25", "A,3.75", "C,100", "B,0.75"]
part2(lines)
```
→ `['A,14.25', 'B,6.00', 'C,100.00']`

**例 3（Part 3，含负数金额——退款场景，会拉低 sum 但不影响 max）**
```python
lines = [
    "A,groceries,10.50",
    "A,transport,4.00",
    "A,groceries,3.75",
    "B,groceries,100",
    "A,groceries,-1.25",
]
part3(lines)
```
→ `['A,groceries,13.00,3,10.50', 'A,transport,4.00,1,4.00', 'B,groceries,100.00,1,100.00']`
（`A,groceries` 三条：`10.50 + 3.75 - 1.25 = 13.00`，`count=3`，`max=10.50`）

## `main()` 命令流

```
PART 1                          PART 2                                  PART 3
A,10.50                         CHUNK_SIZE 2                             A,g,1
B,5.25                          A,10.50                                  A,g,2
A,3.75                          B,5.25                                   B,h,5
→ A,14.25                       A,3.75
  B,5.25                        C,1
                                 → A,14.25
                                   B,5.25
                                   C,1.00
                                                                          → A,g,3.00,2,2.00
                                                                            B,h,5.00,1,5.00
```

## 边界清单

- 空输入（`lines = []`）→ `{}` / 空输出，不报错
- 单条记录
- 同一 `id`（或 `(id, category)`）出现重复行——这是本题的核心场景，不是边界
- 负数金额（退款/冲正）：参与 `sum`，不应成为 `max`
- 非法行：字段数不对（`"A"` 或 `"A,1,2"` 喂给 Part 1）、`amount` 非数字（`"A,xyz"`）、`id`/
  `category` 为空串（`",10"`）→ 均 `ValueError`
- `chunk_size <= 0`、`workers <= 0` → `ValueError`
- `chunk_size` 大于总行数（退化成 1 块）、`chunk_size == 1`（每行一块）——结果必须和不分块一致
- 输出排序：`id`（Part 1/2）或 `(id, category)`（Part 3）字典序，两位小数格式（`"6.00"` 不是
  `"6"` 或 `"6.0"`）

## 追问

1. **内存上限**：如果整份 CSV 装不进内存，Part 1 的 `lines` 参数应该是什么？——期望候选人说出
   "一个生成器/文件迭代器，而不是先 `readlines()` 整份文件"，对应 `iter_rows` 的流式写法。
2. **为什么分块还要合并，而不是每块算完直接输出？**——因为同一个 `id` 可能分散在不同块里，块内
   聚合只是"局部和"，必须再合并才是全局答案。
3. **为什么用多进程而不是多线程？**——这一步是 CPU-bound（`Decimal` 加法 + `csv` 解析），CPython
   的 GIL 让多线程在这里几乎不加速；生产实现应该用 `ProcessPoolExecutor`，代价是每块要跨进程
   pickle。本题用线程演示同一个"分发—合并"模式，不代表这是最优选择。
4. **`pandas.read_csv(chunksize=...)` 呢？**——同一个模式的库实现：`chunksize` 参数本身就是
   "分块迭代器"，每块是一个 DataFrame，`.groupby(id).sum()` 再对多个块的结果 `pd.concat` +
   再 `groupby().sum()` 一次；HackerRank 的执行环境不一定装了 pandas，所以本题的参考解只依赖
   标准库，`pandas` 只在测试里作为交叉验证。

## 来源与置信度

- **HIGH（一手）**：LeetCode Discuss 7423863（2025-12，Quant Developer-Python，Round 3）："given
  a dataframe or csv with millions of records, group by a common identifier and find aggregated
  sums… solved by chunking and re-aggregating"；面试官允许查语法。
- Part 3（多键多聚合）为重建，练习同一套单遍累加骨架扩到复合键与多个聚合函数。

## 考什么

单遍累加 vs 分块-合并的等价性（结合律）· 流式解析不整份 `readlines()` · `Decimal` 金额处理 ·
`concurrent.futures` 的"分发工作、合并结果"模式 · 多键分组扩展。
