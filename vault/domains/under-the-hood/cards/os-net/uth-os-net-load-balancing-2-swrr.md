---
id: uth-os-net-load-balancing-2-swrr
node: os-net.load-balancing
type: qa
step: 2
---
## Q
**平滑加权轮询**｜Nginx · upstream round_robin · 1.31

权重 5:1:1 的三台机器，怎样避免连续 5 次打到同一台？

## A
**背景。** 权重 5:1:1，最直接的加权轮询是 a 连发 5 次，再 b、c 各一次：aaaaabc。a 一次承受 5 连击，是突发。想打散，又不想靠随机数。平滑加权轮询给每台机器记一个得分 `current_weight`：每轮每台都加上自己的权重，选得分最大的，再让它减去总权重。

**结构。** 权重 a=5、b=1、c=1，总权重 7。下表是每轮加完权重后的得分，框出的是被选中的：

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">每轮先加权重 再选最大的 选中后减 7</text>
<text x="70" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" font-weight="bold">轮</text>
<text x="150" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" font-weight="bold">a (5)</text>
<text x="210" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" font-weight="bold">b (1)</text>
<text x="270" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" font-weight="bold">c (1)</text>
<line x1="40" y1="44" x2="300" y2="44" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="70" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">1</text>
<rect x="126" y="49" width="48" height="20" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="150" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">5</text>
<text x="210" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<text x="270" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<text x="70" y="85" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">2</text>
<rect x="126" y="71" width="48" height="20" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="150" y="85" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">3</text>
<text x="210" y="85" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">2</text>
<text x="270" y="85" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">2</text>
<text x="70" y="107" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">3</text>
<text x="150" y="107" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<rect x="186" y="93" width="48" height="20" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="210" y="107" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">3</text>
<text x="270" y="107" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">3</text>
<text x="70" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">4</text>
<rect x="126" y="115" width="48" height="20" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="150" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">6</text>
<text x="210" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">-3</text>
<text x="270" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">4</text>
<text x="70" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">5</text>
<text x="150" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">4</text>
<text x="210" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">-2</text>
<rect x="246" y="137" width="48" height="20" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="270" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">5</text>
<text x="70" y="173" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">6</text>
<rect x="126" y="159" width="48" height="20" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="150" y="173" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">9</text>
<text x="210" y="173" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">-1</text>
<text x="270" y="173" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">-1</text>
<text x="70" y="195" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">7</text>
<rect x="126" y="181" width="48" height="20" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="150" y="195" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">7</text>
<text x="210" y="195" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<text x="270" y="195" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0</text>
<text x="170" y="228" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">选中的依次是 a a b a c a a</text>
</svg>
```

**细节。**

- 七轮选择依次是 a a b a c a a，七轮之后所有得分回到 0，进入下一个循环
- 每次扫一遍后端，O(n)；已下线（`down`）、失败超限、并发连接数已达 `max_conns` 的后端会被跳过

**为什么。** 朴素加权轮询会 aaaaabc 地突发，平滑版把 a 均匀打散，而且不依赖随机数。

**例题：** LC 767 重构字符串

重新排列字符串 `s`，使任意两个相邻字符都不同，返回任意一种排列，做不到就返回 `""`。例：`"aab"` → `"aba"`；`"aaab"` → `""`。

```python
from collections import Counter
from heapq import heapify, heappop, heappush


def reorganize_string(s: str) -> str:
    heap = [(-cnt, ch) for ch, cnt in Counter(s).items()]
    heapify(heap)                           # 出现次数最多的字符在堆顶
    out: list[str] = []
    held = (0, "")                          # 上一轮刚用过、暂时不能再选的 (负计数, 字符)
    while heap:
        cnt, ch = heappop(heap)
        out.append(ch)
        if held[0]:
            heappush(heap, held)            # 上一个字符隔了一位，可以重新参选
        held = (cnt + 1, ch)                # 用掉一个，剩余数量暂存
    return "".join(out) if len(out) == len(s) else ""
```
