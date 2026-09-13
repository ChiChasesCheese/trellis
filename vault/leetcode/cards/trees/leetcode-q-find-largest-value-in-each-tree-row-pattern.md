---
id: leetcode-q-find-largest-value-in-each-tree-row-pattern
node: trees.binary-tree
type: qa
anki: 1787268625788
tags: [lc::515, leetcode, pattern, recall]
---
## Q
如何用 BFS 求二叉树每一层的最大值？

## A
用 deque 做层序遍历，每层开始前用 `max(que, key=lambda x: x.val).val` 取出当前层所有节点的最大值加入结果，再用 `for _ in range(len(que))` 固定本层节点数逐个 pop 并把子节点入队。核心是「先按当前 queue 长度锁定本层范围，再遍历更新答案，最后展开下一层」。

**Evidence**

```
que = deque([root])
res = []
while que:
    res.append(max(que, key=lambda x: x.val).val)
    for _ in range(len(que)):
        node = que.popleft()
        if node.left:
            que.append(node.left)
        if node.right:
            que.append(node.right)
return res
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F515%20-%20Find%20Largest%20Value%20in%20Each%20Tree%20Row)
