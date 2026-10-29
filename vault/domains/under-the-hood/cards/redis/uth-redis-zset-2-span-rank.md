---
id: uth-redis-zset-2-span-rank
node: redis.zset
type: qa
step: 2
---
## Q
**ZRANK 怎么做到 O(log n)**｜Redis · 8.10

跳表本来只能按“值”查找，Redis 怎么知道一个成员排第几？

## A
**背景。** 跳表天生只会“按值找位置”，不知道前面有几个元素。想知道排名，最笨的办法是从头数，O(n)。办法：让每条“向右跳”的边记下它越过了多少个元素，沿路把这些数加起来，就是排名。

**结构。** 每个节点的每一层，除了指向下一个节点的指针，还记一个跨度（span）：这一跳越过了多少个元素。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 225">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">每条边上的数字 = 跨度 span: 这一跳越过几个元素</text>
<rect x="26" y="92" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="42" y="105.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">头</text>
<rect x="78" y="92" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="94" y="105.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a</text>
<rect x="130" y="92" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="146" y="105.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">b</text>
<rect x="182" y="92" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="198" y="105.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">c</text>
<rect x="234" y="92" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="250" y="105.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">d</text>
<rect x="286" y="92" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="302" y="105.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">e</text>
<line x1="58" y1="102" x2="78" y2="102" stroke="currentColor" stroke-width="1"/>
<polygon points="78,102 72.0,104.7 72.0,99.3" fill="currentColor"/>
<text x="68" y="97" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<line x1="110" y1="102" x2="130" y2="102" stroke="currentColor" stroke-width="1"/>
<polygon points="130,102 124.0,104.7 124.0,99.3" fill="currentColor"/>
<text x="120" y="97" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<line x1="162" y1="102" x2="182" y2="102" stroke="currentColor" stroke-width="1"/>
<polygon points="182,102 176.0,104.7 176.0,99.3" fill="currentColor"/>
<text x="172" y="97" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<line x1="214" y1="102" x2="234" y2="102" stroke="currentColor" stroke-width="1"/>
<polygon points="234,102 228.0,104.7 228.0,99.3" fill="currentColor"/>
<text x="224" y="97" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<line x1="266" y1="102" x2="286" y2="102" stroke="currentColor" stroke-width="1"/>
<polygon points="286,102 280.0,104.7 280.0,99.3" fill="currentColor"/>
<text x="276" y="97" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="26" y="66" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="130" y="66" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="234" y="66" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<line x1="58" y1="76" x2="130" y2="76" stroke="currentColor" stroke-width="1"/>
<polygon points="130,76 124.0,78.7 124.0,73.3" fill="currentColor"/>
<text x="94" y="71" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<line x1="162" y1="76" x2="234" y2="76" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="234,76 228.0,78.7 228.0,73.3" style="fill:var(--accent,#3b6fd4)"/>
<text x="198" y="71" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="26" y="40" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="130" y="40" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<line x1="58" y1="50" x2="130" y2="50" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="130,50 124.0,52.7 124.0,47.3" style="fill:var(--accent,#3b6fd4)"/>
<text x="94" y="45" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<text x="4" y="106" text-anchor="start" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L0</text>
<text x="4" y="80" text-anchor="start" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L1</text>
<text x="4" y="54" text-anchor="start" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L2</text>
<text x="8" y="128" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">查 d: 头 → b (L2, span 2), b → d (L1, span 2)</text>
<text x="8" y="146" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">把走过的 span 加起来: 2 + 2 = 4, d 排第 4</text>
<text x="8" y="172" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">ZRANK = 沿查找路径累加每次向右走的 span</text>
<text x="8" y="190" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">ZRANGE 按排名取元素, 也沿 span 跳, 不必逐个数</text>
<text x="8" y="208" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">升层概率 1/4: 模拟一百万次平均层数约 1.33, P = 1/2 约 2</text>
</svg>
```

**细节。**

- 查找路径上，把每次“向右走”的 span 累加，就是目标的排名
- 反过来，`ZRANGE` 按排名取元素，也是沿着 span 跳，不必逐个数
- 升层概率 1/4，模拟一百万次平均层数约 1.33，P = 1/2 则约 2

**为什么。** 每个节点平均只有 1.33 个指针，比 P = 1/2 少约三分之一。

**例题：** LC 528 按权重随机选择

给正整数数组 `w`，`w[i]` 是下标 `i` 的权重，实现 `pickIndex()`：以 `w[i] / sum(w)` 的概率返回下标 `i`。例：`w = [1,3]` 时，返回 `1` 的概率是 75%。做法是先累加出前缀和，再二分查找“第几个位置”落在哪，和跳表沿着跨度从排名找到元素是同一类“累计数到位置”的换算。

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
