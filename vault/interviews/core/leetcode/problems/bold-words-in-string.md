---
slug: bold-words-in-string
---
## Q
**LC 758 字符串中的加粗单词**｜Medium

给单词数组 `words` 和字符串 `s`，把 `s` 中出现的所有 `words` 子串用 `<b>` `</b>` 加粗；相交或相邻的加粗区间要合并成一对标签。

## A
**一句话。** 先把每个单词的所有出现位置标成「要加粗」，再按标记数组扫描，在连续段的首尾放标签，合并自然完成。

```python
def bold_words(words, s):
    bold = [False] * (len(s) + 1)    # 多一格，免去越界判断
    for w in words:
        i = s.find(w)
        while i != -1:
            for k in range(i, i + len(w)):
                bold[k] = True
            i = s.find(w, i + 1)     # 出现位置可以重叠
    ans = []
    for i, c in enumerate(s):
        if bold[i] and (i == 0 or not bold[i - 1]):
            ans.append("<b>")
        ans.append(c)
        if bold[i] and not bold[i + 1]:
            ans.append("</b>")
    return "".join(ans)
```

**复杂度。** 时间 `O(n·Σ|w|)` 量级（查找加标记），空间 `O(n)`。

**易错点。**
- `find` 后从 `i + len(w)` 继续：会漏掉重叠出现，如 `"aaa"` 里的 `"aa"`。
- 对每个单词单独加标签：相邻或相交的区间要合并，必须先标记再统一输出。

**追问。**
- 先合并区间再加标签行吗？：可以，把所有 `[start, end]` 区间排序合并，和标记数组等价。

**同模式。** LC 616 给字符串添加加粗标签、LC 56 合并区间、LC 57 插入区间
