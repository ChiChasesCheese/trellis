---
slug: maximum-number-of-balloons
---
## Q
**LC 1189 “气球” 的最大数量**｜Easy

用 `text` 里的字母（每个最多用一次）最多能拼出几个 `"balloon"`？

## A
**一句话。** 计数后，每个所需字母能支撑 `现有 // 需要` 份，取最小值；`l` 和 `o` 各需要 2 个。

```python
def max_number_of_balloons(text):
    have = Counter(text)
    need = Counter("balloon")
    return min(have[c] // k for c, k in need.items())
```

**复杂度。** 时间 `O(n)`，空间 `O(26)`。

**易错点。**
- 忘了 `l`、`o` 要两个：`"balon"` 会得 `1`，应为 `0`。
- 用 `have[c]` 不除：只看了有没有，没看够几份。

**追问。**
- 任意目标单词（LC 2287）？：同一写法，`need = Counter(target)`。
- 只能用一次每个字母，但要拼多个不同单词？：变成背包或搜索，不再是简单取最小。

**同模式。** LC 383 赎金信、LC 242 有效的字母异位词、LC 2287 重排字符形成目标字符串
