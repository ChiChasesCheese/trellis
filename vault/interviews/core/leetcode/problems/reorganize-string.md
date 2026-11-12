---
slug: reorganize-string
---
## Q
**LC 767 重构字符串**｜Medium

重排字符串 `s` 的字符，使相邻字符都不同，返回任意一种；做不到返回 `""`。

## A
**一句话。** 最大堆每次取剩余次数最多的字符，刚用过的先放一边，隔一步再放回堆。

```python
def reorganize_string(s):
    heap = [(-c, ch) for ch, c in Counter(s).items()]
    heapify(heap)                 # 次数最多的在堆顶
    out = []
    held = (0, "")                # 上一轮刚用过，暂不能选
    while heap:
        cnt, ch = heappop(heap)
        out.append(ch)
        if held[0]:
            heappush(heap, held)  # 隔了一位，可重新参选
        held = (cnt + 1, ch)
    return "".join(out) if len(out) == len(s) else ""
```

**复杂度。** 时间 `O(n log k)`（`k<=26`），空间 `O(n)`。

**易错点。**
- 取出后立刻放回堆：`"aab"` 得 `"aab"`，应为 `"aba"`。
- 循环后不检查长度：`"aaab"` 退出时 `out="aba"`，还有一个 `a` 在 `held` 里，必须返回 `""`。

**追问。**
- 只问可不可行？：`max(Counter(s).values()) <= (n+1)//2`。
- 间隔至少 `k` 位（LC 358）？：暂存槽换成长度 `k` 的队列，满了把最老的放回堆。

**同模式。** LC 358 K 距离间隔重排字符串、LC 621 任务调度器、LC 1054 距离相等的条形码、LC 1405 最长快乐字符串
