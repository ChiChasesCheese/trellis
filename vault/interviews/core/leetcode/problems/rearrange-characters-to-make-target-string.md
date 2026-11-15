---
slug: rearrange-characters-to-make-target-string
---
## Q
**LC 2287 重排字符形成目标字符串**｜Easy

字符串 `s` 和 `target`。从 `s` 中取出字符重新排列，最多能拼出多少个 `target`（每个字符只能用一次）。

## A
**一句话。** 数 `s` 和 `target` 中每个字符的个数，对 `target` 里的每种字符取 `s 中的个数 // target 中的个数`，最小值就是答案。

```python
def rearrange_characters(s, target):
    have, need = Counter(s), Counter(target)
    return min(have[c] // k for c, k in need.items())
```

**复杂度。** 时间 `O(|s| + |target|)`，空间 `O(1)`。

**易错点。**
- 用总字符数相除：最少的那一种字符决定上限，要逐字符取 `min`。
- `target` 里同一字符出现多次：要除以 `need[c]`，不是除以 `1`。

**追问。**
- 字符不在 `s` 里怎么办？：`Counter` 返回 `0`，除出 `0`，整体就是 `0`。

**同模式。** LC 1189 “气球” 的最大数量、LC 383 赎金信、LC 242 有效的字母异位词
