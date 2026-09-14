---
id: leetcode-c-endlesscheng-9ozfk9-monotonic-stack-lexicographically-smallest-subsequence-recognition
node: stack-queue-monotonic.monotonic-stack-lexicographic-subsequence
type: cloze
anki: 1787272403806
tags: [concept-cloze, leetcode, recall, recognition]
---
保持原相对顺序并要求字典序最小、且选择可撤销时，使用 {{c1::贪心单调栈}}。

按原顺序构造结果时，若当前字符更小且栈顶在后面还能补回，就删除栈顶以优先较小前缀。用剩余出现次数判断能否补回，并用集合或计数状态满足去重等约束。

**Evidence**

四、最小字典序

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F03.04%20-%20%E5%8D%95%E8%B0%83%E6%A0%88%E6%9E%84%E9%80%A0%E6%9C%80%E5%B0%8F%E5%AD%97%E5%85%B8%E5%BA%8F%E5%AD%90%E5%BA%8F%E5%88%97)
