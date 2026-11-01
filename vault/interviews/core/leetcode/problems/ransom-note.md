---
slug: ransom-note
---
## Q
**LC 383 赎金信**｜Easy

给你两个字符串 `ransomNote` 和 `magazine`，判断 `ransomNote` 能不能由 `magazine` 里面的字符构成；能返回 `true`，否则返回 `false`。`magazine` 中的每个字符只能在 `ransomNote` 中使用一次。`1 <= ransomNote.length, magazine.length <= 10^5`，两者由小写英文字母组成。例：`ransomNote = "a", magazine = "b"` → `false`；`ransomNote = "aa", magazine = "ab"` → `false`；`ransomNote = "aa", magazine = "aab"` → `true`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 频次表（multiset 包含判断）。

**一句话。** 数出 `magazine` 里每个字母的库存，逐个扣除 `ransomNote` 需要的字母，库存不足就失败。

**识别。** 「每个字符只能用一次」是多重集合（multiset）包含问题，只看次数、不看顺序；`10^5` 排除对每个字符做 `O(n)` 的 `index` / `remove`。

**推导。** 暴力：对 `ransomNote` 的每个字符在 `magazine` 里找一个未用过的并删除，列表删除和查找都是 `O(n)`，总共 `O(nm)`。浪费在于每次都重新搜索；一次统计库存，每个需求 `O(1)` 扣减。

```python
def can_construct(ransom_note: str, magazine: str) -> bool:
    stock = Counter(magazine)             # 每个字母的库存
    for ch in ransom_note:
        if stock[ch] == 0:                # 库存用完：不够用了（Counter 查缺失键返回 0，不会插入）
            return False
        stock[ch] -= 1
    return True
```

运行：`("a", "b")` → `False`，`("aa", "ab")` → `False`，`("aa", "aab")` → `True`，`("ab", "ba")` → `True`。

**复杂度。** 时间 `O(n + m)`，空间 `O(1)`（最多 26 个字母）。

**拓展优化。**
- 更短的写法：`not Counter(ransom_note) - Counter(magazine)`。`Counter` 相减只保留正数，结果为空就说明没有缺口。
- 只含小写字母时可以用长度 26 的数组，`ord(ch) - 97` 做下标，常数更小。
- `ransom_note` 比 `magazine` 长时可以直接返回 `False`，省掉统计。

**易错点。**
- 只比较「出现过」而不比较次数：`("aa", "ab")` 会被误判成 `True`（正确 `False`）。
- 把字符串当集合 `set(ransom_note) <= set(magazine)` 同样丢掉次数，错误同上。
- 方向别写反：库存来自 `magazine`，需求来自 `ransom_note`。`("aab", "ab")` 反过来检查会得到 `True`，正确是 `False`。

**同模式。** LC 242 有效的字母异位词、LC 387 字符串中的第一个唯一字符、LC 409 最长回文串、LC 49 字母异位词分组。
