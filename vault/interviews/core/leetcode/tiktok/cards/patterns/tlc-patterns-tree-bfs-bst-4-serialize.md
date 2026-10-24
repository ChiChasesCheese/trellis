---
id: tlc-patterns-tree-bfs-bst-4-serialize
node: patterns.tree-bfs-bst
type: qa
step: 4
---
## Q
**二叉树 BFS 与 BST 性质｜序列化与反序列化（LC 297）**

为什么序列化二叉树必须写出空节点？前序版本和层序版本的写法各是什么？

## A
只写节点值，不同的树会得到同一个字符串。**反例**：树 `[1,2]`（`2` 是左孩子）和 `[1,null,2]`（`2` 是右孩子），只写值都是 `"1,2"`，无法还原。加上空节点标记后分别是 `"1,2,#,#,#"` 和 `"1,#,2,#,#"`，唯一。

**前序 DFS**：序列化和反序列化用同样的访问顺序。

```python
class Codec:
    def serialize(self, root: TreeNode | None) -> str:
        out: list[str] = []
        def dfs(node: TreeNode | None) -> None:
            if node is None:
                out.append("#")            # 空节点也要记录
                return
            out.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(out)

    def deserialize(self, data: str) -> TreeNode | None:
        it = iter(data.split(","))
        def build() -> TreeNode | None:
            v = next(it)                   # 迭代器按序消费，天然保持位置
            if v == "#":
                return None
            node = TreeNode(int(v))
            node.left = build()            # 与序列化相同的前序顺序
            node.right = build()
            return node
        return build()
```

运行：`[1,2,3,null,null,4,5]` → `"1,2,#,#,3,4,#,#,5,#,#"`，还原后再序列化得到同一个字符串；空树 → `"#"`，还原得 `None`。

- **层序版**：队列里放节点（包括 `None`），出队时写值或 `#`；反序列化用另一个队列逐个给出队节点接左右孩子。格式与 LeetCode 的数组表示一致。
- 前序版更短，但递归深度等于树高；`10^4` 个节点的退化链会超过默认递归上限，层序版没有此问题。
- **N 叉树（LC 428）**：每个节点写「值 + 孩子个数」，反序列化时按个数递归读孩子。
- 值里含分隔符（如字符串节点）时，要转义或用长度前缀。
