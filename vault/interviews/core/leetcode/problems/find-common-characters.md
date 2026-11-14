---
slug: find-common-characters
---
## Q
**LC 1002 查找共用字符**｜Easy

返回在 `words` 每个单词中都出现的字符，重复的按次数算（两边都有两个 `l` 才输出两个）。

## A
**一句话。** 每个单词计数，多个计数表求交集（每个字母取最小次数），再展开。

```python
def common_chars(words):
    common = Counter(words[0])
    for w in words[1:]:
        common &= Counter(w)     # 逐字母取最小次数
    return list(common.elements())
```

**复杂度。** 时间 `O(Σ|w|)`，空间 `O(26)`。

**易错点。**
- 用 `set` 求交集：丢了次数，`["bella","label","roller"]` 只得一个 `l`，应为两个。
- 交集初值用空 `Counter()`：和空表求交永远是空。

**追问。**
- 不用 `Counter`？：长度 26 的数组 `mn`，初值无穷大，每个单词计数后逐位取 `min`。
- 字符集很大？：仍取最小值，只是键换成字典。

**同模式。** LC 242 有效的字母异位词、LC 349 两个数组的交集、LC 350 两个数组的交集 II
