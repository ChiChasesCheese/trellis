---
id: leetcode-c-endlesscheng-wr1mjp-monotonic-stack-and-queue-template
node: stack-queue-monotonic.monotonic-stack-and-queue
type: cloze
anki: 1787272473080
tags: [concept-cloze, leetcode, recall, template]
---
维护窗口最大值时，插入 x 前应弹出队尾所有 {{c1::nums[dq[-1]] <= x}} 的下标。

```
from collections import deque

def window_max(nums, k):
    dq = deque()
    ans = []
    for i, x in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            ans.append(nums[dq[0]])
    return ans
```

**Evidence**

其他算法套路（每日一题题解精选）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.12%20-%20%E5%8D%95%E8%B0%83%E6%A0%88%E4%B8%8E%E5%8D%95%E8%B0%83%E9%98%9F%E5%88%97)
