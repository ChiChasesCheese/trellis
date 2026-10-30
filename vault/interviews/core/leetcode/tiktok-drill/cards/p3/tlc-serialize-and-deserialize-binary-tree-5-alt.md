---
id: tlc-serialize-and-deserialize-binary-tree-5-alt
node: p3.serialize-and-deserialize-binary-tree
type: qa
step: 5
---
## Q
**LC 297 二叉树的序列化与反序列化**｜另一种解法

前序遍历加空位标记的递归写法是怎样的？它和层序版本相比，什么时候该选哪个？

## A
**思路。** 前序：先输出根，再递归输出左子树、右子树；空节点输出 `"#"`。还原时用同一个迭代器按前序消费标记：读到 `"#"` 返回 `None`，否则建节点，先递归建左子树、再递归建右子树。

```python
class CodecPreorder:
    def serialize(self, root: TreeNode | None) -> str:
        out: list[str] = []
        def dfs(node: TreeNode | None) -> None:
            if node is None:
                out.append("#")
                return
            out.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(out)

    def deserialize(self, data: str) -> TreeNode | None:
        tokens = iter(data.split(","))
        def build() -> TreeNode | None:
            tok = next(tokens)
            if tok == "#":
                return None
            node = TreeNode(int(tok))
            node.left = build()                    # 先左后右，与序列化顺序一致
            node.right = build()
            return node
        return build()
```

运行：`[1,2,3,null,null,4,5]` → `"1,2,#,#,3,4,#,#,5,#,#"`，还原后相同；`[]` → `"#"`。

**复杂度。** 时间 `O(n)`；空间 `O(h)` 的调用栈加 `O(n)` 的输出，`h` 为树高。序列也含 `2n + 1` 个标记。

**什么时候选哪个。**
- 面试默认先写前序递归：十几行，思路最直观，容易说清「前序 + 空位 = 唯一确定」。
- 树深：题目结点数可达 `10^4`，一条链就是 `10^4` 层，Python 默认递归上限约 `1000`，前序递归版会 `RecursionError`；此时用层序版本，或者先 `sys.setrecursionlimit(20000)`。
- 需要和 LeetCode 的输入格式（层序加 `null`）一致，或要边读边建：层序版本更贴近。
- 对 BST 或要最小化序列长度：前序版本可以丢掉空位标记。

**补充。** 两个版本共同的不变量：序列里空位标记的数量恰好比非空节点多一个（一棵有 `n` 个节点的二叉树有 `n + 1` 个空指针），这也是还原时可以确定「何时读完」的依据。
