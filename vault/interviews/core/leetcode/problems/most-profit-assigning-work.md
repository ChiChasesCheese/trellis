---
slug: most-profit-assigning-work
---
## Q
**LC 826 安排工作以达到最大收益**｜Medium

`difficulty[i]`、`profit[i]` 是第 `i` 份工作的难度和报酬，`worker[j]` 是第 `j` 个工人的能力。每个工人至多做一份难度不超过自己能力的工作，同一份工作可被多人做。求最大总收益。

## A
**一句话。** 工作按难度排序，工人按能力排序，双指针推进并维护「已解锁工作的最高报酬」，每个工人取当前最高。

```python
def max_profit_assignment(difficulty, profit, worker):
    jobs = sorted(zip(difficulty, profit))
    ans = best = i = 0
    for w in sorted(worker):          # 能力从小到大
        while i < len(jobs) and jobs[i][0] <= w:
            best = max(best, jobs[i][1])   # 已解锁里的最高报酬
            i += 1
        ans += best                   # 能力强的工人只会更好
    return ans
```

**复杂度。** 时间 `O(n log n + m log m)`，空间 `O(n)`。

**易错点。**
- 只取难度最接近的工作：难度高的不一定报酬高，要取「难度不超过能力」里报酬最大者。
- 每次从头扫工作：指针要单调前进，否则变成 `O(nm)`。

**追问。**
- 不排序工人怎么办？：工作排序后做「难度前缀最大报酬」，每个工人二分查找。

**同模式。** LC 455 分发饼干、LC 870 优势洗牌、LC 881 救生艇
