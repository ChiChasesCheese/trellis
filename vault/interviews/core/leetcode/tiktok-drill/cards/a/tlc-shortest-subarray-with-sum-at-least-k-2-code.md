---
id: tlc-shortest-subarray-with-sum-at-least-k-2-code
node: a.shortest-subarray-with-sum-at-least-k
type: qa
step: 2
---
## Q
**LC 862 和至少为 K 的最短子数组**｜写出 Python 实现

整数数组 `nums`（长度 `1` 到 `10^5`，元素在 `-10^5` 到 `10^5`，可以为负）和整数 `k`（`1 <= k <= 10^9`）。返回和至少为 `k` 的最短非空连续子数组的长度，不存在返回 `-1`。要求 `O(n)`。

## A
**思路。** 先算前缀和 `pre`（含开头的 `0`）。扫描右端点 `j`，用一个双端队列保存候选起点，保持其前缀和严格递增：队首满足 `pre[j] - pre[i] >= k` 就弹出并更新答案；入队前把队尾前缀和不小于 `pre[j]` 的起点弹掉。

```python
from collections import deque
from itertools import accumulate


def shortest_subarray(nums: list[int], k: int) -> int:
    n = len(nums)
    pre = [0, *accumulate(nums)]           # pre[j] - pre[i] 是 nums[i:j] 的和
    dq: deque[int] = deque()               # 存下标，对应的前缀和严格递增
    best = n + 1
    for j, cur in enumerate(pre):
        while dq and cur - pre[dq[0]] >= k:    # 队首起点已满足：记录并弹出（再往后只会更长）
            best = min(best, j - dq.popleft())
        while dq and pre[dq[-1]] >= cur:       # 队尾前缀和不小于 cur：起点更晚且更优，队尾作废
            dq.pop()
        dq.append(j)
    return best if best <= n else -1
```

运行：`[1]`、`k = 1` → `1`；`[1,2]`、`k = 4` → `-1`；`[2,-1,2]`、`k = 3` → `3`；`[84,-37,32,40,95]`、`k = 167` → `3`；`[-4,6]`、`k = 6` → `1`。

**复杂度。** 时间 `O(n)`：每个下标入队一次、出队至多一次，两个 `while` 的总次数不超过 `2(n + 1)`；空间 `O(n)`。

**写法要点。** `[0, *accumulate(nums)]` 用解包把开头的 `0` 和累加结果拼成前缀和（也可以写 `accumulate(nums, initial=0)`）；`deque` 的 `popleft()` 是 `O(1)`，用 `list.pop(0)` 会退化成 `O(n^2)`；队列里存**下标**而不是前缀和值，才能算长度 `j - i`；用 `n + 1` 作为「未找到」的哨兵，最后统一判断。
