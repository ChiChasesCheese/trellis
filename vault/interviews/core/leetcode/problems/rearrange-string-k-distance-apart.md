---
slug: rearrange-string-k-distance-apart
---
## Q
**LC 358 K 距离间隔重排字符串**｜Hard

重排字符串 `s`，使相同字母相邻两次出现的下标之差至少为 `k`。做不到返回 `""`。

## A
**一句话。** 最大堆加冷却队列：每个位置放剩余次数最多且已冷却的字母，放过的字母等 `k` 个位置后再回堆。

```python
def rearrange_string(s, k):
    if k <= 1:
        return s
    heap = [(-c, ch) for ch, c in Counter(s).items()]
    heapify(heap)
    cool, res = deque(), []      # cool: (可再用的位置, -剩余, 字母)
    for i in range(len(s)):
        while cool and cool[0][0] <= i:
            _, c, ch = cool.popleft()
            heappush(heap, (c, ch))
        if not heap:
            return ""
        c, ch = heappop(heap)
        res.append(ch)
        if c + 1 < 0:            # 还有剩余才进冷却
            cool.append((i + k, c + 1, ch))
    return "".join(res)
```

**复杂度。** 时间 `O(n log σ)`，空间 `O(n)`。

**易错点。**
- 释放条件写成 `cool[0][0] < i`：多等一个位置，`("aabbcc", 3)` 返回 `""`，应为 `"abcabc"`。
- 剩余为 `0` 的字母也进冷却：之后以 `(0, ch)` 回堆被再次选中，多放字母。

**追问。**
- 为什么贪心取剩余最多的？：把次数多的字母拖到后面只会更难排开。
- 字符集不止 26 个？：复杂度随种类数 `σ` 变成 `O(n log σ)`，思路不变。

**同模式。** LC 621 任务调度器、LC 767 重构字符串、LC 1054 距离相等的条形码、LC 1405 最长快乐字符串
