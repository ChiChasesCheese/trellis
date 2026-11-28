---
id: mlp-coding-pc01-followups
node: coding.pc01
step: 2
type: qa
---
## Q
**百万行分组求和：追问与变体**｜编程轮

写完单遍 dict 累加和分块聚合之后，面试官会继续追问哪些问题？每个怎么答？

## A
- **文件装不进内存：** 参数传文件迭代器或生成器，不要 `readlines()`；`csv.reader(f)` 本来就是逐行读。
- **为什么分块后还要合并：** 同一个 id 可能分散在不同块里，块内总额只是局部和，合并后才是全局答案。
- **多线程还是多进程：** 解析和 `Decimal` 加法是 CPU 密集型任务，CPython 的 GIL（全局解释器锁，同一时刻只有一个线程跑 Python 代码）让多线程几乎不加速；要加速用 `ProcessPoolExecutor`，代价是每块数据要在进程间序列化（pickle）。线程版只是演示"分发、合并"的模式。
- **pandas 怎么做：** `pd.read_csv(chunksize=n)` 返回块迭代器，每块 `groupby(id).sum()`，再把各块结果 `concat` 后 `groupby().sum()` 一次，和手写是同一个模式。
- **多键多聚合：** key 换成元组 `(id, category)`，同一遍里同时维护 sum、count、max：

```python
g = groups.setdefault((key, cat), {"sum": Decimal("0.00"), "count": 0, "max": None})
g["sum"] += amt
g["count"] += 1
if g["max"] is None or amt > g["max"]:   # 负数退款拉低 sum，但不该成为 max
    g["max"] = amt
```

- **会多花一个测试用例的边界：** 空输入返回空结果；`chunk_size` 大于行数（只有一块）或等于 1（每行一块），结果必须与不分块相同；字段数不对、id 为空、金额不是数字都抛 `ValueError`；输出必须是 `6.00`，不是 `6` 或 `6.0`。

**英文答法。**
- "If it doesn't fit in memory, I'd **stream** the file and keep only the running totals."
- "For real speed-up I'd use **processes**, because this work is CPU-bound and the GIL blocks threads."
- "Because aggregation is associative, I can **assert** in a test that results don't depend on chunk size or worker count."
