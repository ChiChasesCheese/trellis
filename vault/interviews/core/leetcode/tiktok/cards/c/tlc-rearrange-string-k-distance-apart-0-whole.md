---
id: tlc-rearrange-string-k-distance-apart-0-whole
node: c.rearrange-string-k-distance-apart
type: qa
---
## Q
**LC 358 K 距离间隔重排字符串**｜Hard · LC TikTok 全时段热度 25/100

给定非空字符串 `s` 和整数 `k`，把 `s` 中的字母重新排列，使得重排后相同字母的位置间隔距离**至少**为 `k`（同一字母相邻两次出现的下标之差不小于 `k`）。如果无法做到，返回空字符串 `""`。`1 <= s.length <= 3 * 10^5`，`s` 仅由小写英文字母组成，`0 <= k <= s.length`。合法答案可能不唯一，返回任意一个。例：`s = "aabbcc"`，`k = 3` → `"abcabc"`；`s = "aaabc"`，`k = 3` → `""`；`s = "aaadbbcc"`，`k = 2` → `"abacabcd"`（任一合法排列均可）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 贪心：每个位置放当前剩余次数最多、且已经"冷却"完毕的字母；放过的字母进入冷却队列，`k` 个位置之后才能回到候选堆。

**识别。** 「相同元素之间至少间隔 k」：任务调度器（LC 621）和重排字符串（LC 767，`k = 2`）的同族。最大堆按剩余次数选，加一个冷却队列保证间隔。

**推导。** 回溯枚举所有排列，指数级。贪心的理由：出现次数最多的字母最难安排，应该尽早、尽量均匀地放；每一步放"可用字母中剩余最多的"。字母放下后在接下来 `k - 1` 个位置不能再用，进冷却队列，到位置 `i + k` 时放回堆。某一步堆为空（没有可用字母）就无解。

```python
from collections import Counter, deque
from heapq import heapify, heappop, heappush


def rearrange_string(s: str, k: int) -> str:
    if k <= 1:                                   # 间隔 0 或 1 没有限制
        return s
    heap = [(-cnt, ch) for ch, cnt in Counter(s).items()]   # 最大堆：剩余次数多的先放
    heapify(heap)
    cooling: deque[tuple[int, int, str]] = deque()    # (可再使用的位置, -剩余次数, 字母)
    res: list[str] = []
    for i in range(len(s)):
        while cooling and cooling[0][0] <= i:    # 冷却结束的字母回到候选堆
            _, neg_cnt, ch = cooling.popleft()
            heappush(heap, (neg_cnt, ch))
        if not heap:                             # 此位置没有字母可放：无解
            return ""
        neg_cnt, ch = heappop(heap)
        res.append(ch)
        if neg_cnt + 1 < 0:                      # 还有剩余：冷却 k 个位置后才能再用
            cooling.append((i + k, neg_cnt + 1, ch))
    return "".join(res)
```

运行：`("aabbcc", 3)` → `"abcabc"`，`("aaabc", 3)` → `""`，`("aaadbbcc", 2)` → `"abacabcd"`；`("a", 0)` → `"a"`，`("aa", 1)` → `"aa"`。

**复杂度。** 时间 `O(n log σ)`（`σ ≤ 26` 个字母，堆操作常数级），空间 `O(σ + n)`。

**拓展优化。**
- 只判断能否做到，不构造：设最大次数 `m`，有 `c` 个字母次数同为 `m`，可行当且仅当 `(m - 1) * k + c <= n`。这是任务调度器（LC 621）的公式，构造时的贪心保证了该条件即充分。
- 字母种类只有 26 个，堆的规模是常数，面试里可以说明用数组线性取最大也是 `O(26 n)`。

**易错点。**
- 冷却队列的释放条件写成 `cooling[0][0] < i`：多等了一个位置，`("aabbcc", 3)` 在第 3 个位置没有可用字母而返回 `""`，正确是 `"abcabc"`。
- 放完字母后忘了判断剩余次数是否为 0：次数为 0 的字母进入冷却队列后会以 `(0, ch)` 回到堆，被再次选中，字母多放。

**追问。**
- 为什么贪心不会出错：每一步取剩余次数最多的字母，是调度类题目的标准交换论证——把更多的字母留到后面只会更难安排。
- 字母表不止 26 个（任意字符）：堆随种类数增大，复杂度 `O(n log σ)`。

**同模式。** LC 621 任务调度器、LC 767 重构字符串、LC 984 不含 AAA 或 BBB 的字符串、LC 1054 距离相等的条形码、LC 1405 最长快乐字符串。
