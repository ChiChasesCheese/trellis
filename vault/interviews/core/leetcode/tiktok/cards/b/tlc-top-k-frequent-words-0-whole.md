---
id: tlc-top-k-frequent-words-0-whole
node: b.top-k-frequent-words
type: qa
---
## Q
**LC 692 前K个高频单词**｜Medium · CodeTop 国内累计 1 次 · 最近 2026-07-22（CodeTop）

给单词列表 `words` 和整数 `k`，返回出现次数最多的前 `k` 个单词：按出现次数**从高到低**排序，次数相同的按**字典序**排。`1 <= words.length <= 500`，`1 <= words[i].length <= 10`，`words[i]` 由小写英文字母组成，`k` 的取值范围是 `[1, 不同单词的数量]`。进阶：尝试 `O(n log k)` 时间、`O(n)` 空间。例：`["i","love","leetcode","i","love","coding"], k = 2` → `["i","love"]`（都是 2 次，`"i"` 字典序在前）；`["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4` → `["the","is","sunny","day"]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** `Counter` 计数，再按复合键 `(-次数, 单词)` 排序取前 `k` 个：负号让次数降序，单词本身让同次数时字典序升序，一个键同时表达两个方向。

**识别。** 「前 k 个 + 按频率」是 Top-K 计数：先哈希计数，再选出最大的 `k` 个。这里多了一个**平局规则**（字典序），排序键要同时编码「次数降序、单词升序」两个方向，这是考点所在。`n <= 500`，排序完全够用；进阶的 `O(n log k)` 指向大小为 `k` 的堆。

**推导。** 最直接的做法是每次扫一遍找当前最大，重复 `k` 次，`O(km)`（`m` 为不同单词数）。浪费在于每轮都重新比较所有单词。一次排序把顺序全定下来：`O(m log m)`。再往下，只要前 `k` 个时不必全排：维护大小为 `k` 的堆，`O(m log k)`，`k` 远小于 `m` 时更快。两者的核心都是同一个比较规则：次数大的优先，次数相同字典序小的优先。

```python
from collections import Counter


def top_k_frequent(words: list[str], k: int) -> list[str]:
    count = Counter(words)                                       # 单词 -> 次数
    return sorted(count, key=lambda w: (-count[w], w))[:k]       # 次数降序，同次数按字典序升序
```

运行：样例 1 → `['i', 'love']`，样例 2 → `['the', 'is', 'sunny', 'day']`，`["a"], k = 1` → `['a']`，`["love","i","i","love"], k = 2` → `['i', 'love']`。

**复杂度。** `n` 个单词、`m` 个不同单词、单词长度 `L <= 10`：计数 `O(nL)`，排序 `O(m log m · L)`（字符串比较带 `L`）；空间 `O(m)`。

**易错点。**
- 只按次数排序或用 `Counter.most_common(k)`：平局时保留的是**首次出现的顺序**，不是字典序。`["love","i","i","love"], k = 2` 得到 `['love', 'i']`（正确 `['i', 'love']`）。
- 写成 `key=lambda w: (count[w], w), reverse=True`：`reverse` 把两个分量一起反了，平局变成字典序**降序**，样例 1 得到 `['love', 'i']`。
- 用 `(次数, 单词)` 元组做大小为 `k` 的最小堆：堆顶弹出的平局元素是字典序**最小**的，恰好是该留的。`["a","b","c"], k = 2` 得到 `['b', 'c']`（正确 `['a', 'b']`）。

**追问。**
- 进阶 `O(m log k)`：`heapq.nsmallest(k, count, key=lambda w: (-count[w], w))`，内部就是大小为 `k` 的堆；手写堆则需要自定义 `__lt__`，平局时字典序大的算「更小」。
- 次数有上界 `n`：桶排序，`buckets[c]` 放次数为 `c` 的单词，从高到低取，每个桶内排序。
- 海量数据或数据流：按单词哈希分片，各片局部 Top-K，再合并；近似时用 Count-Min Sketch 加堆。

**同模式。** LC 347 前 K 个高频元素、LC 451 根据字符出现频率排序、LC 973 最接近原点的 K 个点、LC 215 数组中的第 K 个最大元素。
