---
id: tlc-serialize-and-deserialize-binary-tree-5-alt
node: p3.serialize-and-deserialize-binary-tree
type: qa
step: 5
---
## Q
**LC 297 二叉树的序列化与反序列化**｜另一种解法

不用递归的层序（BFS）写法是怎样的？它和前序递归版本相比，什么时候该选哪个？

## A
**思路。** 层序：序列化时队列里放节点（含 `None`），出队时输出值或 `"null"`，非空节点的左右孩子照原样入队。反序列化：先建根；每出队一个节点，从标记流里取两个，非 `"null"` 的建成左、右孩子并入队。

```python
from collections import deque

class CodecLevel:
    def serialize(self, root: TreeNode | None) -> str:
        out: list[str] = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node is None:
                out.append("null")                 # 空位也要占一格
                continue
            out.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        return ",".join(out)

    def deserialize(self, data: str) -> TreeNode | None:
        tokens = iter(data.split(","))
        first = next(tokens)
        if first == "null":
            return None
        root = TreeNode(int(first))
        queue = deque([root])
        while queue:
            node = queue.popleft()
            left, right = next(tokens, "null"), next(tokens, "null")   # 每个节点后面跟着它的两个孩子位
            if left != "null":
                node.left = TreeNode(int(left))
                queue.append(node.left)
            if right != "null":
                node.right = TreeNode(int(right))
                queue.append(node.right)
        return root
```

运行：`[1,2,3,null,null,4,5]` → `"1,2,3,null,null,4,5,null,null,null,null"`，还原后相同；`[]` → `"null"`；`[1,2]` → `"1,2,null,null,null"`；深 `10^4` 的链往返后与原树一致，不会 `RecursionError`。

**复杂度。** 时间 `O(n)`：每个节点入队、出队各一次；空间 `O(n)`：队列最宽时存一层，输出含 `2n + 1` 个标记。

**什么时候选哪个。**
- 面试默认先写前序递归：十几行，思路最直观，容易说清「前序 + 空位 = 唯一确定」。
- 树深：题目结点数可达 `10^4`，一条链就是 `10^4` 层，Python 默认递归上限约 `1000`，前序递归版会 `RecursionError`；此时用本卡的层序版本，或者先 `sys.setrecursionlimit(20000)`。
- 需要和 LeetCode 的输入格式（层序加 `null`）一致，或要边读边建：层序版本更贴近。
- 对 BST 或要最小化序列长度：前序版本可以丢掉空位标记。

**补充。** 两个版本共同的不变量：序列里空位标记的数量恰好比非空节点多一个（一棵有 `n` 个节点的二叉树有 `n + 1` 个空指针），这也是还原时可以确定「何时读完」的依据。
