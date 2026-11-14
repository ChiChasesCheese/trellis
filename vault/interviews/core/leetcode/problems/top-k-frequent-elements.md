---
slug: top-k-frequent-elements
---
## Q
**LC 347 前 K 个高频元素**｜Medium

返回数组中出现频率前 `k` 高的元素，顺序任意，要求优于 `O(n log n)`。

## A
**一句话。** 计数后按频次做桶排序，频次最大是 `n`，从高频桶往低频桶取够 `k` 个。

**图解。** 桶的下标就是出现次数，从高频桶往低频桶取够 `k` 个。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 145">
<text x="49.0" y="30" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="87.0" y="30" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="125.0" y="30" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="163.0" y="30" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="201.0" y="30" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="239.0" y="30" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<text x="277.0" y="30" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<text x="30" y="14" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下标 = 出现次数</text>
<rect x="30" y="36" width="38" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="68" y="36" width="38" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="87.0" y="54.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="106" y="36" width="38" height="28" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="125.0" y="54.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="144" y="36" width="38" height="28" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="163.0" y="54.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="182" y="36" width="38" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="220" y="36" width="38" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="258" y="36" width="38" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<polyline points="296,82 68,82" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="68.0,82.0 74.0,79.0 74.0,85.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="182" y="98" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">从高频桶往低频桶取</text>
<text x="30" y="120" text-anchor="start" font-size="10" font-family="ui-monospace,Menlo,monospace" style="fill:var(--dim,#6b7280)">nums = [1,1,1,2,2,3]，k = 2</text>
<text x="30" y="138" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">取到 1、2 就够 k 个</text>
</svg>

```python
def top_k_frequent(nums, k):
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]  # 下标 = 次数
    for x, c in count.items():
        buckets[c].append(x)
    ans = []
    for b in reversed(buckets):       # 高频到低频
        ans += b
        if len(ans) >= k:
            return ans[:k]
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 桶只开 `n` 个：`[1,1,1]` 频次为 `3`，`buckets[3]` 越界，要开 `n + 1`。
- `heapq.nlargest(k, count)` 不带 `key`：按元素值取最大，`[1,1,1,2,2,3]`、`k=2` 得 `[3,2]`，应为 `[1,2]`，要 `key=count.get`。

**追问。**
- 数据放不下内存？：按哈希分片各自统计 Top-K 再合并，近似用 Count-Min Sketch 加堆。
- 同频次要按字典序？：改成 `sorted(count, key=lambda x: (-count[x], x))`。

**同模式。** LC 215 数组中的第 K 个最大元素、LC 692 前 K 个高频单词、LC 973 最接近原点的 K 个点、LC 451 根据字符出现频率排序
