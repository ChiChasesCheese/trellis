---
id: bank-log-processing-adjacent-runs
node: bank.practical.log-processing
type: qa
step: 3
---
## Q
把相邻且相同的采样合并成一段 `(开始, 结束, 内容, 次数)`。按内容用 `Counter` 计数、忘了冲出最后一段、用 `if last:` 判断「有没有上一段」，各会出什么错？

## A
**只合并相邻的；用 `is not None` 判起点；结尾冲出最后一段**

- **相邻才合并**：`a a b a` 是三段，不是两段。按值计数会把不相邻的也加在一起：这批数据得到 `{("a",): 3, (): 1}`，顺序和分段都丢了；
- **读到第一个不同的就产出上一段**：不要为了「看看是不是最后一段」多读一个采样，对无穷流会一直卡住；
- **结尾冲出**：循环结束时手里还有一段没产出，漏掉它，最后一段就永远丢了；
- **空内容是合法值**：空栈 `()` 是 falsy。用 `if last:` 判断「有没有上一段」，两个连续的空栈会被当成两段（实测：`(1, ())`、`(2, ())` 各自成段）。用 `is not None`；
- **空输入**：没有采样就没有输出，不是一段空记录。

```python
def compress(samples):
    run = None                               # [start, end, stack, count]
    for ts, stack in samples:
        if run is not None and run[2] == stack:
            run[1], run[3] = ts, run[3] + 1
        else:
            if run is not None: yield tuple(run)     # 读到第一个不同的，就产出上一段
            run = [ts, ts, stack, 1]
    if run is not None: yield tuple(run)             # 收尾：别丢最后一段

data = [(1, ("a",)), (2, ("a",)), (3, ()), (4, ("a",))]
print(list(compress(data)))                  # 三段：不相邻的 ("a",) 不合并，空栈合法
print(list(compress([])))                    # []：空输入没有输出
```

<details class="pt"><summary>延伸</summary>

`itertools.groupby(samples, key=...)` 也只合并相邻的，写起来更短；但开始、结束、次数要自己从每组里取，而且一组必须先取完才能继续往下走。这里的 `start`、`end` 是第一个和最后一个被合并采样的时间戳，不是用间隔推出来的时长。完整合同见 [[solution-lcp-stack-trace-stream|流式调用栈处理器（Streaming Stack Trace Processor）]]。

</details>

**知识点：**日志处理与聚合（Log Processing）
