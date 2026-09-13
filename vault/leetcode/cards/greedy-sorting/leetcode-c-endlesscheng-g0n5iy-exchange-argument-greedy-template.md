---
id: leetcode-c-endlesscheng-g0n5iy-exchange-argument-greedy-template
node: greedy-sorting.exchange-argument-greedy
type: cloze
anki: 1787272476080
tags: [concept-cloze, leetcode, recall, template]
---
邻项交换证明确定排序规则后，Python 通常用 {{c1::sorted(..., key=..., reverse=...)}} 实现。

```
def order_jobs(jobs):
    # jobs: (priority, payload)
    return sorted(jobs, key=lambda job: job[0], reverse=True)
```

**Evidence**

贪心

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.01%20-%20%E9%82%BB%E9%A1%B9%E4%BA%A4%E6%8D%A2%E8%B4%AA%E5%BF%83)
