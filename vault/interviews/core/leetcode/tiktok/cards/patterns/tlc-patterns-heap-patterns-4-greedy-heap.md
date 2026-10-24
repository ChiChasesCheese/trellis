---
id: tlc-patterns-heap-patterns-4-greedy-heap
node: patterns.heap-patterns
type: qa
step: 4
---
## Q
**堆（Heap）｜「每次取剩余最多的」贪心：重构字符串与最长快乐字符串**

LC 767、LC 1405 为什么每步取「剩余数量最多」的字符？取出后为什么不能立刻放回堆？

## A
每次放当前剩余最多的字符，能最大限度避免最后只剩一种字符被迫相邻。**刚用过的字符要暂时不放回**，否则下一步又选到它。

```python
import heapq
from collections import Counter
def reorganize_string(s: str) -> str:
    h = [(-c, ch) for ch, c in Counter(s).items()]
    heapq.heapify(h)
    res: list[str] = []
    prev: tuple[int, str] = (0, "")        # 上一轮用掉一个、暂时不能再选的字符
    while h:
        c, ch = heapq.heappop(h)
        res.append(ch)
        if prev[0] < 0:
            heapq.heappush(h, prev)        # 上一轮的字符现在可以重新入堆
        prev = (c + 1, ch)                 # 用掉一个（-c 变小，c + 1 更接近 0）
    return "".join(res) if len(res) == len(s) else ""
print(reorganize_string("aab"), repr(reorganize_string("aaab")), reorganize_string("a"))   # aba '' a
```

- 可行条件：最多的字符次数 `<= (n + 1) // 2`；`"aaab"` 不可行，堆提前耗尽，`len(res) != len(s)`，返回 `""`。
- LC 1405 允许同一字符**连续出现两次**：取最多的 `ch`，若结果末尾已是 `ch ch`，改取次多的；取不出次多的就结束。

```python
def longest_happy_string(a: int, b: int, c: int) -> str:
    h = [(-n, ch) for n, ch in ((a, "a"), (b, "b"), (c, "c")) if n > 0]
    heapq.heapify(h)
    res: list[str] = []
    while h:
        n, ch = heapq.heappop(h)
        if len(res) >= 2 and res[-1] == res[-2] == ch:     # 再放就成三连
            if not h:
                break
            n2, ch2 = heapq.heappop(h)
            res.append(ch2)
            if n2 + 1 < 0:
                heapq.heappush(h, (n2 + 1, ch2))
            heapq.heappush(h, (n, ch))
        else:
            res.append(ch)
            if n + 1 < 0:
                heapq.heappush(h, (n + 1, ch))
    return "".join(res)
print(longest_happy_string(1, 1, 7), longest_happy_string(2, 2, 1), longest_happy_string(7, 1, 0))   # ccaccbcc ababc aabaa
```

两题时间都是 `O(n log 字符种类)`，实际堆最多 3 个元素，相当于 `O(n)`。
