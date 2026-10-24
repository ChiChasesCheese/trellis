---
id: tlc-reorganize-string-2-code
node: b.reorganize-string
type: qa
step: 2
---
## Q
**LC 767 重构字符串**｜写出 Python 实现

字符串 `s`（`1 <= 长度 <= 500`，只含小写字母），重新排列使相邻字符都不同，返回任意一种合法排列；不存在则返回 `""`。

## A
**思路。** 用最大堆按剩余次数取字符。每轮取堆顶放进结果，但它自己要“冷却”一轮：先存在 `held`，下一轮取完新堆顶后再放回堆。这样每轮的堆顶一定不是上一个字符。堆提前空了而结果没排满，说明不可行。

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

运行：`"aab"` → `'aba'`，`"aaab"` → `''`，`"a"` → `'a'`，`"vvvlo"` → `'vlvov'`，`"aabbb"` → `'babab'`；`"a"` 和 `"b"` 各 `250` 个 → `'abababab…'`，长度 `500` 且相邻都不同。

**复杂度。** 时间 `O(n log k)`，`k <= 26` 是不同字符数，每个字符至多进出堆 `次数` 次；空间 `O(k)` 加结果。

**写法要点。** `Counter(s).items()` 直接给出 `(字符, 次数)`；`heapify` 一次建堆，比逐个 `heappush` 少常数；`heapq` 只有最小堆，次数取负；元组比较在次数相同时看字符，结果可复现；`held[0]` 为 `0` 表示没有待放回的字符（计数用完或第一轮），一个判断同时处理两种情况。
