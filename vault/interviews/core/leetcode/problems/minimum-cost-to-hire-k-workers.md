---
slug: minimum-cost-to-hire-k-workers
---
## Q
**LC 857 雇佣 K 名工人的最低成本**｜Hard

雇恰好 `k` 人，组内工资与 `quality` 成正比，且每人不低于自己的最低工资 `wage`。求最小总工资。

## A
**一句话。** 按 `wage/quality` 升序枚举「最大比率的人」，用大根堆始终保留质量最小的 `k` 人，总价 = 比率 × 质量和。

```python
def mincostToHireWorkers(quality, wage, k):
    ws = sorted(zip(quality, wage), key=lambda t: t[1]/t[0])
    heap, tq, best = [], 0, inf   # 大根堆（存负数）、质量和
    for q, w in ws:
        heappush(heap, -q)
        tq += q
        if len(heap) > k:
            tq += heappop(heap)   # 弹出质量最大的
        if len(heap) == k:        # 当前人的比率是组内最大
            best = min(best, tq * w / q)
    return best
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 只挑工资最低的人：工资低不等于比率低，示例 1 得 `150`，应为 `105`。
- 堆没凑够 `k` 个就更新答案：示例 1 第一个人单独得 `50`，应为 `105`。
- 用小根堆弹出质量最小的：保留的反而是质量最大的 `k` 人。

**追问。**
- 为什么按比率排序？：组内人人按最大比率付薪才都不低于最低工资，排序后扫到的人就是当前最大比率。
- 为什么堆里留质量小的？：比率固定后总价正比于质量和，质量和越小越省。

**同模式。** LC 295 数据流的中位数、LC 502 IPO、LC 2542 最大子序列的分数、LC 1383 最大的团队表现值
