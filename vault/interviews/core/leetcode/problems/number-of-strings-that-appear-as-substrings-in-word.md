---
slug: number-of-strings-that-appear-as-substrings-in-word
---
## Q
**LC 1967 作为子字符串出现在单词中的字符串数目**｜Easy

统计 `patterns` 中有多少个字符串是 `word` 的子串。长度都 `≤ 100`。

## A
**一句话。** 规模很小，对每个模式串直接做子串判断 `p in word`。

```python
def num_of_strings(patterns, word):
    return sum(p in word for p in patterns)   # 重复的模式各算一次
```

**复杂度。** 时间 `O(Σ|p| · |word|)`，空间 `O(1)`。

**易错点。**
- 先 `set(patterns)` 去重：重复出现的模式要各算一次。
- 判断成子序列：要求连续出现。

**追问。**
- 模式很多、很长？：对所有模式建 AC 自动机，`word` 扫一遍。
- 单个模式要线性时间？：KMP 或 Z 函数。

**同模式。** LC 28 找出字符串中第一个匹配项的下标、LC 1408 数组中的字符串匹配、LC 796 旋转字符串
