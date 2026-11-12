---
slug: add-bold-tag-in-string
---
## Q
**LC 616 给字符串添加加粗标签**｜Medium

`s` 中凡出现在 `words` 里的子串都加粗 `<b>…</b>`；重叠或相邻的子串合并成一对标签。

## A
**一句话。** Trie 匹配得到每个字符是否被覆盖，再对连续被覆盖的一段首尾放标签。

```python
def add_bold_tag(s, words):
    trie = {}
    for w in words:
        node = trie
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = {}                # 单词结尾

    n = len(s)
    bold = [False] * n
    end = 0                           # 已覆盖到的右端（开）
    for i in range(n):
        node, j = trie, i
        while j < n and s[j] in node:
            node = node[s[j]]
            j += 1
            if "$" in node:           # 路径上每个结尾都算
                end = max(end, j)
        bold[i] = i < end
    out = []
    for i, ch in enumerate(s):
        if bold[i] and (i == 0 or not bold[i - 1]):
            out.append("<b>")
        out.append(ch)
        if bold[i] and (i == n - 1 or not bold[i + 1]):
            out.append("</b>")
    return "".join(out)
```

**复杂度。** 时间 `O(n·L + Σ|w|)`，空间 `O(Σ|w|)`。

**易错点。**
- 只合并重叠不合并相邻：`"abcd"`、`["ab","cd"]` 应为 `<b>abcd</b>`。
- `end` 是开区间却用 `i <= end`：`("abxc", ["ab"])` 多加粗一个 `x`。
- 匹配到第一个单词结尾就停：`["a","ab"]` 配 `"ab"` 会漏掉 `b`。

**追问。**
- 不用 Trie 怎么做？：对每个单词用 `find` 找所有出现位置，直接标记区间，`O(n·Σ|w|)`。
- LC 758 有什么不同？：完全相同。

**同模式。** LC 56 合并区间、LC 758 字符串中的加粗单词、LC 208 实现前缀树、LC 648 单词替换
