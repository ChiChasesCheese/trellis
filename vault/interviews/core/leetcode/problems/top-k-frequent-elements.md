---
slug: top-k-frequent-elements
---
## Q
**LC 347 前 K 个高频元素**｜Medium

返回数组中出现频率前 `k` 高的元素，顺序任意，要求优于 `O(n log n)`。

## A
**一句话。** 计数后按频次做桶排序，频次最大是 `n`，从高频桶往低频桶取够 `k` 个。

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
