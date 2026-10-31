---
id: tlc-add-bold-tag-in-string-0-whole
node: c.add-bold-tag-in-string
type: qa
---
## Q
**LC 616 给字符串添加加粗标签**｜Medium · LC TikTok 全时段热度 38/100

给定字符串 `s` 和字符串数组 `words`。`s` 中凡是出现在 `words` 里的子串都要加粗：在其前后加 `<b>` 和 `</b>`。两个这样的子串重叠，只用一对标签包住；两个子串紧挨着（连续），也合并成一对。返回加粗后的字符串。`1 <= s.length <= 1000`，`0 <= words.length <= 100`，`1 <= words[i].length <= 1000`，由英文字母和数字组成，`words` 里的值互不相同。例：`s = "abcxyz123"`，`words = ["abc","123"]` → `"<b>abc</b>xyz<b>123</b>"`；`s = "aaabbb"`，`words = ["aa","b"]` → `"<b>aaabbb</b>"`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先给 `s` 的每个字符标记「是否被加粗」，再扫一遍：在连续被标记的一段前后各放一对标签。

**识别。** 「多个区间覆盖后合并、重叠和相邻都合并」：区间合并，但字符串长度只有 1000，用逐字符布尔数组比排序合并区间更不容易错。找出所有匹配位置是主要工作量，多个单词同时匹配用前缀树（Trie）。

**推导。** 先对每个起点 `i` 找出所有以 `i` 开头的匹配单词，其中最长的结束位置记作 `end`；`end` 之前（含）的字符都应该加粗，用一个滚动的「覆盖到哪里」的变量标记即可。把 `words` 建成 Trie，从 `i` 往下走一条路径就能一次得到所有匹配，不需要逐个单词 `startswith`。最后扫描标记数组，在 `False→True` 处插入 `<b>`，在 `True→False` 处插入 `</b>`。

**简单解法。** 不建 Trie，对每个起点逐个单词 `startswith`。

```python
def add_bold_tag_scan(s: str, words: list[str]) -> str:
    n = len(s)
    bold = [False] * n
    end = 0                                      # 目前已确定加粗到哪里（不含）
    for i in range(n):
        for w in words:
            if s.startswith(w, i):
                end = max(end, i + len(w))       # 匹配 [i, i+len(w))，延长覆盖区间
        bold[i] = i < end
    out: list[str] = []
    for i, ch in enumerate(s):
        if bold[i] and (i == 0 or not bold[i - 1]):
            out.append("<b>")                    # 一段加粗的开头
        out.append(ch)
        if bold[i] and (i == n - 1 or not bold[i + 1]):
            out.append("</b>")                   # 一段加粗的结尾
    return "".join(out)
```

`O(n · W · L)`（`W` 为单词数，`L` 为单词长度），上限约 `1000 · 100` 次 `startswith`，可以过；单词数很多时 Trie 更好。

最优解：

```python
def add_bold_tag(s: str, words: list[str]) -> str:
    trie: dict[str, dict] = {}
    for w in words:
        node = trie
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = {}                           # "$" 标记某个单词到此结束

    n = len(s)
    bold = [False] * n
    end = 0
    for i in range(n):
        node = trie
        j = i
        while j < n and s[j] in node:            # 沿 Trie 走一条路径，路径上每个单词结尾都是一个匹配
            node = node[s[j]]
            j += 1
            if "$" in node:
                end = max(end, j)
        bold[i] = i < end
    out: list[str] = []
    for i, ch in enumerate(s):
        if bold[i] and (i == 0 or not bold[i - 1]):
            out.append("<b>")
        out.append(ch)
        if bold[i] and (i == n - 1 or not bold[i + 1]):
            out.append("</b>")
    return "".join(out)
```

运行：`("abcxyz123", ["abc","123"])` → `"<b>abc</b>xyz<b>123</b>"`，`("aaabbb", ["aa","b"])` → `"<b>aaabbb</b>"`；`("abc", [])` → `"abc"`；`("abcd", ["ab","bc","cd"])` → `"<b>abcd</b>"`（相邻或重叠都合并）。

**复杂度。** 建 Trie `O(Σ|w|)`，扫描 `O(n · L)`（`L` 为最长单词），输出 `O(n)`；空间 `O(Σ|w|)`。

**拓展优化。**
- 单词很多、`s` 很长：Aho–Corasick 自动机，一次扫描 `O(n + Σ|w| + 匹配数)`。
- 用 `end` 滚动标记而不是对每个匹配逐个字符置 `True`，避免 `O(匹配数 × 单词长度)` 的重复写入。

**易错点。**
- 只合并重叠、不合并相邻：`"abcd"` 配 `["ab","cd"]` 要得到 `<b>abcd</b>`，不是 `<b>ab</b><b>cd</b>`；用布尔数组按「连续被标记」分段自然合并。
- `end` 取半开的 `i + len(w)` 却判断 `i <= end`：会多加粗紧随其后的一个字符，`("abxc", ["ab"])` 变成 `<b>abx</b>c`，应为 `<b>ab</b>xc`。
- 在 Trie 里到达单词结尾就停止：路径上更长的单词还没看，`["a","ab"]` 配 `"ab"` 会漏掉 `b`。

**追问。**
- LC 758 字符串中的加粗单词：与它完全相同。
- 把标签换成别的、或者处理大小写不敏感：只改匹配方式，合并逻辑不变。

**同模式。** LC 56 合并区间、LC 758 字符串中的加粗单词、LC 208 实现前缀树、LC 648 单词替换、LC 1065 字符串的索引对。
