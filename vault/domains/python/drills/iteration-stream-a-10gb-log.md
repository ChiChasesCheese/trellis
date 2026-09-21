---
nodes: [iteration.generators, iteration.itertools, iteration.context-managers, iteration.iterator-protocol]
tags: [drill, interview]
---
# Drill：用生成器管道统计 10 GB 日志的每小时错误数

日志文件 10 GB，装不进内存，每行形如：

```
2026-09-21T14:03:12 ERROR payment timeout
2026-09-21T14:03:15 INFO  request ok
```

要求写出「按小时统计 ERROR 行数」的管道，额外内存只允许 O(1)（不含最终结果本身，结果里的小时数很少）。

**限制与要求**
- 不许把整个文件或整份行列表读进内存（不能 `f.readlines()`、不能先 `list(...)` 物化中间结果）。
- 用生成器函数或生成器表达式串成管道，不许在中间用列表推导物化一层。
- 文件必须用 `with` 打开，异常路径下也要保证关闭。
- 5 分钟内写完，先说内存复杂度结论再写代码。

**分关要求**
- 第 1 关（约 5 分钟）：写出生成器管道 + 用 `with` 管理文件。
- 第 2 关：追问——如果改用 `itertools.groupby()` 按小时分组，对输入顺序有什么要求？日志本身按时间顺序写入，还需要额外排序吗？
- 第 3 关：追问——如果要同时统计「按小时的错误数」和「按小时的总行数」两份指标，用 `itertools.tee()` 拆成两条分支，什么情况下反而比 `list(lines)` 再遍历两次更差？
- 第 4 关：追问——写完的管道对象能不能被两次 `for` 遍历拿到同样的统计结果？为什么某些线上代码会在这里踩坑？

**评分点（强答案会命中）**
- 生成器（表达式或函数）只在被 `next()` 驱动时才计算下一个值，任意时刻只保留当前一步需要的状态，内存 O(1)；列表推导会立刻物化成完整 list，内存正比于行数 [[genexp-lazy-vs-listcomp-materialize]]
- `with open(path) as f: ...` 展开为「`__enter__` → 执行块 → 无论正常结束还是异常都调用 `__exit__`」，保证文件句柄一定被关闭一次 [[with-statement-desugars-to-try-finally]]
- `groupby()` 只在相邻元素 key 变化时切分新组，不会跨越整个序列聚合同 key 元素；日志本身按时间戳升序写入，同一小时的行天然相邻，不需要额外排序，但如果输入源不保证有序就必须先排序，否则会把同一小时拆成多个不连续的组 [[groupby-requires-presorted-input]]
- `tee()` 要在两分支之间缓存「进度差」内的元素，一个分支遥遥领先另一个时缓存会逼近整个序列大小；提前就知道会有一个分支几乎读完、另一个才刚开始时，直接 `list(it)` 再各自遍历通常更快也更省心 [[tee-buffers-gap-between-branches]]
- 生成器耗尽后没有「倒带」机制，`__next__()` 只会不断抛 `StopIteration`；要再统计一遍必须重新调用生成器函数或重新打开文件，产生一个全新的迭代器对象 [[generator-is-one-shot-cannot-restart]] [[iterator-exhausted-must-reiter]]
- 用 `@contextlib.contextmanager` 自己写文件相关的上下文管理器时，必须把 `yield` 包在 `try/finally` 里，因为 `with` 块内的异常会在 `yield` 处重新抛入生成器，只有 `finally` 能保证无论是否异常都执行清理 [[contextmanager-decorator-yield-splits-enter-exit]]

**参考答案**

```python
from collections import Counter

def read_lines(path):
    with open(path) as f:
        yield from f

def error_hours(lines):
    for line in lines:
        ts, level, *_ = line.split(maxsplit=2)
        if level == "ERROR":
            yield ts[:13]  # 精确到小时，如 "2026-09-21T14"

def hourly_error_counts(path):
    counts = Counter()
    for hour in error_hours(read_lines(path)):
        counts[hour] += 1
    return counts
```

`read_lines` 用 `with` 打开文件、`yield from f` 逐行产出，文件对象本身就是行迭代器，异常时 `__exit__` 仍会被调用；`error_hours` 过滤并截断出小时粒度的 key，两层生成器串联，没有任何一层物化整份数据，额外内存只有 `Counter`（大小等于不同小时数，通常几十到几百）。

第 2 关：日志天然按时间戳升序追加，同一小时的行本来就相邻，`groupby(error_hours(...))` 不需要额外排序；但只要输入来源不保证严格按时间排序（比如合并了多台机器的日志），就必须先按小时 key 排序，否则会把同一小时拆成几段不连续的组。

第 3 关：如果错误行数远少于总行数，「统计错误数」这条分支会飞快跑完，「统计总行数」这条分支却要陪着遍历全部 10 GB——`tee` 要在这段进度差里缓存所有跳过的行，最坏时接近整个文件大小，完全违背了流式处理的初衷；这种场景下不如先把行物化成 `list`（如果内存允许）或者干脆在同一次遍历里用一个循环同时更新两个 `Counter`，不用 `tee`。

第 4 关：不能。`hourly_error_counts` 内部的生成器管道遍历一次就耗尽，函数返回后 `Counter` 已经是最终结果，但如果代码结构里把某个中间生成器对象保存下来想复用（比如把 `error_hours(read_lines(path))` 赋值给一个变量，两处代码各 `for` 一遍），第二次遍历会直接得到空结果，因为文件已经读到末尾且生成器帧已耗尽——这是把生成器当「可重复的容器」误用的典型 bug，正确做法是每次都重新调用生成器函数（对应重新 `open` 文件）。

**尝试记录**
| 日期 | 用时 | 卡在哪 | 下次 |
|---|---|---|---|
