---
slug: ransom-note
---
## Q
**LC 383 赎金信**｜Easy

判断 `ransomNote` 能否由 `magazine` 中的字符拼成，`magazine` 每个字符只能用一次。

## A
**一句话。** 统计 `magazine` 的字母库存，逐个扣除 `ransomNote` 需要的字母，不够就失败。

```python
def can_construct(ransom_note, magazine):
    stock = Counter(magazine)
    for ch in ransom_note:
        if stock[ch] == 0:      # 库存用完
            return False
        stock[ch] -= 1
    return True
```

**复杂度。** 时间 `O(n + m)`，空间 `O(1)`。

**易错点。**
- 只比「出现过」不比次数：`("aa", "ab")` 误判 `True`，`set(a) <= set(b)` 同理。
- 方向写反：库存来自 `magazine`；`("aab", "ab")` 反过来会得 `True`，应为 `False`。

**追问。**
- 字符集是 Unicode？：`Counter` 照用，空间 `O(字符种类数)`。

**同模式。** LC 242 有效的字母异位词、LC 387 字符串中的第一个唯一字符、LC 409 最长回文串、LC 49 字母异位词分组
