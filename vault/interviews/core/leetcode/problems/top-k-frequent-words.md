---
slug: top-k-frequent-words
---
## Q
**LC 692 前K个高频单词**｜Medium

返回出现次数最多的前 `k` 个单词：次数从高到低，次数相同按字典序。

## A
**一句话。** `Counter` 计数，按复合键 `(-次数, 单词)` 排序取前 `k` 个。

```python
def top_k_frequent(words, k):
    count = Counter(words)
    # 负号让次数降序，单词让同次数字典序升序
    return sorted(count, key=lambda w: (-count[w], w))[:k]
```

**复杂度。** 时间 `O(m log m)`，空间 `O(m)`。

**易错点。**
- 用 `most_common(k)`：平局保留首次出现顺序，`["love","i","i","love"]`、`k=2` 得 `['love','i']`，应为 `['i','love']`。
- `key=(count, w)` 加 `reverse=True`：两个分量一起反，平局变成字典序降序。

**追问。**
- 要 `O(m log k)`？：`heapq.nsmallest(k, count, key=lambda w: (-count[w], w))`。
- 次数有上界 `n`？：桶排序，每个桶内按字典序排。

**同模式。** LC 347 前 K 个高频元素、LC 451 根据字符出现频率排序、LC 973 最接近原点的 K 个点、LC 215 数组中的第 K 个最大元素
