---
id: leetcode-c-endlesscheng-mor1u6-splay-tree-template
node: advanced-ds-heap.splay-tree
type: cloze
anki: 1787272424105
tags: [concept-cloze, leetcode, recall, template]
---
一次右旋后，原根成为 {{c1::新根的右孩子}}。

```
def rotate_right(root):
    pivot = root.left
    root.left = pivot.right
    pivot.right = root
    return pivot
```

**Evidence**

九、伸展树（Splay 树）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.21%20-%20Splay%20%E6%A0%91)
