---
slug: sort-characters-by-frequency
---
## Q
**LC 451 根据字符出现频率排序（Sort Characters By Frequency）**｜Medium

给定一个字符串 `s`，根据字符出现的频率对其进行降序排序。一个字符出现的频率是它出现在字符串中的次数。返回已排序的字符串；如果有多个答案，返回其中任何一个。相同的字符必须放在一起，大小写视为不同字符。`1 <= s.length <= 5 * 10^5`，`s` 由大小写英文字母和数字组成。例：`s = "tree"` → `"eert"`（`"eetr"` 也对）；`s = "cccaaa"` → `"cccaaa"`；`s = "Aabb"` → `"bbAa"`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 计数（`Counter`）后按频率排序；频率不超过 `n`，也可以桶排序。

**一句话。** 先数出每种字符的次数，把字符按次数降序排好，每个字符重复它的次数再拼接。

**识别。** 「按出现频率排序」是 计数 + 排序（Top-K 频率题的同类）。字符集只有 62 种，所以排序的对象是至多 62 个不同字符，不是 `5 * 10^5` 个字符。

**推导。** 直接把整个字符串用「频率、字符」作键排序，`O(n log n)`，且要小心相同字符必须连在一起。更好的做法是对「不同字符」排序：先 `Counter` 数一遍 `O(n)`，再给至多 62 种字符排序，最后用 `ch * count` 展开。

```python
from collections import Counter


def frequency_sort(s: str) -> str:
    cnt = Counter(s)
    # 不同字符至多 62 种：按次数降序排这几种字符，再把每种字符重复 cnt 次拼起来
    return "".join(ch * cnt[ch] for ch in sorted(cnt, key=cnt.__getitem__, reverse=True))
```

运行：`"tree"` → `"eert"`，`"cccaaa"` → `"cccaaa"`，`"Aabb"` → `"bbAa"`，`"a"` → `"a"`。

**复杂度。** 时间 `O(n + k log k)`，`k` 是不同字符数（这里至多 62，即 `O(n)`）；空间 `O(n)`（输出字符串）。

**拓展优化。**
- 字符集不再有界（比如任意 Unicode）：用桶排序，`buckets[c]` 放出现 `c` 次的字符，次数不会超过 `n`，整体严格 `O(n)`。

```python
def frequency_sort_bucket(s: str) -> str:
    cnt = Counter(s)
    buckets: list[list[str]] = [[] for _ in range(len(s) + 1)]   # buckets[c]：出现 c 次的字符各重复 c 次后的串
    for ch, c in cnt.items():
        buckets[c].append(ch * c)
    return "".join(chunk for bucket in reversed(buckets) for chunk in bucket)   # 次数从大到小
```

**易错点。**
- 直接对整个字符串按次数排序（`sorted(s, key=lambda c: -cnt[c])`）：次数相同的不同字符不会聚在一起，`"cacaca"` 原样返回（题面明确判错），正确是 `"cccaaa"` 或 `"aaaccc"`。要对「不同字符」排序后再展开。
- 大小写当成同一个字符：`"Aabb"` 里 `A` 和 `a` 是不同字符，各出现一次，答案 `"bbAa"` 或 `"bbaA"`。

**同模式。** LC 347 前 K 个高频元素、LC 692 前 K 个高频单词、LC 1636 按照频率将数组升序排序、LC 242 有效的字母异位词。
