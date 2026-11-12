---
slug: sort-characters-by-frequency
---
## Q
**LC 451 根据字符出现频率排序**｜Medium

把字符串 `s` 的字符按出现次数降序重排，相同字符必须相邻，大小写算不同字符。

## A
**一句话。** 数次数，对「不同字符」按次数降序排，每个字符重复它的次数再拼接。

```python
def frequency_sort(s):
    cnt = Counter(s)
    order = sorted(cnt, key=cnt.get, reverse=True)
    return "".join(ch * cnt[ch] for ch in order)
```

**复杂度。** 时间 `O(n + k log k)`，空间 `O(n)`。

**易错点。**
- 对整个字符串按次数排序：次数相同的不同字符会交错，`"cacaca"` 原样返回。要排「不同字符」再展开。
- 大小写合并：`"Aabb"` 里 `A`、`a` 是两个字符，答案 `"bbAa"`。

**追问。**
- 想要严格 `O(n)`？：桶排序，下标是次数，桶里放字符。

**同模式。** LC 347 前 K 个高频元素、LC 692 前 K 个高频单词、LC 1636 按照频率将数组升序排序、LC 242 有效的字母异位词
