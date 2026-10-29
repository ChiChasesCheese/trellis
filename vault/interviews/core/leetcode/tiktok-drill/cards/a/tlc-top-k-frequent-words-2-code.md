---
id: tlc-top-k-frequent-words-2-code
node: a.top-k-frequent-words
type: qa
step: 2
---
## Q
**LC 692 前K个高频单词**｜写出 Python 实现

单词列表 `words`（`1 <= 长度 <= 500`，每个单词 1 到 10 个小写字母）和 `k`（`1 <= k <=` 不同单词数）：返回前 `k` 个高频单词，次数降序、同次数字典序升序。

## A
**思路。** 先用 `Counter` 统计次数；再对不同单词排序，键是 `(-次数, 单词)`：元组逐个分量比较，第一分量取负实现降序，第二分量自然升序；取前 `k` 个。

```python
from collections import Counter


def top_k_frequent(words: list[str], k: int) -> list[str]:
    count = Counter(words)                                       # 单词 -> 次数
    return sorted(count, key=lambda w: (-count[w], w))[:k]       # 次数降序，同次数按字典序升序
```

运行：`["i","love","leetcode","i","love","coding"], k = 2` → `['i', 'love']`；`["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4` → `['the', 'is', 'sunny', 'day']`；`["a"], k = 1` → `['a']`；`["love","i","i","love"], k = 2` → `['i', 'love']`。

**复杂度。** 计数 `O(nL)`；排序 `m` 个不同单词 `O(m log m · L)`，`L` 是单词长度（字符串比较的代价）；空间 `O(m)`。

**写法要点。** `sorted(count, ...)` 直接迭代 `Counter` 的键，不必 `.keys()`；复合键元组是 Python 表达「多关键字、方向不同」的标准写法：数值分量取负来反向，字符串分量不能取负，所以让它保持升序、把数值分量反过来。不要用 `reverse=True`，它会把所有分量一起反向。
