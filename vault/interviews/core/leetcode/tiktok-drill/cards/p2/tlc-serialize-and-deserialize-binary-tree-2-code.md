---
id: tlc-serialize-and-deserialize-binary-tree-2-code
node: p2.serialize-and-deserialize-binary-tree
type: qa
step: 2
---
## Q
**LC 297 二叉树的序列化与反序列化**｜写出 Python 实现

实现类 `Codec`：`serialize(root)` 把二叉树变成字符串，`deserialize(data)` 把该字符串还原成与原树结构和值完全相同的树。结点数 `0` 到 `10^4`，值在 `[-1000, 1000]`，格式自定。

## A
**思路。** 前序递归加空位标记。序列化：根、左、右依次输出，空节点输出 `"#"`。反序列化：用同一个标记迭代器，读到 `"#"` 返回 `None`，否则建节点，先递归建左子树再递归建右子树。

```python
class Codec:
    def serialize(self, root: TreeNode | None) -> str:
        out: list[str] = []

        def dfs(node: TreeNode | None) -> None:
            if node is None:
                out.append("#")                    # 空位也要占一格
                return
            out.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(out)

    def deserialize(self, data: str) -> TreeNode | None:
        tokens = iter(data.split(","))             # 标记流只被顺序消费一次

        def build() -> TreeNode | None:
            tok = next(tokens)
            if tok == "#":
                return None
            node = TreeNode(int(tok))
            node.left = build()                    # 先左后右，与序列化的顺序一致
            node.right = build()
            return node

        return build()
```

运行：`[1,2,3,null,null,4,5]` → `"1,2,#,#,3,4,#,#,5,#,#"`，往返后相同；`[]` → `"#"`；`[1]` → `"1,#,#"`；`[1,2]` → `"1,2,#,#,#"`；`[-1000,1000]` → `"-1000,1000,#,#,#"`；深 `10^4` 的链在默认递归上限下抛 `RecursionError`，调高上限后往返相同。

**复杂度。** 时间 `O(n)`：每个节点访问一次；空间 `O(n)`：输出含 `2n + 1` 个标记，另有 `O(h)` 的递归栈（`h` 为树高，链状树 `10^4` 层，会触到默认递归上限）。

**写法要点。** `iter(data.split(","))` 做标记流：每个 `next(tokens)` 只消费一次，递归函数之间共享位置，不需要下标变量和 `nonlocal`；`out` 列表在内层 `dfs` 里直接 `append`，不用 `nonlocal`；`",".join(out)` 一次拼接，不在循环里 `+=`；分隔符 `,` 不会出现在整数里，负号随数字一起被 `int()` 解析。
