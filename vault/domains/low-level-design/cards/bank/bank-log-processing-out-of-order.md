---
id: bank-log-processing-out-of-order
node: bank.practical.log-processing
type: qa
step: 4
---
## Q
日志或采样不严格按时间到达，而下游处理器（要求时间戳递增，或者按时间窗口统计）需要有序的输入，内存又不能随流无限增长。怎么办？

## A
**小顶堆加水位线：只缓冲迟到上限以内的数据**

- **水位线**：已见的最大时间戳减去允许的迟到量 K。时间戳不超过水位线的记录，之后不会再有更早的，可以放行；
- **内存有界**：堆里最多是 K 个时间单位内的记录，与流长度无关；代价是输出整体晚 K；
- **越过水位线才到的**：下游已经处理过它的时间，插不回去。计数并丢弃，或者写旁路，不能撤回已经产出的结果。代码里的 `(1, "z")` 就进了 `late`；
- **堆元组带到达序号**：`(时间戳, 序号, 记录)`。同时间戳按到达顺序出，也不会去比较记录本身，两个 `dict` 比较会抛 `TypeError`；
- **输入结束要冲出堆**：否则最后 K 个单位的数据永远出不来，代码用一个 `None` 哨兵触发；
- **窗口统计是同一个机制**：滚动窗口的起点是 `ts - ts % width`，左闭右开（宽度 60 时，59 属于 [0, 60)，60 属于 [60, 120)）；水位线越过窗口末端，这个窗口才算完，输出之后不再改。

```python
import heapq, itertools, math
def reorder(items, lateness, late):               # items: (ts, payload)
    heap, newest, emitted, tie = [], -math.inf, -math.inf, itertools.count()  # tie：同刻按到达顺序
    for item in itertools.chain(items, [None]):   # None：输入结束，冲出堆里全部
        if item is not None:
            if item[0] < emitted:                 # 比已放行的还早：插不回去
                late.append(item); continue
            heapq.heappush(heap, (item[0], next(tie), item)); newest = max(newest, item[0])
        mark = math.inf if item is None else newest - lateness
        while heap and heap[0][0] <= mark:        # 水位线之下不会再有更早的
            emitted, _, out = heapq.heappop(heap); yield out
late = []
feed = [(1, "a"), (3, "c"), (2, "b"), (6, "f"), (4, "d"), (1, "z"), (5, "e")]
print([p for _, p in reorder(feed, 2, late)], late)   # a..f 有序，late 里是 (1, 'z')
```

<details class="pt"><summary>延伸</summary>

多个来源时，每个来源各有水位线，整体取最小；某个来源长期没有数据，要设空闲超时，否则全局水位线卡住，整条流不再前进。调用栈转换器要求时间戳严格递增，乱序就在它前面用这个缓冲消掉，转换器本身不用改，见 [[solution-lcp-stack-trace-stream|流式调用栈处理器（Streaming Stack Trace Processor）]]；按（时间，序号）出队的最小堆，任务调度器用的也是它。

</details>

**知识点：**日志处理与聚合（Log Processing）
