---
id: leetcode-c-endlesscheng-sjfwqi-subsequence-automaton-recognition
node: strings.subsequence-automaton
type: cloze
anki: 1787272449778
tags: [concept-cloze, leetcode, recall, recognition]
---
固定文本面对大量“某串是否为其子序列”的查询时，建立 {{c1::子序列自动机}}。

预处理文本每个位置之后各字符的最近出现位置；每次匹配模式串只做状态跳转，快速判断其是否为子序列。

**Evidence**

九、子序列自动机

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.10%20-%20%E5%AD%90%E5%BA%8F%E5%88%97%E8%87%AA%E5%8A%A8%E6%9C%BA)
