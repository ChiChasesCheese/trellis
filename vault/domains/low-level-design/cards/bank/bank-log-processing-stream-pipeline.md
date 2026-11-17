---
id: bank-log-processing-stream-pipeline
node: bank.practical.log-processing
type: qa
step: 1
---
## Q
要在 20 GB 的日志里数各个级别的条数。`f.readlines()` 或 `f.read().splitlines()` 为什么不行？写成什么形状，内存才和文件大小无关？

## A
**逐行流过生成器链，只常驻聚合状态**

- **文件本身就是迭代器**：`for line in f` 一次读一行，缓冲有限；`readlines()` 把所有行装进列表，内存和文件同阶；
- **一环一个生成器**：解析、过滤各是一个生成器函数，接成一条链。一行走完全程才读下一行，常驻的只有末端的聚合（这里是 `Counter`，大小是级别个数）；
- **别在中途物化**：`sorted(...)`、`list(...)`、`len(list(...))` 把流装成列表，管道的优势就没了。要排序，先聚合，再排聚合的结果；
- **只能走一遍**：生成器耗尽后再迭代是空的，不报错。文件可以 `seek(0)` 重读，但生成器链要重新造（代码最后两行）；
- **解码也是边界**：`open(path, encoding="utf-8", errors="replace")` 把非法字节变成替换字符，而不是读到一半抛 `UnicodeDecodeError`。要不要容忍，是合同要定的事。

```python
import io
from collections import Counter

def parse(lines):
    for line in lines:                       # 文件对象本身就是逐行的迭代器
        ts, level, msg = line.rstrip("\n").split(" ", 2)
        yield int(ts), level, msg

def only(level, records):
    return (r for r in records if r[1] == level)

log = io.StringIO("1 INFO boot\n2 ERROR disk\n3 INFO ok\n4 ERROR net\n")
print(Counter(level for _, level, _ in parse(log)))        # 只常驻一个 Counter
log.seek(0)                                  # 文件能回头；生成器不能，要重新造
print([m for _, _, m in only("ERROR", parse(log))])
```

<details class="pt"><summary>延伸</summary>

调用栈采样流的处理器是同一个形状：逐个采样喂给转换器，事件 `yield from` 出去，内存只和栈深成正比，与流长度无关；它还要求「在迭代开始之前不读任何采样」。见 [[solution-lcp-stack-trace-stream|流式调用栈处理器（Streaming Stack Trace Processor）]]。去重流水线则是另一种省读取的办法：先按大小筛，再读头尾抽样，最后才读全文，见 [[solution-lcp-file-deduplication|文件去重流水线（File Deduplication）]]。

</details>

**知识点：**日志处理与聚合（Log Processing）
