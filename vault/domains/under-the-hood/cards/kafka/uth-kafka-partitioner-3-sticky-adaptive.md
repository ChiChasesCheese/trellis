---
id: uth-kafka-partitioner-3-sticky-adaptive
node: kafka.partitioner
type: qa
step: 3
---
## Q
**无 key：粘性分区与加权随机**｜Kafka · 4.0

没有 key 的消息，生产者怎么挑分区？为什么不一条换一个分区地轮流（round-robin）？

## A
**背景。** 没有 key 的消息不要求落在哪个分区，只求分得匀、发得快。直觉做法是一条换一个分区地轮流写。但生产者是先按分区攒批（把几条消息攒成一包）再发的：轮流写把连续的消息拆散到所有分区，每包都很小，请求又多又碎，延迟高。

**结构。** 粘性分区（sticky）：一直写同一个分区，累计写满 `batch.size` 字节才换。3.3 起默认带自适应：换分区时按各分区待发队列的长短做加权随机，队列短（说明那台 broker 处理得快）的更容易被选中。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">轮流: 每个批次都攒不满</text>
<text x="8" y="31" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">p0</text>
<rect x="34" y="22" width="200" height="11" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="34" y="22" width="66" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="46" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">p1</text>
<rect x="34" y="37" width="200" height="11" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="34" y="37" width="66" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="61" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">p2</text>
<rect x="34" y="52" width="200" height="11" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="34" y="52" width="66" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="88" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">粘性: 先写满一个批次再换</text>
<text x="8" y="105" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">p0</text>
<rect x="34" y="96" width="200" height="11" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="34" y="96" width="200" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="120" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">p1</text>
<rect x="34" y="111" width="200" height="11" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="8" y="135" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">p2</text>
<rect x="34" y="126" width="200" height="11" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="8" y="162" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">自适应: 待发队列短的更常被选</text>
<text x="8" y="179" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">p0</text>
<rect x="34" y="170" width="200" height="11" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="34" y="170" width="150" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="244" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">概率低</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">p1</text>
<rect x="34" y="185" width="200" height="11" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="34" y="185" width="90" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="244" y="195" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">中</text>
<text x="8" y="209" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">p2</text>
<rect x="34" y="200" width="200" height="11" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="34" y="200" width="30" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="244" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">概率高</text>
</svg>
```

**细节。**

- 权重存成累计频次表（`cumulativeFrequencyTable`）：随机数落在哪一段，就用 `Arrays.binarySearch` 找到对应分区。
- `partitioner.adaptive.partitioning.enable` 默认 `true`。

**为什么。** 粘性让每一包尽量写满；自适应再把更多消息交给响应快的 broker。

**例题：** LC 528 按权重随机选择

给正整数数组 `w`，实现 `pickIndex()`：以 `w[i] / sum(w)` 的概率随机返回下标 `i`。例：`w = [1, 3]` 时，下标 `0` 的概率是 25%，下标 `1` 是 75%。

```python
import random
from bisect import bisect_right
from itertools import accumulate


class Solution:
    def __init__(self, w: list[int]):
        self.prefix = list(accumulate(w))        # prefix[i] = w[0] + ... + w[i]
        self.total = self.prefix[-1]

    def pickIndex(self) -> int:
        r = random.randrange(self.total)         # 均匀落在 [0, total)
        return bisect_right(self.prefix, r)      # 第一个 prefix[i] > r 的 i
```
