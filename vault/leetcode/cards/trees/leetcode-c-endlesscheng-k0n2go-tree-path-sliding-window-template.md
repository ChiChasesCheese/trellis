---
id: leetcode-c-endlesscheng-k0n2go-tree-path-sliding-window-template
node: trees.tree-path-sliding-window
type: cloze
anki: 1787272446004
tags: [concept-cloze, leetcode, recall, template]
---
处理重复值时，窗口左边界更新为 max(left, {{c1::last[value] + 1}})。

last 记录该值在当前路径上的最近深度。

**Evidence**

§3.12 树上滑动窗口

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F11.20%20-%20%E6%A0%91%E4%B8%8A%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3)
