---
id: tlc-reorganize-string-4-followup
node: b.reorganize-string
type: qa
step: 4
---
## Q
**LC 767 重构字符串**｜追问

面试官接着问：（1）要求相同字符之间至少隔 `k` 个位置（LC 358）？（2）只需要回答“能不能”，不用构造？（3）能不能不用堆，`O(n)` 构造？

## A
1. **间隔 `k`**：暂存槽从一个变量变成长度 `k` 的队列。每轮取堆顶放进结果，把它（次数减一）送进队列；队列长度达到 `k` 时，把最老的那个放回堆。`k = 2` 就是原题。

```python
from collections import Counter, deque
from heapq import heapify, heappop, heappush


def rearrange_k_distance(s: str, k: int) -> str:
    heap = [(-c, ch) for ch, c in Counter(s).items()]
    heapify(heap)
    wait: deque[tuple[int, str]] = deque()
    out: list[str] = []
    while heap:
        c, ch = heappop(heap)
        out.append(ch)
        wait.append((c + 1, ch))
        if len(wait) >= k:
            item = wait.popleft()
            if item[0]:
                heappush(heap, item)
    return "".join(out) if len(out) == len(s) else ""
```

   `("aabbcc", 3)` → `'abcabc'`，`("aaabc", 3)` → `''`。
2. **只判断**：`max(Counter(s).values()) <= (len(s) + 1) // 2`，`O(n)`。
3. **不用堆**：按次数从多到少、同字符聚在一起把字符排成一排，先填偶数下标 `0, 2, 4, …`，再填奇数下标。最多的字符不超过 `(n + 1) // 2` 时一定放得下，因为它占满偶数位的一段，其余字符把间隙补齐。必须按次数排序后再填；按字母序填会让某个字符的两段落在相邻位置，如 `"aabbb"` 填成 `'ababb'`。

**Python 提醒**：切片赋值可以写成 `res[0::2] = chars[:m]`、`res[1::2] = chars[m:]`，扩展切片赋值要求两边长度相等，所以 `m` 取 `(n + 1) // 2`。`deque` 的 `popleft` 是 `O(1)`，列表的 `pop(0)` 是 `O(n)`。
