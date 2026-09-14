---
id: leetcode-c-endlesscheng-9ozfk9-monotonic-stack-lexicographically-smallest-subsequence-invariant
node: stack-queue-monotonic.monotonic-stack-lexicographic-subsequence
type: cloze
anki: 1787272403905
tags: [concept-cloze, invariant, leetcode, recall]
---
只有当栈顶字符比当前字符大且它在后面 {{c1::仍会出现}} 时，才能弹出栈顶。

栈始终是已处理前缀中、在可补回约束下字典序最小的可行结果。；仅当栈顶大于当前字符且栈顶后续仍会出现时，才允许弹出栈顶。；若要求去重，字符在栈中时跳过；被弹出后要解除在栈标记。

**Evidence**

四、最小字典序

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F03.04%20-%20%E5%8D%95%E8%B0%83%E6%A0%88%E6%9E%84%E9%80%A0%E6%9C%80%E5%B0%8F%E5%AD%97%E5%85%B8%E5%BA%8F%E5%AD%90%E5%BA%8F%E5%88%97)
