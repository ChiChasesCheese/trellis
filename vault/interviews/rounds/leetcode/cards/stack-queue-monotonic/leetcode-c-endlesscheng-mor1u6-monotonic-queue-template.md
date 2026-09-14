---
id: leetcode-c-endlesscheng-mor1u6-monotonic-queue-template
node: stack-queue-monotonic.monotonic-queue
type: cloze
anki: 1789002113870
tags: [concept-cloze, leetcode, recall, template]
---
最大值窗口中，入队 x 前从队尾删除所有 {{c1::值不大于 x}} 的候选。

```
from collections import deque

def window_max(nums, k):
    q, ans = deque(), []
    for i, x in enumerate(nums):
        while q and q[0] <= i - k:
            q.popleft()
        while q and nums[q[-1]] <= x:
            q.pop()
        q.append(i)
        if i >= k - 1:
            ans.append(nums[q[0]])
    return ans
```

**Evidence**

§4.4 单调队列

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.08%20-%20%E5%8D%95%E8%B0%83%E5%8F%8C%E7%AB%AF%E9%98%9F%E5%88%97)
