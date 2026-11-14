---
slug: kth-largest-element-in-an-array
---
## Q
**LC 215 数组中的第 K 个最大元素**｜Medium

返回数组排序后的第 `k` 个最大元素（重复值各算一个），要求平均 `O(n)`。

## A
**一句话。** 快速选择（quickselect）：随机 pivot 三路划分，只钻进答案所在的那一堆。

**图解。** 按 pivot 三路划分，只钻进第 `k` 大所在的那一段。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 158">
<text x="10" y="14" text-anchor="start" font-size="10" font-family="ui-monospace,Menlo,monospace" style="fill:var(--dim,#6b7280)">nums = [3, 2, 1, 5, 6, 4]，k = 2</text>
<text x="72" y="53" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">pivot 4</text>
<rect x="80" y="36" width="28" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="94.0" y="52.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="108" y="36" width="28" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="122.0" y="52.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="108" y="31" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">大于</text>
<rect x="148" y="36" width="28" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="162.0" y="52.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="162" y="31" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">等于</text>
<rect x="188" y="36" width="28" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="202.0" y="52.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="216" y="36" width="28" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="230.0" y="52.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="244" y="36" width="28" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="258.0" y="52.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="230" y="31" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">小于</text>
<text x="80" y="80" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">k = 2 ≤ 2 个更大 → 只钻进大于段</text>
<text x="72" y="115" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">pivot 5</text>
<rect x="80" y="98" width="28" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="94.0" y="114.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="94" y="93" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">大于</text>
<rect x="120" y="98" width="28" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="134.0" y="114.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="134" y="93" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">等于</text>
<text x="80" y="142" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">k = 2 落在等于段 → 答案 5</text>
</svg>

```python
def find_kth_largest(nums, k):
    while True:
        pivot = random.choice(nums)
        bigger = [x for x in nums if x > pivot]
        equal = nums.count(pivot)
        if k <= len(bigger):             # 答案在大堆
            nums = bigger
        elif k <= len(bigger) + equal:   # 就是 pivot
            return pivot
        else:                            # 答案在小堆
            k -= len(bigger) + equal
            nums = [x for x in nums if x < pivot]
```

**复杂度。** 时间 期望 `O(n)`，最坏 `O(n^2)`，空间 `O(n)`。

**易错点。**
- 不把相等值单独成一段：全相同的数组每轮只排除一个元素，退化成 `O(n^2)`。
- 进小堆时漏减 `k`：`[3,2,1]`、`k=3`、pivot 为 `2`，小堆里的 `k` 应是 `1`，答案 `1`。
- pivot 固定取第一个：已排序输入每轮只砍一个元素。

**追问。**
- 数据流里持续维护第 `k` 大？：大小为 `k` 的小根堆，堆顶即答案，每个新元素 `heappushpop`，`O(log k)`。
- 要第 `k` 大的不同元素？：先 `set(nums)` 去重再选。

**同模式。** LC 347 前 K 个高频元素、LC 973 最接近原点的 K 个点、LC 703 数据流中的第 K 大元素、LC 295 数据流的中位数
