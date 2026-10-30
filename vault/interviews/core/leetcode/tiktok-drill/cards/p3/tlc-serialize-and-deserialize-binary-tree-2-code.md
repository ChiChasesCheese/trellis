---
id: tlc-serialize-and-deserialize-binary-tree-2-code
node: p3.serialize-and-deserialize-binary-tree
type: qa
step: 2
---
## Q
**LC 297 二叉树的序列化与反序列化**｜写出 Python 实现

实现类 `Codec`：`serialize(root)` 把二叉树变成字符串，`deserialize(data)` 把该字符串还原成与原树结构和值完全相同的树。结点数 `0` 到 `10^4`，值在 `[-1000, 1000]`，格式自定，要求不因树深而栈溢出。

## A
**思路。** 层序遍历。序列化：队列里放节点（含 `None`），出队时输出值或 `"null"`，非空节点的左右孩子照原样入队。反序列化：先建根；每出队一个节点，从标记流里取两个，非 `"null"` 的建成左、右孩子并入队。

```python
from collections import deque

class Codec:
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

运行：`[1,2,3,null,null,4,5]` → `"1,2,3,null,null,4,5,null,null,null,null"`，往返后相同；`[]` → `"null"`；`[1]` → `"1,null,null"`；`[1,2]` → `"1,2,null,null,null"`；`[-1000,1000]` → `"-1000,1000,null,null,null"`。

**复杂度。** 时间 `O(n)`：每个节点入队、出队各一次；空间 `O(n)`：队列最宽时存一层，输出含 `2n + 1` 个标记。

**写法要点。** `iter(data.split(","))` 配合 `next(it, "null")`：标记流用完后自动补 `"null"`，不需要下标和边界判断；`deque` 的 `popleft` 是 `O(1)`，列表的 `pop(0)` 是 `O(n)`；`",".join(out)` 一次拼接，不在循环里 `+=`；分隔符 `,` 不会出现在整数里，负号随数字一起被 `int()` 解析。
